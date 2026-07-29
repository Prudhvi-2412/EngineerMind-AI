from fastapi import APIRouter, Depends, HTTPException, status
from app.api.schemas.auth_schemas import (
    RegisterOrgRequest,
    LoginRequest,
    RefreshTokenRequest,
    TokenResponse
)
from app.api.schemas.user_schemas import UserResponse
from app.application.services.auth_service import AuthService
from app.domain.entities.user import User
from app.domain.exceptions.auth_exceptions import (
    UserAlreadyExistsException,
    OrganizationAlreadyExistsException,
    InvalidCredentialsException,
    InvalidTokenException,
    TokenRevokedException
)
from app.api.dependencies.service_deps import get_auth_service
from app.api.dependencies.auth_deps import get_current_user

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
async def register_organization(
    payload: RegisterOrgRequest,
    auth_service: AuthService = Depends(get_auth_service)
):
    """
    Register a new Organization along with its initial Admin User account.
    """
    try:
        org, user, tokens = await auth_service.register_organization_and_admin(
            org_name=payload.org_name,
            org_slug=payload.org_slug,
            admin_email=payload.admin_email,
            admin_name=payload.admin_name,
            password=payload.password
        )
        return tokens
    except (UserAlreadyExistsException, OrganizationAlreadyExistsException) as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post("/login", response_model=TokenResponse)
async def login(
    payload: LoginRequest,
    auth_service: AuthService = Depends(get_auth_service)
):
    """
    Authenticate user via org_slug, email, and password. Returns JWT Access and Refresh tokens.
    """
    try:
        user, tokens = await auth_service.login_with_password(
            org_slug=payload.org_slug,
            email=payload.email,
            password=payload.password
        )
        return tokens
    except InvalidCredentialsException as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))


@router.post("/refresh", response_model=TokenResponse)
async def refresh_tokens(
    payload: RefreshTokenRequest,
    auth_service: AuthService = Depends(get_auth_service)
):
    """
    Exchange a valid Refresh Token for a new Access and Refresh Token pair (Token Rotation).
    """
    try:
        tokens = await auth_service.refresh_access_token(payload.refresh_token)
        return tokens
    except (InvalidTokenException, InvalidCredentialsException) as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))
    except TokenRevokedException as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
async def logout(
    payload: RefreshTokenRequest,
    auth_service: AuthService = Depends(get_auth_service)
):
    """
    Revoke a refresh token on logout.
    """
    await auth_service.revoke_refresh_token(payload.refresh_token)
    return None


@router.get("/me", response_model=UserResponse)
async def get_my_profile(current_user: User = Depends(get_current_user)):
    """
    Fetch current authenticated user profile.
    """
    return current_user
