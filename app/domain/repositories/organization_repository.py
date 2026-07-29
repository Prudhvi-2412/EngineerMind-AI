from typing import Optional, Protocol
import uuid
from app.domain.entities.organization import Organization


class AbstractOrganizationRepository(Protocol):
    async def create(self, org: Organization) -> Organization:
        ...

    async def get_by_id(self, org_id: uuid.UUID) -> Optional[Organization]:
        ...

    async def get_by_slug(self, slug: str) -> Optional[Organization]:
        ...

    async def update(self, org: Organization) -> Organization:
        ...
