import time
from typing import Dict, Any, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from app.domain.entities.telemetry_event import NormalizedEvent
from app.domain.entities.engineering_event import EngineeringEvent
from app.application.collectors.jira_collector import JiraCollector
from app.application.collectors.slack_collector import SlackCollector
from app.application.collectors.prometheus_collector import PrometheusCollector
from app.application.collectors.grafana_collector import GrafanaCollector
from app.infrastructure.external.redis_dedup import is_duplicate_event
from app.infrastructure.persistence.postgres.repositories.postgres_event_repository import PostgresEventRepository
from app.infrastructure.monitoring.collector_metrics import EVENTS_COLLECTED_TOTAL, EVENT_PROCESSING_LATENCY
from app.tasks.github_sync_tasks import process_engineering_event_task


class EventCollectorService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.event_repo = PostgresEventRepository(session)

    async def ingest_event(
        self,
        source: str,
        payload: Dict[str, Any],
        delivery_id: str
    ) -> Dict[str, Any]:
        start_time = time.time()

        # 1. Deduplication check
        if await is_duplicate_event(delivery_id):
            return {"status": "duplicate_ignored", "delivery_id": delivery_id}

        # 2. Normalize payload based on telemetry source
        normalized_event: Optional[NormalizedEvent] = None

        if source == "jira":
            normalized_event = JiraCollector.normalize(payload, delivery_id)
        elif source == "slack":
            # Handle Slack URL verification challenge
            if payload.get("type") == "url_verification":
                return {"challenge": payload.get("challenge")}
            normalized_event = SlackCollector.normalize(payload, delivery_id)
        elif source == "prometheus":
            normalized_event = PrometheusCollector.normalize(payload, delivery_id)
        elif source == "grafana":
            normalized_event = GrafanaCollector.normalize(payload, delivery_id)
        else:
            raise ValueError(f"Unsupported collector telemetry source: '{source}'")

        # 3. Save event entity to PostgreSQL Event Store
        event_entity = EngineeringEvent.create(
            event_id=normalized_event.event_id,
            event_type=normalized_event.event_action,
            source=normalized_event.source,
            payload={
                "raw": normalized_event.raw_payload,
                "normalized": normalized_event.normalized_payload,
                "category": normalized_event.event_category
            }
        )
        event_model = await self.event_repo.create_event(event_entity)

        # 4. Dispatch async processing job to Celery Worker
        task = process_engineering_event_task.delay(str(event_model.id))

        # 5. Record Prometheus Metrics
        EVENTS_COLLECTED_TOTAL.labels(source=source, event_action=normalized_event.event_action).inc()
        EVENT_PROCESSING_LATENCY.labels(source=source).observe(time.time() - start_time)

        return {
            "status": "accepted",
            "source": source,
            "event_action": normalized_event.event_action,
            "event_db_id": str(event_model.id),
            "task_id": task.id
        }
