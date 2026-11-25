"""Integration tests for ingestion job (ING-002 AC6, AC7, AC8, AC9, AC10)."""

import pytest
from unittest.mock import Mock, patch, AsyncMock, MagicMock
from datetime import datetime, timezone
from uuid import uuid4

from app.services.ingestion_job import IngestionJob, create_ingestion_job
from app.services.ffprobe_validator import ValidationResult, create_validator
from app.services.storage_adapter import LocalFilesystemAdapter, StorageConfig
from app.db.source_repository import SourceRepository
from app.db.models import SourceRecord, UploadSession, MediaAsset


class TestIngestionJob:
    """Test the ingestion job processing pipeline."""

    @pytest.fixture
    def mock_source_store(self):
        """Create a mock source repository."""
        store = Mock()
        store.get_upload_session = Mock()
        store.get_source = Mock()
        store.update_upload_session_status = Mock()
        store.update_source_status = Mock()
        store.get_media_asset = Mock()
        store.get_media_asset_by_source = Mock(return_value=None)  # Default to None for new processing
        store.create_media_asset = Mock()
        return store

    @pytest.fixture
    def mock_storage(self):
        """Create a mock storage adapter."""
        storage = Mock(spec=LocalFilesystemAdapter)
        storage.get_file_path.return_value = "/fake/storage/path/video.mp4"
        storage.compute_checksum.return_value = "a" * 64  # SHA-256 hex
        return storage

    @pytest.fixture
    def mock_validator(self):
        """Create a mock FFprobe validator."""
        validator = Mock()
        return validator

    @pytest.fixture
    def sample_upload_session(self):
        """Create a sample upload session."""
        return UploadSession(
            id="session-123",
            source_id="source-123",
            workspace_id="workspace-123",
            status="validating",
            checksum="b" * 64,  # Matches compute_checksum return value in tests
            storage_key="workspaces/workspace-123/sources/source-123/original/abc123",
            created_at=datetime.now(timezone.utc),
        )

    @pytest.fixture
    def sample_source_record(self):
        """Create a sample source record."""
        return SourceRecord(
            id="source-123",
            workspace_id="workspace-123",
            title="Test Video",
            source_type="upload",
            status="validating",
            validation_job_id="job-123",
                checksum="a" * 64,
                original_metadata={"description": "Test description"},
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc),
        )

    @pytest.fixture
    def valid_validation_result(self):
        """Create a valid validation result."""
        return ValidationResult(
            is_valid=True,
            container="mp4",
            video_codec="h264",
            audio_codec="aac",
            duration_ms=16666,
            width=1920,
            height=1080,
            bitrate=5000000,
            fps=30.0,
            audio_channels=2,
            sample_rate=48000,
            validation_status="validated",
        )

    @pytest.fixture
    def ingestion_job(self, mock_source_store, mock_storage, mock_validator):
        """Create an ingestion job with mocked dependencies."""
        return IngestionJob(
            source_store=mock_source_store,
            storage=mock_storage,
            validator=mock_validator,
        )

    @pytest.mark.asyncio
    async def test_process_valid_media_asset(self, ingestion_job, mock_source_store,
                                              sample_upload_session, sample_source_record,
                                              valid_validation_result):
        """AC6: Process valid media through validation and create MediaAsset."""
        mock_source_store.get_upload_session.return_value = sample_upload_session
        mock_source_store.get_source.return_value = sample_source_record
        ingestion_job.validator.validate = AsyncMock(return_value=valid_validation_result)

        # Mock the storage operations
        ingestion_job.storage.compute_checksum.return_value = "b" * 64

        # Mock source store update methods
        mock_source_store.update_source_status = Mock()
        mock_source_store.create_media_asset = Mock()
        mock_source_store.update_upload_session_status = Mock()

        result = await ingestion_job.process("workspace-123", "session-123")

        assert result.success is True
        assert result.media_asset_id is not None
        assert result.error is None

        # Verify source status updated to ready
        mock_source_store.update_source_status.assert_called()
        status_call = mock_source_store.update_source_status.call_args
        assert status_call.kwargs['status'] == "ready"

        # Verify media asset created
        mock_source_store.create_media_asset.assert_called_once()
        asset_call = mock_source_store.create_media_asset.call_args
        asset = asset_call.args[0]
        assert isinstance(asset, MediaAsset)
        assert asset.container == "mp4"
        assert asset.video_codec == "h264"
        assert asset.audio_codec == "aac"
        assert asset.duration_ms == 16666
        assert asset.validation_status == "validated"

    @pytest.mark.asyncio
    async def test_reject_invalid_media(self, ingestion_job, mock_source_store,
                                         sample_upload_session, sample_source_record):
        """AC7: Reject invalid media and update status to failed."""
        mock_source_store.get_upload_session.return_value = sample_upload_session
        mock_source_store.get_source.return_value = sample_source_record

        # Invalid validation result
        invalid_result = ValidationResult(
            is_valid=False,
            error_message="Unsupported container: avi",
            validation_status="rejected",
        )
        ingestion_job.validator.validate = AsyncMock(return_value=invalid_result)

        mock_source_store.update_source_status = Mock()
        mock_source_store.update_upload_session_status = Mock()

        result = await ingestion_job.process("workspace-123", "session-123")

        assert result.success is False
        assert result.error == "Unsupported container: avi"
        assert result.media_asset_id is None

        # Verify source status updated to failed
        mock_source_store.update_source_status.assert_called()
        status_call = mock_source_store.update_source_status.call_args
        assert status_call.kwargs['status'] == "failed"

        # Verify no media asset created
        mock_source_store.create_media_asset.assert_not_called()

    @pytest.mark.asyncio
    async def test_checksum_verification_on_complete(self, ingestion_job, mock_source_store,
                                                      sample_upload_session, sample_source_record,
                                                      valid_validation_result):
        """AC8: Verify checksum matches before creating MediaAsset."""
        mock_source_store.get_upload_session.return_value = sample_upload_session
        mock_source_store.get_source.return_value = sample_source_record
        ingestion_job.validator.validate = AsyncMock(return_value=valid_validation_result)

        # Checksum from storage doesn't match upload session
        ingestion_job.storage.compute_checksum.return_value = "different_checksum"

        mock_source_store.update_source_status = Mock()
        mock_source_store.update_upload_session_status = Mock()

        result = await ingestion_job.process("workspace-123", "session-123")

        assert result.success is False
        assert "Checksum mismatch" in result.error
        mock_source_store.create_media_asset.assert_not_called()

    @pytest.mark.asyncio
    async def test_storage_key_pattern(self, ingestion_job, mock_source_store,
                                        sample_upload_session, sample_source_record,
                                        valid_validation_result):
        """AC9: Verify storage key follows pattern workspaces/{workspace_id}/sources/{source_id}/original/{hash}."""
        mock_source_store.get_upload_session.return_value = sample_upload_session
        mock_source_store.get_source.return_value = sample_source_record
        ingestion_job.validator.validate = AsyncMock(return_value=valid_validation_result)
        ingestion_job.storage.compute_checksum.return_value = "b" * 64  # Matches upload_session checksum

        mock_source_store.update_source_status = Mock()
        mock_source_store.create_media_asset = Mock()
        mock_source_store.update_upload_session_status = Mock()
        mock_source_store.get_media_asset_by_source = Mock(return_value=None)

        await ingestion_job.process("workspace-123", "session-123")

        # Verify media asset has correct storage key pattern
        mock_source_store.create_media_asset.assert_called_once()
        asset = mock_source_store.create_media_asset.call_args.args[0]

        assert asset.storage_key.startswith("workspaces/workspace-123/sources/source-123/original/")
        # The hash should match the upload session's storage key
        assert asset.storage_key == "workspaces/workspace-123/sources/source-123/original/abc123"

    @pytest.mark.asyncio
    async def test_idempotent_processing(self, ingestion_job, mock_source_store,
                                          sample_upload_session, sample_source_record,
                                          valid_validation_result):
        """AC10: Processing is idempotent - running twice produces same result."""
        mock_source_store.get_upload_session.return_value = sample_upload_session
        mock_source_store.get_source.return_value = sample_source_record
        ingestion_job.validator.validate = AsyncMock(return_value=valid_validation_result)
        ingestion_job.storage.compute_checksum.return_value = "b" * 64  # Matches upload_session checksum

        mock_source_store.update_source_status = Mock()
        mock_source_store.update_upload_session_status = Mock()
        
        # Create a mock media asset for the first run
        mock_asset = MediaAsset(
            id="asset-123",
            source_id="source-123",
            workspace_id="workspace-123",
            storage_key="workspaces/workspace-123/sources/source-123/original/bbbbbbbb",
            checksum="b" * 64,
            container="mp4",
            video_codec="h264",
            audio_codec="aac",
            duration_ms=16666,
            width=1920,
            height=1080,
            bitrate=5000000,
            fps=30.0,
            audio_channels=2,
            sample_rate=48000,
            validation_status="validated",
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc),
        )
        
        # First call to create_media_asset returns the mock asset
        mock_source_store.create_media_asset = Mock(return_value=mock_asset)
        
        # For idempotency test: first call to get_media_asset_by_source returns None (new), 
        # second call returns the existing asset
        call_count = 0
        def mock_get_media_asset_by_source(source_id):
            nonlocal call_count
            call_count += 1
            if call_count == 1:
                return None  # First run - no existing asset
            return mock_asset  # Second run - return existing asset
        
        mock_source_store.get_media_asset_by_source = Mock(side_effect=mock_get_media_asset_by_source)

        # First run
        result1 = await ingestion_job.process("workspace-123", "session-123")
        # Second run (simulate retry)
        result2 = await ingestion_job.process("workspace-123", "session-123")

        assert result1.success is True
        assert result2.success is True
        assert result1.media_asset_id == result2.media_asset_id
        # Should only create media asset once (idempotent)
        assert mock_source_store.create_media_asset.call_count == 1

    @pytest.mark.asyncio
    async def test_upload_session_not_found(self, ingestion_job, mock_source_store):
        """Handle missing upload session gracefully."""
        mock_source_store.get_upload_session.return_value = None

        result = await ingestion_job.process("workspace-123", "nonexistent-session")

        assert result.success is False
        assert "Upload session not found" in result.error

    @pytest.mark.asyncio
    async def test_source_record_not_found(self, ingestion_job, mock_source_store,
                                            sample_upload_session):
        """Handle missing source record gracefully."""
        mock_source_store.get_upload_session.return_value = sample_upload_session
        mock_source_store.get_source.return_value = None

        result = await ingestion_job.process("workspace-123", "session-123")

        assert result.success is False
        assert "Source record not found" in result.error

    @pytest.mark.asyncio
    async def test_validation_error_handling(self, ingestion_job, mock_source_store,
                                              sample_upload_session, sample_source_record):
        """Handle validator exceptions gracefully."""
        mock_source_store.get_upload_session.return_value = sample_upload_session
        mock_source_store.get_source.return_value = sample_source_record
        ingestion_job.validator.validate = AsyncMock(side_effect=Exception("FFprobe crashed"))

        mock_source_store.update_source_status = Mock()
        mock_source_store.update_upload_session_status = Mock()

        result = await ingestion_job.process("workspace-123", "session-123")

        assert result.success is False
        assert "Validation error" in result.error

        # Source should be marked as failed
        mock_source_store.update_source_status.assert_called()
        status_call = mock_source_store.update_source_status.call_args
        assert status_call.kwargs['status'] == "failed"

    @pytest.mark.asyncio
    async def test_storage_error_handling(self, ingestion_job, mock_source_store,
                                           sample_upload_session, sample_source_record,
                                           valid_validation_result):
        """Handle storage errors gracefully."""
        mock_source_store.get_upload_session.return_value = sample_upload_session
        mock_source_store.get_source.return_value = sample_source_record
        mock_source_store.get_media_asset_by_source = Mock(return_value=None)
        ingestion_job.validator.validate = AsyncMock(return_value=valid_validation_result)
        ingestion_job.storage.compute_checksum.side_effect = Exception("Disk full")

        mock_source_store.update_source_status = Mock()
        mock_source_store.update_upload_session_status = Mock()

        result = await ingestion_job.process("workspace-123", "session-123")

        assert result.success is False
        assert "Storage error" in result.error

        mock_source_store.update_source_status.assert_called()
        status_call = mock_source_store.update_source_status.call_args
        assert status_call.kwargs['status'] == "failed"


class TestCreateIngestionJob:
    """Test the factory function for creating ingestion jobs."""

    def test_create_ingestion_job(self):
        """Test factory creates job with correct dependencies."""
        mock_store = Mock(spec=SourceRepository)
        mock_storage = Mock()
        mock_validator = Mock()

        job = create_ingestion_job(
            source_store=mock_store,
            storage=mock_storage,
            validator=mock_validator,
        )

        assert isinstance(job, IngestionJob)
        assert job.source_store == mock_store
        assert job.storage == mock_storage
        assert job.validator == mock_validator


class TestIngestionJobResult:
    """Test the IngestionJob result dataclass."""

    def test_success_result(self):
        """Test successful result creation."""
        from backend.app.services.ingestion_job import IngestionResult

        result = IngestionResult(
            success=True,
            media_asset_id="asset-123",
            error=None,
        )

        assert result.success is True
        assert result.media_asset_id == "asset-123"
        assert result.error is None

    def test_failure_result(self):
        """Test failure result creation."""
        from backend.app.services.ingestion_job import IngestionResult

        result = IngestionResult(
            success=False,
            media_asset_id=None,
            error="Validation failed",
        )

        assert result.success is False
        assert result.media_asset_id is None
        assert result.error == "Validation failed"




