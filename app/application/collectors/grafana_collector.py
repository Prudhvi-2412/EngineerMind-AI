from datetime import datetime, timezone
from typing import Dict, Any
from app.domain.entities.telemetry_event import NormalizedEvent


class GrafanaCollector:
    @staticmethod
    def normalize(payload: Dict[str, Any], delivery_id: str) -> NormalizedEvent:
        state = payload.get("state", "alerting")
        title = payload.get("title", "Grafana Alert")

        eval_matches = payload.get("evalMatches", [])
        matches = [{"metric": m.get("metric"), "value": m.get("value")} for m in eval_matches]

        normalized = {
            "rule_name": payload.get("ruleName"),
            "rule_id": payload.get("ruleId"),
            "dashboard_id": payload.get("dashboardId"),
            "panel_id": payload.get("panelId"),
            "state": state,
            "message": payload.get("message"),
            "matches": matches,
        }

        return NormalizedEvent.create(
            event_id=delivery_id or f"grafana-{payload.get('ruleId')}-{int(datetime.now(timezone.utc).timestamp())}",
            source="grafana",
            event_category="alert",
            event_action=f"alert.{state}",
            raw_payload=payload,
            normalized_payload=normalized
        )
