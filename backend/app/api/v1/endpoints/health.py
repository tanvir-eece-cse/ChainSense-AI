"""
Health check endpoints.
"""

from datetime import datetime

from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
import redis.asyncio as redis

from app.core.config import settings
from app.core.database import get_db

router = APIRouter()


@router.get("/live")
async def liveness_check() -> dict:
    """Kubernetes liveness probe endpoint."""
    return {
        "status": "alive",
        "timestamp": datetime.utcnow().isoformat(),
    }


@router.get("/ready")
async def readiness_check(
    db: AsyncSession = Depends(get_db),
) -> dict:
    """Kubernetes readiness probe endpoint."""
    checks = {
        "database": False,
        "redis": False,
    }
    
    # Check database connection
    try:
        await db.execute(text("SELECT 1"))
        checks["database"] = True
    except Exception:
        pass
    
    # Check Redis connection
    try:
        redis_client = redis.from_url(settings.REDIS_URL)
        await redis_client.ping()
        checks["redis"] = True
        await redis_client.close()
    except Exception:
        pass
    
    all_healthy = all(checks.values())
    
    return {
        "status": "ready" if all_healthy else "degraded",
        "checks": checks,
        "timestamp": datetime.utcnow().isoformat(),
    }


@router.get("/detailed")
async def detailed_health_check(
    db: AsyncSession = Depends(get_db),
) -> dict:
    """Detailed health check with component status."""
    components = {}
    
    # Database
    try:
        start = datetime.utcnow()
        await db.execute(text("SELECT 1"))
        latency = (datetime.utcnow() - start).total_seconds() * 1000
        components["database"] = {
            "status": "healthy",
            "latency_ms": round(latency, 2),
        }
    except Exception as e:
        components["database"] = {
            "status": "unhealthy",
            "error": str(e),
        }
    
    # Redis
    try:
        redis_client = redis.from_url(settings.REDIS_URL)
        start = datetime.utcnow()
        await redis_client.ping()
        latency = (datetime.utcnow() - start).total_seconds() * 1000
        await redis_client.close()
        components["redis"] = {
            "status": "healthy",
            "latency_ms": round(latency, 2),
        }
    except Exception as e:
        components["redis"] = {
            "status": "unhealthy",
            "error": str(e),
        }
    
    # ML Service
    try:
        import httpx
        async with httpx.AsyncClient(timeout=5) as client:
            start = datetime.utcnow()
            response = await client.get(f"{settings.ML_SERVICE_URL}/health")
            latency = (datetime.utcnow() - start).total_seconds() * 1000
            if response.status_code == 200:
                components["ml_service"] = {
                    "status": "healthy",
                    "latency_ms": round(latency, 2),
                }
            else:
                components["ml_service"] = {
                    "status": "degraded",
                    "latency_ms": round(latency, 2),
                }
    except Exception as e:
        components["ml_service"] = {
            "status": "unavailable",
            "error": str(e),
        }
    
    # Overall status
    statuses = [c.get("status") for c in components.values()]
    if all(s == "healthy" for s in statuses):
        overall = "healthy"
    elif any(s == "unhealthy" for s in statuses):
        overall = "unhealthy"
    else:
        overall = "degraded"
    
    return {
        "status": overall,
        "version": settings.VERSION,
        "components": components,
        "timestamp": datetime.utcnow().isoformat(),
    }
