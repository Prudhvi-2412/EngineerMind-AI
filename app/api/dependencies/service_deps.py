from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.dependencies.database_deps import get_db
from app.infrastructure.persistence.postgres.repositories.postgres_user_repository import PostgresUserRepository
from app.infrastructure.persistence.postgres.repositories.postgres_organization_repository import PostgresOrganizationRepository
from app.infrastructure.persistence.postgres.repositories.postgres_token_repository import PostgresRefreshTokenRepository
from app.application.services.auth_service import AuthService
from app.application.services.oauth_service import OAuthService


def get_user_repo(session: AsyncSession = Depends(get_db)) -> PostgresUserRepository:
    return PostgresUserRepository(session)


def get_org_repo(session: AsyncSession = Depends(get_db)) -> PostgresOrganizationRepository:
    return PostgresOrganizationRepository(session)


def get_token_repo(session: AsyncSession = Depends(get_db)) -> PostgresRefreshTokenRepository:
    return PostgresRefreshTokenRepository(session)


def get_auth_service(
    user_repo: PostgresUserRepository = Depends(get_user_repo),
    org_repo: PostgresOrganizationRepository = Depends(get_org_repo),
    token_repo: PostgresRefreshTokenRepository = Depends(get_token_repo)
) -> AuthService:
    return AuthService(user_repo=user_repo, org_repo=org_repo, token_repo=token_repo)


def get_oauth_service(
    user_repo: PostgresUserRepository = Depends(get_user_repo),
    org_repo: PostgresOrganizationRepository = Depends(get_org_repo),
    auth_service: AuthService = Depends(get_auth_service)
) -> OAuthService:
    return OAuthService(user_repo=user_repo, org_repo=org_repo, auth_service=auth_service)
