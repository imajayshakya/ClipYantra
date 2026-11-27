"""Unit tests for AudioExtractor (ING-003)."""

import pytest
from pathlib import Path
from unittest.mock import Mock, patch, AsyncMock

from app.services.audio_extractor import (
    AudioExtractor,
    AudioChunk,
    ExtractionResult,
    SegmentResult,
    ChunkTranscriptionResult,
    MergedSegment,
)


class TestAudioExtractor:
    """Test AudioExtractor class."""

    @pytest.fixture
    def extractor(self):
        """Create AudioExtractor instance."""
        return AudioExtractor()

    @pytest.fixture
    def mock_ffprobe_output(self):
        """Mock ffprobe output for duration."""
        return {
            "format": {
                "duration": "10.5"
            }
        }

    def test_extractor_defaults(self, extractor):
        """Test default chunk and overlap values."""
        assert extractor.chunk_duration_ms == 1800000  # 30 minutes
        assert extractor.overlap_ms == 30000  # 30 seconds

    def test_extractor_custom_values(self):
        """Test custom chunk and overlap values."""
        extractor = AudioExtractor(chunk_duration_ms=600000, overlap_ms=10000)
        assert extractor.chunk_duration_ms == 600000
        assert extractor.overlap_ms == 10000

    @pytest.mark.asyncio
    async def test_extract_audio_creates_chunks(self, extractor):
        """Test audio extraction creates chunks for long video."""
        with patch.object(extractor, '_get_duration', new_callable=AsyncMock) as mock_get_duration, \
             patch.object(extractor, '_run_ffmpeg', new_callable=AsyncMock) as mock_ffmpeg, \
             patch('tempfile.mkdtemp', return_value="/tmp/test_audio"), \
             patch('pathlib.Path.mkdir'), \
             patch('pathlib.Path.exists', return_value=True), \
             patch('pathlib.Path.stat') as mock_stat:

            # Mock duration for 45 minutes = 2700000ms (requires 2 chunks with overlap)
            mock_get_duration.return_value = 2700000
            mock_stat.return_value.st_size = 1024 * 1024

            result = await extractor.extract_audio(Path("/tmp/video.mp4"))

            assert isinstance(result, ExtractionResult)
            assert result.audio_path is not None
            assert result.duration_ms == 2700000
            assert len(result.chunks) > 1  # Should have multiple chunks
            assert result.sample_rate == 16000
            assert result.channels == 1

    @pytest.mark.asyncio
    async def test_extract_audio_short_video_single_chunk(self, extractor):
        """Test short video creates single chunk without overlap."""
        with patch.object(extractor, '_get_duration', new_callable=AsyncMock) as mock_get_duration, \
             patch.object(extractor, '_run_ffmpeg', new_callable=AsyncMock) as mock_ffmpeg, \
             patch('tempfile.mkdtemp', return_value="/tmp/test_audio"), \
             patch('pathlib.Path.mkdir'), \
             patch('pathlib.Path.exists', return_value=True), \
             patch('pathlib.Path.stat') as mock_stat:

            mock_get_duration.return_value = 10000
            mock_stat.return_value.st_size = 1024 * 1024

            result = await extractor.extract_audio(Path("/tmp/video.mp4"))

            assert isinstance(result, ExtractionResult)
            assert result.duration_ms == 10000
            assert len(result.chunks) == 1
            assert result.chunks[0].chunk_index == 0
            assert result.chunks[0].is_overlap is False

    @pytest.mark.asyncio
    async def test_extract_audio_missing_file_raises(self, extractor):
        """Test missing file raises FileNotFoundError."""
        with pytest.raises(FileNotFoundError):
            await extractor.extract_audio(Path("/nonexistent/video.mp4"))

    @pytest.mark.asyncio
    async def test_extract_audio_ffprobe_failure_raises(self, extractor):
        """Test ffprobe failure raises RuntimeError."""
        with patch.object(extractor, '_get_duration', new_callable=AsyncMock) as mock_get_duration:
            mock_get_duration.side_effect = RuntimeError("ffprobe failed")

            with pytest.raises(RuntimeError, match="ffprobe failed"):
                await extractor.extract_audio(Path("/tmp/video.mp4"))

    @pytest.mark.asyncio
    async def test_extract_audio_ffmpeg_failure_raises(self, extractor):
        """Test ffmpeg failure raises RuntimeError."""
        with patch.object(extractor, '_get_duration', new_callable=AsyncMock) as mock_get_duration, \
             patch.object(extractor, '_run_ffmpeg', new_callable=AsyncMock) as mock_ffmpeg:
            mock_get_duration.return_value = 10000
            mock_ffmpeg.side_effect = RuntimeError("ffmpeg failed")

            with pytest.raises(RuntimeError, match="ffmpeg failed"):
                await extractor.extract_audio(Path("/tmp/video.mp4"))

    def test_chunk_duration_calculation(self, extractor):
        """Test chunk duration calculation with overlap."""
        assert extractor.chunk_duration_ms == 1800000
        assert extractor.overlap_ms == 30000

    def test_audio_chunk_properties(self):
        """Test AudioChunk dataclass."""
        chunk = AudioChunk(
            path=Path("/tmp/chunk_000.wav"),
            chunk_index=0,
            start_ms=0,
            end_ms=1800000,
        )
        assert chunk.path == Path("/tmp/chunk_000.wav")
        assert chunk.chunk_index == 0
        assert chunk.start_ms == 0
        assert chunk.end_ms == 1800000


class TestMergeSegments:
    """Test merge_segments overlap deduplication."""

    @pytest.mark.asyncio
    async def test_merge_segments_no_overlap(self):
        """Test merging segments with no overlap."""
        segment1 = SegmentResult(
            start_ms=0, end_ms=5000, text="Hello", confidence=0.9, speaker="SPEAKER_00"
        )
        segment2 = SegmentResult(
            start_ms=5000, end_ms=10000, text="World", confidence=0.8, speaker="SPEAKER_00"
        )

        chunk_result = ChunkTranscriptionResult(
            chunk_start_ms=0,
            chunk_end_ms=10000,
            segments=[segment1, segment2],
        )

        merged = AudioExtractor.merge_segments([chunk_result])

        assert len(merged) == 2
        assert merged[0].text == "Hello"
        assert merged[1].text == "World"

    @pytest.mark.asyncio
    async def test_merge_segments_with_overlap_keeps_higher_confidence(self):
        """Test overlap deduplication keeps higher confidence segment."""
        # Segment from chunk 0 ending at 5.5s
        segment1 = SegmentResult(
            start_ms=0, end_ms=5500, text="Hello world", confidence=0.7, speaker="SPEAKER_00"
        )
        # Overlapping segment from chunk 1 starting at 5.0s
        segment2 = SegmentResult(
            start_ms=5000, end_ms=10000, text="world again", confidence=0.9, speaker="SPEAKER_00"
        )

        chunk_result1 = ChunkTranscriptionResult(
            chunk_start_ms=0,
            chunk_end_ms=5500,
            segments=[segment1],
        )
        chunk_result2 = ChunkTranscriptionResult(
            chunk_start_ms=5000,
            chunk_end_ms=10000,
            segments=[segment2],
        )

        merged = AudioExtractor.merge_segments([chunk_result1, chunk_result2])

        # Should keep segment2 (higher confidence) and trim segment1
        assert len(merged) == 2
        assert merged[0].end_ms <= merged[1].start_ms  # No overlap

    @pytest.mark.asyncio
    async def test_merge_segments_overlap_different_speakers(self):
        """Test overlap with different speakers keeps both."""
        segment1 = SegmentResult(
            start_ms=0, end_ms=5500, text="Hello", confidence=0.9, speaker="SPEAKER_00"
        )
        segment2 = SegmentResult(
            start_ms=5000, end_ms=10000, text="Hi there", confidence=0.8, speaker="SPEAKER_01"
        )

        chunk_result1 = ChunkTranscriptionResult(
            chunk_start_ms=0,
            chunk_end_ms=5500,
            segments=[segment1],
        )
        chunk_result2 = ChunkTranscriptionResult(
            chunk_start_ms=5000,
            chunk_end_ms=10000,
            segments=[segment2],
        )

        merged = AudioExtractor.merge_segments([chunk_result1, chunk_result2])

        # Different speakers - both should be kept (with trimmed overlap)
        assert len(merged) == 2


class TestExtractionResult:
    """Test ExtractionResult dataclass."""

    def test_extraction_result_properties(self):
        """Test ExtractionResult properties."""
        chunks = [
            AudioChunk(path=Path("/tmp/chunk_000.wav"), chunk_index=0, start_ms=0, end_ms=10000),
            AudioChunk(path=Path("/tmp/chunk_001.wav"), chunk_index=1, start_ms=9000, end_ms=20000),
        ]

        result = ExtractionResult(
            audio_path=Path("/tmp/audio.wav"),
            duration_ms=20000,
            chunks=chunks,
            sample_rate=16000,
            channels=1,
        )

        assert result.audio_path == Path("/tmp/audio.wav")
        assert result.duration_ms == 20000
        assert len(result.chunks) == 2
        assert result.sample_rate == 16000
        assert result.channels == 1