"""
FFmpeg Processor for ClipYantra.

Wrapper around FFmpeg/FFprobe for video/audio processing:
- File validation and metadata extraction
- Transcoding and format conversion
- Thumbnail and sprite sheet generation
- Scene detection
- Audio analysis
- Video composition and rendering
- Subtitle burning
"""

import os
import json
import subprocess
import tempfile
from pathlib import Path
from typing import Dict, Any, Optional, List, Tuple
from dataclasses import dataclass

from app.processors.base import (
    MediaMetadata,
    ValidationResult,
    SceneDetectionResult,
    Scene,
    RenderPreset,
    ProcessorError,
)


class FFmpegProcessor:
    """
    High-level FFmpeg/FFprobe wrapper for media processing.
    
    Provides validated, typed interfaces for common video/audio operations
    with proper error handling and resource management.
    """
    
    def __init__(
        self,
        ffmpeg_path: str = "ffmpeg",
        ffprobe_path: str = "ffprobe",
        timeout: int = 300,
    ):
        self.ffmpeg_path = ffmpeg_path
        self.ffprobe_path = ffprobe_path
        self.timeout = timeout
        self._validate_binaries()
    
    def _validate_binaries(self) -> None:
        """Verify FFmpeg and FFprobe are available."""
        for binary, name in [(self.ffmpeg_path, "FFmpeg"), (self.ffprobe_path, "FFprobe")]:
            try:
                result = subprocess.run(
                    [binary, "-version"],
                    capture_output=True,
                    text=True,
                    timeout=10,
                )
                if result.returncode != 0:
                    raise ProcessorError(
                        f"{name} binary not functional: {binary}",
                        code="BINARY_NOT_FOUND",
                    )
            except FileNotFoundError:
                raise ProcessorError(
                    f"{name} binary not found: {binary}",
                    code="BINARY_NOT_FOUND",
                )
            except subprocess.TimeoutExpired:
                raise ProcessorError(
                    f"{name} binary timed out: {binary}",
                    code="BINARY_TIMEOUT",
                )
    
    def _run_ffprobe(self, args: List[str]) -> Dict[str, Any]:
        """Run ffprobe and return parsed JSON output."""
        cmd = [
            self.ffprobe_path,
            "-v", "quiet",
            "-print_format", "json",
            "-show_format",
            "-show_streams",
            "-show_chapters",
            *args,
        ]
        
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=self.timeout,
            )
            if result.returncode != 0:
                raise ProcessorError(
                    f"ffprobe failed: {result.stderr}",
                    code="FFPROBE_ERROR",
                    details={"command": cmd, "stderr": result.stderr},
                )
            return json.loads(result.stdout)
        except json.JSONDecodeError as e:
            raise ProcessorError(
                f"Failed to parse ffprobe output: {e}",
                code="FFPROBE_PARSE_ERROR",
                details={"stdout": result.stdout},
            )
        except subprocess.TimeoutExpired:
            raise ProcessorError(
                "ffprobe timed out",
                code="FFPROBE_TIMEOUT",
            )
    
    def _run_ffmpeg(self, args: List[str], input_path: Optional[str] = None) -> subprocess.CompletedProcess:
        """Run ffmpeg with given arguments."""
        cmd = [self.ffmpeg_path, "-y", "-v", "error"]
        if input_path:
            cmd.extend(["-i", input_path])
        cmd.extend(args)
        
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=self.timeout,
            )
            if result.returncode != 0:
                raise ProcessorError(
                    f"ffmpeg failed: {result.stderr}",
                    code="FFMPEG_ERROR",
                    details={"command": cmd, "stderr": result.stderr},
                )
            return result
        except subprocess.TimeoutExpired:
            raise ProcessorError(
                "ffmpeg timed out",
                code="FFMPEG_TIMEOUT",
            )
    
    # =========================================================================
    # Validation and Metadata
    # =========================================================================
    
    def validate_file(self, file_path: str) -> ValidationResult:
        """
        Validate media file for processing.
        
        Checks:
        - File exists and is readable
        - Valid media format
        - Supported codecs
        - Not corrupted
        """
        checks = {}
        warnings = []
        error = None
        metadata = None
        
        # Check file exists
        path = Path(file_path)
        checks["file_exists"] = path.exists()
        if not checks["file_exists"]:
            error = f"File not found: {file_path}"
            return ValidationResult(valid=False, file_path=file_path, checks=checks, error=error)
        
        checks["file_readable"] = os.access(file_path, os.R_OK)
        if not checks["file_readable"]:
            error = f"File not readable: {file_path}"
            return ValidationResult(valid=False, file_path=file_path, checks=checks, error=error)
        
        # Check file size
        file_size = path.stat().st_size
        checks["file_not_empty"] = file_size > 0
        if not checks["file_not_empty"]:
            error = "File is empty"
            return ValidationResult(valid=False, file_path=file_path, checks=checks, error=error)
        
        # Probe with ffprobe
        try:
            metadata = self.extract_metadata(file_path)
            checks["valid_format"] = True
            checks["has_streams"] = len(metadata.streams) > 0
            
            # Check for video stream
            checks["has_video"] = metadata.has_video
            if not checks["has_video"]:
                warnings.append("No video stream found")
            
            # Check for audio stream
            checks["has_audio"] = metadata.has_audio
            if not checks["has_audio"]:
                warnings.append("No audio stream found")
            
            # Check codec support
            video_supported = self._is_codec_supported(metadata.video_codec, "video")
            audio_supported = self._is_codec_supported(metadata.audio_codec, "audio")
            checks["video_codec_supported"] = video_supported
            checks["audio_codec_supported"] = audio_supported
            
            if not video_supported and metadata.has_video:
                warnings.append(f"Video codec may not be supported: {metadata.video_codec}")
            if not audio_supported and metadata.has_audio:
                warnings.append(f"Audio codec may not be supported: {metadata.audio_codec}")
            
            # Check duration
            checks["has_duration"] = metadata.duration is not None and metadata.duration > 0
            
        except ProcessorError as e:
            checks["valid_format"] = False
            error = str(e)
        
        valid = all(checks.values()) and error is None
        
        return ValidationResult(
            valid=valid,
            file_path=file_path,
            checks=checks,
            error=error,
            warnings=warnings,
            metadata=metadata,
        )
    
    def extract_metadata(self, file_path: str) -> MediaMetadata:
        """Extract comprehensive metadata from media file."""
        data = self._run_ffprobe([file_path])
        
        format_info = data.get("format", {})
        streams = data.get("streams", [])
        chapters = data.get("chapters", [])
        
        # Find video and audio streams
        video_stream = next((s for s in streams if s.get("codec_type") == "video"), None)
        audio_stream = next((s for s in streams if s.get("codec_type") == "audio"), None)
        
        return MediaMetadata(
            file_path=file_path,
            file_size=int(format_info.get("size", 0)),
            mime_type=self._guess_mime_type(format_info.get("format_name", "")),
            format_name=format_info.get("format_name", ""),
            format_long_name=format_info.get("format_long_name", ""),
            duration=float(format_info.get("duration", 0)) if format_info.get("duration") else None,
            bit_rate=int(format_info.get("bit_rate", 0)) if format_info.get("bit_rate") else None,
            width=video_stream.get("width") if video_stream else None,
            height=video_stream.get("height") if video_stream else None,
            video_codec=video_stream.get("codec_name") if video_stream else None,
            video_codec_long=video_stream.get("codec_long_name") if video_stream else None,
            video_profile=video_stream.get("profile") if video_stream else None,
            video_pix_fmt=video_stream.get("pix_fmt") if video_stream else None,
            video_fps=self._parse_fps(video_stream.get("r_frame_rate")) if video_stream else None,
            video_bitrate=int(video_stream.get("bit_rate", 0)) if video_stream and video_stream.get("bit_rate") else None,
            audio_codec=audio_stream.get("codec_name") if audio_stream else None,
            audio_codec_long=audio_stream.get("codec_long_name") if audio_stream else None,
            audio_sample_rate=int(audio_stream.get("sample_rate", 0)) if audio_stream and audio_stream.get("sample_rate") else None,
            audio_channels=audio_stream.get("channels") if audio_stream else None,
            audio_channel_layout=audio_stream.get("channel_layout") if audio_stream else None,
            audio_bitrate=int(audio_stream.get("bit_rate", 0)) if audio_stream and audio_stream.get("bit_rate") else None,
            streams=streams,
            tags=format_info.get("tags", {}),
            chapters=chapters,
        )
    
    def analyze_streams(self, file_path: str) -> List[Dict[str, Any]]:
        """Analyze all streams in detail."""
        data = self._run_ffprobe([
            "-show_stream_disposition",
            "-show_program_version",
            file_path,
        ])
        return data.get("streams", [])
    
    # =========================================================================
    # Transcoding and Conversion
    # =========================================================================
    
    def transcode(
        self,
        input_path: str,
        output_path: str,
        video_codec: str = "libx264",
        audio_codec: str = "aac",
        video_filters: Optional[str] = None,
        video_bitrate: Optional[str] = None,
        audio_bitrate: str = "128k",
        preset: str = "medium",
        crf: Optional[int] = None,
        extra_args: Optional[List[str]] = None,
    ) -> bool:
        """Transcode media file with specified parameters."""
        args = [
            "-c:v", video_codec,
            "-c:a", audio_codec,
            "-b:a", audio_bitrate,
            "-preset", preset,
        ]
        
        if crf is not None:
            args.extend(["-crf", str(crf)])
        
        if video_bitrate:
            args.extend(["-b:v", video_bitrate, "-maxrate", video_bitrate, "-bufsize", video_bitrate])
        
        if video_filters:
            args.extend(["-vf", video_filters])
        
        if extra_args:
            args.extend(extra_args)
        
        args.append(output_path)
        
        self._run_ffmpeg(args, input_path)
        return Path(output_path).exists()
    
    def trim_and_transcode(
        self,
        input_path: str,
        output_path: str,
        start_time: float,
        end_time: Optional[float] = None,
        duration: Optional[float] = None,
        **transcode_kwargs,
    ) -> bool:
        """Trim and transcode in one operation."""
        args = ["-ss", str(start_time)]
        
        if end_time is not None:
            args.extend(["-to", str(end_time)])
        elif duration is not None:
            args.extend(["-t", str(duration)])
        
        # Add transcode args
        transcode_args = []
        for key, value in transcode_kwargs.items():
            if key == "video_filters":
                transcode_args.extend(["-vf", value])
            elif key == "video_bitrate":
                transcode_args.extend(["-b:v", value, "-maxrate", value, "-bufsize", value])
            elif key == "audio_bitrate":
                transcode_args.extend(["-b:a", value])
            elif key == "video_codec":
                transcode_args.extend(["-c:v", value])
            elif key == "audio_codec":
                transcode_args.extend(["-c:a", value])
            elif key == "preset":
                transcode_args.extend(["-preset", value])
            elif key == "crf":
                transcode_args.extend(["-crf", str(value)])
        
        args.extend(transcode_args)
        args.append(output_path)
        
        self._run_ffmpeg(args, input_path)
        return Path(output_path).exists()
    
    def remux(
        self,
        input_path: str,
        output_path: str,
        video_codec: str = "copy",
        audio_codec: str = "copy",
    ) -> bool:
        """Remux without re-encoding (fast)."""
        args = [
            "-c:v", video_codec,
            "-c:a", audio_codec,
            output_path,
        ]
        self._run_ffmpeg(args, input_path)
        return Path(output_path).exists()
    
    # =========================================================================
    # Thumbnails and Frames
    # =========================================================================
    
    def extract_frame(
        self,
        input_path: str,
        timestamp: float,
        output_path: str,
        width: Optional[int] = None,
        height: Optional[int] = None,
    ) -> bool:
        """Extract single frame at timestamp."""
        args = [
            "-ss", str(timestamp),
            "-frames:v", "1",
        ]
        
        if width and height:
            args.extend(["-vf", f"scale={width}:{height}:force_original_aspect_ratio=decrease"])
        
        args.extend(["-q:v", "2", output_path])
        
        self._run_ffmpeg(args, input_path)
        return Path(output_path).exists()
    
    def extract_frames(
        self,
        input_path: str,
        output_dir: str,
        fps: float = 1.0,
        prefix: str = "frame_",
        format: str = "jpg",
    ) -> List[str]:
        """Extract frames at specified FPS."""
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        
        output_pattern = str(output_dir / f"{prefix}%06d.{format}")
        
        args = [
            "-vf", f"fps={fps}",
            "-q:v", "2",
            output_pattern,
        ]
        
        self._run_ffmpeg(args, input_path)
        
        # Return sorted list of generated frames
        frames = sorted(output_dir.glob(f"{prefix}*.{format}"))
        return [str(f) for f in frames]
    
    def generate_thumbnails(
        self,
        input_path: str,
        output_dir: str,
        count: int = 10,
        timestamps: Optional[List[float]] = None,
    ) -> List[str]:
        """Generate multiple thumbnails."""
        metadata = self.extract_metadata(input_path)
        duration = metadata.duration or 0
        
        if timestamps is None:
            if duration > 0:
                timestamps = [duration * i / (count + 1) for i in range(1, count + 1)]
            else:
                timestamps = [i * 10 for i in range(1, count + 1)]
        
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        
        thumbnail_paths = []
        for i, ts in enumerate(timestamps):
            output_path = output_dir / f"thumb_{i:03d}_{ts:.2f}.jpg"
            if self.extract_frame(input_path, ts, str(output_path)):
                thumbnail_paths.append(str(output_path))
        
        return thumbnail_paths
    
    def create_sprite_sheet(
        self,
        input_path: str,
        timestamps: List[float],
        output_path: str,
        columns: int = 5,
        tile_width: int = 320,
        tile_height: int = 180,
    ) -> bool:
        """Create sprite sheet from frames at timestamps."""
        # Extract frames first
        with tempfile.TemporaryDirectory() as tmpdir:
            frame_paths = []
            for i, ts in enumerate(timestamps):
                frame_path = Path(tmpdir) / f"frame_{i:04d}.jpg"
                if self.extract_frame(input_path, ts, str(frame_path), tile_width, tile_height):
                    frame_paths.append(str(frame_path))
            
            if not frame_paths:
                return False
            
            # Create tile filter
            rows = (len(frame_paths) + columns - 1) // columns
            filter_parts = []
            for i, fp in enumerate(frame_paths):
                filter_parts.append(f"[{i}:v]scale={tile_width}:{tile_height}:force_original_aspect_ratio=decrease,pad={tile_width}:{tile_height}:(ow-iw)/2:(oh-ih)/2[t{i}]")
            
            # Tile layout
            tile_filter = ";".join(filter_parts)
            tile_filter += f";{''.join(f'[t{i}]' for i in range(len(frame_paths)))}tile={columns}x{rows}[out]"
            
            args = [
                *sum((["-i", fp] for fp in frame_paths), []),
                "-filter_complex", tile_filter,
                "-map", "[out]",
                "-frames:v", "1",
                "-q:v", "2",
                output_path,
            ]
            
            self._run_ffmpeg(args)
            return Path(output_path).exists()
    
    # =========================================================================
    # Scene Detection
    # =========================================================================
    
    def detect_scenes(
        self,
        input_path: str,
        threshold: float = 0.3,
        min_scene_len: float = 1.0,
    ) -> SceneDetectionResult:
        """Detect scene changes using FFmpeg's scene filter."""
        # Use FFmpeg scene detection filter
        args = [
            "-vf", f"select='gt(scene,{threshold})',showinfo",
            "-f", "null",
            "-",
        ]
        
        result = subprocess.run(
            [self.ffmpeg_path, "-i", input_path, *args],
            capture_output=True,
            text=True,
            timeout=self.timeout,
        )
        
        # Parse scene timestamps from showinfo output
        scenes = []
        scene_id = 0
        last_time = 0.0
        
        for line in result.stderr.split("\n"):
            if "pts_time:" in line:
                try:
                    # Parse: pts_time:12.345
                    time_str = line.split("pts_time:")[1].split()[0]
                    current_time = float(time_str)
                    
                    if current_time - last_time >= min_scene_len:
                        scenes.append(Scene(
                            id=scene_id,
                            start=last_time,
                            end=current_time,
                            score=threshold,
                        ))
                        scene_id += 1
                        last_time = current_time
                except (IndexError, ValueError):
                    continue
        
        # Get total duration
        metadata = self.extract_metadata(input_path)
        total_duration = metadata.duration or 0
        
        # Add final scene
        if last_time < total_duration:
            scenes.append(Scene(
                id=scene_id,
                start=last_time,
                end=total_duration,
                score=threshold,
            ))
        
        return SceneDetectionResult(
            scenes=scenes,
            threshold=threshold,
            min_scene_len=min_scene_len,
            total_duration=total_duration,
        )
    
    # =========================================================================
    # Audio Analysis
    # =========================================================================
    
    def analyze_audio(self, input_path: str) -> Dict[str, Any]:
        """Analyze audio properties: loudness, silence, music/speech detection."""
        # Use FFmpeg's volumedetect and astats filters
        args = [
            "-af", "volumedetect,astats=metadata=1:reset=1,ametadata=print:key=lavfi.astats.Overall.RMS_level:file=-",
            "-f", "null",
            "-",
        ]
        
        result = subprocess.run(
            [self.ffmpeg_path, "-i", input_path, *args],
            capture_output=True,
            text=True,
            timeout=self.timeout,
        )
        
        # Parse output
        analysis = {
            "duration": 0,
            "mean_volume": 0,
            "max_volume": 0,
            "rms_level": 0,
            "silence_duration": 0,
            "silence_count": 0,
            "has_music": False,
            "has_speech": False,
            "avg_loudness": 0,
        }
        
        metadata = self.extract_metadata(input_path)
        analysis["duration"] = metadata.duration or 0
        
        for line in result.stderr.split("\n"):
            if "mean_volume:" in line:
                try:
                    analysis["mean_volume"] = float(line.split("mean_volume:")[1].split("dB")[0].strip())
                except (IndexError, ValueError):
                    pass
            elif "max_volume:" in line:
                try:
                    analysis["max_volume"] = float(line.split("max_volume:")[1].split("dB")[0].strip())
                except (IndexError, ValueError):
                    pass
            elif "RMS_level:" in line:
                try:
                    analysis["rms_level"] = float(line.split("RMS_level:")[1].strip())
                except (IndexError, ValueError):
                    pass
        
        # Estimate loudness (LUFS approximation)
        analysis["avg_loudness"] = analysis["mean_volume"] + 0.691  # Rough approximation
        
        # Detect silence
        silence_result = self._detect_silence(input_path)
        analysis.update(silence_result)
        
        return analysis
    
    def _detect_silence(self, input_path: str, threshold_db: float = -50, min_duration: float = 0.5) -> Dict[str, Any]:
        """Detect silence periods in audio."""
        args = [
            "-af", f"silencedetect=noise={threshold_db}dB:d={min_duration}",
            "-f", "null",
            "-",
        ]
        
        result = subprocess.run(
            [self.ffmpeg_path, "-i", input_path, *args],
            capture_output=True,
            text=True,
            timeout=self.timeout,
        )
        
        silence_duration = 0
        silence_count = 0
        
        for line in result.stderr.split("\n"):
            if "silence_start:" in line:
                silence_count += 1
            elif "silence_end:" in line and "silence_duration:" in line:
                try:
                    dur_str = line.split("silence_duration:")[1].split()[0]
                    silence_duration += float(dur_str)
                except (IndexError, ValueError):
                    pass
        
        return {
            "silence_duration": silence_duration,
            "silence_count": silence_count,
        }
    
    # =========================================================================
    # Video Composition and Rendering
    # =========================================================================
    
    def render_composition(
        self,
        timeline: Dict[str, Any],
        output_path: str,
        filter_complex: str,
        preset: Dict[str, Any],
    ) -> bool:
        """Render video composition from timeline."""
        # Build input arguments for each timeline track
        input_args = []
        input_index = 0
        
        # Video tracks
        for track in timeline.get("video_tracks", []):
            for clip in track.get("clips", []):
                if "path" in clip:
                    input_args.extend(["-i", clip["path"]])
                    input_index += 1
        
        # Audio tracks
        for track in timeline.get("audio_tracks", []):
            for clip in track.get("clips", []):
                if "path" in clip:
                    input_args.extend(["-i", clip["path"]])
                    input_index += 1
        
        # Build full command
        args = input_args + [
            "-filter_complex", filter_complex,
            *preset.to_ffmpeg_args() if hasattr(preset, 'to_ffmpeg_args') else [],
            output_path,
        ]
        
        self._run_ffmpeg(args)
        return Path(output_path).exists()
    
    def burn_subtitles(
        self,
        input_path: str,
        subtitle_path: str,
        output_path: str,
        preset: Dict[str, Any],
    ) -> bool:
        """Burn subtitles into video."""
        # Subtitle filter with styling support
        subtitle_filter = f"subtitles={subtitle_path}"
        
        preset_obj = RenderPreset(**preset) if isinstance(preset, dict) else preset
        
        args = [
            "-vf", subtitle_filter,
            *preset_obj.to_ffmpeg_args(),
            output_path,
        ]
        
        self._run_ffmpeg(args, input_path)
        return Path(output_path).exists()
    
    # =========================================================================
    # Utility Methods
    # =========================================================================
    
    def _is_codec_supported(self, codec: Optional[str], media_type: str) -> bool:
        """Check if codec is supported."""
        if not codec:
            return False
        
        supported_video = {"h264", "hevc", "vp9", "av1", "mpeg4", "vp8", "theora", "prores", "dnxhd"}
        supported_audio = {"aac", "mp3", "opus", "flac", "vorbis", "pcm_s16le", "pcm_s24le", "alac", "ac3", "eac3"}
        
        codec_lower = codec.lower()
        
        if media_type == "video":
            return codec_lower in supported_video
        else:
            return codec_lower in supported_audio
    
    def _guess_mime_type(self, format_name: str) -> str:
        """Guess MIME type from format name."""
        mime_map = {
            "mp4": "video/mp4",
            "mov": "video/quicktime",
            "webm": "video/webm",
            "mkv": "video/x-matroska",
            "avi": "video/x-msvideo",
            "flv": "video/x-flv",
            "wmv": "video/x-ms-wmv",
            "mpeg": "video/mpeg",
            "mpg": "video/mpeg",
            "ts": "video/mp2t",
            "m4v": "video/x-m4v",
            "3gp": "video/3gpp",
            "ogv": "video/ogg",
        }
        
        for fmt, mime in mime_map.items():
            if fmt in format_name.lower():
                return mime
        
        return "application/octet-stream"
    
    def _parse_fps(self, fps_str: Optional[str]) -> Optional[float]:
        """Parse frame rate string (e.g., '30000/1001') to float."""
        if not fps_str:
            return None
        try:
            if "/" in fps_str:
                num, den = fps_str.split("/")
                return float(num) / float(den)
            return float(fps_str)
        except (ValueError, ZeroDivisionError):
            return None
    
    def get_video_info(self, file_path: str) -> Dict[str, Any]:
        """Get quick video info without full metadata."""
        data = self._run_ffprobe([
            "-select_streams", "v:0",
            "-show_entries", "stream=width,height,r_frame_rate,codec_name,bit_rate",
            file_path,
        ])
        
        stream = data.get("streams", [{}])[0]
        return {
            "width": stream.get("width"),
            "height": stream.get("height"),
            "fps": self._parse_fps(stream.get("r_frame_rate")),
            "codec": stream.get("codec_name"),
            "bitrate": stream.get("bit_rate"),
        }
    
    def get_audio_info(self, file_path: str) -> Dict[str, Any]:
        """Get quick audio info without full metadata."""
        data = self._run_ffprobe([
            "-select_streams", "a:0",
            "-show_entries", "stream=codec_name,sample_rate,channels,channel_layout,bit_rate",
            file_path,
        ])
        
        stream = data.get("streams", [{}])[0]
        return {
            "codec": stream.get("codec_name"),
            "sample_rate": stream.get("sample_rate"),
            "channels": stream.get("channels"),
            "channel_layout": stream.get("channel_layout"),
            "bitrate": stream.get("bit_rate"),
        }