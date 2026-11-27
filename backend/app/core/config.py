"""ClipYantra Configuration Settings."""

import re
from functools import lru_cache
from typing import List, Optional
from pydantic import Field, SecretStr, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class ConfigurationError(ValueError):
    """Raised when configuration is invalid or malformed."""
    pass


def normalize_database_url(url: str) -> str:
    """Normalize database URL for psycopg3."""
    if url.startswith("postgresql://"):
        return url.replace("postgresql://", "postgresql+psycopg://", 1)
    return url


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,  # Allow case-insensitive env vars
        extra="ignore",
    )

    # Application
    project_name: str = "ClipYantra"
    version: str = "0.1.0"
    description: str = "ClipYantra Backend API for video processing and publishing"
    app_env: str = "disabled"
    debug: bool = True
    workspace_timezone: str = "Asia/Kolkata"

    # API
    api_v1_str: str = "/api/v1"
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    api_workers: int = 4

    # CORS
    cors_origins: List[str] = Field(
        default=["http://localhost:3000", "http://localhost:5173"],
        description="Allowed CORS origins",
    )

    # Database
    database_url: Optional[SecretStr] = None
    database_pool_size: int = 20
    database_max_overflow: int = 10
    database_pool_timeout: int = 30

    # Redis
    redis_url: Optional[SecretStr] = None
    redis_max_connections: int = 50

    # Security
    secret_key: str = Field(
        default="your-secret-key-change-in-production",
        description="Secret key for JWT tokens",
    )
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    refresh_token_expire_days: int = 7

    # Storage
    storage_backend: str = Field(
        default="local",
        description="Storage backend: local, s3, gcs, azure",
    )
    local_storage_path: str = "./storage"
    s3_bucket: Optional[str] = None
    s3_region: Optional[str] = None
    s3_access_key: Optional[str] = None
    s3_secret_key: Optional[str] = None
    s3_endpoint_url: Optional[str] = None

    # Celery
    celery_broker_url: str = Field(
        default="redis://localhost:6379/1",
        description="Celery broker URL",
    )
    celery_result_backend: str = Field(
        default="redis://localhost:6379/2",
        description="Celery result backend URL",
    )
    celery_task_track_started: bool = True
    celery_task_time_limit: int = 3600

    # Media Processing
    ffmpeg_path: str = "ffmpeg"
    ffprobe_path: str = "ffprobe"
    max_file_size_mb: int = 5000
    allowed_video_codecs: List[str] = Field(
        default=["h264", "hevc", "vp9", "av1"],
        description="Allowed video codecs",
    )
    allowed_audio_codecs: List[str] = Field(
        default=["aac", "mp3", "opus", "flac"],
        description="Allowed audio codecs",
    )
    allowed_containers: List[str] = Field(
        default=["mp4", "mov", "webm", "mkv"],
        description="Allowed container formats",
    )

    # Transcription (ING-003)
    transcription_routing_policy: str = "local_first"
    whisperx_model: str = "large-v3"
    whisperx_device: str = "auto"
    deepgram_api_key: Optional[str] = None
    deepgram_model: str = "nova-2"
    groq_api_key: Optional[str] = None
    groq_model: str = "whisper-large-v3"
    openai_api_key: Optional[str] = None
    openai_whisper_model: str = "whisper-1"
    nvidia_nim_base_url: Optional[str] = None
    nvidia_nim_model: str = "parakeet-rnnt-1.1b"
    nvidia_nim_api_key: Optional[str] = None

    # Audio Extraction
    audio_sample_rate: int = 16000
    audio_channels: int = 1
    chunk_duration_seconds: int = 1800  # 30 minutes
    chunk_overlap_seconds: int = 30

    # Scene Detection (ING-004)
    scene_default_threshold: float = Field(
        default=0.3,
        ge=0.1,
        le=1.0,
        description="Default scene detection threshold (0.1-1.0)",
    )
    scene_min_duration_ms: int = Field(
        default=1000,
        ge=500,
        description="Minimum scene duration in milliseconds",
    )
    keyframe_default_format: str = Field(
        default="jpeg",
        description="Default keyframe format (jpeg or png)",
    )
    keyframe_default_quality: int = Field(
        default=80,
        ge=50,
        le=100,
        description="Default keyframe quality (50-100)",
    )

    # Logging
    log_level: str = "INFO"
    log_format: str = "json"
    log_file: Optional[str] = None

    # Monitoring
    sentry_dsn: Optional[str] = None
    prometheus_metrics_enabled: bool = True

    # Property aliases for uppercase access (backward compatibility)
    @property
    def PROJECT_NAME(self) -> str:
        return self.project_name

    @property
    def VERSION(self) -> str:
        return self.version

    @property
    def DESCRIPTION(self) -> str:
        return self.description

    @property
    def APP_ENV(self) -> str:
        return self.app_env

    @property
    def DEBUG(self) -> bool:
        return self.debug

    @property
    def WORKSPACE_TIMEZONE(self) -> str:
        return self.workspace_timezone

    @property
    def API_V1_STR(self) -> str:
        return self.api_v1_str

    @property
    def API_HOST(self) -> str:
        return self.api_host

    @property
    def API_PORT(self) -> int:
        return self.api_port

    @property
    def API_WORKERS(self) -> int:
        return self.api_workers

    @property
    def CORS_ORIGINS(self) -> List[str]:
        return self.cors_origins

    @property
    def DATABASE_URL(self) -> Optional[SecretStr]:
        return self.database_url

    @property
    def DATABASE_POOL_SIZE(self) -> int:
        return self.database_pool_size

    @property
    def DATABASE_MAX_OVERFLOW(self) -> int:
        return self.database_max_overflow

    @property
    def DATABASE_POOL_TIMEOUT(self) -> int:
        return self.database_pool_timeout

    @property
    def REDIS_URL(self) -> Optional[SecretStr]:
        return self.redis_url

    @property
    def REDIS_MAX_CONNECTIONS(self) -> int:
        return self.redis_max_connections

    @property
    def SECRET_KEY(self) -> str:
        return self.secret_key

    @property
    def ALGORITHM(self) -> str:
        return self.algorithm

    @property
    def ACCESS_TOKEN_EXPIRE_MINUTES(self) -> int:
        return self.access_token_expire_minutes

    @property
    def REFRESH_TOKEN_EXPIRE_DAYS(self) -> int:
        return self.refresh_token_expire_days

    @property
    def STORAGE_BACKEND(self) -> str:
        return self.storage_backend

    @property
    def LOCAL_STORAGE_PATH(self) -> str:
        return self.local_storage_path

    @property
    def S3_BUCKET(self) -> Optional[str]:
        return self.s3_bucket

    @property
    def S3_REGION(self) -> Optional[str]:
        return self.s3_region

    @property
    def S3_ACCESS_KEY(self) -> Optional[str]:
        return self.s3_access_key

    @property
    def S3_SECRET_KEY(self) -> Optional[str]:
        return self.s3_secret_key

    @property
    def S3_ENDPOINT_URL(self) -> Optional[str]:
        return self.s3_endpoint_url

    @property
    def CELERY_BROKER_URL(self) -> str:
        return self.celery_broker_url

    @property
    def CELERY_RESULT_BACKEND(self) -> str:
        return self.celery_result_backend

    @property
    def CELERY_TASK_TRACK_STARTED(self) -> bool:
        return self.celery_task_track_started

    @property
    def CELERY_TASK_TIME_LIMIT(self) -> int:
        return self.celery_task_time_limit

    @property
    def FFMPEG_PATH(self) -> str:
        return self.ffmpeg_path

    @property
    def FFPROBE_PATH(self) -> str:
        return self.ffprobe_path

    @property
    def MAX_FILE_SIZE_MB(self) -> int:
        return self.max_file_size_mb

    @property
    def ALLOWED_VIDEO_CODECS(self) -> List[str]:
        return self.allowed_video_codecs

    @property
    def ALLOWED_AUDIO_CODECS(self) -> List[str]:
        return self.allowed_audio_codecs

    @property
    def ALLOWED_CONTAINERS(self) -> List[str]:
        return self.allowed_containers

    @property
    def LOG_LEVEL(self) -> str:
        return self.log_level

    @property
    def LOG_FORMAT(self) -> str:
        return self.log_format

    @property
    def LOG_FILE(self) -> Optional[str]:
        return self.log_file

    @property
    def SENTRY_DSN(self) -> Optional[str]:
        return self.sentry_dsn

    @property
    def PROMETHEUS_METRICS_ENABLED(self) -> bool:
        return self.prometheus_metrics_enabled

    # Transcription properties (ING-003)
    @property
    def TRANSCRIPTION_ROUTING_POLICY(self) -> str:
        return self.transcription_routing_policy

    @property
    def WHISPERX_MODEL(self) -> str:
        return self.whisperx_model

    @property
    def WHISPERX_DEVICE(self) -> str:
        return self.whisperx_device

    @property
    def DEEPGRAM_API_KEY(self) -> Optional[str]:
        return self.deepgram_api_key

    @property
    def DEEPGRAM_MODEL(self) -> str:
        return self.deepgram_model

    @property
    def GROQ_API_KEY(self) -> Optional[str]:
        return self.groq_api_key

    @property
    def GROQ_MODEL(self) -> str:
        return self.groq_model

    @property
    def OPENAI_API_KEY(self) -> Optional[str]:
        return self.openai_api_key

    @property
    def OPENAI_WHISPER_MODEL(self) -> str:
        return self.openai_whisper_model

    @property
    def NVIDIA_NIM_BASE_URL(self) -> Optional[str]:
        return self.nvidia_nim_base_url

    @property
    def NVIDIA_NIM_MODEL(self) -> str:
        return self.nvidia_nim_model

    @property
    def NVIDIA_NIM_API_KEY(self) -> Optional[str]:
        return self.nvidia_nim_api_key

    @property
    def AUDIO_SAMPLE_RATE(self) -> int:
        return self.audio_sample_rate

    @property
    def AUDIO_CHANNELS(self) -> int:
        return self.audio_channels

    @property
    def CHUNK_DURATION_SECONDS(self) -> int:
        return self.chunk_duration_seconds

    @property
    def CHUNK_OVERLAP_SECONDS(self) -> int:
        return self.chunk_overlap_seconds

        # Scene Detection properties (ING-004)
        @property
        def SCENE_DEFAULT_THRESHOLD(self) -> float:
            return self.scene_default_threshold

        @property
        def SCENE_MIN_DURATION_MS(self) -> int:
            return self.scene_min_duration_ms

        @property
        def KEYFRAME_DEFAULT_FORMAT(self) -> str:
            return self.keyframe_default_format

        @property
        def KEYFRAME_DEFAULT_QUALITY(self) -> int:
            return self.keyframe_default_quality

    @field_validator("database_url", mode="before")
    @classmethod
    def validate_database_url(cls, v: Optional[str]) -> Optional[SecretStr]:
        if v is None or v == "":
            return None
        # Handle case where v is already a SecretStr (from pydantic model)
        if isinstance(v, SecretStr):
            v = v.get_secret_value()
        # Allow async SQLite (sqlite+aiosqlite://) for testing only
        if v.startswith("sqlite+aiosqlite://"):
            return SecretStr(v)
        # Validate postgresql URL format
        if v.startswith("postgresql://") or v.startswith("postgresql+psycopg://"):
            # Check for whitespace in port area (e.g., "5432 /clip")
            if re.search(r':\d+\s+/', v):
                raise ConfigurationError("DATABASE_URL has malformed port")
            # Basic validation for port range
            port_match = re.search(r':(\d+)/', v)
            if port_match:
                port_str = port_match.group(1)
                # Check for extremely long port
                if len(port_str) > 5:
                    raise ConfigurationError("DATABASE_URL has malformed port")
                try:
                    port = int(port_str)
                except ValueError:
                    raise ConfigurationError("DATABASE_URL has malformed port")
                if port < 1 or port > 65535:
                    raise ConfigurationError(
                        "DATABASE_URL has malformed port"
                    )
            else:
                # No valid port found
                raise ConfigurationError("DATABASE_URL has malformed port")
        else:
            # Not a recognized scheme (only postgresql and async sqlite allowed)
            raise ConfigurationError("DATABASE_URL must be a postgresql URL (async database allowed for testing)")
        return SecretStr(v)

    @field_validator("redis_url", mode="before")
    @classmethod
    def validate_redis_url(cls, v: Optional[str]) -> Optional[SecretStr]:
        if v is None or v == "":
            return None
        return SecretStr(v)


def normalize_database_url(url: Optional[str]) -> Optional[str]:
    """Normalize database URL for SQLAlchemy compatibility."""
    if url is None:
        return None
    if isinstance(url, SecretStr):
        url = url.get_secret_value()
    # Convert postgresql:// to postgresql+psycopg:// for SQLAlchemy
    if url.startswith("postgresql://"):
        return url.replace("postgresql://", "postgresql+psycopg://", 1)
    return url


def load_settings(env_file: Optional[str] = None) -> Settings:
    """Load settings from environment and optional env file."""
    try:
        return Settings(_env_file=env_file)
    except Exception as e:
        # Re-raise ConfigurationError if it's the root cause
        if isinstance(e, ConfigurationError):
            raise
        # Convert pydantic ValidationError to ConfigurationError
        from pydantic import ValidationError
        if isinstance(e, ValidationError):
            # Extract the first error message
            errors = e.errors()
            if errors:
                msg = errors[0].get("msg", str(e))
                raise ConfigurationError(msg) from e
        raise


@lru_cache
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()


settings = get_settings()
