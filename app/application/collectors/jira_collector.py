from datetime import datetime, timezone
from typing import Dict, Any
import uuid
from app.domain.entities.telemetry_event import NormalizedEvent


class JiraCollector:
    @staticmethod
    def normalize(payload: Dict[str, Any], delivery_id: str) -> NormalizedEvent:
        event_type = payload.get("webhookEvent", "jira:issue_updated")
        issue_data = payload.get("issue", {})
        fields = issue_data.get("fields", {})

        action = event_type.replace("jira:", "")
        timestamp_str = payload.get("timestamp")
        timestamp = datetime.fromtimestamp(timestamp_str / 1000.0, tz=timezone.utc) if timestamp_str else datetime.now(timezone.utc)

        normalized = {
            "issue_key": issue_data.get("key"),
            "summary": fields.get("summary"),
            "status": fields.get("status", {}).get("name"),
            "priority": fields.get("priority", {}).get("name"),
            "assignee_email": fields.get("assignee", {}).get("emailAddress") if fields.get("assignee") else None,
            "reporter_email": fields.get("reporter", {}).get("emailAddress") if fields.get("reporter") else None,
            "project_key": fields.get("project", {}).get("key"),
        }

        return NormalizedEvent.create(
            event_id=delivery_id or f"jira-{issue_data.get('key')}-{int(timestamp.timestamp())}",
            source="jira",
            event_category="issue",
            event_action=f"issue.{action}",
            raw_payload=payload,
            normalized_payload=normalized,
            timestamp=timestamp
        )
