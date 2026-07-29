import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from app.infrastructure.persistence.postgres.repositories.postgres_user_repository import PostgresUserRepository
from app.infrastructure.persistence.postgres.repositories.postgres_organization_repository import PostgresOrganizationRepository
from app.infrastructure.persistence.postgres.repositories.postgres_token_repository import PostgresRefreshTokenRepository
from app.application.services.auth_service import AuthService
from app.domain.exceptions.auth_exceptions import InvalidCredentialsException, OrganizationAlreadyExistsException


@pytest.mark.asyncio
async def test_register_organization_and_login_flow(db_session: AsyncSession):
    user_repo = PostgresUserRepository(db_session)
    org_repo = PostgresOrganizationRepository(db_session)
    token_repo = PostgresRefreshTokenRepository(db_session)

    auth_service = AuthService(user_repo=user_repo, org_repo=org_repo, token_repo=token_repo)

    # 1. Register Organization & Admin
    org, user, tokens = await auth_service.register_organization_and_admin(
        org_name="TechCorp",
        org_slug="techcorp",
        admin_email="admin@techcorp.com",
        admin_name="Tech Admin",
        password="P@ssw0rd123!"
    )

    assert org.slug == "techcorp"
    assert user.email == "admin@techcorp.com"
    assert "access_token" in tokens
    assert "refresh_token" in tokens

    # 2. Login with valid credentials
    logged_in_user, login_tokens = await auth_service.login_with_password(
        org_slug="techcorp",
        email="admin@techcorp.com",
        password="P@ssw0rd123!"
    )
    assert logged_in_user.id == user.id
    assert "access_token" in login_tokens

    # 3. Login with invalid password
    with pytest.raises(InvalidCredentialsException):
        await auth_service.login_with_password(
            org_slug="techcorp",
            email="admin@techcorp.com",
            password="WrongPassword"
        )

    # 4. Duplicate Organization Registration
    with pytest.raises(OrganizationAlreadyExistsException):
        await auth_service.register_organization_and_admin(
            org_name="TechCorp Duplicate",
            org_slug="techcorp",
            admin_email="other@techcorp.com",
            admin_name="Other Admin",
            password="P@ssw0rd123!"
        )
