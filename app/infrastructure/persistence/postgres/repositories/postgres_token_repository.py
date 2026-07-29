from typing import Optional
import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from app.domain.entities.token import RefreshToken
from app.domain.repositories.token_repository import AbstractRefreshTokenRepository
from app.infrastructure.persistence.postgres.models.refresh_token_model import RefreshTokenModel
from app.infrastructure.persistence.postgres.mappers.auth_mappers import token_model_to_entity, token_entity_to_model


class PostgresRefreshTokenRepository(AbstractRefreshTokenRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, token: RefreshToken) -> RefreshToken:
        model = token_entity_to_model(token)
        self.session.add(model)
        await self.session.flush()
        return token_model_to_entity(model)

    async def get_by_hash(self, token_hash: str) -> Optional[RefreshToken]:
        stmt = select(RefreshTokenModel).where(RefreshTokenModel.token_hash == token_hash)
        result = await self.session.execute(stmt)
        model = result.scalar_one_or_none()
        return token_model_to_entity(model) if model else None

    async def revoke_family(self, family_id: uuid.UUID) -> None:
        stmt = (
            update(RefreshTokenModel)
            .where(RefreshTokenModel.family_id == family_id)
            .values(is_revoked=True)
        )
        await self.session.execute(stmt)
        await self.session.flush()

    async def revoke_by_hash(self, token_hash: str) -> None:
        stmt = (
            update(RefreshTokenModel)
            .where(RefreshTokenModel.token_hash == token_hash)
            .values(is_revoked=True)
        )
        await self.session.execute(stmt)
        await self.session.flush()
