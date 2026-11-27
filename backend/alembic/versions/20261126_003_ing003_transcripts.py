"""ING-003 transcripts and transcript_segments tables.

Revision ID: 20261126_003
Revises: 20261123_002
Create Date: 2026-11-26

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "20261126_003"
down_revision: Union[str, None] = "20261123_002"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create transcripts table
    op.create_table(
        "transcripts",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("source_id", sa.String(length=36), nullable=False),
        sa.Column("workspace_id", sa.String(length=36), nullable=False),
        sa.Column("media_asset_id", sa.String(length=36), nullable=False),
        sa.Column("provider", sa.String(length=32), nullable=False),
        sa.Column("model", sa.String(length=64), nullable=False),
        sa.Column("language", sa.String(length=10), nullable=False),
        sa.Column("full_text", sa.Text(), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False, server_default="pending"),
        sa.Column("version", sa.Integer(), nullable=False, server_default="1"),
        sa.Column("validation_error", sa.JSON(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(
            ["source_id"],
            ["source_videos.id"],
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["media_asset_id"],
            ["media_assets.id"],
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "ix_transcripts_source",
        "transcripts",
        ["source_id"],
        unique=False,
    )
    op.create_index(
        "ix_transcripts_media_asset",
        "transcripts",
        ["media_asset_id"],
        unique=False,
    )

    # Create transcript_segments table
    op.create_table(
        "transcript_segments",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("transcript_id", sa.String(length=36), nullable=False),
        sa.Column("start_ms", sa.BigInteger(), nullable=False),
        sa.Column("end_ms", sa.BigInteger(), nullable=False),
        sa.Column("text", sa.Text(), nullable=False),
        sa.Column("speaker", sa.String(length=64), nullable=True),
        sa.Column("confidence", sa.Numeric(precision=4, scale=3), nullable=True),
        sa.Column("word_alignments", sa.JSON(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(
            ["transcript_id"],
            ["transcripts.id"],
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "ix_transcript_segments_transcript",
        "transcript_segments",
        ["transcript_id"],
        unique=False,
    )
    op.create_index(
        "ix_transcript_segments_timerange",
        "transcript_segments",
        ["start_ms", "end_ms"],
        unique=False,
    )

    # Add transcription_job_id to source_videos
    with op.batch_alter_table("source_videos") as batch_op:
        batch_op.add_column(sa.Column("transcription_job_id", sa.String(length=36), nullable=True))


def downgrade() -> None:
    with op.batch_alter_table("source_videos") as batch_op:
        batch_op.drop_column("transcription_job_id")

    op.drop_index(
        "ix_transcript_segments_timerange",
        table_name="transcript_segments",
    )
    op.drop_index(
        "ix_transcript_segments_transcript",
        table_name="transcript_segments",
    )
    op.drop_table("transcript_segments")

    op.drop_index(
        "ix_transcripts_media_asset",
        table_name="transcripts",
    )
    op.drop_index(
        "ix_transcripts_source",
        table_name="transcripts",
    )
    op.drop_table("transcripts")