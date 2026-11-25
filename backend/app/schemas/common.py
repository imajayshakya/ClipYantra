"""ClipYantra Common Schemas."""

from typing import Any, Generic, List, Optional, TypeVar
from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class TimestampMixin(BaseModel):
    """Mixin for timestamp fields."""

    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class UUIDMixin(BaseModel):
    """Mixin for UUID primary key."""

    id: UUID

    model_config = ConfigDict(from_attributes=True)


class BaseSchema(UUIDMixin, TimestampMixin):
    """Base schema with UUID and timestamps."""

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)


# Generic types for pagination
T = TypeVar("T")


class PaginationParams(BaseModel):
    """Pagination query parameters."""

    page: int = Field(default=1, ge=1, description="Page number")
    page_size: int = Field(default=20, ge=1, le=100, description="Items per page")

    @property
    def offset(self) -> int:
        return (self.page - 1) * self.page_size

    @property
    def limit(self) -> int:
        return self.page_size


class PaginatedResponse(BaseModel, Generic[T]):
    """Paginated response wrapper."""

    items: List[T]
    total: int
    page: int
    page_size: int
    total_pages: int

    @classmethod
    def create(cls, items: List[T], total: int, params: PaginationParams) -> "PaginatedResponse[T]":
        total_pages = (total + params.page_size - 1) // params.page_size
        return cls(
            items=items,
            total=total,
            page=params.page,
            page_size=params.page_size,
            total_pages=total_pages,
        )


class ErrorResponse(BaseModel):
    """Standard error response."""

    error: dict[str, Any]

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "error": {
                    "code": "VALIDATION_ERROR",
                    "message": "Request validation failed",
                    "details": {"errors": [{"field": "email", "message": "Invalid email format", "type": "value_error"}]},
                }
            }
        }
    )


class HealthResponse(BaseModel):
    """Health check response."""

    status: str = "healthy"
    service: str
    version: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class MessageResponse(BaseModel):
    """Simple message response."""

    message: str
    detail: Optional[str] = None