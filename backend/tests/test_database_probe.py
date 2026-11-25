from unittest.mock import MagicMock, patch

from pydantic import SecretStr

from sqlalchemy.exc import SQLAlchemyError

from app.core.config import Settings
from app.db.database import (
    SqlAlchemyDatabaseProbe,
    create_database_engine,
)


def test_database_probe_reports_ready():
    connection = MagicMock()
    context = MagicMock()
    context.__enter__.return_value = connection
    engine = MagicMock()
    engine.connect.return_value = context

    probe = SqlAlchemyDatabaseProbe(engine)
    result = probe.check()

    connection.exec_driver_sql.assert_called_once_with("SELECT 1")
    assert result.status == "ready"
    assert result.detail is None


def test_database_probe_reports_unavailable_without_exception_detail():
    context = MagicMock()
    context.__enter__.side_effect = SQLAlchemyError("postgresql://user:password@db/clip")
    engine = MagicMock()
    engine.connect.return_value = context

    probe = SqlAlchemyDatabaseProbe(engine)
    result = probe.check()

    assert result.status == "unavailable"
    assert result.detail == "database_unreachable"
    assert "password" not in str(result)


def test_plain_postgresql_url_is_normalized_for_psycopg3():
    settings = Settings(
        database_url=SecretStr(
            "postgresql://user:password@localhost:5432/clip",
        ),
        _env_file=None,
    )

    mock_engine = MagicMock()
    with patch(
            "app.db.database.create_engine",
        return_value=mock_engine,
    ) as mock_create_engine:
        engine = create_database_engine(settings)

    mock_create_engine.assert_called_once_with(
        "postgresql+psycopg://user:password@localhost:5432/clip",
        pool_pre_ping=True,
        connect_args={"connect_timeout": 2},
    )
    assert engine is mock_engine
