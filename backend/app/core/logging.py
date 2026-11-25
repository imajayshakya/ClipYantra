"""ClipYantra Structured Logging Configuration."""

import sys
import logging
import logging.config
from typing import Any, Dict
from pythonjsonlogger import jsonlogger

from app.core.config import settings


class CustomJsonFormatter(jsonlogger.JsonFormatter):
    """Custom JSON formatter with additional fields."""

    def add_fields(self, log_record: Dict[str, Any], record: logging.LogRecord, message_dict: Dict[str, Any]) -> None:
        super().add_fields(log_record, record, message_dict)
        log_record["service"] = settings.PROJECT_NAME
        log_record["version"] = settings.VERSION
        log_record["environment"] = settings.ENVIRONMENT


def get_logging_config() -> Dict[str, Any]:
    """Get logging configuration dictionary."""
    formatters = {
        "json": {
            "()": CustomJsonFormatter,
            "format": "%(asctime)s %(name)s %(levelname)s %(message)s",
            "datefmt": "%Y-%m-%dT%H:%M:%S%z",
        },
        "console": {
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
    }

    handlers = {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "json" if settings.LOG_FORMAT == "json" else "console",
            "stream": sys.stdout,
            "level": settings.LOG_LEVEL,
        },
    }

    if settings.LOG_FILE:
        handlers["file"] = {
            "class": "logging.handlers.RotatingFileHandler",
            "formatter": "json",
            "filename": settings.LOG_FILE,
            "maxBytes": 10485760,  # 10MB
            "backupCount": 5,
            "level": settings.LOG_LEVEL,
        }

    loggers = {
        "": {  # root logger
            "handlers": list(handlers.keys()),
            "level": settings.LOG_LEVEL,
            "propagate": False,
        },
        "uvicorn": {
            "handlers": list(handlers.keys()),
            "level": "INFO",
            "propagate": False,
        },
        "uvicorn.error": {
            "handlers": list(handlers.keys()),
            "level": "INFO",
            "propagate": False,
        },
        "uvicorn.access": {
            "handlers": list(handlers.keys()),
            "level": "INFO",
            "propagate": False,
        },
        "sqlalchemy.engine": {
            "handlers": list(handlers.keys()),
            "level": "WARNING",
            "propagate": False,
        },
        "celery": {
            "handlers": list(handlers.keys()),
            "level": "INFO",
            "propagate": False,
        },
    }

    return {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": formatters,
        "handlers": handlers,
        "loggers": loggers,
    }


def setup_logging() -> None:
    """Configure application logging."""
    config = get_logging_config()
    logging.config.dictConfig(config)

    # Set log level for third-party loggers
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("httpcore").setLevel(logging.WARNING)
    logging.getLogger("asyncio").setLevel(logging.WARNING)