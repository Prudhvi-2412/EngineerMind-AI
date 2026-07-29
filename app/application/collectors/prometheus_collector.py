from datetime import datetime, timezone
from typing import Dict, Any
from app.domain.entities.telemetry_event import NormalizedEvent


class PrometheusCollector:
    @staticmethod
    def normalize(payload: Dict[str, Any], delivery_id: str) -> NormalizedEvent:
        status = payload.get("status", "firing")
        alerts = payload.get("alerts", [])

        normalized_alerts = []
        for alert in alerts:
            labels = alert.get("labels", {})
            annotations = alert.get("annotations", {})
            normalized_alerts.append({
                "alert_name": labels.get("alertname"),
                "severity": labels.get("severity", "warning"),
                "service_name": labels.get("service") or labels.get("job"),
                "summary": annotations.get("summary") or annotations.get("description"),
                "starts_at": alert.get("startsAt"),
                "ends_at": alert.get("endsAt"),
            })

        normalized = {
            "receiver": payload.get("receiver"),
            "status": status,
            "alerts": normalized_alerts,
            "external_url": payload.get("externalURL")
        }

        first_alert_name = normalized_alerts[0]["alert_name"] if normalized_alerts else "alert"

        return NormalizedEvent.create(
            event_id=delivery_id or f"prom-{int(datetime.now(timezone.utc).timestamp())}",
            source="prometheus",
            event_category="alert",
            event_action=f"alert.{status}",
            raw_payload=payload,
            normalized_payload=normalized
        )
