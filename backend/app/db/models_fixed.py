"""ING-001/ING-002 SQLAlchemy source/upload/media entities."""

from datetime import datetime, timezone
from uuid import uuid4

from sqlalchemy import JSON, DateTime, ForeignKey, Index, String, Text, UniqueConstraint, BigInteger, Integer, Numeric
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
        media_asset_id: Mapped[str | None] = mapped_column(String(36), nullable=True)
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
