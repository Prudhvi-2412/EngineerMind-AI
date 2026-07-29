from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from app.api.schemas.auth_schemas import TokenResponse
from app.application.services.oauth_service import OAuthService
from app.api.dependencies.service_deps import get_oauth_service

router = APIRouter(prefix="/auth/oauth", tags=["OAuth Authentication"])


@router.get("/{provider}/url")
async def get_oauth_login_url(
    provider: str,
    state: str = Query("default_state", description="State parameter for CSRF protection"),
    oauth_service: OAuthService = Depends(get_oauth_service)
):
    """
    Get the OAuth authorization redirect URL for GitHub, Google, or Microsoft.
    """
    try:
        url = oauth_service.get_oauth_login_url(provider.lower(), state)
        return {"provider": provider, "url": url}
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/{provider}/callback", response_model=TokenResponse)
async def oauth_callback(
    provider: str,
    code: str = Query(..., description="Authorization code returned by OAuth provider"),
    org_slug: Optional[str] = Query(None, description="Optional organization slug to associate with"),
    oauth_service: OAuthService = Depends(get_oauth_service)
):
    """
    Handle OAuth callback code exchange for GitHub, Google, or Microsoft. Returns JWT access & refresh tokens.
    """
    try:
        user, tokens = await oauth_service.handle_oauth_callback(
            provider=provider.lower(),
            code=code,
            org_slug=org_slug
        )
        return tokens
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"OAuth login failed: {str(e)}"
        )
