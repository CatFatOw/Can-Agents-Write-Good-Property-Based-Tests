"""Routes for choosing which model API/key provider the app should use."""

from __future__ import annotations

import os
from urllib.parse import urlparse

from fastapi import APIRouter, HTTPException, status
from sqlalchemy import text
from starlette.concurrency import run_in_threadpool

import database
from schemas import ModelProviderResponse, ModelProviderSelection

router = APIRouter(prefix="/model-api", tags=["model api"])
api_router = APIRouter(prefix="/api", tags=["legacy model api"])

DEFAULT_CMU_GATEWAY_BASE_URL = "https://ai-gateway.andrew.cmu.edu/v1"
OPENAI_MARKDOWN_MODEL = os.environ.get("OPENAI_MODEL", "gpt-5.5")
OPENAI_METRICS_MODEL = os.environ.get("OPENAI_METRICS_MODEL", "gpt-5.4-mini")
CLAUDE_MARKDOWN_MODEL = os.environ.get("ANTHROPIC_MODEL", "claude-sonnet-4-6")
CLAUDE_METRICS_MODEL = os.environ.get("ANTHROPIC_METRICS_MODEL", CLAUDE_MARKDOWN_MODEL)


PROVIDERS: dict[str, dict[str, object]] = {
    "openai": {
        "id": "openai",
        "label": "GPT / OpenAI",
        "key_label": "OpenAI key",
        "key_placeholder": "sk-...",
        "default_model": OPENAI_MARKDOWN_MODEL,
        "default_markdown_model": OPENAI_MARKDOWN_MODEL,
        "default_metrics_model": OPENAI_METRICS_MODEL,
        "key_url": None,
        "requires_base_url": False,
        "openai_compatible": True,
    },
    "claude": {
        "id": "claude",
        "label": "Claude / Anthropic",
        "key_label": "Anthropic key",
        "key_placeholder": "sk-ant-...",
        "default_model": CLAUDE_MARKDOWN_MODEL,
        "default_markdown_model": CLAUDE_MARKDOWN_MODEL,
        "default_metrics_model": CLAUDE_METRICS_MODEL,
        "key_url": "https://console.anthropic.com/settings/keys",
        "requires_base_url": False,
        "openai_compatible": False,
    },
    "cmu_gateway": {
        "id": "cmu_gateway",
        "label": "CMU AI Gateway",
        "key_label": "Gateway key",
        "key_placeholder": "Paste gateway key",
        "default_model": os.environ.get("CMU_AI_GATEWAY_MODEL") or OPENAI_MARKDOWN_MODEL,
        "default_markdown_model": os.environ.get("CMU_AI_GATEWAY_MODEL") or OPENAI_MARKDOWN_MODEL,
        "default_metrics_model": os.environ.get("CMU_AI_GATEWAY_METRICS_MODEL") or OPENAI_METRICS_MODEL,
        "key_url": "https://ai-gateway.andrew.cmu.edu/ui/?page=api-keys",
        # Dashboard URLs are for key management. The OpenAI-compatible API base
        # URL should point at /v1 unless CMU changes the gateway deployment.
        "requires_base_url": False,
        "openai_compatible": True,
    },
}


def provider_response(provider: dict[str, object]) -> ModelProviderResponse:
    """Shape plain provider metadata through a Pydantic response model."""
    return ModelProviderResponse(**provider)


def redis_status_url() -> str:
    redis_url = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    tls_enabled = os.getenv("REDIS_TLS", "").lower() in {"1", "true", "yes"}
    if (tls_enabled or "upstash.io" in redis_url) and redis_url.startswith("redis://"):
        return redis_url.replace("redis://", "rediss://", 1)
    return redis_url


def queue_status_payload(connected: bool, error: str | None = None) -> dict[str, object]:
    parsed = urlparse(redis_status_url())
    host = parsed.hostname or "localhost"
    is_local = host in {"localhost", "127.0.0.1"}
    payload: dict[str, object] = {
        "connected": connected,
        "broker": "redis",
        "environment": "local" if is_local else "cloud",
        "host": host,
        "tls": parsed.scheme == "rediss",
    }
    if error:
        payload["error"] = error
    return payload


def ping_redis_queue() -> dict[str, object]:
    try:
        import redis

        client = redis.Redis.from_url(
            redis_status_url(),
            socket_connect_timeout=2,
            socket_timeout=2,
            decode_responses=True,
        )
        client.ping()
        return queue_status_payload(True)
    except Exception as exc:
        return queue_status_payload(False, str(exc))


@router.get("/providers", response_model=list[ModelProviderResponse])
async def get_model_providers():
    """Return provider options for the frontend dropdown."""
    return [provider_response(provider) for provider in PROVIDERS.values()]


@router.post("/selection", response_model=ModelProviderResponse)
async def select_model_provider(selection: ModelProviderSelection):
    """Validate a user's provider choice before generation requests use it."""
    provider = PROVIDERS.get(selection.provider)
    if provider is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unknown model provider: {selection.provider}",
        )
    return provider_response(provider)


@api_router.get("/model-providers", response_model=list[ModelProviderResponse])
async def get_legacy_model_providers():
    """Frontend-friendly alias that sits beside the existing /api routes."""
    return await get_model_providers()


@api_router.post("/model-selection", response_model=ModelProviderResponse)
async def select_legacy_model_provider(selection: ModelProviderSelection):
    """Frontend-friendly alias for provider validation."""
    return await select_model_provider(selection)


@api_router.get("/status")
async def get_runtime_status():
    """Report database and Redis/Celery queue health for the app status bar."""
    url = database.engine.url
    backend = url.get_backend_name()
    is_local = backend == "sqlite" or (url.host in {"localhost", "127.0.0.1"})
    queue = await run_in_threadpool(ping_redis_queue)
    try:
        # A lightweight ping makes the UI reflect the real DB state, not just the
        # configured URL. This catches Postgres being down while sqlite fallback works.
        def ping_database():
            with database.engine.connect() as connection:
                connection.execute(text("SELECT 1"))

        await run_in_threadpool(ping_database)
        return {
            "database": {
                "connected": True,
                "backend": backend,
                "environment": "local" if is_local else "cloud",
                "using_local_fallback": backend == "sqlite",
                "name": url.database or "default",
            },
            "queue": queue,
        }
    except Exception as exc:
        return {
            "database": {
                "connected": False,
                "backend": backend,
                "environment": "local" if is_local else "cloud",
                "using_local_fallback": backend == "sqlite",
                "name": url.database or "default",
                "error": str(exc),
            },
            "queue": queue,
        }
