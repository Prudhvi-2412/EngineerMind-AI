from typing import Dict, Any
import httpx
from app.core.config import settings


class MicrosoftOAuthClient:
    def __init__(self):
        self.client_id = settings.MICROSOFT_CLIENT_ID
        self.client_secret = settings.MICROSOFT_CLIENT_SECRET
        self.tenant_id = settings.MICROSOFT_TENANT_ID
        self.redirect_uri = settings.MICROSOFT_REDIRECT_URI

    def get_login_url(self, state: str) -> str:
        return (
            f"https://login.microsoftonline.com/{self.tenant_id}/oauth2/v2.0/authorize?"
            f"client_id={self.client_id}&response_type=code&redirect_uri={self.redirect_uri}"
            f"&response_mode=query&scope=openid%20email%20profile%20User.Read&state={state}"
        )

    async def get_user_info(self, code: str) -> Dict[str, Any]:
        async with httpx.AsyncClient() as client:
            token_res = await client.post(
                f"https://login.microsoftonline.com/{self.tenant_id}/oauth2/v2.0/token",
                data={
                    "client_id": self.client_id,
                    "client_secret": self.client_secret,
                    "code": code,
                    "grant_type": "authorization_code",
                    "redirect_uri": self.redirect_uri
                }
            )
            token_data = token_res.json()
            access_token = token_data.get("access_token")
            if not access_token:
                raise ValueError("Failed to obtain access token from Microsoft")

            user_res = await client.get(
                "https://graph.microsoft.com/v1.0/me",
                headers={"Authorization": f"Bearer {access_token}"}
            )
            user_data = user_res.json()

            return {
                "id": str(user_data.get("id")),
                "email": user_data.get("userPrincipalName") or user_data.get("mail"),
                "name": user_data.get("displayName"),
                "avatar_url": None,
                "provider": "microsoft"
            }
