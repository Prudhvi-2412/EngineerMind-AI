from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Optional
import uuid


@dataclass
class Organization:
    id: uuid.UUID
    name: str
    slug: str
    plan_tier: str = "enterprise"
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    @classmethod
    def create(cls, name: str, slug: str, plan_tier: str = "enterprise") -> "Organization":
        now = datetime.now(timezone.utc)
        return cls(
            id=uuid.uuid4(),
            name=name,
            slug=slug.lower().strip(),
            plan_tier=plan_tier,
            created_at=now,
            updated_at=now
        )
