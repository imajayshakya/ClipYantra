"""ClipYantra Base Service Classes."""

from abc import ABC, abstractmethod
from typing import Any, Generic, TypeVar
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

T = TypeVar("T")
CreateSchema = TypeVar("CreateSchema")
UpdateSchema = TypeVar("UpdateSchema")


class BaseService(ABC, Generic[T, CreateSchema, UpdateSchema]):
    """Base service class with common CRUD operations."""

    def __init__(self, session: AsyncSession):
        self.session = session

    @abstractmethod
    async def create(self, data: CreateSchema) -> T:
        """Create a new entity."""
        pass

    @abstractmethod
    async def get_by_id(self, id: UUID) -> T | None:
        """Get entity by ID."""
        pass

    @abstractmethod
    async def update(self, id: UUID, data: UpdateSchema) -> T | None:
        """Update entity by ID."""
        pass

    @abstractmethod
    async def delete(self, id: UUID) -> bool:
        """Delete entity by ID."""
        pass

    @abstractmethod
    async def list(
        self,
        *,
        skip: int = 0,
        limit: int = 20,
        filters: dict[str, Any] | None = None,
    ) -> list[T]:
        """List entities with pagination and filtering."""
        pass

    @abstractmethod
    async def count(self, filters: dict[str, Any] | None = None) -> int:
        """Count entities with filtering."""
        pass


class ServiceError(Exception):
    """Base service exception."""

    def __init__(self, message: str, code: str = "SERVICE_ERROR", details: dict[str, Any] | None = None):
        self.message = message
        self.code = code
        self.details = details or {}
        super().__init__(message)


class NotFoundError(ServiceError):
    """Entity not found error."""

    def __init__(self, entity_type: str, identifier: Any):
        super().__init__(
            message=f"{entity_type} not found: {identifier}",
            code="NOT_FOUND",
            details={"entity_type": entity_type, "identifier": str(identifier)},
        )


class ValidationError(ServiceError):
    """Validation error."""

    def __init__(self, message: str, field: str | None = None, value: Any = None):
        details = {}
        if field:
            details["field"] = field
        if value is not None:
            details["value"] = str(value)
        super().__init__(
            message=message,
            code="VALIDATION_ERROR",
            details=details,
        )


class ConflictError(ServiceError):
    """Conflict error."""

    def __init__(self, entity_type: str, message: str):
        super().__init__(
            message=message,
            code="CONFLICT",
            details={"entity_type": entity_type},
        )