import asyncio

import httpx
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.api.schemas import RightsDeclaration
from app.core.config import Settings
from app.db.models import Base
from app.db.source_repository import SourceRepository
from app.main import create_app


@pytest.fixture
def source_store():
    engine = create_engine(
        "sqlite+pysqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(engine)
    factory = sessionmaker(bind=engine, expire_on_commit=False)
    try:
        yield SourceRepository(factory)
    finally:
        engine.dispose()


def request(app, method: str, path: str, json=None, headers=None):
    async def send():
        transport = httpx.ASGITransport(app=app)
        async with httpx.AsyncClient(
            transport=transport,
            base_url="http://test",
        ) as client:
            return await client.request(
                method,
                path,
                json=json,
                headers=headers,
            )

    return asyncio.run(send())


def valid_payload() -> dict:
    return {
        "title": "Episode 42",
        "filename": "episode-42.mp4",
        "content_type": "video/mp4",
        "size_bytes": 1048576,
        "checksum": "sha256:abc123",
        "rights_declaration": RightsDeclaration.OWNED.value,
        "rights_note": "Created by the workspace owner",
        "content_profile": "podcast_interview",
    }


def test_create_upload_session_returns_202(source_store):
    app = create_app(
        settings=Settings(app_env="test", database_url=None),
        source_store=source_store,
    )

    response = request(
        app,
        "POST",
        "/api/v1/sources/uploads",
        json=valid_payload(),
        headers={"Idempotency-Key": "http-upload-key-001"},
    )

    assert response.status_code == 202
    payload = response.json()
    assert payload["source_id"]
    assert payload["upload_session_id"]
    assert payload["status"] == "pending_upload"
    assert payload["rights_declaration"] == "owned"


def test_duplicate_idempotency_request_returns_same_ids(source_store):
    app = create_app(
        settings=Settings(app_env="test", database_url=None),
        source_store=source_store,
    )
    headers = {"Idempotency-Key": "http-upload-key-002"}

    first = request(
        app,
        "POST",
        "/api/v1/sources/uploads",
        json=valid_payload(),
        headers=headers,
    )
    second = request(
        app,
        "POST",
        "/api/v1/sources/uploads",
        json=valid_payload(),
        headers=headers,
    )

    assert first.status_code == 202
    assert second.status_code == 202
    assert second.json()["source_id"] == first.json()["source_id"]
    assert second.json()["upload_session_id"] == first.json()["upload_session_id"]


def test_idempotency_conflict_returns_contract_error(source_store):
    app = create_app(
        settings=Settings(app_env="test", database_url=None),
        source_store=source_store,
    )
    headers = {"Idempotency-Key": "http-upload-key-003"}

    first = request(
        app,
        "POST",
        "/api/v1/sources/uploads",
        json=valid_payload(),
        headers=headers,
    )
    changed_payload = valid_payload()
    changed_payload["title"] = "Episode 43"
    second = request(
        app,
        "POST",
        "/api/v1/sources/uploads",
        json=changed_payload,
        headers=headers,
    )

    assert first.status_code == 202
    assert second.status_code == 409
    payload = second.json()
    assert payload["code"] == "IDEMPOTENCY_CONFLICT"
    assert "request_id" in payload


def test_unknown_blocked_rights_return_422(source_store):
    app = create_app(
        settings=Settings(app_env="test", database_url=None),
        source_store=source_store,
    )
    payload = valid_payload()
    payload["rights_declaration"] = "unknown_blocked"

    response = request(
        app,
        "POST",
        "/api/v1/sources/uploads",
        json=payload,
        headers={"Idempotency-Key": "http-upload-key-004"},
    )

    assert response.status_code == 422
    body = response.json()
    assert body["code"] == "RIGHTS_DECLARATION_BLOCKED"
    assert "request_id" in body


def test_invalid_request_uses_error_contract(source_store):
    app = create_app(
        settings=Settings(app_env="test", database_url=None),
        source_store=source_store,
    )
    payload = valid_payload()
    payload.pop("title")

    response = request(
        app,
        "POST",
        "/api/v1/sources/uploads",
        json=payload,
        headers={"Idempotency-Key": "http-upload-key-005"},
    )

    assert response.status_code == 422
    body = response.json()
    assert body["code"] == "VALIDATION_FAILED"
    assert "request_id" in body


def test_source_list_and_detail(source_store):
    app = create_app(
        settings=Settings(app_env="test", database_url=None),
        source_store=source_store,
    )
    created = request(
        app,
        "POST",
        "/api/v1/sources/uploads",
        json=valid_payload(),
        headers={"Idempotency-Key": "http-upload-key-006"},
    )
    source_id = created.json()["source_id"]

    listed = request(app, "GET", "/api/v1/sources")
    detailed = request(app, "GET", f"/api/v1/sources/{source_id}")

    assert listed.status_code == 200
    assert listed.json()["total"] == 1
    assert listed.json()["items"][0]["source_id"] == source_id
    assert detailed.status_code == 200
    assert detailed.json()["rights_declaration"] == "owned"
    assert "password" not in detailed.text


def test_unavailable_source_store_returns_503():
    app = create_app(
        settings=Settings(app_env="test", database_url=None),
        source_store=None,
    )

    response = request(
        app,
        "POST",
        "/api/v1/sources/uploads",
        json=valid_payload(),
        headers={"Idempotency-Key": "http-upload-key-007"},
    )

    assert response.status_code == 503
    assert response.json()["code"] == "SOURCE_STORE_UNAVAILABLE"
