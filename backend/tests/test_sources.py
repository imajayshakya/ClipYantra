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
        "checksum": VALID_CHECKSUM,
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


# ING-002: Tests for complete_upload, presign_upload, and get_media_asset endpoints


# Use a valid 64-char hex checksum for tests
VALID_CHECKSUM = "a" * 64
DIFFERENT_CHECKSUM = "b" * 64


def test_complete_upload_triggers_validation_job(source_store):
    """Test POST /sources/uploads/complete returns 202 with validation job ID."""
    app = create_app(
        settings=Settings(app_env="test", database_url=None),
        source_store=source_store,
    )
    headers = {"Idempotency-Key": "http-upload-key-ing002-001"}

    # Create upload session first
    create_resp = request(
        app,
        "POST",
        "/api/v1/sources/uploads",
        json=valid_payload(),
        headers=headers,
    )
    assert create_resp.status_code == 202
    upload_session_id = create_resp.json()["upload_session_id"]

    # Complete the upload with checksum
    complete_resp = request(
        app,
        "POST",
        "/api/v1/sources/uploads/complete",
        json={
            "upload_session_id": upload_session_id,
            "checksum": VALID_CHECKSUM,
        },
        headers={"Idempotency-Key": "http-upload-key-ing002-complete-001"},
    )

    assert complete_resp.status_code == 202
    payload = complete_resp.json()
    assert payload["source_id"] == create_resp.json()["source_id"]
    assert payload["status"] == "validating"
    assert "validation_job_id" in payload
    assert payload["validation_job_id"]


def test_complete_upload_checksum_mismatch_returns_400(source_store):
    """Test complete_upload returns 400 when checksum doesn't match."""
    app = create_app(
        settings=Settings(app_env="test", database_url=None),
        source_store=source_store,
    )
    headers = {"Idempotency-Key": "http-upload-key-ing002-002"}

    create_resp = request(
        app,
        "POST",
        "/api/v1/sources/uploads",
        json=valid_payload(),
        headers=headers,
    )
    upload_session_id = create_resp.json()["upload_session_id"]

    complete_resp = request(
        app,
        "POST",
        "/api/v1/sources/uploads/complete",
        json={
            "upload_session_id": upload_session_id,
            "checksum": DIFFERENT_CHECKSUM,
        },
        headers={"Idempotency-Key": "http-upload-key-ing002-complete-002"},
    )

    assert complete_resp.status_code == 400
    payload = complete_resp.json()
    assert payload["code"] == "CHECKSUM_MISMATCH"


def test_complete_upload_nonexistent_session_returns_404(source_store):
    """Test complete_upload returns 404 for non-existent upload session."""
    app = create_app(
        settings=Settings(app_env="test", database_url=None),
        source_store=source_store,
    )

    complete_resp = request(
        app,
        "POST",
        "/api/v1/sources/uploads/complete",
        json={
            "upload_session_id": "00000000-0000-0000-0000-000000000000",
            "checksum": VALID_CHECKSUM,
        },
        headers={"Idempotency-Key": "http-upload-key-ing002-complete-003"},
    )

    assert complete_resp.status_code == 404
    payload = complete_resp.json()
    assert payload["code"] == "UPLOAD_SESSION_NOT_FOUND"


def test_complete_upload_idempotent(source_store):
    """Test complete_upload is idempotent - same idempotency key returns same job ID."""
    app = create_app(
        settings=Settings(app_env="test", database_url=None),
        source_store=source_store,
    )
    headers = {"Idempotency-Key": "http-upload-key-ing002-003"}

    create_resp = request(
        app,
        "POST",
        "/api/v1/sources/uploads",
        json=valid_payload(),
        headers=headers,
    )
    upload_session_id = create_resp.json()["upload_session_id"]

    complete_headers = {"Idempotency-Key": "http-upload-key-ing002-complete-004"}
    first = request(
        app,
        "POST",
        "/api/v1/sources/uploads/complete",
        json={
            "upload_session_id": upload_session_id,
            "checksum": VALID_CHECKSUM,
        },
        headers=complete_headers,
    )
    second = request(
        app,
        "POST",
        "/api/v1/sources/uploads/complete",
        json={
            "upload_session_id": upload_session_id,
            "checksum": VALID_CHECKSUM,
        },
        headers=complete_headers,
    )

    assert first.status_code == 202
    assert second.status_code == 202
    # Same validation job ID should be returned
    assert first.json()["validation_job_id"] == second.json()["validation_job_id"]


def test_presign_upload_returns_upload_url(source_store):
    """Test POST /sources/uploads/presign returns presigned URL and storage key."""
    app = create_app(
        settings=Settings(app_env="test", database_url=None),
        source_store=source_store,
    )
    headers = {"Idempotency-Key": "http-upload-key-ing002-004"}

    create_resp = request(
        app,
        "POST",
        "/api/v1/sources/uploads",
        json=valid_payload(),
        headers=headers,
    )
    upload_session_id = create_resp.json()["upload_session_id"]

    presign_resp = request(
        app,
        "POST",
        "/api/v1/sources/uploads/presign",
        json={
            "upload_session_id": upload_session_id,
            "content_type": "video/mp4",
            "size_bytes": 1048576,
        },
    )

    assert presign_resp.status_code == 200
    payload = presign_resp.json()
    assert "upload_url" in payload
    assert "storage_key" in payload
    assert payload["expires_in"] == 3600
    assert payload["storage_key"].startswith("workspaces/")
    assert "sources/" in payload["storage_key"]
    assert "/original/" in payload["storage_key"]


def test_presign_upload_nonexistent_session_returns_404(source_store):
    """Test presign_upload returns 404 for non-existent upload session."""
    app = create_app(
        settings=Settings(app_env="test", database_url=None),
        source_store=source_store,
    )

    presign_resp = request(
        app,
        "POST",
        "/api/v1/sources/uploads/presign",
        json={
            "upload_session_id": "00000000-0000-0000-0000-000000000000",
            "content_type": "video/mp4",
            "size_bytes": 1048576,
        },
    )

    assert presign_resp.status_code == 404
    payload = presign_resp.json()
    assert payload["code"] == "UPLOAD_SESSION_NOT_FOUND"


def test_get_media_asset_not_found_returns_404(source_store):
    """Test GET /media-assets/{id} returns 404 for non-existent asset."""
    app = create_app(
        settings=Settings(app_env="test", database_url=None),
        source_store=source_store,
    )

    resp = request(app, "GET", "/api/v1/media-assets/non-existent-id")

    assert resp.status_code == 404
    payload = resp.json()
    assert payload["code"] == "MEDIA_ASSET_NOT_FOUND"
