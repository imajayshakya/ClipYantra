"""
Ingestion Tasks for ClipYantra.

Handles media file validation, metadata extraction, thumbnail generation,
proxy video creation, and cleanup operations.

Related Requirements: ING-002, ING-003
"""

import os
import hashlib
import mimetypes
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, Any, Optional, List
from dataclasses import dataclass

from celery import shared_task
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

from app.config import settings
from app.processors.ffmpeg_processor import FFmpegProcessor
from app.processors.base import MediaMetadata, ValidationResult


# Database models (placeholder - replace with actual models)
class MediaFile:
    """Placeholder for MediaFile model."""
    pass


class UploadSession:
    """Placeholder for UploadSession model."""
    pass


@dataclass
class IngestionResult:
    """Result of ingestion processing."""
    success: bool
    file_id: Optional[str] = None
    metadata: Optional[MediaMetadata] = None
    error: Optional[str] = None
    proxy_path: Optional[str] = None
    thumbnails: Optional[List[str]] = None


@shared_task(
    bind=True,
    name="app.tasks.ingestion.validate_media_file",
    queue="ingestion",
    max_retries=3,
    default_retry_delay=60,
    autoretry_for=(Exception,),
    retry_backoff=True,
)
def validate_media_file(self, file_path: str, upload_id: str) -> Dict[str, Any]:
    """
    Validate a media file for processing.
    
    Checks:
    - File exists and is readable
    - MIME type is supported
    - File size within limits
    - Codec compatibility
    - Duration within limits
    
    Args:
        file_path: Path to the media file
        upload_id: Unique upload session identifier
        
    Returns:
        Validation result with metadata or error
    """
    try:
        processor = FFmpegProcessor(
            ffmpeg_path=settings.FFMPEG_PATH,
            ffprobe_path=settings.FFPROBE_PATH,
        )
        
        # Validate file
        result: ValidationResult = processor.validate_file(file_path)
        
        if not result.valid:
            return {
                "success": False,
                "upload_id": upload_id,
                "error": result.error,
                "checks": result.checks,
            }
        
        # Extract metadata
        metadata = processor.extract_metadata(file_path)
        
        # Check duration
        if metadata.duration and metadata.duration > settings.MAX_VIDEO_DURATION:
            return {
                "success": False,
                "upload_id": upload_id,
                "error": f"Video duration {metadata.duration}s exceeds maximum {settings.MAX_VIDEO_DURATION}s",
                "metadata": metadata.to_dict(),
            }
        
        # Check file size
        file_size = os.path.getsize(file_path)
        if file_size > settings.MAX_FILE_SIZE:
            return {
                "success": False,
                "upload_id": upload_id,
                "error": f"File size {file_size} bytes exceeds maximum {settings.MAX_FILE_SIZE} bytes",
                "metadata": metadata.to_dict(),
            }
        
        # Compute file hash for deduplication
        file_hash = _compute_file_hash(file_path)
        
        return {
            "success": True,
            "upload_id": upload_id,
            "file_hash": file_hash,
            "file_size": file_size,
            "mime_type": metadata.mime_type,
            "metadata": metadata.to_dict(),
            "checks": result.checks,
        }
        
    except Exception as exc:
        self.retry(exc=exc)
        return {"success": False, "upload_id": upload_id, "error": str(exc)}


@shared_task(
    bind=True,
    name="app.tasks.ingestion.extract_metadata",
    queue="ingestion",
    max_retries=2,
    default_retry_delay=30,
)
def extract_metadata(self, file_path: str, upload_id: str) -> Dict[str, Any]:
    """
    Extract detailed metadata from media file.
    
    Uses ffprobe to extract:
    - Video/audio stream info
    - Codec details
    - Resolution, frame rate, bitrate
    - Duration, chapters
    - Metadata tags
    
    Args:
        file_path: Path to the media file
        upload_id: Unique upload session identifier
        
    Returns:
        Detailed metadata dictionary
    """
    try:
        processor = FFmpegProcessor(
            ffmpeg_path=settings.FFMPEG_PATH,
            ffprobe_path=settings.FFPROBE_PATH,
        )
        
        metadata = processor.extract_metadata(file_path)
        
        # Additional analysis
        streams_info = processor.analyze_streams(file_path)
        
        return {
            "success": True,
            "upload_id": upload_id,
            "metadata": metadata.to_dict(),
            "streams": streams_info,
        }
        
    except Exception as exc:
        self.retry(exc=exc)
        return {"success": False, "upload_id": upload_id, "error": str(exc)}


@shared_task(
    bind=True,
    name="app.tasks.ingestion.generate_thumbnails",
    queue="ingestion",
    max_retries=2,
    default_retry_delay=30,
)
def generate_thumbnails(
    self,
    file_path: str,
    upload_id: str,
    count: int = 10,
    timestamps: Optional[List[float]] = None,
) -> Dict[str, Any]:
    """
    Generate thumbnails from video at specified timestamps.
    
    Args:
        file_path: Path to the video file
        upload_id: Unique upload session identifier
        count: Number of thumbnails to generate (if timestamps not provided)
        timestamps: Specific timestamps in seconds (optional)
        
    Returns:
        List of generated thumbnail paths
    """
    try:
        processor = FFmpegProcessor(
            ffmpeg_path=settings.FFMPEG_PATH,
            ffprobe_path=settings.FFPROBE_PATH,
        )
        
        metadata = processor.extract_metadata(file_path)
        duration = metadata.duration or 0
        
        if timestamps is None:
            # Generate evenly distributed thumbnails
            if duration > 0:
                timestamps = [duration * i / (count + 1) for i in range(1, count + 1)]
            else:
                timestamps = [i * 10 for i in range(1, count + 1)]
        
        output_dir = Path(settings.STORAGE_LOCAL_PATH) / "thumbnails" / upload_id
        output_dir.mkdir(parents=True, exist_ok=True)
        
        thumbnail_paths = []
        for i, ts in enumerate(timestamps):
            output_path = output_dir / f"thumb_{i:03d}_{ts:.2f}.jpg"
            success = processor.extract_frame(file_path, ts, str(output_path))
            if success:
                thumbnail_paths.append(str(output_path))
        
        # Generate sprite sheet
        sprite_path = output_dir / "sprite.jpg"
        processor.create_sprite_sheet(file_path, timestamps, str(sprite_path))
        if sprite_path.exists():
            thumbnail_paths.append(str(sprite_path))
        
        return {
            "success": True,
            "upload_id": upload_id,
            "thumbnails": thumbnail_paths,
            "sprite_sheet": str(sprite_path) if sprite_path.exists() else None,
            "count": len(thumbnail_paths),
        }
        
    except Exception as exc:
        self.retry(exc=exc)
        return {"success": False, "upload_id": upload_id, "error": str(exc)}


@shared_task(
    bind=True,
    name="app.tasks.ingestion.create_proxy_video",
    queue="ingestion",
    max_retries=2,
    default_retry_delay=60,
)
def create_proxy_video(
    self,
    file_path: str,
    upload_id: str,
    preset: str = "proxy",
) -> Dict[str, Any]:
    """
    Create a proxy (lower quality) version for editing/preview.
    
    Args:
        file_path: Path to the source video file
        upload_id: Unique upload session identifier
        preset: Proxy quality preset (proxy, preview, edit)
        
    Returns:
        Proxy video path and metadata
    """
    try:
        processor = FFmpegProcessor(
            ffmpeg_path=settings.FFMPEG_PATH,
            ffprobe_path=settings.FFPROBE_PATH,
        )
        
        output_dir = Path(settings.STORAGE_LOCAL_PATH) / "proxies" / upload_id
        output_dir.mkdir(parents=True, exist_ok=True)
        
        proxy_path = output_dir / f"proxy_{preset}.mp4"
        
        # Proxy presets
        proxy_configs = {
            "proxy": {"vf": "scale=960:540", "b:v": "1M", "preset": "fast"},
            "preview": {"vf": "scale=1280:720", "b:v": "2M", "preset": "medium"},
            "edit": {"vf": "scale=1920:1080", "b:v": "5M", "preset": "slow"},
        }
        
        config = proxy_configs.get(preset, proxy_configs["proxy"])
        
        success = processor.transcode(
            input_path=file_path,
            output_path=str(proxy_path),
            video_codec="libx264",
            audio_codec="aac",
            video_filters=config["vf"],
            video_bitrate=config["b:v"],
            preset=config["preset"],
        )
        
        if not success:
            return {
                "success": False,
                "upload_id": upload_id,
                "error": "Proxy creation failed",
            }
        
        # Verify proxy
        proxy_metadata = processor.extract_metadata(str(proxy_path))
        
        return {
            "success": True,
            "upload_id": upload_id,
            "proxy_path": str(proxy_path),
            "proxy_metadata": proxy_metadata.to_dict(),
            "preset": preset,
        }
        
    except Exception as exc:
        self.retry(exc=exc)
        return {"success": False, "upload_id": upload_id, "error": str(exc)}


@shared_task(
    bind=True,
    name="app.tasks.ingestion.cleanup_expired_uploads",
    queue="ingestion",
)
def cleanup_expired_uploads(self) -> Dict[str, Any]:
    """
    Clean up expired upload sessions and associated files.
    
    Runs periodically to remove:
    - Upload sessions older than EXPIRED_UPLOAD_TTL
    - Temporary files from failed uploads
    - Orphaned proxy/thumbnail files
    
    Returns:
        Cleanup statistics
    """
    try:
        # This would connect to database and clean up
        # Placeholder implementation
        cleaned_sessions = 0
        cleaned_files = 0
        freed_space = 0
        
        # TODO: Implement actual database cleanup
        # engine = create_async_engine(settings.database_url_async)
        # async with AsyncSession(engine) as session:
        #     cutoff = datetime.utcnow() - timedelta(seconds=settings.EXPIRED_UPLOAD_TTL)
        #     # Delete expired sessions
        #     # Delete associated files
        
        return {
            "success": True,
            "cleaned_sessions": cleaned_sessions,
            "cleaned_files": cleaned_files,
            "freed_space_bytes": freed_space,
            "timestamp": datetime.utcnow().isoformat(),
        }
        
    except Exception as exc:
        return {"success": False, "error": str(exc)}


@shared_task(
    bind=True,
    name="app.tasks.ingestion.cleanup_stuck_tasks",
    queue="ingestion",
)
def cleanup_stuck_tasks(self) -> Dict[str, Any]:
    """
    Clean up tasks that appear stuck in processing.
    
    Identifies tasks that:
    - Have been in PROCESSING state longer than STUCK_TASK_THRESHOLD
    - Have no recent heartbeat
    - Are assigned to dead workers
    
    Returns:
        Cleanup statistics
    """
    try:
        # This would check Celery task states and clean up
        # Placeholder implementation
        stuck_count = 0
        recovered_count = 0
        
        # TODO: Implement actual stuck task detection
        # inspect = celery_app.control.inspect()
        # active = inspect.active()
        # scheduled = inspect.scheduled()
        
        return {
            "success": True,
            "stuck_tasks_found": stuck_count,
            "tasks_recovered": recovered_count,
            "timestamp": datetime.utcnow().isoformat(),
        }
        
    except Exception as exc:
        return {"success": False, "error": str(exc)}


def _compute_file_hash(file_path: str, algorithm: str = "sha256") -> str:
    """Compute file hash for deduplication."""
    hash_func = hashlib.new(algorithm)
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            hash_func.update(chunk)
    return hash_func.hexdigest()


# ING-002: Complete media ingestion pipeline
# ING-003: Proxy generation and thumbnail creation