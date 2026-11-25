from pydantic import SecretStr

from app.core.config import ConfigurationError, Settings, load_settings


def test_settings_default_timezone(monkeypatch):
    monkeypatch.delenv("DATABASE_URL", raising=False)
    monkeypatch.delenv("REDIS_URL", raising=False)

    settings = load_settings(env_file=None)

    assert settings.app_env == "disabled"
    assert settings.database_url is None
    assert settings.redis_url is None
    assert settings.workspace_timezone == "Asia/Kolkata"


def test_invalid_database_scheme_is_sanitized(monkeypatch):
    monkeypatch.setenv("DATABASE_URL", "sqlite:///clipyantra.db")

    try:
        load_settings(env_file=None)
    except ConfigurationError as exc:
        message = str(exc)
    else:
        raise AssertionError("ConfigurationError was not raised")

    assert "DATABASE_URL" in message
    assert "postgresql" in message
    assert "clipyantra.db" not in message
    assert "sqlite" not in message


def test_malformed_postgresql_url_is_sanitized(monkeypatch):
    monkeypatch.setenv(
        "DATABASE_URL",
        "postgresql://user:super-secret@localhost:not-a-port/clip",
    )

    try:
        load_settings(env_file=None)
    except ConfigurationError as exc:
        message = str(exc)
    else:
        raise AssertionError("ConfigurationError was not raised")

    assert "malformed" in message.lower()
    assert "super-secret" not in message
    assert "not-a-port" not in message


def test_out_of_range_postgresql_port_is_sanitized(monkeypatch):
    monkeypatch.setenv(
        "DATABASE_URL",
        "postgresql://user:super-secret@localhost:70000/clip",
    )

    try:
        load_settings(env_file=None)
    except ConfigurationError as exc:
        message = str(exc)
    else:
        raise AssertionError("ConfigurationError was not raised")

    assert "malformed" in message.lower()
    assert "super-secret" not in message
    assert "70000" not in message


def test_whitespace_postgresql_port_is_sanitized(monkeypatch):
    monkeypatch.setenv(
        "DATABASE_URL",
        "postgresql://user:super-secret@localhost:5432 /clip",
    )

    try:
        load_settings(env_file=None)
    except ConfigurationError as exc:
        message = str(exc)
    else:
        raise AssertionError("ConfigurationError was not raised")

    assert "malformed" in message.lower()
    assert "super-secret" not in message


def test_extremely_long_postgresql_port_is_sanitized(monkeypatch):
    long_port = "9" * 5000
    monkeypatch.setenv(
        "DATABASE_URL",
        f"postgresql://user:super-secret@localhost:{long_port}/clip",
    )

    try:
        load_settings(env_file=None)
    except ConfigurationError as exc:
        message = str(exc)
    else:
        raise AssertionError("ConfigurationError was not raised")

    assert "malformed" in message.lower()
    assert "super-secret" not in message
    assert long_port not in message


def test_secret_values_are_not_represented_in_settings_repr():
    settings = Settings(
        database_url=SecretStr("postgresql://user:password@localhost:5432/clip"),
        redis_url=SecretStr("rediss://user:password@localhost:6379"),
        _env_file=None,
    )

    represented = repr(settings)

    assert "password" not in represented
    assert "postgresql://" not in represented
    assert "rediss://" not in represented
