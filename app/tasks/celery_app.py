from celery import Celery
from app.core.config import settings

celery_app = Celery(
    "engineering_os_tasks",
    broker=settings.REDIS_URL,
    backend=settings.REDIS_URL
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_routes={
        "app.tasks.github_sync_tasks.process_engineering_event_task": {"queue": "github_webhooks"},
        "app.tasks.github_sync_tasks.sync_repository_full_task": {"queue": "github_sync"},
    },
    task_annotations={
        "*": {
            "rate_limit": "10/m",
        }
    }
)
