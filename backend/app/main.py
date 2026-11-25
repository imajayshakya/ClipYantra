"""ClipYantra FastAPI Application Factory."""

from contextlib import asynccontextmanager
from typing import Optional
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.core.config import Settings, get_settings
from app.core.logging import setup_logging
from app.core.exceptions import (
    ClipYantraException,
    clipyantra_exception_handler,
    validation_exception_handler,
    pydantic_validation_exception_handler,
)
from app.api.v1.api import api_router
from app.api.sources import create_sources_router
from app.db.session import init_db, close_db
from app.api.v1.endpoints.health import router as health_router, set_database_probe


def create_app(
    settings: Optional[Settings] = None,
    database_probe: Optional[object] = None,
    source_store: Optional[object] = None,
) -> FastAPI:
    """Create and configure the FastAPI application."""
    if settings is None:
        settings = get_settings()

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        """Application lifespan manager."""
        # Startup
        setup_logging()
        await init_db()
        yield
        # Shutdown
        await close_db()

    app = FastAPI(
        title=settings.PROJECT_NAME,
        version=settings.VERSION,
        description=settings.DESCRIPTION,
        openapi_url=f"{settings.API_V1_STR}/openapi.json",
        docs_url=f"{settings.API_V1_STR}/docs",
        redoc_url=f"{settings.API_V1_STR}/redoc",
        lifespan=lifespan,
    )

    # CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Exception handlers
    app.add_exception_handler(ClipYantraException, clipyantra_exception_handler)
    app.add_exception_handler(ValueError, validation_exception_handler)
    from fastapi.exceptions import RequestValidationError
    app.add_exception_handler(RequestValidationError, validation_exception_handler)
    from pydantic import ValidationError as PydanticValidationError
    app.add_exception_handler(PydanticValidationError, pydantic_validation_exception_handler)

    # Include API router
    app.include_router(api_router, prefix=settings.API_V1_STR)

    # Include health router directly at /health for liveness/readiness
    app.include_router(health_router, prefix="/health", tags=["health"])

    # Include sources router with source_store (source_store can be None for 503 testing)
    app.include_router(create_sources_router(source_store))

    # Set database probe for health endpoints
    if database_probe is not None:
        set_database_probe(database_probe)

    # Health check endpoint (outside API prefix for load balancers)
    @app.get("/health", tags=["health"])
    async def health_check() -> JSONResponse:
        return JSONResponse(
            content={"status": "healthy", "service": settings.PROJECT_NAME},
            status_code=200,
        )

    return app


app = create_app()
