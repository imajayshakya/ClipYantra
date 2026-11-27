"""ING-001/ING-002 SQLAlchemy source/upload/media entities."""

from datetime import datetime, timezone
from uuid import uuid4

from sqlalchemy import JSON, DateTime, ForeignKey, Index, String, Text, UniqueConstraint, BigInteger, Integer, Numeric, Boolean
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


def new_uuid() -> str:
    return str(uuid4())


class Base(DeclarativeBase):
    pass


class SourceRecord(Base):
    __tablename__ = "source_videos"
    __table_args__ = (
        UniqueConstraint(
            "workspace_id",
            "checksum",
            name="uq_source_videos_workspace_checksum",
        ),
        Index("ix_source_videos_workspace_status", "workspace_id", "status"),
    )

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=new_uuid)
    workspace_id: Mapped[str] = mapped_column(String(36), nullable=False)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    source_type: Mapped[str] = mapped_column(String(32), nullable=False)
    status: Mapped[str] = mapped_column(String(32), nullable=False, default="created")
    checksum: Mapped[str | None] = mapped_column(String(128), nullable=True)
    original_metadata: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    idempotency_key: Mapped[str | None] = mapped_column(String(128), nullable=True)
    payload_fingerprint: Mapped[str | None] = mapped_column(String(64), nullable=True)
    validation_job_id: Mapped[str | None] = mapped_column(String(36), nullable=True)
    completion_idempotency_key: Mapped[str | None] = mapped_column(String(128), nullable=True)
    media_asset_id: Mapped[str | None] = mapped_column(String(36), nullable=True)
    transcription_job_id: Mapped[str | None] = mapped_column(String(36), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=utc_now,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=utc_now,
        onupdate=utc_now,
    )

    rights: Mapped["SourceRights"] = relationship(
        back_populates="source",
        cascade="all, delete-orphan",
        uselist=False,
    )
    upload_sessions: Mapped[list["UploadSession"]] = relationship(
        back_populates="source",
        cascade="all, delete-orphan",
    )
    media_asset: Mapped["MediaAsset"] = relationship(
        back_populates="source",
        cascade="all, delete-orphan",
        uselist=False,
    )
    transcripts: Mapped[list["Transcript"]] = relationship(
        back_populates="source",
        cascade="all, delete-orphan",
    )


class Transcript(Base):
    __tablename__ = "transcripts"
    __table_args__ = (
        Index("ix_transcripts_source", "source_id"),
        Index("ix_transcripts_media_asset", "media_asset_id"),
    )

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=new_uuid)
    source_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("source_videos.id", ondelete="CASCADE"),
        nullable=False,
    )
    workspace_id: Mapped[str] = mapped_column(String(36), nullable=False)
    media_asset_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("media_assets.id", ondelete="CASCADE"),
        nullable=False,
    )
    provider: Mapped[str] = mapped_column(String(32), nullable=False)
    model: Mapped[str] = mapped_column(String(64), nullable=False)
    language: Mapped[str] = mapped_column(String(10), nullable=False)
    full_text: Mapped[str] = mapped_column(Text, nullable=False)
    status: Mapped[str] = mapped_column(String(32), nullable=False, default="pending")
    version: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    validation_error: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=utc_now,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=utc_now,
        onupdate=utc_now,
    )

    source: Mapped["SourceRecord"] = relationship(back_populates="transcripts")
    segments: Mapped[list["TranscriptSegment"]] = relationship(
        back_populates="transcript",
        cascade="all, delete-orphan",
        order_by="TranscriptSegment.start_ms",
    )


class TranscriptSegment(Base):
    __tablename__ = "transcript_segments"
    __table_args__ = (
        Index("ix_transcript_segments_transcript", "transcript_id"),
        Index("ix_transcript_segments_timerange", "start_ms", "end_ms"),
    )

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=new_uuid)
    transcript_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("transcripts.id", ondelete="CASCADE"),
        nullable=False,
    )
    start_ms: Mapped[int] = mapped_column(BigInteger, nullable=False)
    end_ms: Mapped[int] = mapped_column(BigInteger, nullable=False)
    text: Mapped[str] = mapped_column(Text, nullable=False)
    speaker: Mapped[str | None] = mapped_column(String(64), nullable=True)
    confidence: Mapped[float | None] = mapped_column(Numeric(4, 3), nullable=True)
    word_alignments: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=utc_now,
    )

    transcript: Mapped["Transcript"] = relationship(back_populates="segments")


class SourceRights(Base):
    __tablename__ = "source_rights"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=new_uuid)
    source_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("source_videos.id", ondelete="CASCADE"),
        unique=True,
        nullable=False,
    )
    rights_declaration: Mapped[str] = mapped_column(String(32), nullable=False)
    rights_note: Mapped[str | None] = mapped_column(Text, nullable=True)
    provenance: Mapped[str] = mapped_column(String(32), nullable=False, default="local_upload")
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=utc_now,
    )

    source: Mapped["SourceRecord"] = relationship(back_populates="rights")


class UploadSession(Base):
    __tablename__ = "upload_sessions"
    __table_args__ = (
        UniqueConstraint(
            "workspace_id",
            "idempotency_key",
            name="uq_upload_sessions_workspace_idempotency",
        ),
    )

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=new_uuid)
    workspace_id: Mapped[str] = mapped_column(String(36), nullable=False)
    source_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("source_videos.id", ondelete="CASCADE"),
        nullable=False,
    )
    status: Mapped[str] = mapped_column(String(32), nullable=False, default="pending_upload")
    storage_key: Mapped[str | None] = mapped_column(Text, nullable=True)
    checksum: Mapped[str | None] = mapped_column(String(64), nullable=True)
    idempotency_key: Mapped[str | None] = mapped_column(String(128), nullable=True)
    payload_fingerprint: Mapped[str | None] = mapped_column(String(64), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=utc_now,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=utc_now,
        onupdate=utc_now,
    )

    source: Mapped["SourceRecord"] = relationship(back_populates="upload_sessions")


class MediaAsset(Base):
    __tablename__ = "media_assets"
    __table_args__ = (
        UniqueConstraint(
            "source_id",
            name="uq_media_assets_source",
        ),
        Index("ix_media_assets_source", "source_id"),
    )

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=new_uuid)
    source_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("source_videos.id", ondelete="CASCADE"),
        nullable=False,
    )
    workspace_id: Mapped[str] = mapped_column(String(36), nullable=False)
    storage_key: Mapped[str] = mapped_column(Text, nullable=False)
    checksum: Mapped[str] = mapped_column(String(64), nullable=False)
    container: Mapped[str] = mapped_column(String(32), nullable=False)
    video_codec: Mapped[str] = mapped_column(String(32), nullable=False)
    audio_codec: Mapped[str | None] = mapped_column(String(32), nullable=True)
    duration_ms: Mapped[int] = mapped_column(BigInteger, nullable=False)
    width: Mapped[int] = mapped_column(Integer, nullable=False)
    height: Mapped[int] = mapped_column(Integer, nullable=False)
    bitrate: Mapped[int | None] = mapped_column(BigInteger, nullable=True)
    fps: Mapped[float | None] = mapped_column(Numeric(6, 3), nullable=True)
    audio_channels: Mapped[int | None] = mapped_column(Integer, nullable=True)
    sample_rate: Mapped[int | None] = mapped_column(Integer, nullable=True)
    validation_status: Mapped[str] = mapped_column(String(32), nullable=False, default="pending")
    validation_error: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=utc_now,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=utc_now,
        onupdate=utc_now,
    )

    source: Mapped["SourceRecord"] = relationship(back_populates="media_asset")
