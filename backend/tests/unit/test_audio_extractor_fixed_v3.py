"""Unit tests for AudioExtractor service (ING-003)."""

import pytest
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock, AsyncMock

from app.services.audio_extractor import (
    AudioExtractor,
    AudioChunk,
    ExtractionResult,
    ChunkTranscriptionResult,
    SegmentResult,
    MergedSegment,
)


class TestAudioExtractor:
    """Test AudioExtractor functionality."""

    @pytest.fixture
    def extractor(self):
        """Create AudioExtractor instance."""
        return AudioExtractor(
            ffmpeg_path="ffmpeg",
            ffprobe_path="ffprobe",
            chunk_duration_ms=1800 * 1000,  # 30 minutes in ms
            overlap_ms=30 * 1000,  # 30 seconds in ms
        )

    @pytest.mark.asyncio
    async def test_extract_audio_creates_chunks(self, extractor, tmp_path):
        """Test audio extraction creates expected chunks for long video."""
        media_path = tmp_path / "test_video.mp4"
        media_path.write_bytes(b"fake video content")

        output_dir = tmp_path / "audio_chunks"
        output_dir.mkdir(parents=True, exist_ok=True)

        # Mock the async subprocess calls
        with patch.object(extractor, '_get_duration', return_value=2700000) as mock_get_duration, \
             patch.object(extractor, '_run_ffmpeg', new_callable=AsyncMock) as mock_run_ffmpeg, \
             patch.object(extractor, '_create_chunks', new_callable=AsyncMock) as mock_create_chunks:

            # Setup expected chunks
            chunk1 = AudioChunk(
                path=output_dir / "test_video_audio_chunk_000.wav",
                start_ms=0,
                end_ms=1830000,
                chunk_index=0,
                is_overlap=False,
            )
            chunk2 = AudioChunk(
                path=output_dir / "test_video_audio_chunk_001.wav",
                start_ms=1800000,
                end_ms=2700000,
                chunk_index=1,
                is_overlap=True,
            )
            mock_create_chunks.return_value = [chunk1, chunk2]

            result = await extractor.extract_audio(media_path, output_dir)

        assert isinstance(result, ExtractionResult)
        assert len(result.chunks) == 2
        assert result.duration_ms == 2700000  # 45 min in ms

        assert result.chunks[0].start_ms == 0
        assert result.chunks[0].end_ms == 1830000  # 30 min + 30 sec overlap

        assert result.chunks[1].start_ms == 1800000  # 30 min (overlap)
        assert result.chunks[1].end_ms == 2700000  # End of video

    @pytest.mark.asyncio
    async def test_extract_audio_short_video_single_chunk(self, extractor, tmp_path):
        """Test audio extraction for short video (< 30 min)."""
        media_path = tmp_path / "short_video.mp4"
        media_path.write_bytes(b"fake video content")

        output_dir = tmp_path / "audio_chunks"
        output_dir.mkdir(parents=True, exist_ok=True)

        with patch.object(extractor, '_get_duration', return_value=600000) as mock_get_duration, \
             patch.object(extractor, '_run_ffmpeg', new_callable=AsyncMock) as mock_run_ffmpeg, \
             patch.object(extractor, '_create_chunks', new_callable=AsyncMock) as mock_create_chunks:

            chunk = AudioChunk(
                path=output_dir / "short_video_audio.wav",
                start_ms=0,
                end_ms=600000,
                chunk_index=0,
                is_overlap=False,
            )
            mock_create_chunks.return_value = [chunk]

            result = await extractor.extract_audio(media_path, output_dir)

        assert len(result.chunks) == 1
        assert result.chunks[0].start_ms == 0
        assert result.chunks[0].end_ms == 600000

    @pytest.mark.asyncio
    async def test_extract_audio_missing_file_raises(self, extractor):
        """Test extraction raises RuntimeError for missing media (via ffprobe)."""
        with patch.object(extractor, '_get_duration', side_effect=RuntimeError("ffprobe failed: file not found")):
            with pytest.raises(RuntimeError, match="ffprobe failed"):
                await extractor.extract_audio("/nonexistent/video.mp4", Path("/tmp/output"))

    @pytest.mark.asyncio
    async def test_extract_audio_ffprobe_failure_raises(self, extractor, tmp_path):
        """Test extraction raises on ffprobe failure."""
        media_path = tmp_path / "test.mp4"
        media_path.write_bytes(b"content")

        with patch.object(extractor, '_get_duration', side_effect=RuntimeError("ffprobe failed: error")):
            with pytest.raises(RuntimeError, match="ffprobe failed"):
                await extractor.extract_audio(str(media_path), tmp_path / "out")

    @pytest.mark.asyncio
    async def test_extract_audio_ffmpeg_failure_raises(self, extractor, tmp_path):
        """Test extraction raises on ffmpeg failure."""
        media_path = tmp_path / "test.mp4"
        media_path.write_bytes(b"content")

        with patch.object(extractor, '_get_duration', return_value=2700000), \
             patch.object(extractor, '_run_ffmpeg', side_effect=RuntimeError("FFmpeg failed (exit 1): error")):

            with pytest.raises(RuntimeError, match="FFmpeg failed"):
                await extractor.extract_audio(media_path, tmp_path / "out")


class TestMergeSegments:
    """Test segment merging and overlap deduplication."""

    @pytest.fixture
    def extractor(self):
        return AudioExtractor(
            ffmpeg_path="ffmpeg",
            ffprobe_path="ffprobe",
            chunk_duration_ms=1800 * 1000,
            overlap_ms=30 * 1000,
        )

    def test_merge_no_overlap(self, extractor):
        """Test merging segments with no overlap."""
        chunk_results = [
            ChunkTranscriptionResult(
                chunk_start_ms=0,
                chunk_end_ms=20000,
                segments=[
                    SegmentResult(start_ms=0, end_ms=10000, text="Hello", confidence=0.9),
                    SegmentResult(start_ms=10000, end_ms=20000, text="World", confidence=0.8),
                ]
            )
        ]

        merged = extractor.merge_segments(chunk_results)

        assert len(merged) == 2
        assert merged[0].text == "Hello"
        assert merged[1].text == "World"
        assert merged[0].start_ms == 0
        assert merged[0].end_ms == 10000
        assert merged[1].start_ms == 10000
        assert merged[1].end_ms == 20000

    def test_merge_with_overlap_keep_higher_confidence(self, extractor):
        """Test merging keeps higher confidence segment in overlap across chunks."""
        # Use two chunks with overlapping regions to test the merge logic
        chunk_results = [
            ChunkTranscriptionResult(
                chunk_start_ms=0,
                chunk_end_ms=20000,
                segments=[
                    SegmentResult(start_ms=0, end_ms=15000, text="Hello world", confidence=0.7),  # abs: 0-15000
                ]
            ),
            ChunkTranscriptionResult(
                chunk_start_ms=10000,
                chunk_end_ms=30000,
                segments=[
                    SegmentResult(start_ms=0, end_ms=15000, text="world again", confidence=0.9),  # abs: 10000-25000
                ]
            ),
        ]

        merged = extractor.merge_segments(chunk_results)

        # Segment 1: abs 0-15000, conf=0.7
        # Segment 2: abs 10000-25000, conf=0.9 (higher)
        # They overlap (10000 < 15000), so keep higher confidence (seg 2)
        # The higher confidence segment REPLACES the previous one
        assert len(merged) == 1
        assert merged[0].start_ms == 10000
        assert merged[0].end_ms == 25000
        assert merged[0].text == "world again"
        assert merged[0].confidence == 0.9

    def test_merge_with_overlap_keep_first_higher_confidence(self, extractor):
        """Test merging keeps first segment when it has higher confidence across chunks."""
        chunk_results = [
            ChunkTranscriptionResult(
                chunk_start_ms=0,
                chunk_end_ms=20000,
                segments=[
                    SegmentResult(start_ms=0, end_ms=15000, text="Hello world", confidence=0.9),  # abs: 0-15000
                ]
            ),
            ChunkTranscriptionResult(
                chunk_start_ms=10000,
                chunk_end_ms=30000,
                segments=[
                    SegmentResult(start_ms=0, end_ms=15000, text="world again", confidence=0.7),  # abs: 10000-25000
                ]
            ),
        ]

        merged = extractor.merge_segments(chunk_results)

        # Segment 1: abs 0-15000, conf=0.9 (higher)
        # Segment 2: abs 10000-25000, conf=0.7
        # They overlap (10000 < 15000), but first has higher confidence, so kept
        assert len(merged) == 1
        assert merged[0].start_ms == 0
        assert merged[0].end_ms == 15000
        assert merged[0].text == "Hello world"
        assert merged[0].confidence == 0.9

    def test_merge_empty_list(self, extractor):
        """Test merging empty list returns empty."""
        merged = extractor.merge_segments([])
        assert merged == []

    def test_merge_single_segment(self, extractor):
        """Test merging single chunk with single segment."""
        chunk_results = [
            ChunkTranscriptionResult(
                chunk_start_ms=0,
                chunk_end_ms=10000,
                segments=[
                    SegmentResult(start_ms=0, end_ms=10000, text="Hello", confidence=0.9),
                ]
            )
        ]

        merged = extractor.merge_segments(chunk_results)
        assert len(merged) == 1
        assert merged[0].text == "Hello"
        assert merged[0].start_ms == 0
        assert merged[0].end_ms == 10000

    def test_merge_multiple_chunks_with_overlap(self, extractor):
        """Test merging multiple chunks with overlap region."""
        chunk_results = [
            ChunkTranscriptionResult(
                chunk_start_ms=0,
                chunk_end_ms=1830000,
                segments=[
                    SegmentResult(start_ms=0, end_ms=10000, text="First chunk", confidence=0.9),
                    SegmentResult(start_ms=1800000, end_ms=1820000, text="Overlap region", confidence=0.8),
                ]
            ),
            ChunkTranscriptionResult(
                chunk_start_ms=1800000,
                chunk_end_ms=3600000,
                segments=[
                    SegmentResult(start_ms=0, end_ms=20000, text="Overlap again", confidence=0.7),  # abs: 1800000-1820000
                    SegmentResult(start_ms=20000, end_ms=30000, text="Second chunk", confidence=0.9),  # abs: 1820000-1830000
                ]
            ),
        ]

        merged = extractor.merge_segments(chunk_results)

        # Should have merged segments:
        # 1. "First chunk" (0-10000) - no overlap
        # 2. "Overlap region" (1800000-1820000) from chunk 1, confidence 0.8
        # 3. "Overlap again" (1800000-1820000) from chunk 2, confidence 0.7 - overlap with above, lower confidence so discarded
        # 4. "Second chunk" (1820000-1830000) - no overlap with previous kept segment

        # Let's trace through:
        # All segments with absolute times:
        # 1. abs 0-10000, "First chunk", 0.9
        # 2. abs 1800000-1820000, "Overlap region", 0.8
        # 3. abs 1800000-1820000, "Overlap again", 0.7
        # 4. abs 1820000-1830000, "Second chunk", 0.9

        # Sorted by abs_start:
        # 1. abs 0-10000 -> added
        # 2. abs 1800000-1820000 -> no overlap with prev (10000 < 1800000) -> added
        # 3. abs 1800000-1820000 -> overlaps with prev (1800000 < 1820000), conf 0.7 < 0.8 -> discard
        # 4. abs 1820000-1830000 -> no overlap with prev (1820000 >= 1820000) -> added

        assert len(merged) == 3
        assert merged[0].text == "First chunk"
        assert merged[1].text == "Overlap region"
        assert merged[2].text == "Second chunk"


class TestAudioChunk:
    """Test AudioChunk dataclass."""

    def test_chunk_duration_calculation(self):
        """Test chunk duration is calculated correctly."""
        chunk = AudioChunk(
            chunk_index=0,
            path=Path("/tmp/chunk_000.wav"),
            start_ms=0,
            end_ms=1830000,
        )

        assert chunk.end_ms - chunk.start_ms == 1830000

    def test_chunk_overlap_duration(self):
        """Test chunk overlap calculation."""
        chunk1 = AudioChunk(chunk_index=0, path=Path("/tmp/c1.wav"), start_ms=0, end_ms=1830000)
        chunk2 = AudioChunk(chunk_index=1, path=Path("/tmp/c2.wav"), start_ms=1800000, end_ms=3630000)

        overlap = chunk1.end_ms - chunk2.start_ms
        assert overlap == 30000  # 30 seconds


class TestAudioChunkDataclass:
    """Test AudioChunk dataclass fields."""

    def test_audio_chunk_fields(self):
        """Test AudioChunk has all required fields."""
        chunk = AudioChunk(
            path=Path("/tmp/test.wav"),
            start_ms=0,
            end_ms=10000,
            chunk_index=0,
            is_overlap=False,
        )

        assert chunk.path == Path("/tmp/test.wav")
        assert chunk.start_ms == 0
        assert chunk.end_ms == 10000
        assert chunk.chunk_index == 0
        assert chunk.is_overlap is False

    def test_audio_chunk_is_overlap_true(self):
        """Test AudioChunk with is_overlap=True."""
        chunk = AudioChunk(
            path=Path("/tmp/test.wav"),
            start_ms=10000,
            end_ms=20000,
            chunk_index=1,
            is_overlap=True,
        )

        assert chunk.is_overlap is True


class TestExtractionResult:
    """Test ExtractionResult dataclass."""

    def test_extraction_result_fields(self, tmp_path):
        """Test ExtractionResult has all required fields."""
        audio_path = tmp_path / "audio.wav"
        audio_path.write_bytes(b"audio")

        chunks = [
            AudioChunk(
                path=audio_path,
                start_ms=0,
                end_ms=10000,
                chunk_index=0,
                is_overlap=False,
            )
        ]

        result = ExtractionResult(
            audio_path=audio_path,
            duration_ms=10000,
            chunks=chunks,
            sample_rate=16000,
            channels=1,
        )

        assert result.audio_path == audio_path
        assert result.duration_ms == 10000
        assert result.chunks == chunks
        assert result.sample_rate == 16000
        assert result.channels == 1


class TestSegmentResult:
    """Test SegmentResult dataclass."""

    def test_segment_result_fields(self):
        """Test SegmentResult has all required fields."""
        segment = SegmentResult(
            start_ms=0,
            end_ms=10000,
            text="Hello world",
            speaker="SPEAKER_00",
            confidence=0.95,
            word_alignments=[{"word": "Hello", "start_ms": 0, "end_ms": 5000, "confidence": 0.9}],
        )

        assert segment.start_ms == 0
        assert segment.end_ms == 10000
        assert segment.text == "Hello world"
        assert segment.speaker == "SPEAKER_00"
        assert segment.confidence == 0.95
        assert segment.word_alignments is not None

    def test_segment_result_optional_fields(self):
        """Test SegmentResult with optional fields as None."""
        segment = SegmentResult(
            start_ms=0,
            end_ms=10000,
            text="Hello",
        )

        assert segment.speaker is None
        assert segment.confidence is None
        assert segment.word_alignments is None


class TestMergedSegment:
    """Test MergedSegment dataclass."""

    def test_merged_segment_fields(self):
        """Test MergedSegment has all required fields."""
        merged = MergedSegment(
            start_ms=0,
            end_ms=10000,
            text="Hello world",
            speaker="SPEAKER_00",
            confidence=0.95,
            word_alignments=[{"word": "Hello"}],
        )

        assert merged.start_ms == 0
        assert merged.end_ms == 10000
        assert merged.text == "Hello world"
        assert merged.speaker == "SPEAKER_00"
        assert merged.confidence == 0.95
        assert merged.word_alignments is not None


class TestChunkTranscriptionResult:
    """Test ChunkTranscriptionResult dataclass."""

    def test_chunk_transcription_result_fields(self):
        """Test ChunkTranscriptionResult has all required fields."""
        segments = [
            SegmentResult(start_ms=0, end_ms=10000, text="Hello", confidence=0.9),
        ]

        result = ChunkTranscriptionResult(
            chunk_start_ms=0,
            chunk_end_ms=10000,
            segments=segments,
        )

        assert result.chunk_start_ms == 0
        assert result.chunk_end_ms == 10000
        assert result.segments == segments