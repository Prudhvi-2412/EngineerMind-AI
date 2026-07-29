from typing import Dict, Any
from fastapi import APIRouter, Request, Header, Depends, Response, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.dependencies.database_deps import get_db
from app.application.services.collector_service import EventCollectorService
from app.infrastructure.monitoring.collector_metrics import get_prometheus_metrics_payload, CONTENT_TYPE_LATEST

router = APIRouter(tags=["Multi-Source Event Collector & Observability Metrics"])


@router.post("/collect/jira", status_code=status.HTTP_202_ACCEPTED)
async def collect_jira_event(
    request: Request,
    x_atlassian_webhook_identifier: str = Header(None, alias="X-Atlassian-Webhook-Identifier"),
    session: AsyncSession = Depends(get_db)
):
    """
    Ingest Jira issue webhooks (jira:issue_created, jira:issue_updated, jira:issue_deleted).
    """
    payload = await request.json()
    delivery_id = x_atlassian_webhook_identifier or f"jira-evt-{hash(str(payload))}"
    service = EventCollectorService(session)
    return await service.ingest_event("jira", payload, delivery_id)


@router.post("/collect/slack", status_code=status.HTTP_202_ACCEPTED)
async def collect_slack_event(
    request: Request,
    x_slack_request_timestamp: str = Header(None, alias="X-Slack-Request-Timestamp"),
    session: AsyncSession = Depends(get_db)
):
    """
    Ingest Slack Event Subscriptions webhooks (chat.message, app_mention).
    Handles URL verification challenges automatically.
    """
    payload = await request.json()
    if payload.get("type") == "url_verification":
        return {"challenge": payload.get("challenge")}

    event = payload.get("event", {})
    delivery_id = event.get("client_msg_id") or f"slack-evt-{event.get('ts')}"
    service = EventCollectorService(session)
    return await service.ingest_event("slack", payload, delivery_id)


@router.post("/collect/prometheus", status_code=status.HTTP_202_ACCEPTED)
async def collect_prometheus_alert(
    request: Request,
    session: AsyncSession = Depends(get_db)
):
    """
    Ingest Prometheus Alertmanager webhooks (firing & resolved operational alerts).
    """
    payload = await request.json()
    delivery_id = f"prom-alert-{hash(str(payload))}"
    service = EventCollectorService(session)
    return await service.ingest_event("prometheus", payload, delivery_id)


@router.post("/collect/grafana", status_code=status.HTTP_202_ACCEPTED)
async def collect_grafana_alert(
    request: Request,
    session: AsyncSession = Depends(get_db)
):
    """
    Ingest Grafana Webhook alert notifications.
    """
    payload = await request.json()
    delivery_id = f"grafana-alert-{payload.get('ruleId')}-{hash(str(payload))}"
    service = EventCollectorService(session)
    return await service.ingest_event("grafana", payload, delivery_id)


@router.get("/metrics", include_in_schema=False)
async def get_metrics():
    """
    Exposes Prometheus scrape metrics endpoint.
    """
    payload = get_prometheus_metrics_payload()
    return Response(content=payload, media_type=CONTENT_TYPE_LATEST)
