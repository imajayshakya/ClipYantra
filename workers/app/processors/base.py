"""
Base Processor Models for ClipYantra.

Defines data classes for media metadata, validation results,
transcription, diarization, analysis, and rendering results.
"""

from dataclasses import dataclass, field, asdict
from typing import Dict, Any, Optional, List
from datetime import datetime
import json


class ProcessorError(Exception):
    """Base exception for processor errors."""
    def __init__(self, message: str, code: str = "PROCESSOR_ERROR", details: Optional[Dict] = None):
        super().__init__(message)
        self.message = message
        self.code = code
        self.details = details or {}


@dataclass
class MediaMetadata:
    """Media file metadata extracted by ffprobe."""
    file_path: str
    file_size: int
    mime_type: str
    format_name: str
    format_long_name: str
    duration: Optional[float] = None
    bit_rate: Optional[int] = None
    width: Optional[int] = None
    height: Optional[int] = None
    video_codec: Optional[str] = None
    video_codec_long: Optional[str] = None
    video_profile: Optional[str] = None
    video_pix_fmt: Optional[str] = None
    video_fps: Optional[float] = None
    video_bitrate: Optional[int] = None
    audio_codec: Optional[str] = None
    audio_codec_long: Optional[str] = None
    audio_sample_rate: Optional[int] = None
    audio_channels: Optional[int] = None
    audio_channel_layout: Optional[str] = None
    audio_bitrate: Optional[int] = None
    streams: List[Dict[str, Any]] = field(default_factory=list)
    tags: Dict[str, str] = field(default_factory=dict)
    chapters: List[Dict[str, Any]] = field(default_factory=list)
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "MediaMetadata":
        return cls(**data)
    
    @property
    def has_video(self) -> bool:
        return self.width is not None and self.height is not None
    
    @property
    def has_audio(self) -> bool:
        return self.audio_codec is not None
    
    @property
    def aspect_ratio(self) -> Optional[float]:
        if self.width and self.height:
            return self.width / self.height
        return None
    
    @property
    def resolution_string(self) -> str:
        if self.width and self.height:
            return f"{self.width}x{self.height}"
        return "unknown"


@dataclass
class ValidationResult:
    """File validation result."""
    valid: bool
    file_path: str
    checks: Dict[str, bool] = field(default_factory=dict)
    error: Optional[str] = None
    warnings: List[str] = field(default_factory=list)
    metadata: Optional[MediaMetadata] = None
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "valid": self.valid,
            "file_path": self.file_path,
            "checks": self.checks,
            "error": self.error,
            "warnings": self.warnings,
            "metadata": self.metadata.to_dict() if self.metadata else None,
        }


@dataclass
class TranscriptionSegment:
    """Single transcription segment."""
    id: int
    start: float
    end: float
    text: str
    confidence: Optional[float] = None
    speaker: Optional[str] = None
    words: List[Dict[str, Any]] = field(default_factory=list)
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)
    
    @property
    def duration(self) -> float:
        return self.end - self.start


@dataclass
class TranscriptionResult:
    """Complete transcription result."""
    text: str
    language: str
    duration: float
    segments: List[TranscriptionSegment] = field(default_factory=list)
    words: List[Dict[str, Any]] = field(default_factory=list)
    model: Optional[str] = None
    processing_time: Optional[float] = None
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "text": self.text,
            "language": self.language,
            "duration": self.duration,
            "segments": [s.to_dict() for s in self.segments],
            "words": self.words,
            "model": self.model,
            "processing_time": self.processing_time,
        }
    
    def to_json(self) -> str:
        return json.dumps(self.to_dict())
    
    @classmethod
    def from_json(cls, json_str: str) -> "TranscriptionResult":
        data = json.loads(json_str)
        segments = [TranscriptionSegment(**s) for s in data.get("segments", [])]
        return cls(
            text=data["text"],
            language=data["language"],
            duration=data["duration"],
            segments=segments,
            words=data.get("words", []),
            model=data.get("model"),
            processing_time=data.get("processing_time"),
        )
    
    @property
    def word_count(self) -> int:
        return len(self.text.split())
    
    @property
    def segment_count(self) -> int:
        return len(self.segments)


@dataclass
class DiarizationSegment:
    """Speaker diarization segment."""
    start: float
    end: float
    speaker: str
    confidence: Optional[float] = None
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)
    
    @property
    def duration(self) -> float:
        return self.end - self.start


@dataclass
class DiarizationResult:
    """Speaker diarization result."""
    segments: List[DiarizationSegment] = field(default_factory=list)
    speakers: List[str] = field(default_factory=list)
    num_speakers: int = 0
    processing_time: Optional[float] = None
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "segments": [s.to_dict() for s in self.segments],
            "speakers": self.speakers,
            "num_speakers": self.num_speakers,
            "processing_time": self.processing_time,
        }
    
    def to_json(self) -> str:
        return json.dumps(self.to_dict())
    
    @classmethod
    def from_json(cls, json_str: str) -> "DiarizationResult":
        data = json.loads(json_str)
        segments = [DiarizationSegment(**s) for s in data.get("segments", [])]
        return cls(
            segments=segments,
            speakers=data.get("speakers", []),
            num_speakers=data.get("num_speakers", 0),
            processing_time=data.get("processing_time"),
        )
    
    def get_speaker_time(self, speaker: str) -> float:
        """Get total speaking time for a speaker."""
        return sum(s.duration for s in self.segments if s.speaker == speaker)
    
    def get_speaker_segments(self, speaker: str) -> List[DiarizationSegment]:
        """Get all segments for a speaker."""
        return [s for s in self.segments if s.speaker == speaker]


@dataclass
class Scene:
    """Video scene."""
    id: int
    start: float
    end: float
    score: float
    thumbnail_path: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)
    
    @property
    def duration(self) -> float:
        return self.end - self.start


@dataclass
class SceneDetectionResult:
    """Scene detection result."""
    scenes: List[Scene] = field(default_factory=list)
    threshold: float = 0.3
    min_scene_len: float = 1.0
    processing_time: Optional[float] = None
    total_duration: Optional[float] = None
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "scenes": [s.to_dict() for s in self.scenes],
            "threshold": self.threshold,
            "min_scene_len": self.min_scene_len,
            "processing_time": self.processing_time,
            "total_duration": self.total_duration,
        }
    
    @property
    def scene_count(self) -> int:
        return len(self.scenes)
    
    @property
    def avg_scene_duration(self) -> float:
        if not self.scenes:
            return 0
        return sum(s.duration for s in self.scenes) / len(self.scenes)


@dataclass
class Face:
    """Detected face."""
    frame_index: int
    timestamp: float
    bbox: Dict[str, int]  # x, y, width, height
    confidence: float
    landmarks: Optional[Dict[str, List[int]]] = None
    track_id: Optional[int] = None
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class FaceDetectionResult:
    """Face detection result."""
    faces: List[Face] = field(default_factory=list)
    frame_count: int = 0
    unique_tracks: int = 0
    processing_time: Optional[float] = None
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "faces": [f.to_dict() for f in self.faces],
            "frame_count": self.frame_count,
            "unique_tracks": self.unique_tracks,
            "processing_time": self.processing_time,
        }
    
    @property
    def face_count(self) -> int:
        return len(self.faces)


@dataclass
class ContentAnalysisResult:
    """Comprehensive content analysis result."""
    duration: float
    scenes: Optional[SceneDetectionResult] = None
    faces: Optional[FaceDetectionResult] = None
    objects: Optional[List[Dict]] = None
    emotion: Optional[Dict] = None
    audio: Optional[Dict] = None
    processing_time: Optional[float] = None
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "duration": self.duration,
            "scenes": self.scenes.to_dict() if self.scenes else None,
            "faces": self.faces.to_dict() if self.faces else None,
            "objects": self.objects,
            "emotion": self.emotion,
            "audio": self.audio,
            "processing_time": self.processing_time,
        }


@dataclass
class RenderPreset:
    """Video render preset."""
    name: str
    width: int
    height: int
    fps: int
    bitrate: str
    video_codec: str = "libx264"
    audio_codec: str = "aac"
    audio_bitrate: str = "128k"
    preset: str = "medium"
    profile: str = "high"
    level: str = "4.1"
    pixel_format: str = "yuv420p"
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)
    
    def to_ffmpeg_args(self) -> List[str]:
        """Convert preset to FFmpeg arguments."""
        return [
            "-c:v", self.video_codec,
            "-preset", self.preset,
            "-profile:v", self.profile,
            "-level", self.level,
            "-pix_fmt", self.pixel_format,
            "-b:v", self.bitrate,
            "-maxrate", self.bitrate,
            "-bufsize", str(int(self.bitrate.rstrip('kM')) * 2) + self.bitrate[-1],
            "-vf", f"scale={self.width}:{self.height}:force_original_aspect_ratio=decrease,pad={self.width}:{self.height}:(ow-iw)/2:(oh-ih)/2",
            "-r", str(self.fps),
            "-c:a", self.audio_codec,
            "-b:a", self.audio_bitrate,
        ]


@dataclass
class RenderResult:
    """Video render result."""
    output_path: str
    duration: float
    width: int
    height: int
    file_size: int
    format: str
    preset: str
    processing_time: Optional[float] = None
    bitrate: Optional[int] = None
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


# Default render presets
DEFAULT_PRESETS = {
    "vertical": RenderPreset(
        name="vertical",
        width=1080,
        height=1920,
        fps=30,
        bitrate="8M",
    ),
    "horizontal": RenderPreset(
        name="horizontal",
        width=1920,
        height=1080,
        fps=30,
        bitrate="12M",
    ),
    "square": RenderPreset(
        name="square",
        width=1080,
        height=1080,
        fps=30,
        bitrate="8M",
    ),
    "story": RenderPreset(
        name="story",
        width=1080,
        height=1920,
        fps=30,
        bitrate="8M",
    ),
    "preview": RenderPreset(
        name="preview",
        width=1280,
        height=720,
        fps=30,
        bitrate="3M",
        preset="fast",
    ),
    "proxy": RenderPreset(
        name="proxy",
        width=960,
        height=540,
        fps=30,
        bitrate="1M",
        preset="fast",
    ),
    "tiktok": RenderPreset(
        name="tiktok",
        width=1080,
        height=1920,
        fps=30,
        bitrate="8M",
    ),
    "reels": RenderPreset(
        name="reels",
        width=1080,
        height=1920,
        fps=30,
        bitrate="8M",
    ),
    "shorts": RenderPreset(
        name="shorts",
        width=1080,
        height=1920,
        fps=30,
        bitrate="8M",
    ),
    "youtube": RenderPreset(
        name="youtube",
        width=1920,
        height=1080,
        fps=30,
        bitrate="12M",
    ),
}