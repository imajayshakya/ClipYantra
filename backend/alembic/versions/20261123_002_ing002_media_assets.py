"""ING-002 media_assets table and source_videos extensions.

Revision ID: 20261123_002
Revises: 20261123_001
Create Date: 2026-11-23

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "20261123_002"
down_revision: Union[str, None] = "20261123_001"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create media_assets table
    op.create_table(
        "media_assets",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("source_id", sa.String(length=36), nullable=False),
        sa.Column("workspace_id", sa.String(length=36), nullable=False),
        sa.Column("storage_key", sa.Text(), nullable=False),
        sa.Column("checksum", sa.String(length=64), nullable=False),
        sa.Column("container", sa.String(length=32), nullable=False),
        sa.Column("video_codec", sa.String(length=32), nullable=False),
        sa.Column("audio_codec", sa.String(length=32), nullable=True),
        sa.Column("duration_ms", sa.BigInteger(), nullable=False),
        sa.Column("width", sa.Integer(), nullable=False),
        sa.Column("height", sa.Integer(), nullable=False),
        sa.Column("bitrate", sa.BigInteger(), nullable=True),
        sa.Column("fps", sa.Numeric(precision=6, scale=3), nullable=True),
        sa.Column("audio_channels", sa.Integer(), nullable=True),
        sa.Column("sample_rate", sa.Integer(), nullable=True),
        sa.Column("validation_status", sa.String(length=32), nullable=False, server_default="pending"),
        sa.Column("validation_error", sa.JSON(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(
            ["source_id"],
            ["source_videos.id"],
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("source_id", name="uq_media_assets_source"),
    )
    op.create_index(
        "ix_media_assets_source",
        "media_assets",
        ["source_id"],
        unique=False,
    )

    # Add validation_job_id and media_asset_id to source_videos using batch mode for SQLite compatibility
    with op.batch_alter_table("source_videos") as batch_op:
        batch_op.add_column(sa.Column("validation_job_id", sa.String(length=36), nullable=True))
        batch_op.add_column(sa.Column("media_asset_id", sa.String(length=36), nullable=True))
        batch_op.create_foreign_key(
            "fk_source_videos_media_asset_id",
            "media_assets",
            ["media_asset_id"],
            ["id"],
            ondelete="SET NULL",
        )


def downgrade() -> None:
    with op.batch_alter_table("source_videos") as batch_op:
        batch_op.drop_constraint("fk_source_videos_media_asset_id", type_="foreignkey")
        batch_op.drop_column("media_asset_id")
        batch_op.drop_column("validation_job_id")

    op.drop_index(
        "ix_media_assets_source",
        table_name="media_assets",
    )
    op.drop_table("media_assets")