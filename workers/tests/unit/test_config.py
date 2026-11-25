"""
Unit tests for worker configuration.
"""

import os
from unittest.mock import patch

import pytest
from pydantic import ValidationError


class TestConfig:
    """Tests for worker configuration."""

    def test_config_loads_from_env(self):
        """Test that configuration loads from environment variables."""
        with patch.dict(os.environ, {
            "APP_ENV": "testing",
            "DEBUG": "true",
            "DATABASE_URL": "postgresql+asyncpg://test:test@localhost/test",
            "REDIS_URL": "redis://localhost:6379/0",
        }):
            from app.config import settings
            assert settings.app_env == "testing"
            assert settings.debug is True
            assert str(settings.database_url) == "postgresql+asyncpg://test:test@localhost/test"
            assert str(settings.redis_url) == "redis://localhost:6379/0"

    def test_config_defaults(self):
        """Test that configuration has sensible defaults."""
        with patch.dict(os.environ, {
            "APP_ENV": "testing",
            "DATABASE_URL": "postgresql+asyncpg://test:test@localhost/test",
            "REDIS_URL": "redis://localhost:6379/0",
        }, clear=True):
            from app.config import settings
            assert settings.log_level == "INFO"
            assert settings.worker_concurrency == 4
            assert settings.celery_task_serializer == "json"
            assert settings.celery_result_serializer == "json"

    def test_config_validation_database_url(self):
        """Test that database URL is validated."""
        with patch.dict(os.environ, {
            "APP_ENV": "testing",
            "DATABASE_URL": "invalid-url",
            "REDIS_URL": "redis://localhost:6379/0",
        }, clear=True):
            from app.config import Settings
            with pytest.raises(ValidationError):
                Settings()

    def test_config_validation_redis_url(self):
        """Test that Redis URL is validated."""
        with patch.dict(os.environ, {
            "APP_ENV": "testing",
            "DATABASE_URL": "postgresql+asyncpg://test:test@localhost/test",
            "REDIS_URL": "invalid-url",
        }, clear=True):
            from app.config import Settings
            with pytest.raises(ValidationError):
                Settings()

    def test_celery_config(self):
        """Test Celery-specific configuration."""
        with patch.dict(os.environ, {
            "APP_ENV": "testing",
            "DATABASE_URL": "postgresql+asyncpg://test:test@localhost/test",
            "REDIS_URL": "redis://localhost:6379/0",
            "CELERY_WORKER_CONCURRENCY": "8",
            "CELERY_TASK_TIME_LIMIT": "7200",
        }, clear=True):
            from app.config import settings
            assert settings.celery_worker_concurrency == 8
            assert settings.celery_task_time_limit == 7200

    def test_storage_paths(self):
        """Test storage path configuration."""
        with patch.dict(os.environ, {
            "APP_ENV": "testing",
            "DATABASE_URL": "postgresql+asyncpg://test:test@localhost/test",
            "REDIS_URL": "redis://localhost:6379/0",
            "STORAGE_BASE_PATH": "/custom/storage",
        }, clear=True):
            from app.config import settings
            assert str(settings.storage_base_path) == "/custom/storage"
            assert str(settings.upload_path) == "/custom/storage/uploads"
            assert str(settings.thumbnail_path) == "/custom/storage/thumbnails"

    def test_whisper_config(self):
        """Test Whisper configuration."""
        with patch.dict(os.environ, {
            "APP_ENV": "testing",
            "DATABASE_URL": "postgresql+asyncpg://test:test@localhost/test",
            "REDIS_URL": "redis://localhost:6379/0",
            "WHISPER_MODEL": "small",
            "WHISPER_DEVICE": "cuda",
            "WHISPER_COMPUTE_TYPE": "float16",
        }, clear=True):
            from app.config import settings
            assert settings.whisper_model == "small"
            assert settings.whisper_device == "cuda"
            assert settings.whisper_compute_type == "float16"

    def test_feature_flags(self):
        """Test feature flag configuration."""
        with patch.dict(os.environ, {
            "APP_ENV": "testing",
            "DATABASE_URL": "postgresql+asyncpg://test:test@localhost/test",
            "REDIS_URL": "redis://localhost:6379/0",
            "FEATURE_GPU_ACCELERATION": "true",
            "FEATURE_ADVANCED_ANALYSIS": "true",
        }, clear=True):
            from app.config import settings
            assert settings.feature_gpu_acceleration is True
            assert settings.feature_advanced_analysis is True

    def test_monitoring_config(self):
        """Test monitoring configuration."""
        with patch.dict(os.environ, {
            "APP_ENV": "testing",
            "DATABASE_URL": "postgresql+asyncpg://test:test@localhost/test",
            "REDIS_URL": "redis://localhost:6379/0",
            "PROMETHEUS_ENABLED": "true",
            "PROMETHEUS_PORT": "9090",
            "SENTRY_DSN": "https://test@sentry.io/123",
        }, clear=True):
            from app.config import settings
            assert settings.prometheus_enabled is True
            assert settings.prometheus_port == 9090
            assert str(settings.sentry_dsn) == "https://test@sentry.io/123"

    def test_s3_config(self):
        """Test S3 configuration."""
        with patch.dict(os.environ, {
            "APP_ENV": "testing",
            "DATABASE_URL": "postgresql+asyncpg://test:test@localhost/test",
            "REDIS_URL": "redis://localhost:6379/0",
            "S3_ENABLED": "true",
            "S3_BUCKET_NAME": "test-bucket",
            "S3_REGION": "us-west-2",
            "S3_ACCESS_KEY_ID": "test-key",
            "S3_SECRET_ACCESS_KEY": "test-secret",
        }, clear=True):
            from app.config import settings
            assert settings.s3_enabled is True
            assert settings.s3_bucket_name == "test-bucket"
            assert settings.s3_region == "us-west-2"
            assert settings.s3_access_key_id == "test-key"
            assert settings.s3_secret_access_key == "test-secret"

    def test_celery_queues_config(self):
        """Test Celery queue routing configuration."""
        with patch.dict(os.environ, {
            "APP_ENV": "testing",
            "DATABASE_URL": "postgresql+asyncpg://test:test@localhost/test",
            "REDIS_URL": "redis://localhost:6379/0",
        }, clear=True):
            from app.config import settings
            routes = settings.celery_task_routes
            assert "app.tasks.ingestion.*" in routes
            assert routes["app.tasks.ingestion.*"]["queue"] == "ingestion"
            assert "app.tasks.transcription.*" in routes
            assert routes["app.tasks.transcription.*"]["queue"] == "transcription"
            assert "app.tasks.analysis.*" in routes
            assert routes["app.tasks.analysis.*"]["queue"] == "analysis"
            assert "app.tasks.rendering.*" in routes
            assert routes["app.tasks.rendering.*"]["queue"] == "rendering"

    def test_beat_schedule_config(self):
        """Test Celery beat schedule configuration."""
        with patch.dict(os.environ, {
            "APP_ENV": "testing",
            "DATABASE_URL": "postgresql+asyncpg://test:test@localhost/test",
            "REDIS_URL": "redis://localhost:6379/0",
        }, clear=True):
            from app.config import settings
            schedule = settings.celery_beat_schedule
            assert "cleanup-expired-uploads" in schedule
            assert schedule["cleanup-expired-uploads"]["task"] == "app.tasks.ingestion.cleanup_expired_uploads"
            assert "generate-daily-analytics" in schedule
            assert schedule["generate-daily-analytics"]["task"] == "app.tasks.analysis.generate_daily_analytics"