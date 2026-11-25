"""Unit tests for FFprobe validator (ING-002 AC1, AC2, AC3)."""

import pytest
from unittest.mock import Mock, patch, AsyncMock
from pathlib import Path

from app.services.ffprobe_validator import (
    FFprobeValidator,
    ValidationResult,
    UnsupportedFormatError,
    create_validator,
)
from app.services.storage_adapter import LocalFilesystemAdapter, StorageConfig


class TestFFprobeValidator:
    """Test FFprobe validation logic."""

    @pytest.fixture
    def mock_storage(self):
        """Create a mock storage adapter."""
        storage = Mock(spec=LocalFilesystemAdapter)
        storage.get_file_path.return_value = "/fake/path/test_video.mp4"
        return storage

    @pytest.fixture
    def validator(self, mock_storage):
        """Create validator with mock storage."""
        return FFprobeValidator(storage=mock_storage)

    @pytest.fixture
    def sample_ffprobe_output(self):
        """Sample FFprobe JSON output for a valid video."""
        return {
            "streams": [
                {
                    "index": 0,
                    "codec_type": "video",
                    "codec_name": "h264",
                    "codec_long_name": "H.264 / AVC / MPEG-4 AVC / MPEG-4 part 10",
                    "profile": "High",
                    "width": 1920,
                    "height": 1080,
                    "has_b_frames": 2,
                    "sample_aspect_ratio": "1:1",
                    "display_aspect_ratio": "16:9",
                    "pix_fmt": "yuv420p",
                    "level": 40,
                    "color_range": "tv",
                    "color_space": "bt709",
                    "color_transfer": "bt709",
                    "color_primaries": "bt709",
                    "chroma_location": "left",
                    "field_order": "progressive",
                    "refs": 1,
                    "is_avc": "true",
                    "nal_length_size": "4",
                    "r_frame_rate": "30000/1001",
                    "avg_frame_rate": "30000/1001",
                    "time_base": "1/90000",
                    "start_pts": 0,
                    "start_time": "0.000000",
                    "duration_ts": 1500000,
                    "duration": "16.666667",
                    "bit_rate": "5000000",
                    "bits_per_raw_sample": "8",
                    "nb_frames": "500",
                    "disposition": {
                        "default": 1,
                        "dub": 0,
                        "original": 0,
                        "comment": 0,
                        "lyrics": 0,
                        "karaoke": 0,
                        "forced": 0,
                        "hearing_impaired": 0,
                        "visual_impaired": 0,
                        "clean_effects": 0,
                        "attached_pic": 0,
                        "timed_thumbnails": 0,
                        "non_diegetic": 0,
                        "captions": 0,
                        "descriptions": 0,
                        "metadata": 0,
                        "dependent": 0,
                        "still_image": 0,
                    },
                    "tags": {
                        "language": "und",
                        "handler_name": "VideoHandler",
                    },
                },
                {
                    "index": 1,
                    "codec_type": "audio",
                    "codec_name": "aac",
                    "codec_long_name": "AAC (Advanced Audio Coding)",
                    "profile": "LC",
                    "sample_fmt": "fltp",
                    "sample_rate": "48000",
                    "channels": 2,
                    "channel_layout": "stereo",
                    "bits_per_sample": 0,
                    "r_frame_rate": "0/0",
                    "avg_frame_rate": "0/0",
                    "time_base": "1/48000",
                    "start_pts": 0,
                    "start_time": "0.000000",
                    "duration_ts": 800000,
                    "duration": "16.666667",
                    "bit_rate": "128000",
                    "max_bit_rate": "128000",
                    "nb_frames": "782",
                    "disposition": {
                        "default": 1,
                        "dub": 0,
                        "original": 0,
                        "comment": 0,
                        "lyrics": 0,
                        "karaoke": 0,
                        "forced": 0,
                        "hearing_impaired": 0,
                        "visual_impaired": 0,
                        "clean_effects": 0,
                        "attached_pic": 0,
                        "timed_thumbnails": 0,
                        "non_diegetic": 0,
                        "captions": 0,
                        "descriptions": 0,
                        "metadata": 0,
                        "dependent": 0,
                        "still_image": 0,
                    },
                    "tags": {
                        "language": "und",
                        "handler_name": "SoundHandler",
                    },
                },
            ],
            "format": {
                "filename": "/fake/path/test_video.mp4",
                "nb_streams": 2,
                "nb_programs": 0,
                "format_name": "mov,mp4,m4a,3gp,3g2,mj2",
                "format_long_name": "QuickTime / MOV",
                "start_time": "0.000000",
                "duration": "16.666667",
                "size": "10737418",
                "bit_rate": "5128000",
                "probe_score": 100,
                "tags": {
                    "major_brand": "isom",
                    "minor_version": "512",
                    "compatible_brands": "isomiso2avc1mp41",
                    "encoder": "Lavf58.29.100",
                },
            },
        }

    @pytest.mark.asyncio
    async def test_validate_supported_container(self, validator, sample_ffprobe_output):
        """AC1: Validate supported container formats (mp4, mov, mkv, webm, mp3, wav, m4a)."""
        with patch.object(validator, '_run_ffprobe', new_callable=AsyncMock) as mock_ffprobe:
            mock_ffprobe.return_value = sample_ffprobe_output
            
            result = await validator.validate("/fake/path/test_video.mp4")
            
            assert result.is_valid is True
            assert result.container == "mp4"
            assert result.duration_ms == 16666  # ~16.666 seconds
            assert result.width == 1920
            assert result.height == 1080

    @pytest.mark.asyncio
    async def test_validate_supported_video_codecs(self, validator, sample_ffprobe_output):
        """AC1: Validate supported video codecs (h264, hevc, vp9, av1)."""
        with patch.object(validator, '_run_ffprobe', new_callable=AsyncMock) as mock_ffprobe:
            mock_ffprobe.return_value = sample_ffprobe_output
            
            result = await validator.validate("/fake/path/test_video.mp4")
            
            assert result.is_valid is True
            assert result.video_codec == "h264"

    @pytest.mark.asyncio
    async def test_validate_supported_audio_codecs(self, validator, sample_ffprobe_output):
        """AC1: Validate supported audio codecs (aac, opus, mp3, pcm_s16le, flac)."""
        with patch.object(validator, '_run_ffprobe', new_callable=AsyncMock) as mock_ffprobe:
            mock_ffprobe.return_value = sample_ffprobe_output
            
            result = await validator.validate("/fake/path/test_video.mp4")
            
            assert result.is_valid is True
            assert result.audio_codec == "aac"

    @pytest.mark.asyncio
    async def test_reject_unsupported_container(self, validator):
        """AC2: Reject unsupported container formats."""
        unsupported_output = {
            "streams": [
                {
                    "index": 0,
                    "codec_type": "video",
                    "codec_name": "h264",
                    "width": 1920,
                    "height": 1080,
                    "r_frame_rate": "30/1",
                    "duration": "10.0",
                }
            ],
            "format": {
                "format_name": "avi",  # Unsupported container
                "duration": "10.0",
                "size": "1000000",
            },
        }
        
        with patch.object(validator, '_run_ffprobe', new_callable=AsyncMock) as mock_ffprobe:
            mock_ffprobe.return_value = unsupported_output
            
            result = await validator.validate("/fake/path/test_video.avi")
            
            assert result.is_valid is False
            assert "Unsupported container" in result.error_message
            assert result.validation_status == "rejected"

    @pytest.mark.asyncio
    async def test_reject_unsupported_video_codec(self, validator):
        """AC2: Reject unsupported video codecs."""
        unsupported_output = {
            "streams": [
                {
                    "index": 0,
                    "codec_type": "video",
                    "codec_name": "prores",  # Unsupported codec
                    "width": 1920,
                    "height": 1080,
                    "r_frame_rate": "30/1",
                    "duration": "10.0",
                }
            ],
            "format": {
                "format_name": "mov",
                "duration": "10.0",
                "size": "1000000",
            },
        }
        
        with patch.object(validator, '_run_ffprobe', new_callable=AsyncMock) as mock_ffprobe:
            mock_ffprobe.return_value = unsupported_output
            
            result = await validator.validate("/fake/path/test_video.mov")
            
            assert result.is_valid is False
            assert "Unsupported video codec" in result.error_message

    @pytest.mark.asyncio
    async def test_reject_unsupported_audio_codec(self, validator):
        """AC2: Reject unsupported audio codecs."""
        unsupported_output = {
            "streams": [
                {
                    "index": 0,
                    "codec_type": "video",
                    "codec_name": "h264",
                    "width": 1920,
                    "height": 1080,
                    "r_frame_rate": "30/1",
                    "duration": "10.0",
                },
                {
                    "index": 1,
                    "codec_type": "audio",
                    "codec_name": "ac3",  # Unsupported codec
                    "sample_rate": "48000",
                    "channels": 2,
                }
            ],
            "format": {
                "format_name": "mp4",
                "duration": "10.0",
                "size": "1000000",
            },
        }
        
        with patch.object(validator, '_run_ffprobe', new_callable=AsyncMock) as mock_ffprobe:
            mock_ffprobe.return_value = unsupported_output
            
            result = await validator.validate("/fake/path/test_video.mp4")
            
            assert result.is_valid is False
            assert "Unsupported audio codec" in result.error_message

    @pytest.mark.asyncio
    async def test_reject_exceeds_max_duration(self, validator):
        """AC3: Reject media exceeding max duration (2 hours = 7200000 ms)."""
        long_duration_output = {
            "streams": [
                {
                    "index": 0,
                    "codec_type": "video",
                    "codec_name": "h264",
                    "width": 1920,
                    "height": 1080,
                    "r_frame_rate": "30/1",
                    "duration": "7201.0",  # Exceeds 2 hours
                }
            ],
            "format": {
                "format_name": "mp4",
                "duration": "7201.0",
                "size": "1000000000",
            },
        }
        
        with patch.object(validator, '_run_ffprobe', new_callable=AsyncMock) as mock_ffprobe:
            mock_ffprobe.return_value = long_duration_output
            
            result = await validator.validate("/fake/path/test_video.mp4")
            
            assert result.is_valid is False
            assert "exceeds maximum duration" in result.error_message
            assert result.validation_status == "rejected"

    @pytest.mark.asyncio
    async def test_accept_max_duration_boundary(self, validator):
        """AC3: Accept media at exactly max duration boundary."""
        boundary_output = {
            "streams": [
                {
                    "index": 0,
                    "codec_type": "video",
                    "codec_name": "h264",
                    "width": 1920,
                    "height": 1080,
                    "r_frame_rate": "30/1",
                    "duration": "7200.0",  # Exactly 2 hours
                }
            ],
            "format": {
                "format_name": "mp4",
                "duration": "7200.0",
                "size": "1000000000",
            },
        }
        
        with patch.object(validator, '_run_ffprobe', new_callable=AsyncMock) as mock_ffprobe:
            mock_ffprobe.return_value = boundary_output
            
            result = await validator.validate("/fake/path/test_video.mp4")
            
            assert result.is_valid is True
            assert result.duration_ms == 7200000

    @pytest.mark.asyncio
    async def test_validate_audio_only_file(self, validator):
        """Validate audio-only files (mp3, wav, m4a)."""
        audio_output = {
            "streams": [
                {
                    "index": 0,
                    "codec_type": "audio",
                    "codec_name": "mp3",
                    "sample_rate": "44100",
                    "channels": 2,
                    "channel_layout": "stereo",
                    "bit_rate": "192000",
                    "duration": "180.0",
                }
            ],
            "format": {
                "format_name": "mp3",
                "duration": "180.0",
                "size": "4320000",
                "bit_rate": "192000",
            },
        }
        
        with patch.object(validator, '_run_ffprobe', new_callable=AsyncMock) as mock_ffprobe:
            mock_ffprobe.return_value = audio_output
            
            result = await validator.validate("/fake/path/test_audio.mp3")
            
            assert result.is_valid is True
            assert result.container == "mp3"
            assert result.audio_codec == "mp3"
            assert result.video_codec is None
            assert result.width is None
            assert result.height is None

    @pytest.mark.asyncio
    async def test_validate_video_only_file(self, validator):
        """Validate video-only files (no audio track)."""
        video_only_output = {
            "streams": [
                {
                    "index": 0,
                    "codec_type": "video",
                    "codec_name": "h264",
                    "width": 1920,
                    "height": 1080,
                    "r_frame_rate": "30/1",
                    "duration": "10.0",
                }
            ],
            "format": {
                "format_name": "mp4",
                "duration": "10.0",
                "size": "5000000",
            },
        }
        
        with patch.object(validator, '_run_ffprobe', new_callable=AsyncMock) as mock_ffprobe:
            mock_ffprobe.return_value = video_only_output
            
            result = await validator.validate("/fake/path/test_video.mp4")
            
            assert result.is_valid is True
            assert result.video_codec == "h264"
            assert result.audio_codec is None
            assert result.audio_channels is None
            assert result.sample_rate is None

    @pytest.mark.asyncio
    async def test_ffprobe_failure_handling(self, validator):
        """Handle FFprobe execution failures gracefully."""
        with patch.object(validator, '_run_ffprobe', new_callable=AsyncMock) as mock_ffprobe:
            mock_ffprobe.side_effect = FileNotFoundError("ffprobe not found")
            
            result = await validator.validate("/fake/path/test_video.mp4")
            
            assert result.is_valid is False
            assert "FFprobe execution failed" in result.error_message
            assert result.validation_status == "error"

    @pytest.mark.asyncio
    async def test_malformed_ffprobe_output(self, validator):
        """Handle malformed FFprobe JSON output."""
        with patch.object(validator, '_run_ffprobe', new_callable=AsyncMock) as mock_ffprobe:
            mock_ffprobe.return_value = "not valid json"
            
            result = await validator.validate("/fake/path/test_video.mp4")
            
            assert result.is_valid is False
            assert "Failed to parse FFprobe output" in result.error_message

    def test_create_validator_factory(self):
        """Test the factory function creates validator with correct config."""
        storage = Mock()
        validator = create_validator(storage=storage)
        
        assert isinstance(validator, FFprobeValidator)
        assert validator.storage == storage
        assert validator.max_duration_ms == 7200000  # 2 hours


class TestSupportedFormats:
    """Test the supported formats constants."""

    def test_supported_containers(self):
        """Verify supported container list matches CONTRACT-FREEZE.md §12."""
        validator = FFprobeValidator(storage=Mock())
        
        expected_containers = {"mp4", "mov", "mkv", "webm", "mp3", "wav", "m4a"}
        assert validator.SUPPORTED_CONTAINERS == expected_containers

    def test_supported_video_codecs(self):
        """Verify supported video codec list matches CONTRACT-FREEZE.md §12."""
        validator = FFprobeValidator(storage=Mock())
        
        expected_video_codecs = {"h264", "hevc", "vp9", "av1"}
        assert validator.SUPPORTED_VIDEO_CODECS == expected_video_codecs

    def test_supported_audio_codecs(self):
        """Verify supported audio codec list matches CONTRACT-FREEZE.md §12."""
        validator = FFprobeValidator(storage=Mock())
        
        expected_audio_codecs = {"aac", "opus", "mp3", "pcm_s16le", "flac"}
        assert validator.SUPPORTED_AUDIO_CODECS == expected_audio_codecs

    def test_max_duration_constant(self):
        """Verify max duration is 2 hours (7200000 ms)."""
        validator = FFprobeValidator(storage=Mock())
        
        assert validator.MAX_DURATION_MS == 7200000