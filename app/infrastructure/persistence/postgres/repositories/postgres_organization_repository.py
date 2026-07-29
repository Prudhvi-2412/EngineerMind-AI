from typing import Optional
import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.domain.entities.organization import Organization
from app.domain.repositories.organization_repository import AbstractOrganizationRepository
from app.infrastructure.persistence.postgres.models.organization_model import OrganizationModel
from app.infrastructure.persistence.postgres.mappers.auth_mappers import org_model_to_entity, org_entity_to_model


class PostgresOrganizationRepository(AbstractOrganizationRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, org: Organization) -> Organization:
        model = org_entity_to_model(org)
        self.session.add(model)
        await self.session.flush()
        return org_model_to_entity(model)

    async def get_by_id(self, org_id: uuid.UUID) -> Optional[Organization]:
        stmt = select(OrganizationModel).where(OrganizationModel.id == org_id)
        result = await self.session.execute(stmt)
        model = result.scalar_one_or_none()
        return org_model_to_entity(model) if model else None

    async def get_by_slug(self, slug: str) -> Optional[Organization]:
        stmt = select(OrganizationModel).where(OrganizationModel.slug == slug.lower().strip())
        result = await self.session.execute(stmt)
        model = result.scalar_one_or_none()
        return org_model_to_entity(model) if model else None

    async def update(self, org: Organization) -> Organization:
        stmt = select(OrganizationModel).where(OrganizationModel.id == org.id)
        result = await self.session.execute(stmt)
        model = result.scalar_one_or_none()
        if not model:
            raise ValueError(f"Organization with ID {org.id} not found")
        
        model.name = org.name
        model.plan_tier = org.plan_tier
        model.updated_at = org.updated_at
        
        await self.session.flush()
        return org_model_to_entity(model)
