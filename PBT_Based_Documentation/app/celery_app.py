"""Celery distributed task queue setup for long-running app work."""

from celery import Celery 
import os 


def _redis_url() -> str:
    redis_url = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    tls_enabled = os.getenv("REDIS_TLS", "").lower() in {"1", "true", "yes"}
    uses_upstash = "upstash.io" in redis_url
    if (tls_enabled or uses_upstash) and redis_url.startswith("redis://"):
        return redis_url.replace("redis://", "rediss://", 1)
    return redis_url


celery_app = Celery(
    "ibd_distributed_task_queue",
    broker=_redis_url(),
    backend=_redis_url(),
)

celery_app.conf.update(
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    result_expires=60 * 60,
    broker_connection_retry_on_startup=True,
)

# Import tasks here 
from tasks import export_tasks
from tasks import metric_task
