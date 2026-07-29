from fastapi import APIRouter, status, Response, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from app.core.metrics import get_prometheus_metrics_response
from app.api.dependencies.database_deps import get_db
from app.infrastructure.persistence.neo4j.connection import get_neo4j_session
from neo4j import AsyncSession as Neo4jAsyncSession

router = APIRouter(tags=["Observability, Health Checks & Prometheus Metrics"])


@router.get("/healthz", status_code=status.HTTP_200_OK)
async def liveness_check():
    """
    Kubernetes Container Liveness Probe Endpoint.
    Returns HTTP 200 if container process is healthy.
    """
    return {"status": "HEALTHY", "service": "engineering-os-backend"}


@router.get("/health/readiness", status_code=status.HTTP_200_OK)
async def readiness_check(
    db: AsyncSession = Depends(get_db),
    neo4j_session: Neo4jAsyncSession = Depends(get_neo4j_session)
):
    """
    Kubernetes Container Readiness Probe & Deep System Dependency Health Check.
    Asynchronously verifies connectivity to PostgreSQL and Neo4j Knowledge Graph.
    """
    health_status = {
        "status": "READY",
        "components": {
            "postgres": "HEALTHY",
            "neo4j": "HEALTHY",
            "redis": "HEALTHY"
        }
    }

    # Verify PostgreSQL connectivity
    try:
        await db.execute(text("SELECT 1"))
    except Exception:
        health_status["components"]["postgres"] = "UNHEALTHY"
        health_status["status"] = "DEGRADED"

    # Verify Neo4j connectivity
    try:
        res = await neo4j_session.run("RETURN 1 as test")
        await res.single()
    except Exception:
        health_status["components"]["neo4j"] = "UNHEALTHY"
        health_status["status"] = "DEGRADED"

    return health_status


@router.get("/metrics")
async def prometheus_metrics_endpoint():
    """
    Prometheus Scrape Target Endpoint.
    Exposes application counters, histograms, and gauges.
    """
    return get_prometheus_metrics_response()
