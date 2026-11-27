"""ING-003 Transcription API schemas."""

from typing import List, Optional
from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime


class TranscribeRequest(BaseModel):
    """Request to start transcription of a media asset."""
    model_config = ConfigDict(extra="forbid")

    provider_hint: Optional[str] = Field(
        default=None,
        description="Explicit provider hint (e.g., 'whisperx', 'deepgram', 'groq', 'openai', 'nvidia_nim')"
    )
    language: Optional[str] = Field(
        default=None,
        description="Language code (e.g., 'en', 'es', 'hi'). Auto-detect if not specified."
    )
    diarization: bool = Field(
        default=False,
        description="Enable speaker diarization"
    )
    word_alignments: bool = Field(
        default=False,
        description="Enable word-level timestamp alignments"
    )


class WordAlignmentResponse(BaseModel):
    """Word-level alignment response."""
    model_config = ConfigDict(from_attributes=True)

    word: str
    start_ms: int
    end_ms: int
    confidence: float


class TranscriptSegmentResponse(BaseModel):
    """Transcript segment response."""
    model_config = ConfigDict(from_attributes=True)

    id: str
    sequence_index: int
    start_ms: int
    end_ms: int
    text: str
    confidence: float
    speaker: Optional[str] = None
    words: List[WordAlignmentResponse] = []


class TranscriptResponse(BaseModel):
    """Transcript response with metadata."""
    model_config = ConfigDict(from_attributes=True)

    id: str
    media_asset_id: str
    provider_name: str
    model_id: str
    language: str
    full_text: str
    segment_count: int
    total_duration_ms: int
    provider_metadata: dict
    created_at: datetime
    updated_at: datetime


class TranscriptListResponse(BaseModel):
    """Paginated transcript list response."""
    model_config = ConfigDict(from_attributes=True)

    id: str
    media_asset_id: str
    provider_name: str
    model_id: str
    language: str
    segment_count: int
    total_duration_ms: int
    created_at: datetime


class TranscriptionJobStatusResponse(BaseModel):
    """Transcription job status response."""
    model_config = ConfigDict(from_attributes=True)

    transcript_id: Optional[str] = None
    media_asset_id: str
    status: str  # pending, transcribing, transcribed, transcription_failed
    progress_percent: Optional[int] = None
    current_chunk: Optional[int] = None
    total_chunks: Optional[int] = None
    error_message: Optional[str] = None
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None


class TranscriptionStatusResponse(BaseModel):
    """Transcription status response for a media asset."""
    model_config = ConfigDict(from_attributes=True)

    media_asset_id: str
    source_status: str  # ready, transcribing, transcribed, transcription_failed
    transcript_id: Optional[str] = None
    provider: Optional[str] = None
    model: Optional[str] = None
    language: Optional[str] = None
    full_text: Optional[str] = None
    segment_count: int = 0
    total_duration_ms: int = 0
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None