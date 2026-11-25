"""PostgreSQL database engine and readiness probe."""

from dataclasses import dataclass
from typing import Literal, Protocol

from sqlalchemy import Engine, create_engine, text
from sqlalchemy.exc import SQLAlchemyError

from app.core.config import (
    ConfigurationError,
    Settings,
    normalize_database_url,
    load_settings,
)


DatabaseStatus = Literal[
    "ready",
    "unavailable",
    "not_configured",
]


@dataclass(frozen=True)
class DatabaseCheckResult:
    status: DatabaseStatus
    detail: str | None = None


class DatabaseProbe(Protocol):
    def check(self) -> DatabaseCheckResult:
        """Return database readiness without exposing credentials or exceptions."""


class SqlAlchemyDatabaseProbe:
    def __init__(self, engine: Engine) -> None:
        self._engine = engine

    def check(self) -> DatabaseCheckResult:
        try:
            with self._engine.connect() as connection:
                connection.exec_driver_sql("SELECT 1")
            return DatabaseCheckResult(status="ready")
        except SQLAlchemyError:
            return DatabaseCheckResult(
                status="unavailable",
                detail="database_unreachable",
            )
        except Exception:
            return DatabaseCheckResult(
                status="unavailable",
                detail="database_unreachable",
            )


def create_database_engine(settings: Settings) -> Engine:
    if settings.database_url is None:
        raise ConfigurationError("DATABASE_URL is not configured.")

    database_url = settings.database_url.get_secret_value()
    database_url = normalize_database_url(database_url)

    return create_engine(
        database_url,
        pool_pre_ping=True,
        connect_args={"connect_timeout": 2},
    )


def create_database_probe(engine: Engine) -> DatabaseProbe:
    return SqlAlchemyDatabaseProbe(engine)
