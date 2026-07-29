from app.domain.entities.organization import Organization
from app.domain.entities.user import User
from app.domain.entities.token import RefreshToken
from app.domain.entities.rbac import Role
from app.infrastructure.persistence.postgres.models.organization_model import OrganizationModel
from app.infrastructure.persistence.postgres.models.user_model import UserModel
from app.infrastructure.persistence.postgres.models.refresh_token_model import RefreshTokenModel


def org_model_to_entity(model: OrganizationModel) -> Organization:
    return Organization(
        id=model.id,
        name=model.name,
        slug=model.slug,
        plan_tier=model.plan_tier,
        created_at=model.created_at,
        updated_at=model.updated_at
    )


def org_entity_to_model(entity: Organization) -> OrganizationModel:
    return OrganizationModel(
        id=entity.id,
        name=entity.name,
        slug=entity.slug,
        plan_tier=entity.plan_tier,
        created_at=entity.created_at,
        updated_at=entity.updated_at
    )


def user_model_to_entity(model: UserModel) -> User:
    return User(
        id=model.id,
        org_id=model.org_id,
        email=model.email,
        name=model.name,
        role=Role(model.role),
        hashed_password=model.hashed_password,
        avatar_url=model.avatar_url,
        is_active=model.is_active,
        is_verified=model.is_verified,
        github_id=model.github_id,
        google_id=model.google_id,
        microsoft_id=model.microsoft_id,
        created_at=model.created_at,
        updated_at=model.updated_at
    )


def user_entity_to_model(entity: User) -> UserModel:
    return UserModel(
        id=entity.id,
        org_id=entity.org_id,
        email=entity.email,
        name=entity.name,
        role=entity.role.value,
        hashed_password=entity.hashed_password,
        avatar_url=entity.avatar_url,
        is_active=entity.is_active,
        is_verified=entity.is_verified,
        github_id=entity.github_id,
        google_id=entity.google_id,
        microsoft_id=entity.microsoft_id,
        created_at=entity.created_at,
        updated_at=entity.updated_at
    )


def token_model_to_entity(model: RefreshTokenModel) -> RefreshToken:
    return RefreshToken(
        id=model.id,
        user_id=model.user_id,
        token_hash=model.token_hash,
        family_id=model.family_id,
        is_revoked=model.is_revoked,
        expires_at=model.expires_at,
        created_at=model.created_at
    )


def token_entity_to_model(entity: RefreshToken) -> RefreshTokenModel:
    return RefreshTokenModel(
        id=entity.id,
        user_id=entity.user_id,
        token_hash=entity.token_hash,
        family_id=entity.family_id,
        is_revoked=entity.is_revoked,
        expires_at=entity.expires_at,
        created_at=entity.created_at
    )
