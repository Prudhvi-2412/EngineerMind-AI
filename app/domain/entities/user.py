from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Optional
import uuid
from app.domain.entities.rbac import Role


@dataclass
class User:
    id: uuid.UUID
    org_id: uuid.UUID
    email: str
    name: str
    role: Role = Role.ENGINEER
    hashed_password: Optional[str] = None
    avatar_url: Optional[str] = None
    is_active: bool = True
    is_verified: bool = False
    github_id: Optional[str] = None
    google_id: Optional[str] = None
    microsoft_id: Optional[str] = None
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    @classmethod
    def create(
        cls,
        org_id: uuid.UUID,
        email: str,
        name: str,
        role: Role = Role.ENGINEER,
        hashed_password: Optional[str] = None,
        avatar_url: Optional[str] = None,
        github_id: Optional[str] = None,
        google_id: Optional[str] = None,
        microsoft_id: Optional[str] = None,
    ) -> "User":
        now = datetime.now(timezone.utc)
        return cls(
            id=uuid.uuid4(),
            org_id=org_id,
            email=email.lower().strip(),
            name=name.strip(),
            role=role,
            hashed_password=hashed_password,
            avatar_url=avatar_url,
            is_active=True,
            is_verified=True if (github_id or google_id or microsoft_id) else False,
            github_id=github_id,
            google_id=google_id,
            microsoft_id=microsoft_id,
            created_at=now,
            updated_at=now,
        )
