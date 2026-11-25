"""ING-001/ING-002 SQLAlchemy source/upload/media repository."""

import hashlib
import json
from dataclasses import dataclass
from typing import Any

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import selectinload, sessionmaker

from app.api.schemas import (
    RightsDeclaration,
    SourceResponse,
    SourceType,
    UploadSessionCreateRequest,
)
from app.db.models import MediaAsset, SourceRecord, SourceRights, UploadSession


class IdempotencyConflictError(RuntimeError):
    pass


class RightsBlockedError(RuntimeError):
    pass


class SourceStoreUnavailableError(RuntimeError):
    pass


# String enum literals for source/upload status (stored as strings in DB)
SourceStatus = str
UploadStatus = str


@dataclass(frozen=True)
class UploadSessionCreationResult:
    source_id: str
    upload_session_id: str
    status: str
    upload_status: str
    rights_declaration: RightsDeclaration
    created_at: Any


class SourceRepository:
    def __init__(self, session_factory: sessionmaker) -> None:
        self._session_factory = session_factory

    @staticmethod
    def payload_fingerprint(request: UploadSessionCreateRequest) -> str:
        payload = request.model_dump(mode="json")
        canonical = json.dumps(
            payload,
            sort_keys=True,
            separators=(",", ":"),
        )
        return hashlib.sha256(canonical.encode("utf-8")).hexdigest()

    def create_upload_session(
        self,
        workspace_id: str,
        request: UploadSessionCreateRequest,
        idempotency_key: str,
    ) -> UploadSessionCreationResult:
        if request.rights_declaration == RightsDeclaration.UNKNOWN_BLOCKED:
            raise RightsBlockedError(
                "Unknown or blocked rights cannot start an upload session."
            )

        fingerprint = self.payload_fingerprint(request)

        try:
            with self._session_factory() as session:
                existing = self._find_existing(
                    session, workspace_id, idempotency_key
                )
                if existing is not None:
                    return self._replay(session, existing, fingerprint)

                source = SourceRecord(
                    workspace_id=workspace_id,
                    title=request.title,
                    source_type=SourceType.LOCAL_UPLOAD.value,
                    status="created",
                    checksum=request.checksum,
                    original_metadata={
                        "filename": request.filename,
                        "content_type": request.content_type,
                        "size_bytes": request.size_bytes,
                        "content_profile": request.content_profile.value,
                    },
                    idempotency_key=idempotency_key,
                    payload_fingerprint=fingerprint,
                )
                rights = SourceRights(
                    rights_declaration=request.rights_declaration.value,
                    rights_note=request.rights_note,
                    provenance="local_upload",
                )
                source.rights = rights

                upload_session = UploadSession(
                    workspace_id=workspace_id,
                    status="pending_upload",
                    idempotency_key=idempotency_key,
                    payload_fingerprint=fingerprint,
                )
                source.upload_sessions = [upload_session]

                session.add(source)
                try:
                    session.commit()
                except IntegrityError as exc:
                    session.rollback()
                    # A concurrent request with the same idempotency key may
                    # have won the race; replay its result instead of failing.
                    existing = self._find_existing(
                        session, workspace_id, idempotency_key
                    )
                    if existing is None:
                        raise SourceStoreUnavailableError(
                            "Source store rejected the upload session."
                        ) from exc
                    return self._replay(session, existing, fingerprint)

                session.refresh(source)
                session.refresh(upload_session)
                session.refresh(rights)
                return self._creation_result(upload_session, source)
        except SQLAlchemyError as exc:
            raise SourceStoreUnavailableError(
                "Source store is unavailable."
            ) from exc

    @staticmethod
    def _find_existing(
        session,
        workspace_id: str,
        idempotency_key: str,
    ) -> UploadSession | None:
        return session.scalar(
            select(UploadSession).where(
                UploadSession.workspace_id == workspace_id,
                UploadSession.idempotency_key == idempotency_key,
            )
        )

    def _replay(
        self,
        session,
        existing: UploadSession,
        fingerprint: str,
    ) -> UploadSessionCreationResult:
        if existing.payload_fingerprint != fingerprint:
            raise IdempotencyConflictError(
                "Idempotency key was used for a different payload."
            )
        source = session.get(SourceRecord, existing.source_id)
        if source is None:
            raise SourceStoreUnavailableError(
                "Upload session references no source record."
            )
        return self._creation_result(existing, source)

    @staticmethod
    def _creation_result(
        upload_session: UploadSession,
        source: SourceRecord,
    ) -> UploadSessionCreationResult:
        rights = source.rights
        if rights is None:
            raise SourceStoreUnavailableError(
                "Source record has no rights declaration."
            )
        return UploadSessionCreationResult(
            source_id=source.id,
            upload_session_id=upload_session.id,
            status=upload_session.status,
            upload_status=upload_session.status,
            rights_declaration=RightsDeclaration(rights.rights_declaration),
            created_at=upload_session.created_at,
        )

    def list_sources(self, workspace_id: str) -> list[SourceResponse]:
        try:
            with self._session_factory() as session:
                rows = session.scalars(
                    select(SourceRecord)
                    .where(SourceRecord.workspace_id == workspace_id)
                    .options(
                        selectinload(SourceRecord.rights),
                        selectinload(SourceRecord.upload_sessions),
                    )
                    .order_by(SourceRecord.created_at.desc())
                ).all()
                return [self._source_response(row) for row in rows]
        except SQLAlchemyError as exc:
            raise SourceStoreUnavailableError(
                "Source store is unavailable."
            ) from exc

    def get_source(
        self,
        workspace_id: str,
        source_id: str,
    ) -> SourceResponse | None:
        try:
            with self._session_factory() as session:
                row = session.scalar(
                    select(SourceRecord)
                    .where(
                        SourceRecord.workspace_id == workspace_id,
                        SourceRecord.id == source_id,
                    )
                    .options(
                        selectinload(SourceRecord.rights),
                        selectinload(SourceRecord.upload_sessions),
                    )
                )
                if row is None:
                    return None
                return self._source_response(row)
        except SQLAlchemyError as exc:
            raise SourceStoreUnavailableError(
                "Source store is unavailable."
            ) from exc

    @staticmethod
    def _source_response(source: SourceRecord) -> SourceResponse:
        rights = source.rights
        if rights is None:
            raise SourceStoreUnavailableError(
                "Source record has no rights declaration."
            )
        # Deterministic choice: the earliest upload session for the source.
        upload_session = (
            min(source.upload_sessions, key=lambda s: s.created_at)
            if source.upload_sessions
            else None
        )
        return SourceResponse(
            source_id=source.id,
            workspace_id=source.workspace_id,
            title=source.title,
            source_type=SourceType(source.source_type),
            status=source.status,
            checksum=source.checksum,
            rights_declaration=RightsDeclaration(rights.rights_declaration),
            rights_note=rights.rights_note,
            original_metadata=dict(source.original_metadata or {}),
            upload_session_id=upload_session.id if upload_session else None,
            upload_status=upload_session.status if upload_session else None,
            created_at=source.created_at,
            updated_at=source.updated_at,
        )

    # ING-002: Additional repository methods for media asset processing

    def get_upload_session(
        self,
        workspace_id: str,
        session_id: str,
    ) -> UploadSession | None:
        """Get upload session by ID."""
        try:
            with self._session_factory() as session:
                return session.scalar(
                    select(UploadSession).where(
                        UploadSession.workspace_id == workspace_id,
                        UploadSession.id == session_id,
                )
                )
        except SQLAlchemyError as exc:
            raise SourceStoreUnavailableError(
                "Source store is unavailable."
            ) from exc

    def update_upload_session_status(
        self,
        workspace_id: str,
        session_id: str,
        status: str,
    ) -> bool:
        """Update upload session status."""
        try:
            with self._session_factory() as session:
                upload_session = session.scalar(
                    select(UploadSession).where(
                        UploadSession.workspace_id == workspace_id,
                        UploadSession.id == session_id,
                )
                )
                if upload_session is None:
                    return False
                upload_session.status = status
                session.commit()
                return True
        except SQLAlchemyError as exc:
            raise SourceStoreUnavailableError(
                "Source store is unavailable."
            ) from exc

    def update_source_status(
        self,
        workspace_id: str,
        source_id: str,
        status: str,
        validation_job_id: str | None = None,
    ) -> bool:
        """Update source record status and optionally validation job ID."""
        try:
            with self._session_factory() as session:
                source = session.scalar(
                    select(SourceRecord).where(
                        SourceRecord.workspace_id == workspace_id,
                        SourceRecord.id == source_id,
                )
                )
                if source is None:
                    return False
                source.status = status
                if validation_job_id is not None:
                    source.validation_job_id = validation_job_id
                session.commit()
                return True
        except SQLAlchemyError as exc:
            raise SourceStoreUnavailableError(
                "Source store is unavailable."
            ) from exc

    def get_media_asset(self, media_asset_id: str) -> MediaAsset | None:
        """Get media asset by ID."""
        try:
            with self._session_factory() as session:
                return session.get(MediaAsset, media_asset_id)
        except SQLAlchemyError as exc:
            raise SourceStoreUnavailableError(
                "Source store is unavailable."
            ) from exc

    def get_media_asset_by_source(self, source_id: str) -> MediaAsset | None:
        """Get media asset by source ID."""
        try:
            with self._session_factory() as session:
                return session.scalar(
                    select(MediaAsset).where(MediaAsset.source_id == source_id)
                )
        except SQLAlchemyError as exc:
            raise SourceStoreUnavailableError(
                "Source store is unavailable."
            ) from exc

    def create_media_asset(self, media_asset: MediaAsset) -> MediaAsset:
        """Create a new media asset record."""
        try:
            with self._session_factory() as session:
                session.add(media_asset)
                try:
                    session.commit()
                except IntegrityError as exc:
                    session.rollback()
                    raise SourceStoreUnavailableError(
                        "Media asset already exists."
                    ) from exc
                session.refresh(media_asset)
                return media_asset
        except SQLAlchemyError as exc:
            raise SourceStoreUnavailableError(
                "Source store is unavailable."
            ) from exc


def create_source_repository(engine) -> SourceRepository:
    factory = sessionmaker(bind=engine, expire_on_commit=False)
    return SourceRepository(factory)