from datetime import datetime, timezone
from typing import Dict, Any
from app.domain.entities.telemetry_event import NormalizedEvent


class SlackCollector:
    @staticmethod
    def normalize(payload: Dict[str, Any], delivery_id: str) -> NormalizedEvent:
        event = payload.get("event", {})
        event_type = event.get("type", "message")

        timestamp_str = event.get("ts")
        timestamp = datetime.fromtimestamp(float(timestamp_str), tz=timezone.utc) if timestamp_str else datetime.now(timezone.utc)

        normalized = {
            "channel_id": event.get("channel"),
            "user_id": event.get("user"),
            "text": event.get("text"),
            "thread_ts": event.get("thread_ts"),
            "team_id": payload.get("team_id"),
        }

        return NormalizedEvent.create(
            event_id=delivery_id or f"slack-{event.get('client_msg_id') or event.get('ts')}",
            source="slack",
            event_category="communication",
            event_action=f"chat.{event_type}",
            raw_payload=payload,
            normalized_payload=normalized,
            timestamp=timestamp
        )
