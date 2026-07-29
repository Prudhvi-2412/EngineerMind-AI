from dataclasses import dataclass, field
from datetime import datetime, timezone
import uuid


@dataclass
class RefreshToken:
    id: uuid.UUID
    user_id: uuid.UUID
    token_hash: str
    family_id: uuid.UUID
    is_revoked: bool = False
    expires_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    @classmethod
    def create(
        cls,
        user_id: uuid.UUID,
        token_hash: str,
        expires_at: datetime,
        family_id: uuid.UUID | None = None
    ) -> "RefreshToken":
        now = datetime.now(timezone.utc)
        return cls(
            id=uuid.uuid4(),
            user_id=user_id,
            token_hash=token_hash,
            family_id=family_id or uuid.uuid4(),
            is_revoked=False,
            expires_at=expires_at,
            created_at=now
        )
