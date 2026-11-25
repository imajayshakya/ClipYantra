"""ClipYantra Custom Exceptions and Handlers."""

from typing import Any, Dict, Optional
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from pydantic import ValidationError
from sqlalchemy.exc import SQLAlchemyError


class ClipYantraException(Exception):
    """Base exception for ClipYantra application."""

    def __init__(
        self,
        message: str,
        status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR,
        error_code: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None,
    ):
        self.message = message
        self.status_code = status_code
        self.error_code = error_code or self.__class__.__name__
        self.details = details or {}
        super().__init__(self.message)


class NotFoundError(ClipYantraException):
    """Resource not found exception."""

    def __init__(self, resource: str, identifier: Any):
        super().__init__(
            message=f"{resource} not found: {identifier}",
            status_code=status.HTTP_404_NOT_FOUND,
            error_code="NOT_FOUND",
            details={"resource": resource, "identifier": str(identifier)},
        )


class ValidationError(ClipYantraException):
    """Input validation error."""

    def __init__(self, message: str, field: Optional[str] = None, value: Any = None):
        details = {}
        if field:
            details["field"] = field
        if value is not None:
            details["value"] = str(value)
        super().__init__(
            message=message,
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            error_code="VALIDATION_ERROR",
            details=details,
        )


class AuthenticationError(ClipYantraException):
    """Authentication failed exception."""

    def __init__(self, message: str = "Authentication failed"):
        super().__init__(
            message=message,
            status_code=status.HTTP_401_UNAUTHORIZED,
            error_code="AUTHENTICATION_ERROR",
        )


class AuthorizationError(ClipYantraException):
    """Authorization failed exception."""

    def __init__(self, message: str = "Insufficient permissions"):
        super().__init__(
            message=message,
            status_code=status.HTTP_403_FORBIDDEN,
            error_code="AUTHORIZATION_ERROR",
        )


class ConflictError(ClipYantraException):
    """Resource conflict exception."""

    def __init__(self, resource: str, message: str):
        super().__init__(
            message=message,
            status_code=status.HTTP_409_CONFLICT,
            error_code="CONFLICT",
            details={"resource": resource},
        )


class RateLimitError(ClipYantraException):
    """Rate limit exceeded exception."""

    def __init__(self, message: str = "Rate limit exceeded", retry_after: Optional[int] = None):
        details = {}
        if retry_after:
            details["retry_after"] = retry_after
        super().__init__(
            message=message,
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            error_code="RATE_LIMIT_EXCEEDED",
            details=details,
        )


class ExternalServiceError(ClipYantraException):
    """External service error exception."""

    def __init__(self, service: str, message: str, status_code: int = status.HTTP_502_BAD_GATEWAY):
        super().__init__(
            message=f"{service} error: {message}",
            status_code=status_code,
            error_code="EXTERNAL_SERVICE_ERROR",
            details={"service": service},
        )


class StorageError(ClipYantraException):
    """Storage operation error."""

    def __init__(self, operation: str, message: str):
        super().__init__(
            message=f"Storage {operation} failed: {message}",
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            error_code="STORAGE_ERROR",
            details={"operation": operation},
        )


class MediaProcessingError(ClipYantraException):
    """Media processing error."""

    def __init__(self, operation: str, message: str, file_path: Optional[str] = None):
        details = {"operation": operation}
        if file_path:
            details["file_path"] = file_path
        super().__init__(
            message=f"Media processing {operation} failed: {message}",
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            error_code="MEDIA_PROCESSING_ERROR",
            details=details,
        )


async def clipyantra_exception_handler(request: Request, exc: ClipYantraException) -> JSONResponse:
    """Handle ClipYantra exceptions."""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": {
                "code": exc.error_code,
                "message": exc.message,
                "details": exc.details,
            },
            "path": str(request.url.path),
        },
    )


async def validation_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    """Handle request validation errors."""
    errors = []
    for error in exc.errors():
        errors.append({
            "field": ".".join(str(x) for x in error["loc"]),
            "message": error["msg"],
            "type": error["type"],
        })

    from uuid import uuid4
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "code": "VALIDATION_FAILED",
            "message": "Request validation failed",
            "details": {"errors": errors},
            "request_id": str(uuid4()),
        },
    )


async def pydantic_validation_exception_handler(request: Request, exc: ValidationError) -> JSONResponse:
    """Handle Pydantic validation errors."""
    errors = []
    for error in exc.errors():
        errors.append({
            "field": ".".join(str(x) for x in error["loc"]),
            "message": error["msg"],
            "type": error["type"],
        })

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "error": {
                "code": "VALIDATION_ERROR",
                "message": "Data validation failed",
                "details": {"errors": errors},
            },
            "path": str(request.url.path),
        },
    )


async def sqlalchemy_exception_handler(request: Request, exc: SQLAlchemyError) -> JSONResponse:
    """Handle SQLAlchemy errors."""
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": {
                "code": "DATABASE_ERROR",
                "message": "Database operation failed",
                "details": {"type": exc.__class__.__name__},
            },
            "path": str(request.url.path),
        },
    )


def register_exception_handlers(app: FastAPI) -> None:
    """Register all exception handlers with the FastAPI app."""
    app.add_exception_handler(ClipYantraException, clipyantra_exception_handler)
    app.add_exception_handler(RequestValidationError, validation_exception_handler)
    app.add_exception_handler(ValidationError, pydantic_validation_exception_handler)
    app.add_exception_handler(SQLAlchemyError, sqlalchemy_exception_handler)