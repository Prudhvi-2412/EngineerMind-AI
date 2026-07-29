from typing import Dict, Any
import httpx
from app.core.config import settings


class GitHubOAuthClient:
    def __init__(self):
        self.client_id = settings.GITHUB_CLIENT_ID
        self.client_secret = settings.GITHUB_CLIENT_SECRET
        self.redirect_uri = settings.GITHUB_REDIRECT_URI

    def get_login_url(self, state: str) -> str:
        return (
            f"https://github.com/login/oauth/authorize?"
            f"client_id={self.client_id}&redirect_uri={self.redirect_uri}&scope=user:email&state={state}"
        )

    async def get_user_info(self, code: str) -> Dict[str, Any]:
        async with httpx.AsyncClient() as client:
            token_res = await client.post(
                "https://github.com/login/oauth/access_token",
                data={
                    "client_id": self.client_id,
                    "client_secret": self.client_secret,
                    "code": code,
                    "redirect_uri": self.redirect_uri
                },
                headers={"Accept": "application/json"}
            )
            token_data = token_res.json()
            access_token = token_data.get("access_token")
            if not access_token:
                raise ValueError("Failed to obtain access token from GitHub")

            user_res = await client.get(
                "https://api.github.com/user",
                headers={
                    "Authorization": f"Bearer {access_token}",
                    "Accept": "application/json"
                }
            )
            user_data = user_res.json()

            # Get primary email if user's email is private
            email = user_data.get("email")
            if not email:
                emails_res = await client.get(
                    "https://api.github.com/user/emails",
                    headers={"Authorization": f"Bearer {access_token}"}
                )
                emails = emails_res.json()
                for e in emails:
                    if e.get("primary"):
                        email = e.get("email")
                        break

            return {
                "id": str(user_data.get("id")),
                "email": email,
                "name": user_data.get("name") or user_data.get("login"),
                "avatar_url": user_data.get("avatar_url"),
                "provider": "github"
            }
