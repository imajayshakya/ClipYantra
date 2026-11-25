"""ClipYantra Base Repository Classes."""

from abc import ABC, abstractmethod
from typing import Any, Generic, List, Optional, TypeVar
from uuid import UUID

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.base import BaseModel

ModelType = TypeVar("ModelType", bound=BaseModel)


class BaseRepository(ABC, Generic[ModelType]):
    """Base repository with common database operations."""

    def __init__(self, session: AsyncSession, model: type[ModelType]):
        self.session = session
        self.model = model

    async def create(self, **kwargs: Any) -> ModelType:
        """Create a new entity."""
        instance = self.model(**kwargs)
        self.session.add(instance)
        await self.session.flush()
        await self.session.refresh(instance)
        return instance

    async def get_by_id(self, id: UUID) -> Optional[ModelType]:
        """Get entity by ID."""
        result = await self.session.execute(
            select(self.model).where(self.model.id == id)
        )
        return result.scalar_one_or_none()

    async def update(self, id: UUID, **kwargs: Any) -> Optional[ModelType]:
        """Update entity by ID."""
        instance = await self.get_by_id(id)
        if instance is None:
            return None
        for key, value in kwargs.items():
            setattr(instance, key, value)
        await self.session.flush()
        await self.session.refresh(instance)
        return instance

    async def delete(self, id: UUID) -> bool:
        """Delete entity by ID."""
        instance = await self.get_by_id(id)
        if instance is None:
            return False
        await self.session.delete(instance)
        await self.session.flush()
        return True

    async def list(
        self,
        *,
        skip: int = 0,
        limit: int = 20,
        filters: Optional[dict[str, Any]] = None,
        order_by: Optional[str] = None,
    ) -> List[ModelType]:
        """List entities with pagination and filtering."""
        query = select(self.model)

        if filters:
            for key, value in filters.items():
                if hasattr(self.model, key):
                    query = query.where(getattr(self.model, key) == value)

        if order_by and hasattr(self.model, order_by):
            query = query.order_by(getattr(self.model, order_by))
        else:
            query = query.order_by(self.model.created_at.desc())

        query = query.offset(skip).limit(limit)
        result = await self.session.execute(query)
        return list(result.scalars().all())

    async def count(self, filters: Optional[dict[str, Any]] = None) -> int:
        """Count entities with filtering."""
        query = select(func.count(self.model.id))

        if filters:
            for key, value in filters.items():
                if hasattr(self.model, key):
                    query = query.where(getattr(self.model, key) == value)

        result = await self.session.execute(query)
        return result.scalar_one()

    async def exists(self, id: UUID) -> bool:
        """Check if entity exists by ID."""
        result = await self.session.execute(
            select(func.count(self.model.id)).where(self.model.id == id)
        )
        return result.scalar_one() > 0


class RepositoryError(Exception):
    """Base repository exception."""

    def __init__(self, message: str, code: str = "REPOSITORY_ERROR", details: Optional[dict[str, Any]] = None):
        self.message = message
        self.code = code
        self.details = details or {}
        super().__init__(message)