from datetime import datetime
from typing import Optional
import uuid
from pydantic import BaseModel, EmailStr
from app.domain.entities.rbac import Role


class UserResponse(BaseModel):
    id: uuid.UUID
    org_id: uuid.UUID
    email: EmailStr
    name: str
    role: Role
    avatar_url: Optional[str] = None
    is_active: bool
    is_verified: bool
    created_at: datetime

    class Config:
        from_attributes = True


class UserCreateRequest(BaseModel):
    email: EmailStr
    name: str
    role: Role = Role.ENGINEER
    password: str
