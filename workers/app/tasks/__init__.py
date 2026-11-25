"""
ClipYantra Tasks Package

This package contains all Celery tasks organized by domain:
- ingestion: Media upload, validation, preprocessing
- transcription: Speech-to-text, speaker diarization
- analysis: Scene detection, face detection, content analysis
- rendering: Video composition, export, format conversion
"""

from app.tasks.ingestion import (
    validate_media_file,
    extract_metadata,
    generate_thumbnails,
    create_proxy_video,
    cleanup_expired_uploads,
    cleanup_stuck_tasks,
)
from app.tasks.transcription import (
    transcribe_audio,
    diarize_speakers,
    align_transcript,
    translate_transcript,
)
from app.tasks.analysis import (
    detect_scenes,
    detect_faces,
    analyze_content,
    generate_daily_analytics,
)
from app.tasks.rendering import (
    compose_video,
    render_captions,
    export_video,
    create_clips,
)

__all__ = [
    # Ingestion
    "validate_media_file",
    "extract_metadata",
    "generate_thumbnails",
    "create_proxy_video",
    "cleanup_expired_uploads",
    "cleanup_stuck_tasks",
    # Transcription
    "transcribe_audio",
    "diarize_speakers",
    "align_transcript",
    "translate_transcript",
    # Analysis
    "detect_scenes",
    "detect_faces",
    "analyze_content",
    "generate_daily_analytics",
    # Rendering
    "compose_video",
    "render_captions",
    "export_video",
    "create_clips",
]