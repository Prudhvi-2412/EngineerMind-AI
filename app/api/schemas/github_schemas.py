import uuid
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class SyncRepoRequest(BaseModel):
    owner: str = Field(..., example="octocat")
    repo: str = Field(..., example="Hello-World")
    github_token: Optional[str] = Field(None, example="ghp_1234567890abcdef")


class SyncJobResponse(BaseModel):
    task_id: str
    status: str
    message: str


class GithubRepoResponse(BaseModel):
    id: uuid.UUID
    org_id: uuid.UUID
    github_repo_id: int
    name: str
    full_name: str
    url: str
    default_branch: str
    is_private: bool
    language: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True


class WebhookResponse(BaseModel):
    status: str = "accepted"
    event: str
    task_id: str
