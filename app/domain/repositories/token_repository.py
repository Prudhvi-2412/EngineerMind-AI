from typing import Optional, Protocol
import uuid
from app.domain.entities.token import RefreshToken


class AbstractRefreshTokenRepository(Protocol):
    async def create(self, token: RefreshToken) -> RefreshToken:
        ...

    async def get_by_hash(self, token_hash: str) -> Optional[RefreshToken]:
        ...

    async def revoke_family(self, family_id: uuid.UUID) -> None:
        ...

    async def revoke_by_hash(self, token_hash: str) -> None:
        ...
