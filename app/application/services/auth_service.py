from datetime import datetime, timezone, timedelta
import hashlib
from typing import Dict, Any, Tuple
import uuid
from app.core.config import settings
from app.core.security import verify_password, get_password_hash, create_access_token, create_refresh_token, decode_token
from app.domain.entities.user import User
from app.domain.entities.organization import Organization
from app.domain.entities.token import RefreshToken
from app.domain.entities.rbac import Role
from app.domain.repositories.user_repository import AbstractUserRepository
from app.domain.repositories.organization_repository import AbstractOrganizationRepository
from app.domain.repositories.token_repository import AbstractRefreshTokenRepository
from app.domain.exceptions.auth_exceptions import (
    InvalidCredentialsException,
    UserAlreadyExistsException,
    OrganizationAlreadyExistsException,
    InvalidTokenException,
    TokenRevokedException
)


class AuthService:
    def __init__(
        self,
        user_repo: AbstractUserRepository,
        org_repo: AbstractOrganizationRepository,
        token_repo: AbstractRefreshTokenRepository
    ):
        self.user_repo = user_repo
        self.org_repo = org_repo
        self.token_repo = token_repo

    async def register_organization_and_admin(
        self,
        org_name: str,
        org_slug: str,
        admin_email: str,
        admin_name: str,
        password: str
    ) -> Tuple[Organization, User, Dict[str, str]]:
        existing_org = await self.org_repo.get_by_slug(org_slug)
        if existing_org:
            raise OrganizationAlreadyExistsException()

        org = Organization.create(name=org_name, slug=org_slug)
        saved_org = await self.org_repo.create(org)

        existing_user = await self.user_repo.get_by_email(saved_org.id, admin_email)
        if existing_user:
            raise UserAlreadyExistsException()

        hashed_password = get_password_hash(password)
        user = User.create(
            org_id=saved_org.id,
            email=admin_email,
            name=admin_name,
            role=Role.ADMIN,
            hashed_password=hashed_password
        )
        saved_user = await self.user_repo.create(user)

        tokens = await self._generate_tokens_and_save_refresh(saved_user)
        return saved_org, saved_user, tokens

    async def login_with_password(
        self,
        org_slug: str,
        email: str,
        password: str
    ) -> Tuple[User, Dict[str, str]]:
        org = await self.org_repo.get_by_slug(org_slug)
        if not org:
            raise InvalidCredentialsException("Invalid organization or credentials")

        user = await self.user_repo.get_by_email(org.id, email)
        if not user or not user.hashed_password:
            raise InvalidCredentialsException()

        if not verify_password(password, user.hashed_password):
            raise InvalidCredentialsException()

        if not user.is_active:
            raise InvalidCredentialsException("Account is deactivated")

        tokens = await self._generate_tokens_and_save_refresh(user)
        return user, tokens

    async def refresh_access_token(self, refresh_token_str: str) -> Dict[str, str]:
        try:
            payload = decode_token(refresh_token_str, is_refresh=True)
        except ValueError:
            raise InvalidTokenException("Invalid refresh token signature or expired")

        if payload.get("type") != "refresh":
            raise InvalidTokenException("Token is not a refresh token")

        user_id_str = payload.get("sub")
        family_id_str = payload.get("family")
        if not user_id_str or not family_id_str:
            raise InvalidTokenException("Malformed token payload")

        user_id = uuid.UUID(user_id_str)
        family_id = uuid.UUID(family_id_str)

        token_hash = hashlib.sha256(refresh_token_str.encode()).hexdigest()
        token_record = await self.token_repo.get_by_hash(token_hash)

        # Token Reuse Detection (Security feature)
        if token_record and token_record.is_revoked:
            await self.token_repo.revoke_family(family_id)
            raise TokenRevokedException("Token reuse detected! Token family revoked for security.")

        if not token_record or token_record.expires_at < datetime.now(timezone.utc):
            raise InvalidTokenException("Refresh token expired or not found")

        # Revoke the used token (Token Rotation)
        await self.token_repo.revoke_by_hash(token_hash)

        user = await self.user_repo.get_by_id(user_id)
        if not user or not user.is_active:
            raise InvalidCredentialsException("User inactive or not found")

        # Issue new token pair with same family ID
        return await self._generate_tokens_and_save_refresh(user, family_id=family_id)

    async def revoke_refresh_token(self, refresh_token_str: str) -> None:
        token_hash = hashlib.sha256(refresh_token_str.encode()).hexdigest()
        await self.token_repo.revoke_by_hash(token_hash)

    async def _generate_tokens_and_save_refresh(
        self,
        user: User,
        family_id: uuid.UUID | None = None
    ) -> Dict[str, str]:
        access_token = create_access_token(
            subject=user.id,
            org_id=user.org_id,
            role=user.role.value
        )

        current_family = family_id or uuid.uuid4()
        refresh_token = create_refresh_token(
            subject=user.id,
            token_family_id=current_family
        )

        token_hash = hashlib.sha256(refresh_token.encode()).hexdigest()
        expires_at = datetime.now(timezone.utc) + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)

        refresh_entity = RefreshToken.create(
            user_id=user.id,
            token_hash=token_hash,
            expires_at=expires_at,
            family_id=current_family
        )
        await self.token_repo.create(refresh_entity)

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer"
        }
