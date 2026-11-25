"""ClipYantra Database Session Management."""

from contextlib import asynccontextmanager
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.pool import NullPool

from app.core.config import settings


class DatabaseManager:
    """Manages database connections and sessions."""

    def __init__(self) -> None:
        self._engine: AsyncEngine | None = None
        self._session_factory: async_sessionmaker[AsyncSession] | None = None

    @property
    def engine(self) -> AsyncEngine:
        """Get or create the async engine."""
        if self._engine is None:
                # Handle case where DATABASE_URL is not configured
                database_url = settings.DATABASE_URL
                if database_url is None:
                    # Return a dummy engine for testing - will fail on actual use
                    from sqlalchemy.ext.asyncio import create_async_engine
                    self._engine = create_async_engine("sqlite+aiosqlite:///:memory:")
                else:
                    self._engine = create_async_engine(
                        database_url.get_secret_value() if hasattr(database_url, 'get_secret_value') else str(database_url),
                        echo=settings.DEBUG,
                        pool_size=settings.DATABASE_POOL_SIZE,
                        max_overflow=settings.DATABASE_MAX_OVERFLOW,
                        pool_timeout=settings.DATABASE_POOL_TIMEOUT,
                        pool_pre_ping=True,
                        poolclass=NullPool if settings.APP_ENV == "testing" else None,
                    )
        return self._engine

    @property
    def session_factory(self) -> async_sessionmaker[AsyncSession]:
        """Get or create the session factory."""
        if self._session_factory is None:
            self._session_factory = async_sessionmaker(
                bind=self.engine,
                class_=AsyncSession,
                expire_on_commit=False,
                autoflush=False,
                autocommit=False,
            )
        return self._session_factory

    async def init(self) -> None:
        """Initialize database connection."""
        # Test connection
        async with self.engine.begin() as conn:
            await conn.run_sync(lambda _: None)

    async def close(self) -> None:
        """Close database connections."""
        if self._engine:
            await self._engine.dispose()
            self._engine = None
            self._session_factory = None

    @asynccontextmanager
    async def session(self) -> AsyncGenerator[AsyncSession, None]:
        """Get a database session."""
        async with self.session_factory() as session:
            try:
                yield session
                await session.commit()
            except Exception:
                await session.rollback()
                raise
            finally:
                await session.close()


# Global database manager instance
db_manager = DatabaseManager()


async def init_db() -> None:
    """Initialize database on application startup."""
    await db_manager.init()


async def close_db() -> None:
    """Close database on application shutdown."""
    await db_manager.close()


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """FastAPI dependency for database session."""
    async with db_manager.session() as session:
        yield session
