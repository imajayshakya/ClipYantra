import uuid

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.api.schemas import (
    RightsDeclaration,
    UploadSessionCreateRequest,
)
from app.db.models import Base
from app.db.source_repository import (
    IdempotencyConflictError,
    RightsBlockedError,
    SourceRepository,
)


@pytest.fixture
def session_factory():
    engine = create_engine(
        "sqlite+pysqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(engine)
    factory = sessionmaker(bind=engine, expire_on_commit=False)
    try:
        yield factory
    finally:
        engine.dispose()


def valid_request() -> UploadSessionCreateRequest:
    return UploadSessionCreateRequest(
        title="Episode 42",
        filename="episode-42.mp4",
        content_type="video/mp4",
        size_bytes=1048576,
        checksum="sha256:abc123",
        rights_declaration=RightsDeclaration.OWNED,
        rights_note="Created by the workspace owner",
        content_profile="podcast_interview",
    )


def test_create_upload_session_persists_source_rights_and_session(session_factory):
    repository = SourceRepository(session_factory)

    result = repository.create_upload_session(
        workspace_id="00000000-0000-0000-0000-000000000001",
        request=valid_request(),
        idempotency_key="upload-key-001",
    )

    assert result.source_id
    assert result.upload_session_id
    assert result.status == "pending_upload"

    source = repository.get_source(
        workspace_id="00000000-0000-0000-0000-000000000001",
        source_id=result.source_id,
    )
    assert source is not None
    assert source.title == "Episode 42"
    assert source.rights_declaration == "owned"


def test_duplicate_idempotency_key_returns_same_ids(session_factory):
    repository = SourceRepository(session_factory)
    workspace_id = "00000000-0000-0000-0000-000000000001"

    first = repository.create_upload_session(
        workspace_id=workspace_id,
        request=valid_request(),
        idempotency_key="upload-key-002",
    )
    second = repository.create_upload_session(
        workspace_id=workspace_id,
        request=valid_request(),
        idempotency_key="upload-key-002",
    )

    assert second.source_id == first.source_id
    assert second.upload_session_id == first.upload_session_id
    assert len(repository.list_sources(workspace_id=workspace_id)) == 1


def test_different_payload_for_same_idempotency_key_conflicts(session_factory):
    repository = SourceRepository(session_factory)
    workspace_id = "00000000-0000-0000-0000-000000000001"
    first_request = valid_request()
    second_request = valid_request().model_copy(update={"title": "Episode 43"})

    repository.create_upload_session(
        workspace_id=workspace_id,
        request=first_request,
        idempotency_key="upload-key-003",
    )

    with pytest.raises(IdempotencyConflictError):
        repository.create_upload_session(
            workspace_id=workspace_id,
            request=second_request,
            idempotency_key="upload-key-003",
        )


def test_unknown_blocked_rights_create_no_rows(session_factory):
    repository = SourceRepository(session_factory)
    workspace_id = "00000000-0000-0000-0000-000000000001"
    request = valid_request().model_copy(
        update={"rights_declaration": RightsDeclaration.UNKNOWN_BLOCKED}
    )

    with pytest.raises(RightsBlockedError):
        repository.create_upload_session(
            workspace_id=workspace_id,
            request=request,
            idempotency_key="upload-key-004",
        )

    assert repository.list_sources(workspace_id=workspace_id) == []


def test_source_is_readable_in_a_separate_session(session_factory):
    repository = SourceRepository(session_factory)
    workspace_id = "00000000-0000-0000-0000-000000000001"

    created = repository.create_upload_session(
        workspace_id=workspace_id,
        request=valid_request(),
        idempotency_key="upload-key-005",
    )

    with session_factory() as session:
        from backend.app.db.models import SourceRecord

        row = session.get(SourceRecord, created.source_id)
        assert row is not None
        assert row.title == "Episode 42"
