from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Optional, Dict, Any
import uuid


@dataclass
class EngineeringEvent:
    id: uuid.UUID
    event_id: str  # X-GitHub-Delivery
    event_type: str
    source: str
    payload: Dict[str, Any]
    status: str = "RECEIVED"
    org_id: Optional[uuid.UUID] = None
    repo_id: Optional[uuid.UUID] = None
    retry_count: int = 0
    error_message: Optional[str] = None
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    processed_at: Optional[datetime] = None

    @classmethod
    def create(
        cls,
        event_id: str,
        event_type: str,
        payload: Dict[str, Any],
        source: str = "github",
        org_id: Optional[uuid.UUID] = None,
        repo_id: Optional[uuid.UUID] = None,
    ) -> "EngineeringEvent":
        return cls(
            id=uuid.uuid4(),
            event_id=event_id,
            event_type=event_type,
            source=source,
            payload=payload,
            status="RECEIVED",
            org_id=org_id,
            repo_id=repo_id,
            created_at=datetime.now(timezone.utc)
        )
