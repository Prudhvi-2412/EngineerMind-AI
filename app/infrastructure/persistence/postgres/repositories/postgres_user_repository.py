from typing import Optional, List
import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.domain.entities.user import User
from app.domain.repositories.user_repository import AbstractUserRepository
from app.infrastructure.persistence.postgres.models.user_model import UserModel
from app.infrastructure.persistence.postgres.mappers.auth_mappers import user_model_to_entity, user_entity_to_model


class PostgresUserRepository(AbstractUserRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, user: User) -> User:
        model = user_entity_to_model(user)
        self.session.add(model)
        await self.session.flush()
        return user_model_to_entity(model)

    async def get_by_id(self, user_id: uuid.UUID) -> Optional[User]:
        stmt = select(UserModel).where(UserModel.id == user_id)
        result = await self.session.execute(stmt)
        model = result.scalar_one_or_none()
        return user_model_to_entity(model) if model else None

    async def get_by_email(self, org_id: uuid.UUID, email: str) -> Optional[User]:
        stmt = select(UserModel).where(UserModel.org_id == org_id, UserModel.email == email.lower().strip())
        result = await self.session.execute(stmt)
        model = result.scalar_one_or_none()
        return user_model_to_entity(model) if model else None

    async def get_by_email_global(self, email: str) -> Optional[User]:
        stmt = select(UserModel).where(UserModel.email == email.lower().strip())
        result = await self.session.execute(stmt)
        model = result.scalar_one_or_none()
        return user_model_to_entity(model) if model else None

    async def get_by_oauth_id(self, provider: str, oauth_id: str) -> Optional[User]:
        if provider == "github":
            stmt = select(UserModel).where(UserModel.github_id == oauth_id)
        elif provider == "google":
            stmt = select(UserModel).where(UserModel.google_id == oauth_id)
        elif provider == "microsoft":
            stmt = select(UserModel).where(UserModel.microsoft_id == oauth_id)
        else:
            return None
        
        result = await self.session.execute(stmt)
        model = result.scalar_one_or_none()
        return user_model_to_entity(model) if model else None

    async def update(self, user: User) -> User:
        stmt = select(UserModel).where(UserModel.id == user.id)
        result = await self.session.execute(stmt)
        model = result.scalar_one_or_none()
        if not model:
            raise ValueError(f"User with ID {user.id} not found")
        
        model.name = user.name
        model.role = user.role.value
        model.hashed_password = user.hashed_password
        model.avatar_url = user.avatar_url
        model.is_active = user.is_active
        model.is_verified = user.is_verified
        model.github_id = user.github_id
        model.google_id = user.google_id
        model.microsoft_id = user.microsoft_id
        model.updated_at = user.updated_at
        
        await self.session.flush()
        return user_model_to_entity(model)

    async def list_by_org(self, org_id: uuid.UUID, skip: int = 0, limit: int = 100) -> List[User]:
        stmt = select(UserModel).where(UserModel.org_id == org_id).offset(skip).limit(limit)
        result = await self.session.execute(stmt)
        models = result.scalars().all()
        return [user_model_to_entity(m) for m in models]
