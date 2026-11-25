"""
Unit tests for FFmpeg processor.
"""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from pathlib import Path

from app.processors.ffmpeg_processor import FFmpegProcessor
from app.processors.base import MediaMetadata, RenderPreset


class TestFFmpegProcessor:
    """Tests for FFmpegProcessor."""

    @pytest.fixture
    def processor(self):
        """Create processor instance."""
        return FFmpegProcessor(ffmpeg_path="ffmpeg", ffprobe_path="ffprobe")

    @pytest.fixture
    def mock_ffprobe_output(self):
        """Mock ffprobe JSON output."""
        return {
            "format": {
                "filename": "/test/video.mp4",
                "nb_streams": 2,
                "nb_programs": 0,
                "format_name": "mov,mp4,m4a,3gp,3g2,mj2",
                "format_long_name": "QuickTime / MOV",
                "start_time": "0.000000",
                "duration": "120.500000",
                "size": "52428800",
                "bit_rate": "3483648",
                "probe_score": 100
            },
            "streams": [
                {
                    "index": 0,
                    "codec_name": "h264",
                    "codec_long_name": "H.264 / AVC / MPEG-4 AVC / MPEG-4 part 10",
                    "profile": "High",
                    "codec_type": "video",
                    "codec_time_base": "1/60",
                    "codec_tag_string": "avc1",
                    "codec_tag": "0x31637661",
                    "width": 1920,
                    "height": 1080,
                    "coded_width": 1920,
                    "coded_height": 1080,
                    "closed_captions": 0,
                    "film_grain": 0,
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
                    "r_frame_rate": "30/1",
                    "avg_frame_rate": "30/1",
                    "time_base": "1/15360",
                    "start_pts": 0,
                    "start_time": "0.000000",
                    "duration_ts": 1850880,
                    "duration": "120.500000",
                    "bit_rate": "3355443",
                    "bits_per_raw_sample": "8",
                    "nb_frames": "3615"
                },
                {
                    "index": 1,
                    "codec_name": "aac",
                    "codec_long_name": "AAC (Advanced Audio Coding)",
                    "profile": "LC",
                    "codec_type": "audio",
                    "codec_time_base": "1/48000",
                    "codec_tag_string": "mp4a",
                    "codec_tag": "0x6134706d",
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
                    "duration_ts": 5784000,
                    "duration": "120.500000",
                    "bit_rate": "128000",
                    "nb_frames": "5648"
                }
            ]
        }

    @pytest.mark.asyncio
    async def test_validate_media_valid(self, processor, mock_ffprobe_output):
        """Test media validation with valid file."""
        with patch.object(processor, '_run_ffprobe', new_callable=AsyncMock) as mock_run:
            mock_run.return_value = mock_ffprobe_output
            
            result = await processor.validate_media("/test/video.mp4")
            
            assert result.valid is True
            assert result.duration == 120.5
            assert result.width == 1920
            assert result.height == 1080
            assert result.video_codec == "h264"
            assert result.audio_codec == "aac"
            assert len(result.errors) == 0

    @pytest.mark.asyncio
    async def test_validate_media_invalid(self, processor):
        """Test media validation with invalid file."""
        with patch.object(processor, '_run_ffprobe', new_callable=AsyncMock) as mock_run:
            mock_run.side_effect = Exception("ffprobe failed")
            
            result = await processor.validate_media("/test/invalid.mp4")
            
            assert result.valid is False
            assert len(result.errors) > 0
            assert "ffprobe failed" in result.errors[0]

    @pytest.mark.asyncio
    async def test_validate_media_no_video_stream(self, processor):
        """Test media validation with audio-only file."""
        audio_only_output = {
            "format": {"duration": "60.0", "size": "1024000", "bit_rate": "136533"},
            "streams": [
                {
                    "index": 0,
                    "codec_type": "audio",
                    "codec_name": "mp3",
                    "sample_rate": "44100",
                    "channels": 2
                }
            ]
        }
        
        with patch.object(processor, '_run_ffprobe', new_callable=AsyncMock) as mock_run:
            mock_run.return_value = audio_only_output
            
            result = await processor.validate_media("/test/audio.mp3")
            
            assert result.valid is True
            assert result.width is None
            assert result.height is None
            assert result.video_codec is None

    @pytest.mark.asyncio
    async def test_extract_metadata(self, processor, mock_ffprobe_output):
        """Test metadata extraction."""
        with patch.object(processor, '_run_ffprobe', new_callable=AsyncMock) as mock_run:
            mock_run.return_value = mock_ffprobe_output
            
            metadata = await processor.extract_metadata("/test/video.mp4")
            
            assert isinstance(metadata, MediaMetadata)
            assert metadata.duration == 120.5
            assert metadata.width == 1920
            assert metadata.height == 1080
            assert metadata.frame_rate == 30.0
            assert metadata.video_codec == "h264"
            assert metadata.audio_codec == "aac"
            assert metadata.bitrate == 3483648
            assert metadata.size == 52428800
            assert len(metadata.streams) == 2

    @pytest.mark.asyncio
    async def test_generate_thumbnails(self, processor):
        """Test thumbnail generation."""
        with patch.object(processor, '_run_ffmpeg', new_callable=AsyncMock) as mock_run:
            mock_run.return_value = (0, "", "")
            
            thumbnails = await processor.generate_thumbnails(
                "/test/video.mp4",
                output_dir="/test/thumbnails",
                interval=10.0,
                count=12
            )
            
            assert len(thumbnails) == 12
            assert all(t.endswith(".jpg") for t in thumbnails)
            mock_run.assert_called_once()

    @pytest.mark.asyncio
    async def test_generate_sprite(self, processor):
        """Test sprite sheet generation."""
        with patch.object(processor, '_run_ffmpeg', new_callable=AsyncMock) as mock_run:
            mock_run.return_value = (0, "", "")
            
            sprite_path, vtt_path = await processor.generate_sprite(
                "/test/video.mp4",
                output_dir="/test/sprites",
                interval=5.0,
                cols=5,
                rows=5
            )
            
            assert sprite_path.endswith(".jpg")
            assert vtt_path.endswith(".vtt")
            mock_run.assert_called_once()

    @pytest.mark.asyncio
    async def test_transcode_proxy(self, processor):
        """Test proxy transcoding."""
        with patch.object(processor, '_run_ffmpeg', new_callable=AsyncMock) as mock_run:
            mock_run.return_value = (0, "", "")
            
            proxy_path = await processor.transcode_proxy(
                "/test/video.mp4",
                output_dir="/test/proxies",
                resolution="854x480",
                video_bitrate="1000k",
                audio_bitrate="96k"
            )
            
            assert proxy_path.endswith("_proxy.mp4")
            mock_run.assert_called_once()
            # Verify proxy parameters in call
            call_args = mock_run.call_args[0][0]
            assert "-vf" in call_args
            assert "scale=854:480" in " ".join(call_args)
            assert "-b:v" in call_args
            assert "1000k" in " ".join(call_args)

    @pytest.mark.asyncio
    async def test_transcode_to_format(self, processor):
        """Test transcoding to specific format."""
        with patch.object(processor, '_run_ffmpeg', new_callable=AsyncMock) as mock_run:
            mock_run.return_value = (0, "", "")
            
            output_path = await processor.transcode_to_format(
                "/test/video.mp4",
                output_path="/test/output.webm",
                video_codec="libvpx-vp9",
                audio_codec="libopus",
                crf=30
            )
            
            assert output_path == "/test/output.webm"
            call_args = mock_run.call_args[0][0]
            assert "-c:v" in call_args
            assert "libvpx-vp9" in call_args
            assert "-c:a" in call_args
            assert "libopus" in call_args

    @pytest.mark.asyncio
    async def test_detect_scenes(self, processor):
        """Test scene detection."""
        # Mock ffprobe output for scene detection
        scene_output = (
            "lavfi.scene_score=0.5\n"
            "lavfi.scene_score=0.3\n"
            "lavfi.scene_score=0.8\n"
            "lavfi.scene_score=0.2\n"
        )
        
        with patch.object(processor, '_run_ffmpeg', new_callable=AsyncMock) as mock_run:
            mock_run.return_value = (0, scene_output, "")
            
            from app.processors.base import SceneDetectionResult, Scene
            result = await processor.detect_scenes(
                "/test/video.mp4",
                threshold=0.4,
                min_scene_len=1.0
            )
            
            assert isinstance(result, SceneDetectionResult)
            assert len(result.scenes) == 2  # Only scores > 0.4
            assert all(s.score >= 0.4 for s in result.scenes)

    @pytest.mark.asyncio
    async def test_analyze_audio(self, processor):
        """Test audio analysis."""
        # Mock ffmpeg output for audio analysis
        audio_stats = (
            "[Parsed_astats_0 @ 0x...] Overall: -20.5 dB\n"
            "[Parsed_astats_0 @ 0x...] Peak level: -1.2 dB\n"
            "[Parsed_astats_0 @ 0x...] RMS level: -23.1 dB\n"
            "[Parsed_ebur128_0 @ 0x...] Integrated loudness: -18.0 LUFS\n"
            "[Parsed_ebur128_0 @ 0x...] Loudness range: 8.0 LU\n"
        )
        
        with patch.object(processor, '_run_ffmpeg', new_callable=AsyncMock) as mock_run:
            mock_run.return_value = (0, audio_stats, "")
            
            result = await processor.analyze_audio("/test/video.mp4")
            
            assert "peak_level_db" in result
            assert "rms_level_db" in result
            assert "integrated_loudness_lufs" in result
            assert "loudness_range_lu" in result
            assert result["peak_level_db"] == -1.2
            assert result["rms_level_db"] == -23.1

    @pytest.mark.asyncio
    async def test_extract_audio(self, processor):
        """Test audio extraction."""
        with patch.object(processor, '_run_ffmpeg', new_callable=AsyncMock) as mock_run:
            mock_run.return_value = (0, "", "")
            
            audio_path = await processor.extract_audio(
                "/test/video.mp4",
                output_path="/test/audio.wav",
                sample_rate=16000,
                channels=1
            )
            
            assert audio_path == "/test/audio.wav"
            call_args = mock_run.call_args[0][0]
            assert "-ar" in call_args
            assert "16000" in call_args
            assert "-ac" in call_args
            assert "1" in call_args

    @pytest.mark.asyncio
    async def test_compose_video(self, processor):
        """Test video composition."""
        segments = [
            {"input": "/test/clip1.mp4", "start": 0, "duration": 10},
            {"input": "/test/clip2.mp4", "start": 5, "duration": 15},
        ]
        
        with patch.object(processor, '_run_ffmpeg', new_callable=AsyncMock) as mock_run:
            mock_run.return_value = (0, "", "")
            
            output_path = await processor.compose_video(
                segments,
                output_path="/test/composed.mp4",
                transition_duration=1.0
            )
            
            assert output_path == "/test/composed.mp4"
            mock_run.assert_called_once()

    @pytest.mark.asyncio
    async def test_burn_captions(self, processor):
        """Test caption burning."""
        with patch.object(processor, '_run_ffmpeg', new_callable=AsyncMock) as mock_run:
            mock_run.return_value = (0, "", "")
            
            output_path = await processor.burn_captions(
                "/test/video.mp4",
                caption_path="/test/captions.srt",
                output_path="/test/with_captions.mp4",
                font_size=24,
                font_color="white",
                outline_color="black",
                outline_width=2
            )
            
            assert output_path == "/test/with_captions.mp4"
            call_args = mock_run.call_args[0][0]
            assert "-vf" in call_args
            assert "subtitles=" in " ".join(call_args)

    @pytest.mark.asyncio
    async def test_create_clip(self, processor):
        """Test clip creation."""
        with patch.object(processor, '_run_ffmpeg', new_callable=AsyncMock) as mock_run:
            mock_run.return_value = (0, "", "")
            
            clip_path = await processor.create_clip(
                "/test/video.mp4",
                start_time=10.0,
                end_time=30.0,
                output_path="/test/clip.mp4"
            )
            
            assert clip_path == "/test/clip.mp4"
            call_args = mock_run.call_args[0][0]
            assert "-ss" in call_args
            assert "10.0" in call_args
            assert "-t" in call_args
            assert "20.0" in call_args

    @pytest.mark.asyncio
    async def test_concat_videos(self, processor):
        """Test video concatenation."""
        inputs = ["/test/clip1.mp4", "/test/clip2.mp4", "/test/clip3.mp4"]
        
        with patch.object(processor, '_run_ffmpeg', new_callable=AsyncMock) as mock_run:
            mock_run.return_value = (0, "", "")
            
            output_path = await processor.concat_videos(
                inputs,
                output_path="/test/concat.mp4"
            )
            
            assert output_path == "/test/concat.mp4"
            mock_run.assert_called_once()
            # Verify concat filter used
            call_args = mock_run.call_args[0][0]
            assert "concat" in " ".join(call_args)

    def test_get_render_presets(self, processor):
        """Test render preset retrieval."""
        presets = processor.get_render_presets()
        
        assert isinstance(presets, dict)
        assert "social_1080p" in presets
        assert "social_720p" in presets
        assert "youtube_1080p" in presets
        assert "youtube_4k" in presets
        
        for name, preset in presets.items():
            assert isinstance(preset, RenderPreset)
            assert preset.name == name
            assert preset.width > 0
            assert preset.height > 0
            assert preset.fps > 0

    @pytest.mark.asyncio
    async def test_render_with_preset(self, processor):
        """Test rendering with preset."""
        preset = RenderPreset(
            name="test_preset",
            width=1280,
            height=720,
            fps=30,
            video_codec="libx264",
            video_bitrate="2000k",
            audio_codec="aac",
            audio_bitrate="128k",
            preset="fast",
            extra_args=[]
        )
        
        with patch.object(processor, '_run_ffmpeg', new_callable=AsyncMock) as mock_run:
            mock_run.return_value = (0, "", "")
            
            from app.processors.base import RenderResult
            result = await processor.render_with_preset(
                "/test/video.mp4",
                preset,
                output_path="/test/rendered.mp4"
            )
            
            assert isinstance(result, RenderResult)
            assert result.output_path == "/test/rendered.mp4"
            assert result.preset_used == "test_preset"
            mock_run.assert_called_once()

    @pytest.mark.asyncio
    async def test_run_ffmpeg_timeout(self, processor):
        """Test FFmpeg timeout handling."""
        import asyncio
        
        with patch('asyncio.create_subprocess_exec', new_callable=AsyncMock) as mock_exec:
            mock_proc = AsyncMock()
            mock_proc.communicate.side_effect = asyncio.TimeoutError()
            mock_exec.return_value = mock_proc
            
            with pytest.raises(asyncio.TimeoutError):
                await processor._run_ffmpeg(["-i", "/test/video.mp4", "-f", "null", "-"], timeout=1)

    @pytest.mark.asyncio
    async def test_run_ffmpeg_error(self, processor):
        """Test FFmpeg error handling."""
        with patch('asyncio.create_subprocess_exec', new_callable=AsyncMock) as mock_exec:
            mock_proc = AsyncMock()
            mock_proc.communicate.return_value = (b"", b"Error: Invalid argument")
            mock_proc.returncode = 1
            mock_exec.return_value = mock_proc
            
            with pytest.raises(RuntimeError) as exc_info:
                await processor._run_ffmpeg(["-i", "/test/video.mp4", "-f", "null", "-"])
            
            assert "FFmpeg failed" in str(exc_info.value)
            assert "Invalid argument" in str(exc_info.value)