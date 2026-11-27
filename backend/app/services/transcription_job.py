"""ING-003 Transcription Celery job pipeline."""

import logging
import os
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import List, Optional

from celery import shared_task
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from app.db.models import MediaAsset, SourceRecord, Transcript, TranscriptSegment
from app.services.audio_extractor import AudioExtractor, AudioChunk
from app.services.capability_registry import create_capability_registry
from app.services.transcription_provider import (
    TranscriptionRequest,
    TranscriptionResult,
)
from app.core.config import get_settings

logger = logging.getLogger(__name__)


@shared_task(
    bind=True,
    name="app.services.transcription_job.transcribe_media_asset",
    max_retries=3,
    default_retry_delay=60,
    autoretry_for=(Exception,),
    retry_backoff=True,
    retry_backoff_max=300,
)
def transcribe_media_asset(
    self,
    media_asset_id: str,
    provider_hint: Optional[str] = None,
    language: Optional[str] = None,
    diarization: bool = False,
    word_alignments: bool = False,
) -> dict:
    """
    Celery task to transcribe a MediaAsset.
    
    Pipeline:
    1. Fetch MediaAsset and SourceRecord
    2. Update status to 'transcribing'
    3. Extract audio to WAV chunks (30min with 30s overlap)
    4. Select provider via capability registry
    5. Transcribe each chunk
    6. Merge and deduplicate segments
    7. Store Transcript and TranscriptSegments
    8. Update status to 'transcribed' or 'transcription_failed'
    
    Args:
        media_asset_id: UUID of MediaAsset
        provider_hint: Optional provider hint
        language: Optional language code
        diarization: Whether diarization is required
        word_alignments: Whether word alignments are required
        
    Returns:
        Dict with transcript_id and metadata
    """
    settings = get_settings()
    db = SessionLocal()
    
    try:
        # Step 1: Fetch MediaAsset and SourceRecord
        media_asset = db.get(MediaAsset, media_asset_id)
        if not media_asset:
            raise ValueError(f"MediaAsset not found: {media_asset_id}")
        
        source_record = db.get(SourceRecord, media_asset.source_id)
        if not source_record:
            raise ValueError(f"SourceRecord not found for MediaAsset: {media_asset_id}")
        
        # Step 2: Update status to 'transcribing'
        source_record.status = "transcribing"
        source_record.updated_at = datetime.now(timezone.utc)
        db.commit()
        
        logger.info(f"Starting transcription for MediaAsset {media_asset_id}")
        
        # Step 3: Extract audio to WAV chunks
        audio_extractor = AudioExtractor(
            ffmpeg_path=settings.FFMPEG_PATH,
            ffprobe_path=settings.FFPROBE_PATH,
            sample_rate=settings.AUDIO_SAMPLE_RATE,
            channels=settings.AUDIO_CHANNELS,
            chunk_duration_seconds=settings.CHUNK_DURATION_SECONDS,
            chunk_overlap_seconds=settings.CHUNK_OVERLAP_SECONDS,
        )
        
        # Get media file path
        media_path = _get_media_file_path(media_asset, settings)
        if not os.path.exists(media_path):
            raise FileNotFoundError(f"Media file not found: {media_path}")
        
        extraction_result = audio_extractor.extract_audio(
            media_path=media_path,
            output_dir=Path(settings.LOCAL_STORAGE_PATH) / "audio_chunks" / media_asset_id,
        )
        
        logger.info(f"Extracted {len(extraction_result.chunks)} audio chunks")
        
        # Step 4: Select provider via capability registry
        capability_registry = create_capability_registry(settings)
        
        provider = capability_registry.get_transcription_provider(
            hint=provider_hint,
            language=language,
            diarization=diarization,
            word_alignments=word_alignments,
        )
        
        logger.info(f"Selected provider: {provider.provider_name} ({provider.model_id})")
        
        # Step 5: Transcribe each chunk
        all_segments: List = []
        provider_metadata = {
            "provider": provider.provider_name,
            "model": provider.model_id,
            "chunks_processed": 0,
            "total_duration_ms": 0,
            "started_at": datetime.now(timezone.utc).isoformat(),
        }
        
        for chunk in extraction_result.chunks:
            # Create transcription request
            request = TranscriptionRequest(
                audio_path=chunk.file_path,
                language=language,
                diarization=diarization,
                word_alignments=word_alignments,
                metadata={
                    "chunk_index": chunk.index,
                    "chunk_start_ms": chunk.start_ms,
                    "chunk_end_ms": chunk.end_ms,
                    "media_asset_id": media_asset_id,
                },
            )
            
            # Transcribe chunk
            result: TranscriptionResult = provider.transcribe(request)
            
            # Convert segments to absolute timestamps
            for segment in result.segments:
                # Adjust timestamps to be absolute from media start
                segment.start_ms += chunk.start_ms
                segment.end_ms += chunk.start_ms
                if segment.words:
                    for word in segment.words:
                        word.start_ms += chunk.start_ms
                        word.end_ms += chunk.start_ms
                all_segments.append(segment)
            
            # Accumulate provider metadata
            provider_metadata["chunks_processed"] += 1
            provider_metadata["total_duration_ms"] += chunk.duration_ms
            
            # Update metadata from provider
            if result.provider_metadata:
                if "language" in result.provider_metadata:
                    provider_metadata["detected_language"] = result.provider_metadata["language"]
                if "duration" in result.provider_metadata:
                    provider_metadata["provider_duration"] = result.provider_metadata["duration"]
        
        provider_metadata["completed_at"] = datetime.now(timezone.utc).isoformat()
        
        # Step 6: Merge and deduplicate segments (handle overlaps)
        merged_segments = _merge_overlapping_segments(all_segments)
        
        logger.info(f"Merged {len(all_segments)} segments into {len(merged_segments)}")
        
        # Step 7: Store Transcript and TranscriptSegments
        transcript = Transcript(
            id=str(uuid.uuid4()),
            media_asset_id=media_asset_id,
            provider_name=provider.provider_name,
            model_id=provider.model_id,
            language=language or provider_metadata.get("detected_language", "unknown"),
            full_text=" ".join(s.text for s in merged_segments),
            segment_count=len(merged_segments),
            total_duration_ms=sum(s.end_ms - s.start_ms for s in merged_segments),
            provider_metadata=provider_metadata,
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc),
        )
        db.add(transcript)
        db.flush()
        
        # Store segments
        for i, segment in enumerate(merged_segments):
            transcript_segment = TranscriptSegment(
                id=str(uuid.uuid4()),
                transcript_id=transcript.id,
                sequence_index=i,
                start_ms=segment.start_ms,
                end_ms=segment.end_ms,
                text=segment.text,
                confidence=segment.confidence,
                speaker=segment.speaker,
                words=segment.words,
                created_at=datetime.now(timezone.utc),
            )
            db.add(transcript_segment)
        
        # Step 8: Update status to 'transcribed'
        source_record.status = "transcribed"
        source_record.updated_at = datetime.now(timezone.utc)
        db.commit()
        
        logger.info(f"Transcription completed for MediaAsset {media_asset_id}, Transcript ID: {transcript.id}")
        
        return {
            "transcript_id": transcript.id,
            "media_asset_id": media_asset_id,
            "segment_count": len(merged_segments),
            "language": transcript.language,
            "provider": provider.provider_name,
            "model": provider.model_id,
        }
        
    except Exception as e:
        logger.error(f"Transcription failed for MediaAsset {media_asset_id}: {e}", exc_info=True)

        # Update status to 'transcription_failed'
        try:
            source_record = db.get(SourceRecord, media_asset.source_id) if media_asset else None
            if source_record:
                source_record.status = "transcription_failed"
                source_record.updated_at = datetime.now(timezone.utc)
                db.commit()
        except Exception:
            pass  # Don't mask original error

        # Re-raise for Celery retry
        raise self.retry(exc=e)
        
    finally:
        db.close()


def _get_media_file_path(media_asset: MediaAsset, settings) -> str:
    """Get absolute path to media file."""
    # MediaAsset has storage_path which could be relative to local storage
    if media_asset.storage_path.startswith("/"):
        return media_asset.storage_path
    else:
        # Relative to local storage
        return os.path.join(settings.LOCAL_STORAGE_PATH, media_asset.storage_path)


def _merge_overlapping_segments(segments) -> List:
    """
    Merge overlapping segments from different chunks.
    Keeps the segment with higher confidence in overlap regions.
    """
    if not segments:
        return []
    
    # Sort by start time
    sorted_segments = sorted(segments, key=lambda s: s.start_ms)
    merged = []
    
    for segment in sorted_segments:
        if not merged:
            merged.append(segment)
            continue
        
        last = merged[-1]
        
        # Check for overlap
        if segment.start_ms < last.end_ms:
            # Overlap detected - keep higher confidence segment for overlap region
            overlap_ms = last.end_ms - segment.start_ms
            
            if segment.confidence > last.confidence:
                # New segment is better - trim last, keep new
                last.end_ms = segment.start_ms
                # Only add new if it has meaningful duration
                if segment.end_ms > segment.start_ms:
                    merged.append(segment)
            else:
                # Last segment is better - trim new
                segment.start_ms = last.end_ms
                if segment.end_ms > segment.start_ms:
                    merged.append(segment)
        else:
            # No overlap
            merged.append(segment)
    
    return merged


@shared_task(
    bind=True,
    name="app.services.transcription_job.retry_failed_transcription",
    max_retries=1,
)
def retry_failed_transcription(self, media_asset_id: str) -> dict:
    """
    Retry a failed transcription.
    Resets status and re-queues the transcription task.
    """
    db = SessionLocal()
    try:
        media_asset = db.get(MediaAsset, media_asset_id)
        if not media_asset:
            raise ValueError(f"MediaAsset not found: {media_asset_id}")
        
        source_record = db.get(SourceRecord, media_asset.source_id)
        if not source_record:
            raise ValueError(f"SourceRecord not found")
        
        if source_record.status != "transcription_failed":
            raise ValueError(f"Can only retry failed transcriptions, current status: {source_record.status}")
        
        # Reset status
        source_record.status = "pending"
        source_record.updated_at = datetime.now(timezone.utc)
        db.commit()
        
        # Re-queue
        result = transcribe_media_asset.delay(media_asset_id)
        
        return {
            "task_id": result.id,
            "media_asset_id": media_asset_id,
        }
        
    finally:
        db.close()