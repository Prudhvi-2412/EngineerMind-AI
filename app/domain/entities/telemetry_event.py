from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Optional, Dict, Any
import uuid


@dataclass
class NormalizedEvent:
    event_id: str
    source: str             # github, jira, slack, prometheus, grafana
    event_category: str     # code, issue, communication, metric, alert
    event_action: str       # e.g., issue.created, alert.firing
    timestamp: datetime
    raw_payload: Dict[str, Any]
    normalized_payload: Dict[str, Any]
    org_id: Optional[uuid.UUID] = None
    repo_id: Optional[uuid.UUID] = None

    @classmethod
    def create(
        cls,
        event_id: str,
        source: str,
        event_category: str,
        event_action: str,
        raw_payload: Dict[str, Any],
        normalized_payload: Dict[str, Any],
        timestamp: Optional[datetime] = None,
        org_id: Optional[uuid.UUID] = None,
        repo_id: Optional[uuid.UUID] = None,
    ) -> "NormalizedEvent":
        return cls(
            event_id=event_id,
            source=source,
            event_category=event_category,
            event_action=event_action,
            timestamp=timestamp or datetime.now(timezone.utc),
            raw_payload=raw_payload,
            normalized_payload=normalized_payload,
            org_id=org_id,
            repo_id=repo_id,
        )
