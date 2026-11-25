"""ING-002 FFprobe validation service for media file analysis."""

from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional
import json
import subprocess
import shlex


class ValidationError(Exception):
    """Base class for validation errors with structured error codes."""
    
    def __init__(self, code: str, message: str, details: Optional[dict] = None):
        self.code = code
        self.message = message
        self.details = details or {}
        super().__init__(message)


class UnsupportedFormatError(ValidationError):
    """Raised when media format is not supported."""
    
    def __init__(self, message: str, details: Optional[dict] = None):
        super().__init__(code="UNSUPPORTED_FORMAT", message=message, details=details)


class CorruptMediaError(ValidationError):
    """Raised when media file is corrupted or unreadable."""
    
    def __init__(self, message: str, details: Optional[dict] = None):
        super().__init__(code="CORRUPT_MEDIA", message=message, details=details)


@dataclass
class ValidationResult:
    """Result of media validation."""
    is_valid: bool
    container: Optional[str] = None
    video_codec: Optional[str] = None
    audio_codec: Optional[str] = None
    duration_ms: Optional[int] = None
    width: Optional[int] = None
    height: Optional[int] = None
    bitrate: Optional[int] = None
    fps: Optional[float] = None
    audio_channels: Optional[int] = None
    sample_rate: Optional[int] = None
    error_message: Optional[str] = None
    error_code: Optional[str] = None
    validation_status: str = "pending"


# Supported formats per CONTRACT-FREEZE.md §12
SUPPORTED_CONTAINERS = {"mp4", "mov", "mkv", "webm", "mp3", "wav", "m4a"}
SUPPORTED_VIDEO_CODECS = {"h264", "hevc", "vp9", "av1"}
SUPPORTED_AUDIO_CODECS = {"aac", "opus", "mp3", "pcm_s16le", "flac"}
MAX_DURATION_MS = 2 * 60 * 60 * 1000  # 2 hours in milliseconds


class FFprobeValidator:
    """Validates media files using FFprobe."""

    def __init__(self, storage, max_duration_ms: int = MAX_DURATION_MS):
        self.storage = storage
        self.max_duration_ms = max_duration_ms
        self.SUPPORTED_CONTAINERS = SUPPORTED_CONTAINERS
        self.SUPPORTED_VIDEO_CODECS = SUPPORTED_VIDEO_CODECS
        self.SUPPORTED_AUDIO_CODECS = SUPPORTED_AUDIO_CODECS
        self.MAX_DURATION_MS = MAX_DURATION_MS

    async def validate(self, storage_key: str) -> ValidationResult:
        """Validate a media file by storage key and extract metadata.
        
        Args:
            storage_key: Storage key of the media file
            
        Returns:
            ValidationResult with validation status and media info
        """
        # Get file path from storage
        file_path = self.storage.get_file_path(storage_key)
        if not file_path:
            return ValidationResult(
                is_valid=False,
                error_message=f"File not found in storage: {storage_key}",
                validation_status="error",
                error_code="FILE_NOT_FOUND",
            )

        # Run FFprobe
        try:
            ffprobe_data = await self._run_ffprobe(file_path)
        except FileNotFoundError:
            return ValidationResult(
                is_valid=False,
                error_message="FFprobe execution failed: FFprobe executable not found",
                validation_status="error",
                error_code="FFPROBE_NOT_FOUND",
            )
        except subprocess.TimeoutExpired:
            return ValidationResult(
                is_valid=False,
                error_message="FFprobe timed out",
                validation_status="error",
                error_code="FFPROBE_TIMEOUT",
            )
        except CorruptMediaError as e:
            return ValidationResult(
                is_valid=False,
                error_message=e.message,
                validation_status="rejected",
                error_code=e.code,
            )
        except json.JSONDecodeError:
            return ValidationResult(
                is_valid=False,
                error_message="Failed to parse FFprobe output",
                validation_status="error",
                error_code="FFPROBE_PARSE_ERROR",
            )

        # Parse and validate
        try:
            return self._parse_and_validate(ffprobe_data)
        except UnsupportedFormatError as e:
            return ValidationResult(
                is_valid=False,
                error_message=str(e),
                validation_status="rejected",
                error_code=e.code,
            )

    async def _run_ffprobe(self, file_path: str) -> dict:
        """Run FFprobe and parse output."""
        cmd = [
            "ffprobe",
            "-v", "quiet",
            "-print_format", "json",
            "-show_format",
            "-show_streams",
            file_path,
        ]
        
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=30,
                check=True,
            )
        except subprocess.CalledProcessError as e:
            # FFprobe failed - likely corrupt or unreadable media file
            self._raise_corrupt_media_error(
                stderr=e.stderr,
                details={"returncode": e.returncode, "stderr": e.stderr, "stdout": e.stdout}
            )
        
        data = json.loads(result.stdout)
        return data
    
    def _raise_corrupt_media_error(self, stderr: str, details: Optional[dict] = None) -> None:
        """Raise CorruptMediaError with structured details."""
        raise CorruptMediaError(
            message=f"Media file is corrupt or unreadable: {stderr}",
            details=details or {"stderr": stderr}
        )

    def _parse_and_validate(self, data) -> ValidationResult:
        """Parse FFprobe JSON output and validate formats."""
        # Handle malformed input
        if not isinstance(data, dict):
            raise UnsupportedFormatError("Failed to parse FFprobe output: invalid format")
        
        format_info = data.get("format", {})
        streams = data.get("streams", [])
        
        # Find video and audio streams
        video_stream = next((s for s in streams if s.get("codec_type") == "video"), None)
        audio_stream = next((s for s in streams if s.get("codec_type") == "audio"), None)
        
        # Container format - handle multiple formats, prefer mp4 if present
        format_names = format_info.get("format_name", "").split(",")
        # Normalize to lowercase
        format_names = [f.strip().lower() for f in format_names]
        # Prefer mp4 if available, otherwise first one
        if "mp4" in format_names:
            container = "mp4"
        else:
            container = format_names[0] if format_names else "unknown"
        
        # Validate container
        if container not in self.SUPPORTED_CONTAINERS:
            raise UnsupportedFormatError(
                f"Unsupported container format: {container}. Supported: {sorted(self.SUPPORTED_CONTAINERS)}"
            )
        
        # Video codec
        video_codec = None
        width = None
        height = None
        fps = None
        if video_stream:
            video_codec = video_stream.get("codec_name", "").lower()
            if video_codec not in self.SUPPORTED_VIDEO_CODECS:
                raise UnsupportedFormatError(
                    f"Unsupported video codec: {video_codec}. Supported: {sorted(self.SUPPORTED_VIDEO_CODECS)}"
                )
            width = video_stream.get("width")
            height = video_stream.get("height")
            fps_str = video_stream.get("r_frame_rate") or video_stream.get("avg_frame_rate")
            if fps_str and "/" in fps_str:
                num, den = fps_str.split("/")
                if int(den) != 0:
                    fps = round(int(num) / int(den), 3)
        
        # Audio codec
        audio_codec = None
        audio_channels = None
        sample_rate = None
        if audio_stream:
            audio_codec = audio_stream.get("codec_name", "").lower()
            if audio_codec not in self.SUPPORTED_AUDIO_CODECS:
                raise UnsupportedFormatError(
                    f"Unsupported audio codec: {audio_codec}. Supported: {sorted(self.SUPPORTED_AUDIO_CODECS)}"
                )
            audio_channels = audio_stream.get("channels")
            sample_rate = audio_stream.get("sample_rate")
            if sample_rate:
                sample_rate = int(sample_rate)
        
        # Duration in milliseconds
        duration_str = format_info.get("duration") or (video_stream.get("duration") if video_stream else None)
        if duration_str:
            duration_ms = int(float(duration_str) * 1000)
        else:
            duration_ms = 0
        
        # Validate duration
        if duration_ms > self.MAX_DURATION_MS:
            raise UnsupportedFormatError(
                f"Duration exceeds maximum duration: {duration_ms}ms (max: {self.MAX_DURATION_MS}ms)"
            )
        
        # Bitrate
        bitrate = format_info.get("bit_rate")
        if bitrate:
            bitrate = int(bitrate)
        
        return ValidationResult(
            is_valid=True,
            container=container,
            video_codec=video_codec,
            audio_codec=audio_codec,
            duration_ms=duration_ms,
            width=width,
            height=height,
            bitrate=bitrate,
            fps=fps,
            audio_channels=audio_channels,
            sample_rate=sample_rate,
            validation_status="validated",
        )


def create_validator(storage, max_duration_ms: int = MAX_DURATION_MS) -> FFprobeValidator:
    """Factory function to create FFprobe validator."""
    return FFprobeValidator(storage=storage, max_duration_ms=max_duration_ms)
