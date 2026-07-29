from typing import List
import uuid
from fastapi import APIRouter, Depends, HTTPException, status
from app.api.schemas.user_schemas import UserResponse, UserCreateRequest
from app.domain.entities.user import User
from app.domain.entities.rbac import Role, Permission
from app.core.security import get_password_hash
from app.infrastructure.persistence.postgres.repositories.postgres_user_repository import PostgresUserRepository
from app.api.dependencies.service_deps import get_user_repo
from app.api.dependencies.auth_deps import get_current_user
from app.api.dependencies.rbac_deps import require_role, require_permission

router = APIRouter(prefix="/users", tags=["Users Management"])


@router.get("", response_model=List[UserResponse])
async def list_org_users(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(require_permission(Permission.USERS_READ)),
    user_repo: PostgresUserRepository = Depends(get_user_repo)
):
    """
    List all users in the authenticated user's organization. (Requires 'users:read' permission)
    """
    return await user_repo.list_by_org(current_user.org_id, skip=skip, limit=limit)


@router.post("", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user_in_org(
    payload: UserCreateRequest,
    current_user: User = Depends(require_permission(Permission.USERS_WRITE)),
    user_repo: PostgresUserRepository = Depends(get_user_repo)
):
    """
    Create a new user within the authenticated user's organization. (Requires 'users:write' permission)
    """
    existing = await user_repo.get_by_email(current_user.org_id, payload.email)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exists in your organization"
        )

    hashed_pw = get_password_hash(payload.password)
    user = User.create(
        org_id=current_user.org_id,
        email=payload.email,
        name=payload.name,
        role=payload.role,
        hashed_password=hashed_pw
    )
    return await user_repo.create(user)


@router.get("/{user_id}", response_model=UserResponse)
async def get_user_by_id(
    user_id: uuid.UUID,
    current_user: User = Depends(require_permission(Permission.USERS_READ)),
    user_repo: PostgresUserRepository = Depends(get_user_repo)
):
    """
    Get user profile by ID. Must belong to the same organization.
    """
    user = await user_repo.get_by_id(user_id)
    if not user or user.org_id != current_user.org_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user
