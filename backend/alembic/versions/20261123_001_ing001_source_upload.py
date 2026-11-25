"""ING-001 source, rights and upload-session tables.

Revision ID: 20261123_001
Revises:
Create Date: 2026-11-23

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "20261123_001"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "source_videos",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("workspace_id", sa.String(length=36), nullable=False),
        sa.Column("title", sa.String(length=200), nullable=False),
        sa.Column("source_type", sa.String(length=32), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("checksum", sa.String(length=128), nullable=True),
        sa.Column("original_metadata", sa.JSON(), nullable=False),
        sa.Column("idempotency_key", sa.String(length=128), nullable=True),
        sa.Column("payload_fingerprint", sa.String(length=64), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "workspace_id",
            "checksum",
            name="uq_source_videos_workspace_checksum",
        ),
    )
    op.create_index(
        "ix_source_videos_workspace_status",
        "source_videos",
        ["workspace_id", "status"],
        unique=False,
    )

    op.create_table(
        "source_rights",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("source_id", sa.String(length=36), nullable=False),
        sa.Column("rights_declaration", sa.String(length=32), nullable=False),
        sa.Column("rights_note", sa.Text(), nullable=True),
        sa.Column("provenance", sa.String(length=32), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(
            ["source_id"],
            ["source_videos.id"],
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("source_id"),
    )

    op.create_table(
        "upload_sessions",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("workspace_id", sa.String(length=36), nullable=False),
        sa.Column("source_id", sa.String(length=36), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("idempotency_key", sa.String(length=128), nullable=True),
        sa.Column("payload_fingerprint", sa.String(length=64), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(
            ["source_id"],
            ["source_videos.id"],
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "workspace_id",
            "idempotency_key",
            name="uq_upload_sessions_workspace_idempotency",
        ),
    )


def downgrade() -> None:
    op.drop_table("upload_sessions")
    op.drop_table("source_rights")
    op.drop_index(
        "ix_source_videos_workspace_status",
        table_name="source_videos",
    )
    op.drop_table("source_videos")
