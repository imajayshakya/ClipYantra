"""Integration tests for Transcription API endpoints (ING-003)."""

import pytest
from unittest.mock import Mock, patch, AsyncMock
from uuid import uuid4
from datetime import datetime, timezone

from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.main import create_app
from app.db.models import MediaAsset, SourceRecord, Transcript, TranscriptSegment
from app.db.session import get_db
from app.schemas.transcription import TranscribeRequest


class TestTranscriptionAPI:
    """Test transcription API endpoints."""

    @pytest.fixture
    def app(self):
        """Create test app."""
        return create_app()

    @pytest.fixture
    def mock_session(self):
        """Create mock async database session."""
        session = AsyncMock(spec=AsyncSession)
        return session

    @pytest.fixture
    def client(self, app, mock_session):
        """Create test client with overridden DB dependency."""
        app.dependency_overrides[get_db] = lambda: mock_session
        client = TestClient(app)
        yield client
        app.dependency_overrides.clear()

    @pytest.fixture(autouse=True)
    def mock_celery_delay(self):
        """Mock all Celery delay calls to prevent Redis connection errors."""
        with patch("app.api.v1.endpoints.transcription.transcribe_media_asset.delay") as mock_delay, \
             patch("app.api.v1.endpoints.transcription.retry_failed_transcription.delay") as mock_retry:
            mock_task = Mock()
            mock_task.id = "test-task-id"
            mock_delay.return_value = mock_task
            mock_retry.return_value = mock_task
            yield mock_delay, mock_retry

    @pytest.fixture
    def sample_media_asset(self):
        """Create sample MediaAsset."""
        source_id = str(uuid4())
        return MediaAsset(
            id=str(uuid4()),
            source_id=source_id,
            workspace_id="test_workspace",
            storage_key="videos/test_video.mp4",
            checksum="abc123",
            container="videos",
            video_codec="h264",
            audio_codec="aac",
            duration_ms=2700000,
            width=1920,
            height=1080,
            validation_status="ready",
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc),
        )

    @pytest.fixture
    def sample_source_record(self, sample_media_asset):
        """Create sample SourceRecord."""
        return SourceRecord(
            id=sample_media_asset.source_id,
            title="Test Video",
            source_type="upload",
            status="ready",
            workspace_id="test_workspace",
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc),
        )

    @pytest.fixture
    def sample_transcript(self, sample_media_asset):
        """Create sample Transcript."""
        return Transcript(
            id=str(uuid4()),
            source_id=sample_media_asset.source_id,
            media_asset_id=sample_media_asset.id,
            workspace_id=sample_media_asset.workspace_id,
            provider="whisperx",
            model="large-v3",
            language="en",
            full_text="Hello world. This is a test transcript.",
            status="completed",
            version=1,
            validation_error=None,
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc),
        )

    @pytest.fixture
    def sample_segments(self, sample_transcript):
        """Create sample TranscriptSegments."""
        return [
            TranscriptSegment(
                id=str(uuid4()),
                transcript_id=sample_transcript.id,
                start_ms=0,
                end_ms=10000,
                text="Hello world.",
                confidence=0.95,
                speaker="SPEAKER_00",
                word_alignments=[],
                created_at=datetime.now(timezone.utc),
            ),
            TranscriptSegment(
                id=str(uuid4()),
                transcript_id=sample_transcript.id,
                start_ms=10000,
                end_ms=20000,
                text="This is a test transcript.",
                confidence=0.92,
                speaker="SPEAKER_01",
                word_alignments=[],
                created_at=datetime.now(timezone.utc),
            ),
        ]

    @patch("app.api.v1.endpoints.transcription.transcribe_media_asset.delay")
    def test_start_transcription_success(
        self, mock_delay, client, mock_session, sample_media_asset, sample_source_record
    ):
        """Test starting transcription successfully."""
        mock_session.get.side_effect = [sample_media_asset, sample_source_record]
        mock_task = Mock()
        mock_task.id = "test-task-id"
        mock_delay.return_value = mock_task

        response = client.post(
            f"/api/v1/media-assets/{sample_media_asset.id}/transcribe",
            json={
                "provider_hint": "whisperx",
                "language": "en",
                "diarization": True,
                "word_alignments": True,
            },
        )

        assert response.status_code == 202
        data = response.json()
        assert data["media_asset_id"] == sample_media_asset.id
        assert data["status"] == "pending"
        assert data["progress_percent"] == 0

        mock_delay.assert_called_once()
        call_args = mock_delay.call_args
        assert call_args.kwargs["media_asset_id"] == sample_media_asset.id
        assert call_args.kwargs["provider_hint"] == "whisperx"
        assert call_args.kwargs["language"] == "en"
        assert call_args.kwargs["diarization"] is True
        assert call_args.kwargs["word_alignments"] is True

    def test_start_transcription_media_asset_not_found(self, client, mock_session):
        """Test starting transcription for non-existent media asset."""
        mock_session.get.return_value = None

        response = client.post(
            f"/api/v1/media-assets/{uuid4()}/transcribe",
            json={"language": "en"},
        )

        assert response.status_code == 404
        assert "not found" in response.json()["detail"].lower()

    def test_start_transcription_source_record_not_found(
        self, client, mock_session, sample_media_asset
    ):
        """Test starting transcription when source record missing."""
        mock_session.get.side_effect = [sample_media_asset, None]

        response = client.post(
            f"/api/v1/media-assets/{sample_media_asset.id}/transcribe",
            json={"language": "en"},
        )

        assert response.status_code == 404
        assert "sourcerecord" in response.json()["detail"].lower()

    def test_start_transcription_already_transcribed(
        self, mock_celery_delay, client, mock_session, sample_media_asset, sample_source_record, sample_transcript
    ):
        """Test starting transcription when already transcribed (idempotent - returns existing job)."""
        mock_delay, _ = mock_celery_delay
        sample_source_record.status = "transcribed"
        mock_session.get.side_effect = [sample_media_asset, sample_source_record]

        mock_result = Mock()
        mock_result.scalar_one_or_none.return_value = sample_transcript
        mock_session.execute.return_value = mock_result

        response = client.post(
            f"/api/v1/media-assets/{sample_media_asset.id}/transcribe",
            json={"language": "en"},
        )

        assert response.status_code == 202
        data = response.json()
        assert data["transcript_id"] == sample_transcript.id
        assert data["status"] == "transcribed"
        assert data["progress_percent"] == 100
        mock_delay.assert_not_called()

    def test_get_transcription_status(self, mock_celery_delay, client, mock_session, sample_media_asset, sample_source_record, sample_transcript, sample_segments):
        """Test getting transcription status."""
        mock_delay, _ = mock_celery_delay
        sample_source_record.status = "completed"
        mock_session.get.side_effect = [sample_media_asset, sample_source_record]

        mock_result = Mock()
        mock_result.scalars.return_value.first.return_value = sample_transcript

        segments_result = Mock()
        segments_result.scalars.return_value.all.return_value = sample_segments

        mock_session.execute.side_effect = [mock_result, segments_result]

        response = client.get(f"/api/v1/media-assets/{sample_media_asset.id}/transcription")

        assert response.status_code == 200
        data = response.json()
        assert data["transcript_id"] == sample_transcript.id
        assert data["media_asset_id"] == sample_media_asset.id
        assert data["provider"] == "whisperx"
        assert data["language"] == "en"
        assert data["source_status"] == "completed"

    def test_get_transcription_status_not_found(self, client, mock_session, sample_media_asset):
        """Test getting transcription status when no transcript exists."""
        mock_session.get.return_value = None

        response = client.get(f"/api/v1/media-assets/{sample_media_asset.id}/transcription")

        assert response.status_code == 404
        assert "not found" in response.json()["detail"].lower()

    def test_retry_transcription(
        self, mock_celery_delay, client, mock_session, sample_media_asset, sample_source_record
    ):
        """Test retrying transcription."""
        mock_delay, mock_retry = mock_celery_delay
        sample_source_record.status = "transcription_failed"
        mock_session.get.side_effect = [sample_media_asset, sample_source_record]

        response = client.post(
            f"/api/v1/media-assets/{sample_media_asset.id}/transcribe/retry",
            json={"language": "en"},
        )

        assert response.status_code == 202
        data = response.json()
        assert data["media_asset_id"] == sample_media_asset.id
        assert data["status"] == "pending"
        mock_retry.assert_called_once()

    def test_retry_transcription_not_in_failed_state(
        self, mock_celery_delay, client, mock_session, sample_media_asset, sample_source_record
    ):
        """Test retrying transcription when not in failed state."""
        mock_delay, mock_retry = mock_celery_delay
        sample_source_record.status = "transcribing"
        mock_session.get.side_effect = [sample_media_asset, sample_source_record]

        response = client.post(
            f"/api/v1/media-assets/{sample_media_asset.id}/transcribe/retry",
            json={"language": "en"},
        )

        assert response.status_code == 400
        assert "can only retry failed transcriptions" in response.json()["detail"].lower()
        mock_retry.assert_not_called()

    def test_list_transcripts(self, client, mock_session, sample_media_asset, sample_transcript):
        """Test listing transcripts for a media asset."""
        mock_result = Mock()
        mock_result.scalars.return_value.all.return_value = [sample_transcript]
        mock_session.execute.return_value = mock_result

        response = client.get(f"/api/v1/media-assets/{sample_media_asset.id}/transcripts")

        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["id"] == sample_transcript.id
        assert data[0]["media_asset_id"] == sample_media_asset.id

    def test_get_transcript_detail(self, client, mock_session, sample_media_asset, sample_transcript, sample_segments):
        """Test getting transcript detail with segments."""
        mock_session.get.side_effect = [sample_media_asset, sample_transcript]

        segments_result = Mock()
        segments_result.scalars.return_value.all.return_value = sample_segments
        mock_session.execute.return_value = segments_result

        response = client.get(f"/api/v1/media-assets/{sample_media_asset.id}/transcripts/{sample_transcript.id}")

        assert response.status_code == 200
        data = response.json()
        assert data["id"] == sample_transcript.id
        assert data["media_asset_id"] == sample_media_asset.id
        assert data["segment_count"] == 2
        assert data["total_duration_ms"] == 20000

    def test_get_transcript_detail_not_found(self, client, mock_session, sample_media_asset):
        """Test getting transcript detail when transcript doesn't exist."""
        mock_result = Mock()
        mock_result.scalars.return_value.first.return_value = None
        mock_session.execute.return_value = mock_result

        response = client.get(f"/api/v1/media-assets/{sample_media_asset.id}/transcripts/{uuid4()}")

        assert response.status_code == 404
        assert "not found" in response.json()["detail"].lower()