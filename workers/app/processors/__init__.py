"""
ClipYantra Processors Package

Core media processing utilities:
- FFmpegProcessor: Video/audio processing wrapper
- WhisperProcessor: Speech-to-text and diarization
- Base classes and data models
"""

from app.processors.base import (
    MediaMetadata,
    ValidationResult,
    TranscriptionResult,
    DiarizationResult,
    SceneDetectionResult,
    FaceDetectionResult,
    ContentAnalysisResult,
    RenderResult,
    RenderPreset,
    ProcessorError,
)

from app.processors.ffmpeg_processor import FFmpegProcessor
from app.processors.whisper_processor import WhisperProcessor

__all__ = [
    # Base models
    "MediaMetadata",
    "ValidationResult",
    "TranscriptionResult",
    "DiarizationResult",
    "SceneDetectionResult",
    "FaceDetectionResult",
    "ContentAnalysisResult",
    "RenderResult",
    "RenderPreset",
    "ProcessorError",
    # Processors
    "FFmpegProcessor",
    "WhisperProcessor",
]