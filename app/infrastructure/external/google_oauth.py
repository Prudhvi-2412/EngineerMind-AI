from typing import Dict, Any
import httpx
from app.core.config import settings


class GoogleOAuthClient:
    def __init__(self):
        self.client_id = settings.GOOGLE_CLIENT_ID
        self.client_secret = settings.GOOGLE_CLIENT_SECRET
        self.redirect_uri = settings.GOOGLE_REDIRECT_URI

    def get_login_url(self, state: str) -> str:
        return (
            f"https://accounts.google.com/o/oauth2/v2/auth?"
            f"client_id={self.client_id}&redirect_uri={self.redirect_uri}&response_type=code"
            f"&scope=openid%20email%20profile&state={state}"
        )

    async def get_user_info(self, code: str) -> Dict[str, Any]:
        async with httpx.AsyncClient() as client:
            token_res = await client.post(
                "https://oauth2.googleapis.com/token",
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
                raise ValueError("Failed to obtain access token from Google")

            user_res = await client.get(
                "https://www.googleapis.com/oauth2/v2/userinfo",
                headers={"Authorization": f"Bearer {access_token}"}
            )
            user_data = user_res.json()

            return {
                "id": str(user_data.get("id")),
                "email": user_data.get("email"),
                "name": user_data.get("name"),
                "avatar_url": user_data.get("picture"),
                "provider": "google"
            }
