"""
Celery Application Configuration for ClipYantra Workers.

This module creates and configures the Celery application with:
- Redis as message broker
- Redis as result backend
- Task routing and queues
- Worker configuration
- Beat scheduler for periodic tasks
"""

import os
from celery import Celery
from celery.schedules import crontab

from app.config import settings


def create_celery_app() -> Celery:
    """Create and configure the Celery application."""
    
    celery_app = Celery(
        "clipyantra",
        broker=settings.CELERY_BROKER_URL,
        backend=settings.CELERY_RESULT_BACKEND,
        include=[
            "app.tasks.ingestion",
            "app.tasks.transcription",
            "app.tasks.analysis",
            "app.tasks.rendering",
        ],
    )
    
    # Core Configuration
    celery_app.conf.update(
        # Task Serialization
        task_serializer="json",
        result_serializer="json",
        accept_content=["json"],
        
        # Timezone
        timezone="UTC",
        enable_utc=True,
        
        # Task Tracking
        task_track_started=True,
        task_send_sent_event=True,
        
        # Result Backend
        result_expires=3600,  # 1 hour
        result_compression="gzip",
        
        # Worker Configuration
        worker_prefetch_multiplier=settings.CELERY_PREFETCH_MULTIPLIER,
        worker_concurrency=settings.CELERY_CONCURRENCY,
        worker_max_tasks_per_child=settings.CELERY_MAX_TASKS_PER_CHILD,
        worker_disable_rate_limits=False,
        
        # Task Execution
        task_acks_late=True,
        task_reject_on_worker_lost=True,
        task_ignore_result=False,
        
        # Retry Policy
        task_autoretry_for=(Exception,),
        task_retry_backoff=True,
        task_retry_backoff_max=600,
        task_retry_jitter=True,
        
        # Routing
        task_routes={
            "app.tasks.ingestion.*": {"queue": "ingestion"},
            "app.tasks.transcription.*": {"queue": "transcription"},
            "app.tasks.analysis.*": {"queue": "analysis"},
            "app.tasks.rendering.*": {"queue": "rendering"},
        },
        
        # Queue Configuration
        task_create_missing_queues=True,
        task_default_queue="default",
        task_default_exchange="clipyantra",
        task_default_exchange_type="topic",
        task_default_routing_key="default",
        
        # Beat Schedule (Periodic Tasks)
        beat_schedule={
            "cleanup-expired-uploads": {
                "task": "app.tasks.ingestion.cleanup_expired_uploads",
                "schedule": crontab(hour=2, minute=0),  # Daily at 2 AM UTC
            },
            "cleanup-stuck-tasks": {
                "task": "app.tasks.ingestion.cleanup_stuck_tasks",
                "schedule": crontab(minute="*/15"),  # Every 15 minutes
            },
            "generate-daily-analytics": {
                "task": "app.tasks.analysis.generate_daily_analytics",
                "schedule": crontab(hour=3, minute=0),  # Daily at 3 AM UTC
            },
        },
        
        # Monitoring
        worker_send_task_events=True,
        task_send_sent_event=True,
        
        # Security
        task_secure_serialization=True,
    )
    
    # Configure queues with priorities
    celery_app.conf.task_queues = {
        "ingestion": {
            "exchange": "clipyantra",
            "exchange_type": "topic",
            "routing_key": "ingestion.*",
            "max_priority": 10,
        },
        "transcription": {
            "exchange": "clipyantra",
            "exchange_type": "topic",
            "routing_key": "transcription.*",
            "max_priority": 10,
        },
        "analysis": {
            "exchange": "clipyantra",
            "exchange_type": "topic",
            "routing_key": "analysis.*",
            "max_priority": 5,
        },
        "rendering": {
            "exchange": "clipyantra",
            "exchange_type": "topic",
            "routing_key": "rendering.*",
            "max_priority": 5,
        },
        "default": {
            "exchange": "clipyantra",
            "exchange_type": "topic",
            "routing_key": "default",
            "max_priority": 5,
        },
    }
    
    # Auto-discover tasks
    celery_app.autodiscover_tasks([
        "app.tasks.ingestion",
        "app.tasks.transcription",
        "app.tasks.analysis",
        "app.tasks.rendering",
    ])
    
    return celery_app


# Create the Celery app instance
celery_app = create_celery_app()


@celery_app.task(bind=True, ignore_result=True)
def debug_task(self):
    """Debug task to verify worker connectivity."""
    print(f"Request: {self.request!r}")


if __name__ == "__main__":
    celery_app.start()