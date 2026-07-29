from typing import Dict, Any, Tuple
from app.domain.entities.user import User
from app.domain.entities.organization import Organization
from app.domain.entities.rbac import Role
from app.domain.repositories.user_repository import AbstractUserRepository
from app.domain.repositories.organization_repository import AbstractOrganizationRepository
from app.application.services.auth_service import AuthService
from app.infrastructure.external.github_oauth import GitHubOAuthClient
from app.infrastructure.external.google_oauth import GoogleOAuthClient
from app.infrastructure.external.microsoft_oauth import MicrosoftOAuthClient


class OAuthService:
    def __init__(
        self,
        user_repo: AbstractUserRepository,
        org_repo: AbstractOrganizationRepository,
        auth_service: AuthService
    ):
        self.user_repo = user_repo
        self.org_repo = org_repo
        self.auth_service = auth_service
        self.github_client = GitHubOAuthClient()
        self.google_client = GoogleOAuthClient()
        self.microsoft_client = MicrosoftOAuthClient()

    def get_oauth_login_url(self, provider: str, state: str) -> str:
        if provider == "github":
            return self.github_client.get_login_url(state)
        elif provider == "google":
            return self.google_client.get_login_url(state)
        elif provider == "microsoft":
            return self.microsoft_client.get_login_url(state)
        else:
            raise ValueError(f"Unsupported OAuth provider: {provider}")

    async def handle_oauth_callback(
        self,
        provider: str,
        code: str,
        org_slug: str | None = None
    ) -> Tuple[User, Dict[str, str]]:
        if provider == "github":
            info = await self.github_client.get_user_info(code)
        elif provider == "google":
            info = await self.google_client.get_user_info(code)
        elif provider == "microsoft":
            info = await self.microsoft_client.get_user_info(code)
        else:
            raise ValueError(f"Unsupported OAuth provider: {provider}")

        oauth_id = info["id"]
        email = info["email"]
        name = info["name"]
        avatar_url = info.get("avatar_url")

        # 1. Check if user exists by OAuth provider ID
        user = await self.user_repo.get_by_oauth_id(provider, oauth_id)
        if user:
            tokens = await self.auth_service._generate_tokens_and_save_refresh(user)
            return user, tokens

        # 2. Check if user exists globally by Email
        user = await self.user_repo.get_by_email_global(email)
        if user:
            # Link provider ID
            if provider == "github":
                user.github_id = oauth_id
            elif provider == "google":
                user.google_id = oauth_id
            elif provider == "microsoft":
                user.microsoft_id = oauth_id
            
            user.is_verified = True
            if avatar_url and not user.avatar_url:
                user.avatar_url = avatar_url

            updated_user = await self.user_repo.update(user)
            tokens = await self.auth_service._generate_tokens_and_save_refresh(updated_user)
            return updated_user, tokens

        # 3. Create new Organization & User if non-existent
        if org_slug:
            org = await self.org_repo.get_by_slug(org_slug)
            if not org:
                org = Organization.create(name=f"{name}'s Org", slug=org_slug)
                org = await self.org_repo.create(org)
        else:
            # Generate slug from email domain or user name
            derived_slug = f"org-{oauth_id[:8]}"
            org = Organization.create(name=f"{name}'s Workspace", slug=derived_slug)
            org = await self.org_repo.create(org)

        new_user = User.create(
            org_id=org.id,
            email=email,
            name=name,
            role=Role.ADMIN,
            avatar_url=avatar_url,
            github_id=oauth_id if provider == "github" else None,
            google_id=oauth_id if provider == "google" else None,
            microsoft_id=oauth_id if provider == "microsoft" else None
        )
        saved_user = await self.user_repo.create(new_user)
        tokens = await self.auth_service._generate_tokens_and_save_refresh(saved_user)
        return saved_user, tokens
