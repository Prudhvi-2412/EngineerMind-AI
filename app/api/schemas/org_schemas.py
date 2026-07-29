from datetime import datetime
import uuid
from pydantic import BaseModel


class OrganizationResponse(BaseModel):
    id: uuid.UUID
    name: str
    slug: str
    plan_tier: str
    created_at: datetime

    class Config:
        from_attributes = True
