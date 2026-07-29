from typing import Optional, Protocol, List
import uuid
from app.domain.entities.user import User


class AbstractUserRepository(Protocol):
    async def create(self, user: User) -> User:
        ...

    async def get_by_id(self, user_id: uuid.UUID) -> Optional[User]:
        ...

    async def get_by_email(self, org_id: uuid.UUID, email: str) -> Optional[User]:
        ...

    async def get_by_email_global(self, email: str) -> Optional[User]:
        ...

    async def get_by_oauth_id(self, provider: str, oauth_id: str) -> Optional[User]:
        ...

    async def update(self, user: User) -> User:
        ...

    async def list_by_org(self, org_id: uuid.UUID, skip: int = 0, limit: int = 100) -> List[User]:
        ...
