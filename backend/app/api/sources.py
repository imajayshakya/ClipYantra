"""ING-001/ING-002 source upload-session, source-record, and media-asset routes."""

from uuid import uuid4

from fastapi import APIRouter, Header

from app.api.schemas import (
    CompleteUploadRequest,
    CompleteUploadResponse,
    ErrorResponse,
    MediaAssetResponse,
    PresignResponse,
    PresignUploadRequest,
    SourceListResponse,
    SourceResponse,
    UploadSessionCreateRequest,
)
from app.db.source_repository import (
    IdempotencyConflictError,
    RightsBlockedError,
    SourceRepository,
    SourceStoreUnavailableError,
)
from app.db.models import MediaAsset, SourceRecord, UploadSession
from app.services.ingestion_job import IngestionJob, create_ingestion_job
from app.services.storage_adapter import StorageConfig, create_storage_adapter
from app.services.ffprobe_validator import create_validator


DEFAULT_WORKSPACE_ID = "00000000-0000-0000-0000-000000000001"
STORAGE_ROOT = "./storage"


def error_response(
    code: str,
    message: str,
    details: dict | None = None,
) -> ErrorResponse:
    return ErrorResponse(
        code=code,
        message=message,
        details=details or {},
    )


def create_sources_router(source_store: SourceRepository | None) -> APIRouter:
    router = APIRouter(prefix="/api/v1", tags=["sources"])

    @router.post(
        "/sources/uploads",
        status_code=202,
    )
    def create_upload_session(
        request: UploadSessionCreateRequest,
        idempotency_key: str | None = Header(
            default=None,
            alias="Idempotency-Key",
        ),
    ):
        if source_store is None:
            return _json_error(
                status_code=503,
                response=error_response(
                    "SOURCE_STORE_UNAVAILABLE",
                    "The source store is unavailable.",
                ),
            )

        resolved_key = idempotency_key or str(uuid4())

        try:
            result = source_store.create_upload_session(
                workspace_id=DEFAULT_WORKSPACE_ID,
                request=request,
                idempotency_key=resolved_key,
            )
        except IdempotencyConflictError:
            return _json_error(
                status_code=409,
                response=error_response(
                    "IDEMPOTENCY_CONFLICT",
                    "The idempotency key was used for a different payload.",
                ),
            )
        except RightsBlockedError:
            return _json_error(
                status_code=422,
                response=error_response(
                    "RIGHTS_DECLARATION_BLOCKED",
                    "Unknown or blocked rights cannot start an upload session.",
                ),
            )
        except SourceStoreUnavailableError:
            return _json_error(
                status_code=503,
                response=error_response(
                    "SOURCE_STORE_UNAVAILABLE",
                    "The source store is unavailable.",
                ),
            )

        return {
            "source_id": result.source_id,
            "upload_session_id": result.upload_session_id,
            "status": "pending_upload",
            "upload_status": "pending_upload",
            "rights_declaration": result.rights_declaration,
            "created_at": result.created_at,
        }

    @router.get("/sources")
    def list_sources() -> SourceListResponse:
        if source_store is None:
            return _json_error(
                status_code=503,
                response=error_response(
                    "SOURCE_STORE_UNAVAILABLE",
                    "The source store is unavailable.",
                ),
            )
        try:
            items = source_store.list_sources(
                workspace_id=DEFAULT_WORKSPACE_ID
            )
        except SourceStoreUnavailableError:
            return _json_error(
                status_code=503,
                response=error_response(
                    "SOURCE_STORE_UNAVAILABLE",
                    "The source store is unavailable.",
                ),
            )
        return SourceListResponse(items=items, total=len(items), next_cursor=None)

    @router.get("/sources/{source_id}")
    def get_source(source_id: str):
        if source_store is None:
            return _json_error(
                status_code=503,
                response=error_response(
                    "SOURCE_STORE_UNAVAILABLE",
                    "The source store is unavailable.",
                ),
            )
        try:
            source = source_store.get_source(
                workspace_id=DEFAULT_WORKSPACE_ID,
                source_id=source_id,
            )
        except SourceStoreUnavailableError:
            return _json_error(
                status_code=503,
                response=error_response(
                    "SOURCE_STORE_UNAVAILABLE",
                    "The source store is unavailable.",
                ),
            )
        if source is None:
            return _json_error(
                status_code=404,
                response=error_response(
                    "SOURCE_NOT_FOUND",
                    "The requested source was not found.",
                ),
            )
        return source

    # ING-002: Complete upload and trigger validation
    @router.post(
        "/sources/uploads/complete",
        status_code=202,
    )
    def complete_upload(
        request: CompleteUploadRequest,
        idempotency_key: str | None = Header(
            default=None,
            alias="Idempotency-Key",
        ),
    ):
        if source_store is None:
            return _json_error(
                status_code=503,
                response=error_response(
                    "SOURCE_STORE_UNAVAILABLE",
                    "The source store is unavailable.",
                ),
            )

        # Verify upload session exists and belongs to workspace
        upload_session = source_store.get_upload_session(
            workspace_id=DEFAULT_WORKSPACE_ID,
            session_id=request.upload_session_id,
        )
        if not upload_session:
            return _json_error(
                status_code=404,
                response=error_response(
                    "UPLOAD_SESSION_NOT_FOUND",
                    "Upload session not found.",
                ),
            )

        # Verify checksum matches
        if upload_session.checksum and upload_session.checksum != request.checksum:
            return _json_error(
                status_code=400,
                response=error_response(
                    "CHECKSUM_MISMATCH",
                    "Provided checksum does not match uploaded file.",
                ),
            )

        # Update upload session with checksum and status
        source = source_store.get_source(
            workspace_id=DEFAULT_WORKSPACE_ID,
            source_id=upload_session.source_id,
        )
        if not source:
            return _json_error(
                status_code=404,
                response=error_response(
                    "SOURCE_NOT_FOUND",
                    "Source record not found.",
                ),
            )

        # Check idempotency: if completion_idempotency_key is provided and matches existing
        completion_key = idempotency_key or f"complete-{request.upload_session_id}"

        existing_source = source_store.get_source_by_idempotency_key(
            workspace_id=DEFAULT_WORKSPACE_ID,
            idempotency_key=completion_key,
        )
        if existing_source and existing_source.validation_job_id:
            # Return existing validation job ID for idempotent request
            return CompleteUploadResponse(
                source_id=existing_source.id,
                status=existing_source.status,
                validation_job_id=existing_source.validation_job_id,
            )

        # Create validation job ID
        validation_job_id = str(uuid4())

        # Update source with validation job ID
        source_store.update_source_status(
            workspace_id=DEFAULT_WORKSPACE_ID,
            source_id=source.source_id,
            status="validating",
            validation_job_id=validation_job_id,
        )

        # Store completion idempotency key for future idempotent requests
        source_store.update_source_completion_idempotency(
            workspace_id=DEFAULT_WORKSPACE_ID,
            source_id=source.source_id,
            idempotency_key=completion_key,
        )

        # Update upload session status
        source_store.update_upload_session_status(
            workspace_id=DEFAULT_WORKSPACE_ID,
            session_id=request.upload_session_id,
            status="validating",
        )

        # In a real implementation, this would be queued to Celery
        # For now, we return the validation job ID
        return CompleteUploadResponse(
            source_id=source.source_id,
            status="validating",
            validation_job_id=validation_job_id,
        )

    # ING-002: Get presigned upload URL
    @router.post(
        "/sources/uploads/presign",
        status_code=200,
    )
    def presign_upload(
        request: PresignUploadRequest,
    ) -> PresignResponse:
        if source_store is None:
            return _json_error(
                status_code=503,
                response=error_response(
                    "SOURCE_STORE_UNAVAILABLE",
                    "The source store is unavailable.",
                ),
            )

        # Verify upload session exists
        upload_session = source_store.get_upload_session(
            workspace_id=DEFAULT_WORKSPACE_ID,
            session_id=request.upload_session_id,
        )
        if not upload_session:
            return _json_error(
                status_code=404,
                response=error_response(
                    "UPLOAD_SESSION_NOT_FOUND",
                    "Upload session not found.",
                ),
            )

        # Generate storage key
        source = source_store.get_source(
            workspace_id=DEFAULT_WORKSPACE_ID,
            source_id=upload_session.source_id,
        )
        if not source:
            return _json_error(
                status_code=404,
                response=error_response(
                    "SOURCE_NOT_FOUND",
                    "Source record not found.",
                ),
            )

        storage_key = f"workspaces/{DEFAULT_WORKSPACE_ID}/sources/{source.source_id}/original/{uuid4().hex[:8]}"
        
        # Create storage adapter
        storage_config = StorageConfig(backend="local", local_root=STORAGE_ROOT)
        storage = create_storage_adapter(storage_config)
        
        # Get presigned URL
        upload_url = storage.get_presigned_upload_url(storage_key, expires_in=3600)

        return PresignResponse(
            upload_url=upload_url,
            storage_key=storage_key,
            expires_in=3600,
        )

    # ING-002: Get media asset by ID
    @router.get(
        "/media-assets/{media_asset_id}",
        status_code=200,
    )
    def get_media_asset(media_asset_id: str):
        if source_store is None:
            return _json_error(
                status_code=503,
                response=error_response(
                    "SOURCE_STORE_UNAVAILABLE",
                    "The source store is unavailable.",
                ),
            )

        media_asset = source_store.get_media_asset(media_asset_id)
        if not media_asset:
            return _json_error(
                status_code=404,
                response=error_response(
                    "MEDIA_ASSET_NOT_FOUND",
                    "Media asset not found.",
                ),
            )

        return MediaAssetResponse(
            media_asset_id=media_asset.id,
            source_id=media_asset.source_id,
            workspace_id=media_asset.workspace_id,
            storage_key=media_asset.storage_key,
            checksum=media_asset.checksum,
            container=media_asset.container,
            video_codec=media_asset.video_codec,
            audio_codec=media_asset.audio_codec,
            duration_ms=media_asset.duration_ms,
            width=media_asset.width,
            height=media_asset.height,
            bitrate=media_asset.bitrate,
            fps=float(media_asset.fps) if media_asset.fps else None,
            audio_channels=media_asset.audio_channels,
            sample_rate=media_asset.sample_rate,
            validation_status=media_asset.validation_status,
            created_at=media_asset.created_at,
            updated_at=media_asset.updated_at,
        )

    return router


def _json_error(status_code: int, response: ErrorResponse):
    from fastapi.responses import JSONResponse

    return JSONResponse(
        status_code=status_code,
        content=response.model_dump(mode="json"),
    )
