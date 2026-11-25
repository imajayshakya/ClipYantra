"""ClipYantra Test Configuration and Fixtures."""

import asyncio
import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.pool import StaticPool

from app.db.base import Base
from app.db.session import db_manager
from app.main import app


# Test database URL (in-memory SQLite for fast tests)
TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"


@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="function")
async def test_engine():
    """Create a test database engine."""
    engine = create_async_engine(
        TEST_DATABASE_URL,
        echo=False,
        poolclass=StaticPool,
        connect_args={"check_same_thread": False},
    )

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield engine

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

    await engine.dispose()


@pytest_asyncio.fixture(scope="function")
async def db_session(test_engine) -> AsyncSession:
    """Create a test database session."""
    async_session = async_sessionmaker(
        bind=test_engine,
        class_=AsyncSession,
        expire_on_commit=False,
        autoflush=False,
        autocommit=False,
    )

    async with async_session() as session:
        yield session


@pytest_asyncio.fixture(scope="function")
async def async_client(db_session: AsyncSession) -> AsyncClient:
    """Create an async HTTP client for testing."""

    # Override the database dependency
    async def override_get_db():
        yield db_session

    app.dependency_overrides[db_manager.session] = override_get_db

    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
    ) as client:
        yield client

    app.dependency_overrides.clear()


@pytest.fixture
def sample_source_data():
    """Sample source data for testing."""
    return {
        "name": "Test Source",
        "url": "https://example.com/video.mp4",
        "description": "A test video source",
    }


@pytest.fixture
def sample_media_asset_data():
    """Sample media asset data for testing."""
    return {
        "filename": "test_video.mp4",
        "content_type": "video/mp4",
        "size_bytes": 1024 * 1024 * 10,  # 10MB
        "duration_seconds": 120.5,
        "width": 1920,
        "height": 1080,
        "codec": "h264",
        "bitrate": 5000000,
    }
