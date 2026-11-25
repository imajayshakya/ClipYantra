"""ING-001 Pydantic API schemas."""

from datetime import datetime
from enum import Enum
from typing import Any
from uuid import uuid4

from pydantic import BaseModel, Field


class SourceType(str, Enum):
    LOCAL_UPLOAD = "local_upload"


class RightsDeclaration(str, Enum):
    OWNED = "owned"
    AUTHORIZED = "authorized"
    PUBLIC_DOMAIN = "public_domain"
    UNKNOWN_BLOCKED = "unknown_blocked"


class ContentProfile(str, Enum):
    PODCAST_INTERVIEW = "podcast_interview"
    EDUCATIONAL_TECHNICAL = "educational_technical"
    GAMING = "gaming"
    ENTERTAINMENT_FUNNY = "entertainment_funny"


class UploadSessionCreateRequest(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    filename: str | None = Field(default=None, max_length=255)
    content_type: str | None = Field(default=None, max_length=100)
    size_bytes: int | None = Field(default=None, ge=0)
    checksum: str | None = Field(default=None, max_length=128)
    rights_declaration: RightsDeclaration
    rights_note: str | None = Field(default=None, max_length=1000)
    content_profile: ContentProfile


class SourceCreateRequest(BaseModel):
    source_type: SourceType = SourceType.LOCAL_UPLOAD
    title: str = Field(min_length=1, max_length=200)
    rights_declaration: RightsDeclaration
    rights_note: str | None = Field(default=None, max_length=1000)
    content_profile: ContentProfile
    storage_reference: str | None = Field(default=None, max_length=1024)


class UploadSessionCreateResponse(BaseModel):
    source_id: str
    upload_session_id: str
    status: str
    upload_status: str
    rights_declaration: RightsDeclaration
    created_at: datetime


class SourceResponse(BaseModel):
    source_id: str
    workspace_id: str
    title: str
    source_type: SourceType
    status: str
    checksum: str | None
    rights_declaration: RightsDeclaration
    rights_note: str | None
    original_metadata: dict[str, Any]
    upload_session_id: str | None
    upload_status: str | None
    created_at: datetime
    updated_at: datetime


class SourceListResponse(BaseModel):
    items: list[SourceResponse]
    total: int
    next_cursor: str | None = None


class ErrorResponse(BaseModel):
    code: str
    message: str
    details: dict[str, Any] = Field(default_factory=dict)
    request_id: str = Field(default_factory=lambda: str(uuid4()))


# ING-002 Schemas
class MediaAssetResponse(BaseModel):
    media_asset_id: str
    source_id: str
    workspace_id: str
    storage_key: str
    checksum: str
    container: str
    video_codec: str
    audio_codec: str | None
    duration_ms: int
    width: int
    height: int
    bitrate: int | None
    fps: float | None
    audio_channels: int | None
    sample_rate: int | None
    validation_status: str
    created_at: datetime
    updated_at: datetime


class CompleteUploadRequest(BaseModel):
    upload_session_id: str
    checksum: str = Field(min_length=64, max_length=64)


class CompleteUploadResponse(BaseModel):
    source_id: str
    status: str
    validation_job_id: str | None = None


class PresignUploadRequest(BaseModel):
    upload_session_id: str
    content_type: str = Field(max_length=100)
    size_bytes: int = Field(ge=0)


class PresignResponse(BaseModel):
    upload_url: str
    storage_key: str
    expires_in: int
