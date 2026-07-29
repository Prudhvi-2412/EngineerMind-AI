from datetime import datetime, timezone
from typing import Dict, Any
import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from app.infrastructure.persistence.postgres.repositories.postgres_github_repository import PostgresGithubRepository
from app.domain.entities.github import GithubCommit, GithubPullRequest, GithubIssue


class WebhookEventProcessor:
    def __init__(self, session: AsyncSession):
        self.github_repo = PostgresGithubRepository(session)

    async def process(self, event_type: str, payload: Dict[str, Any]) -> None:
        action = payload.get("action")
        
        if event_type == "pull_request":
            if action == "opened":
                await self._handle_pr_opened(payload)
            elif action == "synchronize": # PR Updated with new commits
                await self._handle_pr_updated(payload)
            elif action == "closed" and payload.get("pull_request", {}).get("merged"):
                await self._handle_pr_merged(payload)
        elif event_type == "issues" and action == "opened":
            await self._handle_issue_created(payload)
        elif event_type == "push":
            await self._handle_push(payload)

    async def _handle_pr_opened(self, payload: Dict[str, Any]) -> None:
        pr_data = payload["pull_request"]
        repo_data = payload["repository"]

        db_repo = await self.github_repo.get_by_full_name(repo_data["full_name"])
        if not db_repo:
            return

        pr_entity = GithubPullRequest(
            id=uuid.uuid4(),
            repo_id=db_repo.id,
            github_pr_number=pr_data["number"],
            title=pr_data["title"],
            state="open",
            author_username=pr_data["user"]["login"],
            source_branch=pr_data["head"]["ref"],
            target_branch=pr_data["base"]["ref"],
            additions=pr_data.get("additions", 0),
            deletions=pr_data.get("deletions", 0),
            changed_files=pr_data.get("changed_files", 0),
            created_at=datetime.fromisoformat(pr_data["created_at"].replace("Z", "+00:00"))
        )
        await self.github_repo.upsert_pull_request(pr_entity)

    async def _handle_pr_updated(self, payload: Dict[str, Any]) -> None:
        pr_data = payload["pull_request"]
        repo_data = payload["repository"]

        db_repo = await self.github_repo.get_by_full_name(repo_data["full_name"])
        if not db_repo:
            return

        pr_entity = GithubPullRequest(
            id=uuid.uuid4(),
            repo_id=db_repo.id,
            github_pr_number=pr_data["number"],
            title=pr_data["title"],
            state="open",
            author_username=pr_data["user"]["login"],
            source_branch=pr_data["head"]["ref"],
            target_branch=pr_data["base"]["ref"],
            additions=pr_data.get("additions", 0),
            deletions=pr_data.get("deletions", 0),
            changed_files=pr_data.get("changed_files", 0),
            created_at=datetime.fromisoformat(pr_data["created_at"].replace("Z", "+00:00"))
        )
        await self.github_repo.upsert_pull_request(pr_entity)

    async def _handle_pr_merged(self, payload: Dict[str, Any]) -> None:
        pr_data = payload["pull_request"]
        repo_data = payload["repository"]

        db_repo = await self.github_repo.get_by_full_name(repo_data["full_name"])
        if not db_repo:
            return

        merged_at = datetime.fromisoformat(pr_data["merged_at"].replace("Z", "+00:00")) if pr_data.get("merged_at") else datetime.now(timezone.utc)
        closed_at = datetime.fromisoformat(pr_data["closed_at"].replace("Z", "+00:00")) if pr_data.get("closed_at") else merged_at

        pr_entity = GithubPullRequest(
            id=uuid.uuid4(),
            repo_id=db_repo.id,
            github_pr_number=pr_data["number"],
            title=pr_data["title"],
            state="merged",
            author_username=pr_data["user"]["login"],
            source_branch=pr_data["head"]["ref"],
            target_branch=pr_data["base"]["ref"],
            additions=pr_data.get("additions", 0),
            deletions=pr_data.get("deletions", 0),
            changed_files=pr_data.get("changed_files", 0),
            created_at=datetime.fromisoformat(pr_data["created_at"].replace("Z", "+00:00")),
            merged_at=merged_at,
            closed_at=closed_at
        )
        await self.github_repo.upsert_pull_request(pr_entity)

    async def _handle_issue_created(self, payload: Dict[str, Any]) -> None:
        issue_data = payload["issue"]
        repo_data = payload["repository"]

        db_repo = await self.github_repo.get_by_full_name(repo_data["full_name"])
        if not db_repo:
            return

        issue_entity = GithubIssue(
            id=uuid.uuid4(),
            repo_id=db_repo.id,
            github_issue_number=issue_data["number"],
            title=issue_data["title"],
            state="open",
            author_username=issue_data["user"]["login"],
            created_at=datetime.fromisoformat(issue_data["created_at"].replace("Z", "+00:00"))
        )
        await self.github_repo.upsert_issue(issue_entity)

    async def _handle_push(self, payload: Dict[str, Any]) -> None:
        repo_data = payload["repository"]
        commits_data = payload.get("commits", [])

        db_repo = await self.github_repo.get_by_full_name(repo_data["full_name"])
        if not db_repo:
            return

        for c in commits_data:
            commit_entity = GithubCommit(
                id=uuid.uuid4(),
                repo_id=db_repo.id,
                sha=c["id"],
                author_email=c.get("author", {}).get("email", "unknown@github.com"),
                author_name=c.get("author", {}).get("name", "Unknown"),
                message=c.get("message", ""),
                additions=len(c.get("added", [])),
                deletions=len(c.get("removed", [])),
                committed_at=datetime.fromisoformat(c["timestamp"].replace("Z", "+00:00")) if c.get("timestamp") else datetime.now(timezone.utc)
            )
            await self.github_repo.upsert_commit(commit_entity)
