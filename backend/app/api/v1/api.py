"""ClipYantra API v1 Router Aggregator."""

from fastapi import APIRouter

from app.api.v1.endpoints import health
from app.api.sources import create_sources_router

api_router = APIRouter()

# Health check endpoints
api_router.include_router(health.router, prefix="/health", tags=["health"])

# Source management endpoints
# Note: source_store will be injected via create_app, so we don't include it here
# The actual sources router is created in create_app with the source_store

# Placeholder for future feature routers
# from app.api.v1.endpoints import ingestion, media, publishing
# api_router.include_router(ingestion.router, prefix="/ingestion", tags=["ingestion"])
# api_router.include_router(media.router, prefix="/media", tags=["media"])
# api_router.include_router(publishing.router, prefix="/publishing", tags=["publishing"])
