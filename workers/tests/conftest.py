"""
Pytest configuration and shared fixtures for ClipYantra Workers tests.
"""

import asyncio
import os
import tempfile
from pathlib import Path
from typing import AsyncGenerator, Generator
from unittest.mock import AsyncMock, MagicMock

import pytest
import pytest_asyncio
from faker import Faker

# Set test environment variables before importing app modules
os.environ.setdefault("APP_ENV", "testing")
os.environ.setdefault("DEBUG", "true")
os.environ.setdefault("LOG_LEVEL", "DEBUG")
os.environ.setdefault("DATABASE_URL", "postgresql+asyncpg://postgres:postgres@localhost:5432/clipyantra_test")
os.environ.setdefault("REDIS_URL", "redis://localhost:6379/1")
os.environ.setdefault("CELERY_TASK_ALWAYS_EAGER", "true")
os.environ.setdefault("CELERY_TASK_EAGER_PROPAGATES", "true")


@pytest.fixture(scope="session")
def event_loop() -> Generator[asyncio.AbstractEventLoop, None, None]:
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
def faker() -> Faker:
    """Faker instance for generating test data."""
    return Faker()


@pytest.fixture
def temp_dir() -> Generator[Path, None, None]:
    """Create a temporary directory for test files."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


@pytest.fixture
def sample_video_path(temp_dir: Path) -> Path:
    """Create a sample video file for testing."""
    video_path = temp_dir / "sample.mp4"
    # Create a minimal valid MP4 file (just header)
    video_path.write_bytes(b"\x00\x00\x00\x18ftypmp42\x00\x00\x00\x00mp42isom")
    return video_path


@pytest.fixture
def sample_audio_path(temp_dir: Path) -> Path:
    """Create a sample audio file for testing."""
    audio_path = temp_dir / "sample.wav"
    # Create a minimal valid WAV file (just header)
    audio_path.write_bytes(b"RIFF$\x00\x00\x00WAVEfmt \x10\x00\x00\x00\x01\x00\x01\x00\x00\x04\x00\x00\x00\x04\x00\x00\x01\x00\x08\x00data\x00\x00\x00\x00")
    return audio_path


@pytest.fixture
def mock_celery_app():
    """Mock Celery app for testing tasks without broker."""
    from unittest.mock import MagicMock
    app = MagicMock()
    app.send_task = MagicMock()
    app.control.inspect = MagicMock()
    return app


@pytest.fixture
def mock_redis():
    """Mock Redis client."""
    return AsyncMock()


@pytest.fixture
def mock_db_session():
    """Mock database session."""
    return AsyncMock()


@pytest.fixture
def sample_media_metadata():
    """Sample media metadata for testing."""
    from app.processors.base import MediaMetadata
    return MediaMetadata(
        duration=120.5,
        width=1920,
        height=1080,
        frame_rate=30.0,
        video_codec="h264",
        audio_codec="aac",
        bitrate=5000000,
        format_name="mp4",
        format_long_name="QuickTime / MOV",
        size=1024 * 1024 * 50,  # 50 MB
        streams=[
            {
                "index": 0,
                "codec_type": "video",
                "codec_name": "h264",
                "width": 1920,
                "height": 1080,
                "r_frame_rate": "30/1",
                "bit_rate": "5000000"
            },
            {
                "index": 1,
                "codec_type": "audio",
                "codec_name": "aac",
                "sample_rate": "48000",
                "channels": 2,
                "bit_rate": "128000"
            }
        ]
    )


@pytest.fixture
def sample_transcription_result():
    """Sample transcription result for testing."""
    from app.processors.base import TranscriptionResult, TranscriptionSegment
    return TranscriptionResult(
        text="Hello world. This is a test transcription.",
        language="en",
        language_probability=0.99,
        duration=120.5,
        segments=[
            TranscriptionSegment(
                id=0,
                start=0.0,
                end=5.0,
                text="Hello world.",
                words=[
                    {"word": "Hello", "start": 0.0, "end": 0.5, "probability": 0.99},
                    {"word": "world", "start": 0.5, "end": 1.0, "probability": 0.98}
                ],
                avg_logprob=-0.1,
                compression_ratio=1.5,
                no_speech_prob=0.01
            ),
            TranscriptionSegment(
                id=1,
                start=5.0,
                end=10.0,
                text="This is a test transcription.",
                words=[
                    {"word": "This", "start": 5.0, "end": 5.2, "probability": 0.99},
                    {"word": "is", "start": 5.2, "end": 5.3, "probability": 0.99},
                    {"word": "a", "start": 5.3, "end": 5.4, "probability": 0.99},
                    {"word": "test", "start": 5.4, "end": 5.7, "probability": 0.98},
                    {"word": "transcription", "start": 5.7, "end": 6.5, "probability": 0.97}
                ],
                avg_logprob=-0.2,
                compression_ratio=1.4,
                no_speech_prob=0.02
            )
        ]
    )


@pytest.fixture
def sample_render_preset():
    """Sample render preset for testing."""
    from app.processors.base import RenderPreset
    return RenderPreset(
        name="social_1080p",
        width=1920,
        height=1080,
        fps=30,
        video_codec="libx264",
        video_bitrate="5000k",
        audio_codec="aac",
        audio_bitrate="128k",
        preset="medium",
        profile="high",
        level="4.1",
        pixel_format="yuv420p",
        extra_args=["-movflags", "+faststart"]
    )


# Async fixtures for integration tests
@pytest_asyncio.fixture
async def async_temp_dir() -> AsyncGenerator[Path, None]:
    """Create a temporary directory for async tests."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


# Markers
def pytest_configure(config):
    """Configure pytest markers."""
    config.addinivalue_line("markers", "unit: Unit tests")
    config.addinivalue_line("markers", "integration: Integration tests")
    config.addinivalue_line("markers", "slow: Slow tests")
    config.addinivalue_line("markers", "gpu: Tests requiring GPU")
    config.addinivalue_line("markers", "ffmpeg: Tests requiring FFmpeg")
    config.addinivalue_line("markers", "whisper: Tests requiring Whisper model")


# Collection hooks
def pytest_collection_modifyitems(config, items):
    """Modify test collection to add markers based on path."""
    for item in items:
        # Mark integration tests
        if "integration" in str(item.fspath):
            item.add_marker(pytest.mark.integration)
        # Mark unit tests
        elif "unit" in str(item.fspath):
            item.add_marker(pytest.mark.unit)
        # Mark slow tests by name
        if "slow" in item.name.lower() or "performance" in item.name.lower():
            item.add_marker(pytest.mark.slow)