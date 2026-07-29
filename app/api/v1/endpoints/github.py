from typing import List
from fastapi import APIRouter, Request, Header, Depends, HTTPException, status
from app.core.config import settings
from app.api.schemas.github_schemas import (
    SyncRepoRequest,
    SyncJobResponse,
    GithubRepoResponse,
    WebhookResponse
)
from app.infrastructure.external.github_client import verify_webhook_signature
from app.infrastructure.external.redis_dedup import is_duplicate_event
from app.infrastructure.persistence.postgres.repositories.postgres_github_repository import PostgresGithubRepository
from app.infrastructure.persistence.postgres.repositories.postgres_event_repository import PostgresEventRepository
from app.domain.entities.engineering_event import EngineeringEvent
from app.api.dependencies.database_deps import get_db
from app.api.dependencies.auth_deps import get_current_user
from app.api.dependencies.rbac_deps import require_permission
from app.domain.entities.user import User
from app.domain.entities.rbac import Permission
from app.tasks.github_sync_tasks import process_engineering_event_task, sync_repository_full_task
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix="/github", tags=["GitHub Integration & Webhooks"])


@router.post("/webhooks", response_model=WebhookResponse, status_code=status.HTTP_202_ACCEPTED)
async def handle_github_webhook(
    request: Request,
    x_github_event: str = Header(..., alias="X-GitHub-Event"),
    x_github_delivery: str = Header(..., alias="X-GitHub-Delivery"),
    x_hub_signature_256: str = Header(..., alias="X-Hub-Signature-256"),
    session: AsyncSession = Depends(get_db)
):
    """
    Ingest GitHub Webhook events (push, pull_request, issues).
    1. Verifies HMAC-SHA256 signature.
    2. Redis distributed lock & deduplication.
    3. Persists raw event into PostgreSQL engineering_events table.
    4. Dispatches async processing task to Celery / Redis queue.
    """
    body = await request.body()
    
    # 1. Verify Webhook HMAC Signature
    is_valid = verify_webhook_signature(
        payload_body=body,
        signature_header=x_hub_signature_256,
        secret=settings.GITHUB_WEBHOOK_SECRET
    )
    if not is_valid:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid GitHub webhook HMAC-SHA256 signature"
        )

    # 2. Redis Deduplication check
    is_duplicate = await is_duplicate_event(x_github_delivery)
    if is_duplicate:
        return WebhookResponse(
            status="duplicate_ignored",
            event=x_github_event,
            task_id="none"
        )

    payload = await request.json()
    action = payload.get("action")
    full_event_type = f"{x_github_event}.{action}" if action else x_github_event

    # 3. Store raw event into PostgreSQL
    event_entity = EngineeringEvent.create(
        event_id=x_github_delivery,
        event_type=full_event_type,
        payload=payload,
        source="github"
    )
    event_repo = PostgresEventRepository(session)
    event_model = await event_repo.create_event(event_entity)

    # 4. Enqueue to Celery
    task = process_engineering_event_task.delay(str(event_model.id))

    return WebhookResponse(
        status="accepted",
        event=full_event_type,
        task_id=task.id
    )


@router.post("/sync", response_model=SyncJobResponse, status_code=status.HTTP_202_ACCEPTED)
async def trigger_repo_sync(
    payload: SyncRepoRequest,
    current_user: User = Depends(require_permission(Permission.METRICS_READ))
):
    """
    Trigger full asynchronous background sync of GitHub Repository, Commits, PRs, and Issues.
    """
    task = sync_repository_full_task.delay(
        org_id_str=str(current_user.org_id),
        owner=payload.owner,
        repo=payload.repo,
        github_token=payload.github_token
    )

    return SyncJobResponse(
        task_id=task.id,
        status="enqueued",
        message=f"Sync job enqueued for {payload.owner}/{payload.repo}"
    )


@router.get("/repos", response_model=List[GithubRepoResponse])
async def list_synced_repos(
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db)
):
    """
    List all synced GitHub repositories for the current user's organization.
    """
    github_repo = PostgresGithubRepository(session)
    models = await github_repo.list_by_org(current_user.org_id)
    return models
