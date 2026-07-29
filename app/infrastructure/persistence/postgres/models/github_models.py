from datetime import datetime, timezone
from typing import Optional
import uuid
from sqlalchemy import String, Boolean, Integer, DateTime, ForeignKey, Text, BigInteger
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from app.infrastructure.persistence.postgres.models.base import Base


class RepositoryModel(Base):
    __tablename__ = "repositories"

    id: Mapped[uuid.UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    org_id: Mapped[uuid.UUID] = mapped_column(PG_UUID(as_uuid=True), ForeignKey("organizations.id", ondelete="CASCADE"), nullable=False, index=True)
    github_repo_id: Mapped[int] = mapped_column(BigInteger, nullable=False, unique=True, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    full_name: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    url: Mapped[str] = mapped_column(String(500), nullable=False)
    default_branch: Mapped[str] = mapped_column(String(100), nullable=False, default="main")
    is_private: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    language: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    commits = relationship("CommitModel", back_populates="repository", cascade="all, delete-orphan")
    pull_requests = relationship("PullRequestModel", back_populates="repository", cascade="all, delete-orphan")
    issues = relationship("IssueModel", back_populates="repository", cascade="all, delete-orphan")


class CommitModel(Base):
    __tablename__ = "commits"

    id: Mapped[uuid.UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    repo_id: Mapped[uuid.UUID] = mapped_column(PG_UUID(as_uuid=True), ForeignKey("repositories.id", ondelete="CASCADE"), nullable=False, index=True)
    sha: Mapped[str] = mapped_column(String(40), nullable=False, unique=True, index=True)
    author_email: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    author_name: Mapped[str] = mapped_column(String(255), nullable=False)
    message: Mapped[str] = mapped_column(Text, nullable=False)
    additions: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    deletions: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    committed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, index=True)

    repository = relationship("RepositoryModel", back_populates="commits")


class PullRequestModel(Base):
    __tablename__ = "pull_requests"

    id: Mapped[uuid.UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    repo_id: Mapped[uuid.UUID] = mapped_column(PG_UUID(as_uuid=True), ForeignKey("repositories.id", ondelete="CASCADE"), nullable=False, index=True)
    github_pr_number: Mapped[int] = mapped_column(Integer, nullable=False, index=True)
    title: Mapped[str] = mapped_column(String(500), nullable=False)
    state: Mapped[str] = mapped_column(String(50), nullable=False, default="open", index=True)
    author_username: Mapped[str] = mapped_column(String(255), nullable=False)
    source_branch: Mapped[str] = mapped_column(String(255), nullable=False)
    target_branch: Mapped[str] = mapped_column(String(255), nullable=False)
    additions: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    deletions: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    changed_files: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, index=True)
    merged_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    closed_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)

    repository = relationship("RepositoryModel", back_populates="pull_requests")


class IssueModel(Base):
    __tablename__ = "issues"

    id: Mapped[uuid.UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    repo_id: Mapped[uuid.UUID] = mapped_column(PG_UUID(as_uuid=True), ForeignKey("repositories.id", ondelete="CASCADE"), nullable=False, index=True)
    github_issue_number: Mapped[int] = mapped_column(Integer, nullable=False, index=True)
    title: Mapped[str] = mapped_column(String(500), nullable=False)
    state: Mapped[str] = mapped_column(String(50), nullable=False, default="open", index=True)
    author_username: Mapped[str] = mapped_column(String(255), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    closed_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)

    repository = relationship("RepositoryModel", back_populates="issues")
