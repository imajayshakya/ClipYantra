"""
ClipYantra Workers - Main Entry Point

This module provides the main entry point for running Celery workers.
It can be run directly or imported by Celery.
"""

import sys
from app.celery_app import celery_app


def main():
    """Main entry point for worker process."""
    # Start the Celery worker
    celery_app.worker_main([
        'worker',
        '--loglevel=info',
        '--concurrency=4',
        '--queues=ingestion,transcription,analysis,rendering,default',
        '--hostname=worker@%h'
    ])


if __name__ == '__main__':
    main()