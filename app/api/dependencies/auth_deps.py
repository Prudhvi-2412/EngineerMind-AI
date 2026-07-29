import uuid
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from app.core.security import decode_token
from app.domain.entities.user import User
from app.infrastructure.persistence.postgres.repositories.postgres_user_repository import PostgresUserRepository
from app.api.dependencies.service_deps import get_user_repo

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    user_repo: PostgresUserRepository = Depends(get_user_repo)
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = decode_token(token, is_refresh=False)
        user_id_str: str = payload.get("sub")
        if user_id_str is None:
            raise credentials_exception
        user_id = uuid.UUID(user_id_str)
    except Exception:
        raise credentials_exception

    user = await user_repo.get_by_id(user_id)
    if user is None or not user.is_active:
        raise credentials_exception
    return user
