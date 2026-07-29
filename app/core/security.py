from datetime import datetime, timedelta, timezone
from typing import Any, Dict, Optional, Union
from jose import JWTError, jwt
from passlib.context import CryptContext
from app.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def create_access_token(
    subject: Union[str, Any],
    org_id: str,
    role: str,
    expires_delta: Optional[timedelta] = None
) -> str:
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode: Dict[str, Any] = {
        "sub": str(subject),
        "org_id": str(org_id),
        "role": str(role),
        "exp": expire,
        "type": "access"
    }
    encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


def create_refresh_token(
    subject: Union[str, Any],
    token_family_id: str,
    expires_delta: Optional[timedelta] = None
) -> str:
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    
    to_encode: Dict[str, Any] = {
        "sub": str(subject),
        "family": str(token_family_id),
        "exp": expire,
        "type": "refresh"
    }
    encoded_jwt = jwt.encode(to_encode, settings.JWT_REFRESH_SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


def decode_token(token: str, is_refresh: bool = False) -> Dict[str, Any]:
    secret_key = settings.JWT_REFRESH_SECRET_KEY if is_refresh else settings.JWT_SECRET_KEY
    try:
        payload = jwt.decode(token, secret_key, algorithms=[settings.ALGORITHM])
        return payload
    except JWTError as e:
        raise ValueError(f"Invalid token: {str(e)}")
