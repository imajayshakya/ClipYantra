"""ClipYantra Health Check Endpoints."""

from dataclasses import dataclass
from typing import Any, Dict, Literal, Optional
from fastapi import APIRouter, Depends, Response
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.db.session import get_db
from app.schemas.common import HealthResponse

router = APIRouter()

# Database probe will be injected via app state
_db_probe: Optional[Any] = None


def set_database_probe(probe: Optional[Any]) -> None:
    """Set the database probe for health checks."""
    global _db_probe
    _db_probe = probe


@dataclass
class ComponentStatus:
    status: str
    detail: Optional[str] = None


@router.get(
    "/live",
    response_model=HealthResponse,
    summary="Liveness check",
    description="Check if the service is alive",
)
async def liveness_check() -> HealthResponse:
    """Liveness check for Kubernetes."""
    return HealthResponse(
        status="alive",
        service=settings.PROJECT_NAME,
        version=settings.VERSION,
    )


@router.get(
    "/ready",
    response_model=Dict[str, Any],
    summary="Readiness check",
    description="Check if the service is ready to accept traffic",
)
async def readiness_check(
    response: Response,
    db: Optional[AsyncSession] = Depends(get_db),
) -> Dict[str, Any]:
    """Readiness check for Kubernetes/load balancers with component status."""
    
    # Check database
    db_status = "not_configured"
    db_detail = None
    
    if _db_probe is not None:
        result = _db_probe.check()
        db_status = result.status
        db_detail = result.detail
    elif db is not None:
        # Fallback to checking database directly
        try:
            await db.execute(text("SELECT 1"))
            db_status = "ready"
        except Exception:
            db_status = "unavailable"
            db_detail = "database_unreachable"
    
    components = {
        "database": {"status": db_status, **({"detail": db_detail} if db_detail else {})},
        "redis": {"status": "not_configured"},
        "object_storage": {"status": "not_configured"},
        "worker": {"status": "not_configured"},
    }
    
    # Determine overall status
    overall_status = "ready"
    status_code = 200
    if db_status != "ready":
        overall_status = "degraded"
        status_code = 503
    
    response.status_code = status_code
    return {
        "status": overall_status,
        "service": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "components": components,
    }


@router.get(
    "",
    response_model=HealthResponse,
    summary="Health check",
    description="Check the health status of the API and its dependencies",
)
async def health_check(
    db: AsyncSession = Depends(get_db),
) -> HealthResponse:
    """Basic health check endpoint."""
    try:
        await db.execute(text("SELECT 1"))
        db_status = "healthy"
    except Exception:
        db_status = "unhealthy"

    return HealthResponse(
        status="healthy" if db_status == "healthy" else "degraded",
        service=settings.PROJECT_NAME,
        version=settings.VERSION,
    )