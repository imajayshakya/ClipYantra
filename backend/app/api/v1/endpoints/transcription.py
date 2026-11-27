"""ING-003 Transcription Endpoints."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

from app.db.session import get_db
from app.db.models import MediaAsset, SourceRecord, Transcript, TranscriptSegment
from app.schemas.transcription import (
    TranscribeRequest,
    TranscriptResponse,
    TranscriptListResponse,
    TranscriptionJobStatusResponse,
    TranscriptionStatusResponse,
)
from app.services.transcription_job import transcribe_media_asset, retry_failed_transcription

router = APIRouter(prefix="/media-assets", tags=["transcription"])


@router.post(
    "/{media_asset_id}/transcribe",
    response_model=TranscriptionJobStatusResponse,
    status_code=status.HTTP_202_ACCEPTED,
    summary="Start transcription of a media asset",
    description="Queue a transcription job for the specified media asset",
)
async def start_transcription(
    media_asset_id: UUID,
    request: TranscribeRequest,
    db: AsyncSession = Depends(get_db),
) -> TranscriptionJobStatusResponse:
    """Start transcription job for a media asset."""
    # Verify media asset exists
    media_asset = await db.get(MediaAsset, str(media_asset_id))
    if not media_asset:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"MediaAsset {media_asset_id} not found",
        )

    # Check source record status
    source_record = await db.get(SourceRecord, media_asset.source_id)
    if not source_record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"SourceRecord not found for MediaAsset {media_asset_id}",
        )

    # Check if already transcribed or in progress
    if source_record.status in ("transcribing", "transcribed"):
        # Check for existing transcript
        result = await db.execute(
            select(Transcript).where(Transcript.media_asset_id == str(media_asset_id))
        )
        existing_transcript = result.scalar_one_or_none()

        if existing_transcript:
            return TranscriptionJobStatusResponse(
                transcript_id=existing_transcript.id,
                media_asset_id=str(media_asset_id),
                status=source_record.status,
                progress_percent=100 if source_record.status == "transcribed" else 50,
                started_at=existing_transcript.created_at,
                completed_at=existing_transcript.updated_at if source_record.status == "transcribed" else None,
            )

    # Queue transcription task
    task = transcribe_media_asset.delay(
        media_asset_id=str(media_asset_id),
        provider_hint=request.provider_hint,
        language=request.language,
        diarization=request.diarization,
        word_alignments=request.word_alignments,
    )

    return TranscriptionJobStatusResponse(
        media_asset_id=str(media_asset_id),
        status="pending",
        progress_percent=0,
        current_chunk=0,
        total_chunks=None,
    )


@router.get(
    "/{media_asset_id}/transcription",
    response_model=TranscriptionStatusResponse,
    summary="Get transcription status for a media asset",
    description="Get the current transcription status and transcript if completed",
)
async def get_transcription_status(
    media_asset_id: UUID,
    db: AsyncSession = Depends(get_db),
) -> TranscriptionStatusResponse:
    """Get transcription status for a media asset."""
    # Verify media asset exists
    media_asset = await db.get(MediaAsset, str(media_asset_id))
    if not media_asset:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"MediaAsset {media_asset_id} not found",
        )

    # Get latest transcript for this media asset
    result = await db.execute(
        select(Transcript)
        .where(Transcript.media_asset_id == str(media_asset_id))
        .order_by(Transcript.created_at.desc())
    )
    transcript = result.scalars().first()

    # Get source record for status
    source_record = await db.get(SourceRecord, media_asset.source_id)

    segment_count = 0
    total_duration_ms = 0
    if transcript:
        # Load segments
        segments_result = await db.execute(
            select(TranscriptSegment)
            .where(TranscriptSegment.transcript_id == str(transcript.id))
            .order_by(TranscriptSegment.start_ms)
        )
        segments = segments_result.scalars().all()
        segment_count = len(segments)
        total_duration_ms = sum(s.end_ms - s.start_ms for s in segments) if segments else 0

    return TranscriptionStatusResponse(
        media_asset_id=str(media_asset_id),
        source_status=source_record.status if source_record else "unknown",
        transcript_id=transcript.id if transcript else None,
        provider=transcript.provider if transcript else None,
        model=transcript.model if transcript else None,
        language=transcript.language if transcript else None,
        full_text=transcript.full_text if transcript else None,
        segment_count=segment_count,
        total_duration_ms=total_duration_ms,
        created_at=transcript.created_at if transcript else None,
        updated_at=transcript.updated_at if transcript else None,
    )


@router.post(
    "/{media_asset_id}/transcribe/retry",
    response_model=TranscriptionJobStatusResponse,
    status_code=status.HTTP_202_ACCEPTED,
    summary="Retry transcription for a media asset",
    description="Retry a previously failed transcription job",
)
async def retry_transcription_endpoint(
    media_asset_id: UUID,
    request: TranscribeRequest,
    db: AsyncSession = Depends(get_db),
) -> TranscriptionJobStatusResponse:
    """Retry transcription for a media asset."""
    # Verify media asset exists
    media_asset = await db.get(MediaAsset, str(media_asset_id))
    if not media_asset:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"MediaAsset {media_asset_id} not found",
        )

    # Check source record
    source_record = await db.get(SourceRecord, media_asset.source_id)
    if not source_record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"SourceRecord not found for MediaAsset {media_asset_id}",
        )

    # Check if in failed state
    if source_record.status != "transcription_failed":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Can only retry failed transcriptions",
        )

    # Queue retry task
    task = retry_failed_transcription.delay(str(media_asset_id))

    return TranscriptionJobStatusResponse(
        media_asset_id=str(media_asset_id),
        status="pending",
        progress_percent=0,
    )


@router.get(
    "/{media_asset_id}/transcripts",
    response_model=list[TranscriptListResponse],
    summary="List transcripts for a media asset",
    description="Get all transcripts for the specified media asset",
)
async def list_transcripts(
    media_asset_id: UUID,
    db: AsyncSession = Depends(get_db),
) -> list[TranscriptListResponse]:
    """List all transcripts for a media asset."""
    # Verify media asset exists
    media_asset = await db.get(MediaAsset, str(media_asset_id))
    if not media_asset:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"MediaAsset {media_asset_id} not found",
        )

    result = await db.execute(
        select(Transcript)
        .where(Transcript.media_asset_id == str(media_asset_id))
        .order_by(Transcript.created_at.desc())
    )
    transcripts = result.scalars().all()

    return [
        TranscriptListResponse(
            id=t.id,
            media_asset_id=t.media_asset_id,
            provider_name=t.provider,
            model_id=t.model,
            language=t.language,
            segment_count=len(t.segments) if t.segments else 0,
            total_duration_ms=sum(s.end_ms - s.start_ms for s in t.segments) if t.segments else 0,
            created_at=t.created_at,
        )
        for t in transcripts
    ]


@router.get(
    "/{media_asset_id}/transcripts/{transcript_id}",
    response_model=TranscriptResponse,
    summary="Get transcript by ID",
    description="Get full transcript with segments",
)
async def get_transcript(
    media_asset_id: UUID,
    transcript_id: UUID,
    db: AsyncSession = Depends(get_db),
) -> TranscriptResponse:
    """Get transcript by ID with all segments."""
    # Verify media asset exists
    media_asset = await db.get(MediaAsset, str(media_asset_id))
    if not media_asset:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"MediaAsset {media_asset_id} not found",
        )

    transcript = await db.get(Transcript, str(transcript_id))
    if not transcript:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Transcript {transcript_id} not found",
        )

    # Verify transcript belongs to this media asset
    if transcript.media_asset_id != str(media_asset_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Transcript {transcript_id} not found for MediaAsset {media_asset_id}",
        )

    # Load segments
    result = await db.execute(
        select(TranscriptSegment)
        .where(TranscriptSegment.transcript_id == str(transcript_id))
        .order_by(TranscriptSegment.start_ms)
    )
    segments = result.scalars().all()

    return TranscriptResponse(
        id=transcript.id,
        media_asset_id=transcript.media_asset_id,
        provider_name=transcript.provider,
        model_id=transcript.model,
        language=transcript.language,
        full_text=transcript.full_text,
        segment_count=len(segments) if segments else 0,
        total_duration_ms=sum(s.end_ms - s.start_ms for s in segments) if segments else 0,
        provider_metadata={},
        created_at=transcript.created_at,
        updated_at=transcript.updated_at,
    )


@router.post(
    "/{media_asset_id}/transcripts/{transcript_id}/retry",
    response_model=TranscriptionJobStatusResponse,
    status_code=status.HTTP_202_ACCEPTED,
    summary="Retry failed transcription",
    description="Retry a previously failed transcription job",
)
async def retry_transcription(
    media_asset_id: UUID,
    transcript_id: UUID,
    db: AsyncSession = Depends(get_db),
) -> TranscriptionJobStatusResponse:
    """Retry a failed transcription."""
    # Verify media asset exists
    media_asset = await db.get(MediaAsset, str(media_asset_id))
    if not media_asset:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"MediaAsset {media_asset_id} not found",
        )

    transcript = await db.get(Transcript, str(transcript_id))
    if not transcript:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Transcript {transcript_id} not found",
        )

    if transcript.media_asset_id != str(media_asset_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Transcript {transcript_id} not found for MediaAsset {media_asset_id}",
        )

    source_record = await db.get(SourceRecord, media_asset.source_id)
    if not source_record or source_record.status != "transcription_failed":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Can only retry failed transcriptions",
        )

    # Queue retry task
    task = retry_failed_transcription.delay(str(media_asset_id))

    return TranscriptionJobStatusResponse(
        media_asset_id=str(media_asset_id),
        status="pending",
        progress_percent=0,
    )