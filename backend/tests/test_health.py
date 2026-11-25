import asyncio

import httpx
from pydantic import SecretStr

from app.core.config import Settings
from app.db.database import DatabaseCheckResult
from app.main import create_app


class FakeDatabaseProbe:
    def __init__(self, result: DatabaseCheckResult):
        self.result = result

    def check(self) -> DatabaseCheckResult:
        return self.result


def get(app, path: str):
    async def request():
        transport = httpx.ASGITransport(app=app)
        async with httpx.AsyncClient(
            transport=transport,
            base_url="http://test",
        ) as client:
            return await client.get(path)

    return asyncio.run(request())


def test_liveness_does_not_require_database():
    settings = Settings(app_env="test", database_url=None)
    app = create_app(settings=settings, database_probe=FakeDatabaseProbe(DatabaseCheckResult("not_configured")))

    response = get(app, "/health/live")

    assert response.status_code == 200
    payload = response.json()
    assert payload["status"] == "alive"
    assert "database_url" not in payload


def test_readiness_without_database_is_degraded():
    settings = Settings(app_env="test", database_url=None)
    app = create_app(settings=settings, database_probe=FakeDatabaseProbe(DatabaseCheckResult("not_configured")))

    response = get(app, "/health/ready")

    assert response.status_code == 503
    payload = response.json()
    assert payload["status"] == "degraded"
    assert payload["components"]["database"]["status"] == "not_configured"


def test_readiness_ready_when_database_accepts_select_one():
    settings = Settings(
        app_env="test",
        database_url=SecretStr("postgresql://user:password@localhost:5432/clip"),
    )
    app = create_app(settings=settings, database_probe=FakeDatabaseProbe(DatabaseCheckResult("ready")))

    response = get(app, "/health/ready")

    assert response.status_code == 200
    payload = response.json()
    assert payload["status"] == "ready"
    assert payload["components"]["database"]["status"] == "ready"


def test_readiness_unavailable_when_database_probe_fails():
    settings = Settings(
        app_env="test",
        database_url=SecretStr("postgresql://user:password@localhost:5432/clip"),
    )
    app = create_app(
        settings=settings,
        database_probe=FakeDatabaseProbe(DatabaseCheckResult("unavailable", "database_unreachable")),
    )

    response = get(app, "/health/ready")

    assert response.status_code == 503
    payload = response.json()
    assert payload["status"] == "degraded"
    assert payload["components"]["database"]["status"] == "unavailable"
    assert payload["components"]["database"]["detail"] == "database_unreachable"


def test_unimplemented_component_states_are_explicit():
    settings = Settings(app_env="test", database_url=None)
    app = create_app(settings=settings, database_probe=FakeDatabaseProbe(DatabaseCheckResult("not_configured")))

    payload = get(app, "/health/ready").json()

    assert payload["components"]["redis"]["status"] == "not_configured"
    assert payload["components"]["object_storage"]["status"] == "not_configured"
    assert payload["components"]["worker"]["status"] == "not_configured"
    for status in ("ready", "healthy"):
        assert all(component["status"] != status for component in payload["components"].values())


def test_health_payload_never_contains_secrets():
    database_secret = "postgresql://user:super-secret@localhost:5432/clip"
    redis_secret = "rediss://user:redis-secret@localhost:6379"
    settings = Settings(
        app_env="test",
        database_url=SecretStr(database_secret),
        redis_url=SecretStr(redis_secret),
    )
    app = create_app(settings=settings, database_probe=FakeDatabaseProbe(DatabaseCheckResult("ready")))

    response = get(app, "/health/ready")
    payload_text = response.text

    assert "super-secret" not in payload_text
    assert "redis-secret" not in payload_text
    assert "postgresql://" not in payload_text
    assert "rediss://" not in payload_text
