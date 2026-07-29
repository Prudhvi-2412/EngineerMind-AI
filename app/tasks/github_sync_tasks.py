import asyncio
from datetime import datetime, timezone
import uuid
from typing import Dict, Any
from app.tasks.celery_app import celery_app
from app.infrastructure.external.github_client import GitHubApiClient, RateLimitExceededException
from app.infrastructure.persistence.postgres.connection import AsyncSessionLocal
from app.infrastructure.persistence.postgres.repositories.postgres_github_repository import PostgresGithubRepository
from app.infrastructure.persistence.postgres.repositories.postgres_event_repository import PostgresEventRepository
from app.application.services.webhook_event_processor import WebhookEventProcessor
from app.domain.entities.github import GithubRepository, GithubCommit, GithubPullRequest, GithubIssue


def run_async(coro):
    """Helper to run async code inside synchronous Celery worker task"""
    return asyncio.get_event_loop().run_until_complete(coro)


@celery_app.task(bind=True, max_retries=5, default_retry_delay=10)
def process_engineering_event_task(self, event_db_id_str: str):
    """
    Celery worker task to process a stored Engineering Event asynchronously.
    Updates event status in database and executes specialized business logic handlers.
    """
    event_uuid = uuid.UUID(event_db_id_str)

    async def _execute():
        async with AsyncSessionLocal() as session:
            event_repo = PostgresEventRepository(session)
            event_model = await event_repo.get_by_id(event_uuid)

            if not event_model:
                return

            await event_repo.update_status(event_uuid, "PROCESSING")
            await session.commit()

            try:
                processor = WebhookEventProcessor(session)
                await processor.process(event_model.event_type, event_model.payload)
                await event_repo.update_status(event_uuid, "PROCESSED")
                await session.commit()
            except Exception as exc:
                retries = self.request.retries + 1
                if retries >= self.max_retries:
                    await event_repo.update_status(event_uuid, "FAILED", error_message=str(exc), retry_count=retries)
                    await session.commit()
                    raise exc
                else:
                    await event_repo.update_status(event_uuid, "RECEIVED", error_message=str(exc), retry_count=retries)
                    await session.commit()
                    raise self.retry(exc=exc, countdown=2 ** retries * 5)

    run_async(_execute())


@celery_app.task(bind=True, max_retries=5, default_retry_delay=60)
def sync_repository_full_task(self, org_id_str: str, owner: str, repo: str, github_token: str = None):
    """
    Full background backfill task syncing Repository, Commits, PRs, and Issues from GitHub REST API
    """
    try:
        client = GitHubApiClient(token=github_token)
        org_id = uuid.UUID(org_id_str)

        async def _execute_sync():
            async with AsyncSessionLocal() as session:
                github_repo = PostgresGithubRepository(session)

                # 1. Sync Repository
                raw_repo = await client.get_repository(owner, repo)
                repo_entity = GithubRepository(
                    id=uuid.uuid4(),
                    org_id=org_id,
                    github_repo_id=raw_repo["id"],
                    name=raw_repo["name"],
                    full_name=raw_repo["full_name"],
                    url=raw_repo["html_url"],
                    default_branch=raw_repo.get("default_branch", "main"),
                    is_private=raw_repo.get("private", False),
                    language=raw_repo.get("language")
                )
                db_repo = await github_repo.upsert_repository(repo_entity)

                # 2. Sync Commits
                raw_commits = await client.get_commits(owner, repo)
                for c in raw_commits:
                    commit_data = c.get("commit", {})
                    author_data = commit_data.get("author", {})
                    commit_entity = GithubCommit(
                        id=uuid.uuid4(),
                        repo_id=db_repo.id,
                        sha=c["sha"],
                        author_email=author_data.get("email", "unknown@github.com"),
                        author_name=author_data.get("name", "Unknown"),
                        message=commit_data.get("message", ""),
                        additions=c.get("stats", {}).get("additions", 0),
                        deletions=c.get("stats", {}).get("deletions", 0),
                        committed_at=datetime.fromisoformat(author_data.get("date").replace("Z", "+00:00")) if author_data.get("date") else datetime.now(timezone.utc)
                    )
                    await github_repo.upsert_commit(commit_entity)

                # 3. Sync Pull Requests
                raw_prs = await client.get_pull_requests(owner, repo)
                for pr in raw_prs:
                    pr_entity = GithubPullRequest(
                        id=uuid.uuid4(),
                        repo_id=db_repo.id,
                        github_pr_number=pr["number"],
                        title=pr["title"],
                        state=pr["state"],
                        author_username=pr.get("user", {}).get("login", "unknown"),
                        source_branch=pr.get("head", {}).get("ref", "branch"),
                        target_branch=pr.get("base", {}).get("ref", "main"),
                        additions=pr.get("additions", 0),
                        deletions=pr.get("deletions", 0),
                        changed_files=pr.get("changed_files", 0),
                        created_at=datetime.fromisoformat(pr["created_at"].replace("Z", "+00:00"))
                    )
                    await github_repo.upsert_pull_request(pr_entity)

                # 4. Sync Issues
                raw_issues = await client.get_issues(owner, repo)
                for issue in raw_issues:
                    issue_entity = GithubIssue(
                        id=uuid.uuid4(),
                        repo_id=db_repo.id,
                        github_issue_number=issue["number"],
                        title=issue["title"],
                        state=issue["state"],
                        author_username=issue.get("user", {}).get("login", "unknown"),
                        created_at=datetime.fromisoformat(issue["created_at"].replace("Z", "+00:00"))
                    )
                    await github_repo.upsert_issue(issue_entity)

                await session.commit()

        run_async(_execute_sync())
        return {"status": "success", "repo": f"{owner}/{repo}"}

    except RateLimitExceededException as rate_exc:
        countdown = max(10, rate_exc.reset_timestamp - int(datetime.now(timezone.utc).timestamp()))
        raise self.retry(exc=rate_exc, countdown=countdown)
    except Exception as exc:
        raise self.retry(exc=exc, countdown=2 ** self.request.retries * 30)
