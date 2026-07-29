from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Optional
import uuid


@dataclass
class GithubRepository:
    id: uuid.UUID
    org_id: uuid.UUID
    github_repo_id: int
    name: str
    full_name: str
    url: str
    default_branch: str = "main"
    is_private: bool = False
    language: Optional[str] = None
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


@dataclass
class GithubCommit:
    id: uuid.UUID
    repo_id: uuid.UUID
    sha: str
    author_email: str
    author_name: str
    message: str
    additions: int = 0
    deletions: int = 0
    committed_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


@dataclass
class GithubPullRequest:
    id: uuid.UUID
    repo_id: uuid.UUID
    github_pr_number: int
    title: str
    state: str
    author_username: str
    source_branch: str
    target_branch: str
    additions: int = 0
    deletions: int = 0
    changed_files: int = 0
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    merged_at: Optional[datetime] = None
    closed_at: Optional[datetime] = None


@dataclass
class GithubIssue:
    id: uuid.UUID
    repo_id: uuid.UUID
    github_issue_number: int
    title: str
    state: str
    author_username: str
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    closed_at: Optional[datetime] = None
