"""ING-002 Ingestion job service for processing uploaded media."""

from dataclasses import dataclass
from typing import Optional
from uuid import uuid4

from app.db.source_repository import SourceRepository
from app.db.models import MediaAsset
from app.services.storage_adapter import StorageAdapter
from app.services.ffprobe_validator import ValidationResult


@dataclass
class IngestionResult:
    """Result of ingestion job."""
    success: bool
    media_asset_id: Optional[str] = None
    error: Optional[str] = None


class IngestionJob:
    """Processes uploaded media through validation and storage."""

    def __init__(
        self,
        source_store: SourceRepository,
        storage: StorageAdapter,
        validator,
    ):
        self.source_store = source_store
        self.storage = storage
        self.validator = validator

    async def process(self, workspace_id: str, session_id: str) -> IngestionResult:
        """Process a completed upload session.
        
        Args:
            workspace_id: Workspace ID for the upload session
            session_id: ID of the UploadSession to process
            
        Returns:
            IngestionResult with success status and media asset ID or error
        """
        # Load upload session
        upload_session = self.source_store.get_upload_session(
            workspace_id=workspace_id,
            session_id=session_id
        )
        
        if not upload_session:
            return IngestionResult(
                success=False,
                error="Upload session not found",
            )
        
        # Load source record
        source = self.source_store.get_source(
            workspace_id=workspace_id,
            source_id=upload_session.source_id
        )
        
        if not source:
            return IngestionResult(
                success=False,
                error="Source record not found",
            )
        
        # Check if already processed (idempotent)
        existing_asset = self.source_store.get_media_asset_by_source(upload_session.source_id)
        if existing_asset:
            return IngestionResult(
                success=True,
                media_asset_id=existing_asset.id,
            )
        
        # Update status to validating
        self.source_store.update_source_status(
            workspace_id=workspace_id,
            source_id=source.id,
            status="validating",
            validation_job_id=str(uuid4()),
        )
        self.source_store.update_upload_session_status(
            workspace_id=workspace_id,
            session_id=session_id,
            status="validating",
        )
        
        # Get file path from storage for validation
        file_path = self.storage.get_file_path(upload_session.storage_key)
        if not file_path:
            self.source_store.update_source_status(
                workspace_id=workspace_id,
                source_id=source.id,
                status="failed",
            )
            self.source_store.update_upload_session_status(
                workspace_id=workspace_id,
                session_id=session_id,
                status="validation_failed",
            )
            return IngestionResult(
                success=False,
                error="File not found in storage",
            )
        
        # Validate media
        try:
            validation_result = await self.validator.validate(file_path)
        except Exception as e:
            self.source_store.update_source_status(
                workspace_id=workspace_id,
                source_id=source.id,
                status="failed",
            )
            self.source_store.update_upload_session_status(
                workspace_id=workspace_id,
                session_id=session_id,
                status="validation_failed",
            )
            return IngestionResult(
                success=False,
                error=f"Validation error: {str(e)}",
            )
        
        if not validation_result.is_valid:
            self.source_store.update_source_status(
                workspace_id=workspace_id,
                source_id=source.id,
                status="failed",
            )
            self.source_store.update_upload_session_status(
                workspace_id=workspace_id,
                session_id=session_id,
                status="validation_failed",
            )
            return IngestionResult(
                success=False,
                error=validation_result.error_message or "Validation failed",
            )
        # Verify checksum
        try:
            storage_checksum = self.storage.compute_checksum(upload_session.storage_key)
        except Exception as e:
                    self.source_store.update_source_status(
                        workspace_id=workspace_id,
                        source_id=source.id,
                        status="failed",
                    )
                    self.source_store.update_upload_session_status(
                        workspace_id=workspace_id,
                        session_id=session_id,
                        status="validation_failed",
                    )
                    return IngestionResult(
                        success=False,
                        error=f"Storage error: {str(e)}",
                    )

        if upload_session.checksum and storage_checksum != upload_session.checksum:
            self.source_store.update_source_status(
                workspace_id=workspace_id,
                source_id=source.id,
                status="failed",
            )
            self.source_store.update_upload_session_status(
                workspace_id=workspace_id,
                session_id=session_id,
                status="validation_failed",
            )
            return IngestionResult(
                success=False,
                error="Checksum mismatch",
            )
        
        # Validation passed - create MediaAsset
        media_asset = MediaAsset(
            id=str(uuid4()),
            source_id=source.id,
            workspace_id=workspace_id,
            storage_key=upload_session.storage_key,
            checksum=storage_checksum,
            container=validation_result.container,
            video_codec=validation_result.video_codec,
            audio_codec=validation_result.audio_codec,
            duration_ms=validation_result.duration_ms,
            width=validation_result.width,
            height=validation_result.height,
            bitrate=validation_result.bitrate,
            fps=validation_result.fps,
            audio_channels=validation_result.audio_channels,
            sample_rate=validation_result.sample_rate,
            validation_status="validated",
        )
        
        # Create media asset via repository
        try:
                    created_asset = self.source_store.create_media_asset(media_asset)
        except Exception as e:
            self.source_store.update_source_status(
                workspace_id=workspace_id,
                source_id=source.id,
                status="failed",
            )
            self.source_store.update_upload_session_status(
                workspace_id=workspace_id,
                session_id=session_id,
                status="validation_failed",
            )
            return IngestionResult(
                success=False,
                error=f"Storage error: {str(e)}",
            )
        
        # Update source record
        self.source_store.update_source_status(
            workspace_id=workspace_id,
            source_id=source.id,
            status="ready",
        )
        
        # Update upload session
        self.source_store.update_upload_session_status(
            workspace_id=workspace_id,
            session_id=session_id,
            status="completed",
        )
        
        return IngestionResult(
            success=True,
                    media_asset_id=created_asset.id,
        )


def create_ingestion_job(
    source_store: SourceRepository,
    storage: StorageAdapter,
    validator,
) -> IngestionJob:
    """Factory function to create ingestion job with dependencies."""
    return IngestionJob(source_store, storage, validator)

