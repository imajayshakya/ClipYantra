"""
Worker Configuration Settings for ClipYantra.

This module manages all configuration for the worker processes
using Pydantic Settings for validation and environment variable parsing.
"""

import os
from functools import lru_cache
from pathlib import Path
from typing import List, Optional

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class WorkerSettings(BaseSettings):
    """Worker-specific configuration settings."""
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
    )
    
    # Environment
    ENVIRONMENT: str = Field(default="development", description="Runtime environment")
    DEBUG: bool = Field(default=False, description="Enable debug mode")
    LOG_LEVEL: str = Field(default="INFO", description="Logging level")
    
    # Database
    DATABASE_URL: str = Field(
        default="postgresql://postgres:postgres@localhost:5432/clipyantra",
        description="PostgreSQL connection URL"
    )
    DATABASE_POOL_SIZE: int = Field(default=5, description="Database connection pool size")
    DATABASE_MAX_OVERFLOW: int = Field(default=10, description="Max overflow connections")
    
    # Redis
    REDIS_URL: str = Field(
        default="redis://localhost:6379/0",
        description="Redis connection URL"
    )
    REDIS_MAX_CONNECTIONS: int = Field(default=20, description="Max Redis connections")
    REDIS_SOCKET_TIMEOUT: int = Field(default=5, description="Redis socket timeout (seconds)")
    REDIS_SOCKET_CONNECT_TIMEOUT: int = Field(default=5, description="Redis connect timeout (seconds)")
    
    # Celery Configuration
    CELERY_BROKER_URL: str = Field(
        default="redis://localhost:6379/1",
        description="Celery broker URL (Redis)"
    )
    CELERY_RESULT_BACKEND: str = Field(
        default="redis://localhost:6379/2",
        description="Celery result backend URL"
    )
    CELERY_CONCURRENCY: int = Field(default=4, description="Number of worker processes/threads")
    CELERY_PREFETCH_MULTIPLIER: int = Field(default=1, description="Task prefetch multiplier")
    CELERY_MAX_TASKS_PER_CHILD: int = Field(default=1000, description="Max tasks per worker child")
    CELERY_TASK_SOFT_TIME_LIMIT: int = Field(default=300, description="Soft time limit (seconds)")
    CELERY_TASK_TIME_LIMIT: int = Field(default=360, description="Hard time limit (seconds)")
    
    # Storage
    STORAGE_TYPE: str = Field(default="local", description="Storage backend: local, s3, gcs")
    STORAGE_LOCAL_PATH: str = Field(default="/app/data", description="Local storage path")
    STORAGE_S3_BUCKET: Optional[str] = Field(default=None, description="S3 bucket name")
    STORAGE_S3_REGION: str = Field(default="us-east-1", description="S3 region")
    STORAGE_S3_ACCESS_KEY: Optional[str] = Field(default=None, description="S3 access key")
    STORAGE_S3_SECRET_KEY: Optional[str] = Field(default=None, description="S3 secret key")
    STORAGE_GCS_BUCKET: Optional[str] = Field(default=None, description="GCS bucket name")
    STORAGE_GCS_PROJECT: Optional[str] = Field(default=None, description="GCS project ID")
    STORAGE_GCS_CREDENTIALS: Optional[str] = Field(default=None, description="GCS credentials JSON")
    
    # Media Processing
    FFMPEG_PATH: str = Field(default="ffmpeg", description="Path to ffmpeg binary")
    FFPROBE_PATH: str = Field(default="ffprobe", description="Path to ffprobe binary")
    MAX_VIDEO_DURATION: int = Field(default=7200, description="Max video duration (seconds)")
    MAX_FILE_SIZE: int = Field(default=5368709120, description="Max file size (5GB)")
    SUPPORTED_VIDEO_CODECS: List[str] = Field(
        default=["h264", "hevc", "vp9", "av1"],
        description="Supported video codecs"
    )
    SUPPORTED_AUDIO_CODECS: List[str] = Field(
        default=["aac", "mp3", "opus", "flac"],
        description="Supported audio codecs"
    )
    
    # Transcription
    WHISPER_MODEL: str = Field(default="base", description="Whisper model size: tiny, base, small, medium, large")
    WHISPER_DEVICE: str = Field(default="cpu", description="Whisper device: cpu, cuda")
    WHISPER_COMPUTE_TYPE: str = Field(default="int8", description="Whisper compute type: float16, int8")
    WHISPER_LANGUAGE: Optional[str] = Field(default=None, description="Force language (None for auto-detect)")
    TRANSCRIPTION_MAX_SPEAKERS: int = Field(default=10, description="Max speakers for diarization")
    
    # Analysis
    SCENE_DETECTION_THRESHOLD: float = Field(default=0.3, description="Scene detection threshold")
    ENABLE_FACE_DETECTION: bool = Field(default=True, description="Enable face detection")
    ENABLE_OBJECT_DETECTION: bool = Field(default=False, description="Enable object detection")
    ENABLE_SPEECH_EMOTION: bool = Field(default=False, description="Enable speech emotion analysis")
    
    # Rendering
    RENDER_PRESETS: dict = Field(
        default={
            "vertical": {"width": 1080, "height": 1920, "fps": 30, "bitrate": "8M"},
            "horizontal": {"width": 1920, "height": 1080, "fps": 30, "bitrate": "12M"},
            "square": {"width": 1080, "height": 1080, "fps": 30, "bitrate": "8M"},
            "story": {"width": 1080, "height": 1920, "fps": 30, "bitrate": "8M"},
        },
        description="Rendering presets"
    )
    DEFAULT_RENDER_PRESET: str = Field(default="vertical", description="Default render preset")
    MAX_CONCURRENT_RENDERS: int = Field(default=2, description="Max concurrent render jobs")
    
    # Webhooks & Callbacks
    WEBHOOK_URL: Optional[str] = Field(default=None, description="Webhook URL for task completion")
    WEBHOOK_SECRET: Optional[str] = Field(default=None, description="Webhook signing secret")
    WEBHOOK_TIMEOUT: int = Field(default=30, description="Webhook timeout (seconds)")
    WEBHOOK_MAX_RETRIES: int = Field(default=3, description="Max webhook retries")
    
    # Monitoring
    SENTRY_DSN: Optional[str] = Field(default=None, description="Sentry DSN for error tracking")
    PROMETHEUS_PORT: int = Field(default=9090, description="Prometheus metrics port")
    ENABLE_METRICS: bool = Field(default=True, description="Enable Prometheus metrics")
    
    # Security
    INTERNAL_API_KEY: Optional[str] = Field(default=None, description="Internal API key for service-to-service auth")
    ALLOWED_TASK_ORIGINS: List[str] = Field(default=[], description="Allowed origins for task submission")
    
    # Cleanup
    TEMP_FILE_TTL: int = Field(default=3600, description="Temp file TTL (seconds)")
    EXPIRED_UPLOAD_TTL: int = Field(default=86400, description="Expired upload TTL (seconds)")
    STUCK_TASK_THRESHOLD: int = Field(default=1800, description="Stuck task threshold (seconds)")
    
    @field_validator("ENVIRONMENT")
    @classmethod
    def validate_environment(cls, v: str) -> str:
        allowed = ["development", "staging", "production", "test"]
        if v not in allowed:
            raise ValueError(f"ENVIRONMENT must be one of {allowed}")
        return v
    
    @field_validator("LOG_LEVEL")
    @classmethod
    def validate_log_level(cls, v: str) -> str:
        allowed = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
        if v.upper() not in allowed:
            raise ValueError(f"LOG_LEVEL must be one of {allowed}")
        return v.upper()
    
    @field_validator("STORAGE_TYPE")
    @classmethod
    def validate_storage_type(cls, v: str) -> str:
        allowed = ["local", "s3", "gcs"]
        if v not in allowed:
            raise ValueError(f"STORAGE_TYPE must be one of {allowed}")
        return v
    
    @field_validator("WHISPER_MODEL")
    @classmethod
    def validate_whisper_model(cls, v: str) -> str:
        allowed = ["tiny", "base", "small", "medium", "large", "large-v2", "large-v3"]
        if v not in allowed:
            raise ValueError(f"WHISPER_MODEL must be one of {allowed}")
        return v
    
    @field_validator("WHISPER_DEVICE")
    @classmethod
    def validate_whisper_device(cls, v: str) -> str:
        allowed = ["cpu", "cuda", "mps"]
        if v not in allowed:
            raise ValueError(f"WHISPER_DEVICE must be one of {allowed}")
        return v
    
    @property
    def is_production(self) -> bool:
        return self.ENVIRONMENT == "production"
    
    @property
    def is_development(self) -> bool:
        return self.ENVIRONMENT == "development"
    
    @property
    def database_url_async(self) -> str:
        """Get async database URL for SQLAlchemy async engine."""
        return self.DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://")


@lru_cache()
def get_settings() -> WorkerSettings:
    """Get cached settings instance."""
    return WorkerSettings()


# Global settings instance
settings = get_settings()