from typing import List
from fastapi import Depends, HTTPException, status
from app.domain.entities.user import User
from app.domain.entities.rbac import Role, Permission, has_permission
from app.api.dependencies.auth_deps import get_current_user


def require_role(allowed_roles: List[Role]):
    async def role_checker(current_user: User = Depends(get_current_user)) -> User:
        if current_user.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"User role '{current_user.role.value}' is not authorized. Allowed roles: {[r.value for r in allowed_roles]}"
            )
        return current_user
    return role_checker


def require_permission(permission: Permission):
    async def permission_checker(current_user: User = Depends(get_current_user)) -> User:
        if not has_permission(current_user.role, permission):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"User role '{current_user.role.value}' lacks required permission: '{permission.value}'"
            )
        return current_user
    return permission_checker
