"""Liveness and readiness health contracts."""

from typing import Literal

from fastapi import APIRouter
from fastapi.responses import JSONResponse

from app.core.config import Settings
from app.db.database import DatabaseCheckResult, DatabaseProbe


ComponentStatus = Literal[
    "ready",
    "unavailable",
    "not_configured",
]


def get_health_status(
    settings: Settings,
    database_probe: DatabaseProbe | None,
) -> dict:
    if settings.database_url is None:
        database = DatabaseCheckResult(status="not_configured")
    elif database_probe is None:
        database = DatabaseCheckResult(status="not_configured")
    else:
        database = database_probe.check()

    overall_status = "ready" if database.status == "ready" else "degraded"
    database_component = {"status": database.status}
    if database.detail:
        database_component["detail"] = database.detail

    return {
        "status": overall_status,
        "components": {
            "database": database_component,
            "redis": {"status": "not_configured"},
            "object_storage": {"status": "not_configured"},
            "worker": {"status": "not_configured"},
        },
    }


def create_health_router(
    settings: Settings,
    database_probe: DatabaseProbe | None,
) -> APIRouter:
    router = APIRouter(prefix="/health", tags=["health"])

    @router.get("/live")
    def liveness() -> dict:
        return {
            "status": "alive",
            "app": settings.app_name,
            "environment": settings.app_env,
        }

    @router.get("/ready")
    def readiness() -> dict:
        payload = get_health_status(settings, database_probe)
        status_code = 200 if payload["status"] == "ready" else 503
        return JSONResponse(status_code=status_code, content=payload)

    return router
