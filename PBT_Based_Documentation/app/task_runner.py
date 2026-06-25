"""Decide whether to offload work to Celery/Redis or run it inline.

The app must keep working when Redis/Celery is unavailable -- for example a
Render deploy without a Key Value instance, a misconfigured ``REDIS_URL``, or the
worker simply being down. In those cases tasks run synchronously inside the web
process so the model-calling and metrics pipeline never breaks. When a broker is
reachable, heavy work (mutation testing, CSV exports) is queued to the Celery
worker as intended.
"""

from __future__ import annotations

import os
import time
from typing import Any, Callable

from fastapi import Response
from starlette.concurrency import run_in_threadpool

# Support both `PYTHONPATH=app ...` and package-style `app....` launches, matching
# the dual-import pattern the rest of the app uses.
try:
    from celery_app import celery_app
except ImportError:
    from app.celery_app import celery_app


# Probing the broker on every request would add a Redis round-trip to each call,
# so the result is cached for a short window. A failed enqueue clears it early.
_CHECK_TTL_SECONDS = 30.0
_state: dict[str, Any] = {"checked_at": 0.0, "available": False}


def _force_sync() -> bool:
    """Allow operators to pin inline execution regardless of broker state."""
    return os.getenv("CELERY_TASK_MODE", "").strip().lower() in {
        "sync",
        "eager",
        "inline",
        "off",
        "disabled",
    }


def broker_available(force_refresh: bool = False) -> bool:
    """Return True if the Celery broker (Redis) is reachable.

    The check is cached for a few seconds so individual requests do not each pay
    a connection round-trip.
    """
    if _force_sync():
        return False
    now = time.monotonic()
    if not force_refresh and (now - _state["checked_at"]) < _CHECK_TTL_SECONDS:
        return _state["available"]
    try:
        connection = celery_app.connection_for_write()
        try:
            connection.ensure_connection(max_retries=0, timeout=2)
        finally:
            connection.release()
        available = True
    except Exception:
        available = False
    _state["checked_at"] = now
    _state["available"] = available
    return available


def _mark_broker_down() -> None:
    """Force the next ``broker_available`` call to re-probe after a failure."""
    _state["checked_at"] = 0.0
    _state["available"] = False


async def dispatch_json(celery_task, sync_callable: Callable[..., Any], *args) -> Any:
    """Queue a task when a broker is reachable, else run it inline.

    Returns ``{"task_id", "status": "queued"}`` for the frontend to poll when the
    work was queued, or the task's actual result when it ran synchronously. The
    frontend's ``postJson`` polls only when a ``task_id`` is present and otherwise
    uses the response body directly, so both shapes are valid.
    """
    if broker_available():
        try:
            async_result = celery_task.delay(*args)
            return {"task_id": async_result.id, "status": "queued"}
        except Exception:
            # The broker died between the health check and the enqueue. Fall back
            # to inline execution so the request still succeeds.
            _mark_broker_down()
    return await run_in_threadpool(sync_callable, *args)


async def run_task_inline(celery_task, *args) -> Any:
    """Execute a Celery task body synchronously in the current process.

    Calling a Celery task object directly (rather than ``.delay``) runs it locally
    without touching the broker, which is exactly what the inline fallback needs.
    """
    return await run_in_threadpool(celery_task, *args)


def csv_response(result: dict) -> Response:
    """Return a worker CSV payload as a direct download.

    Used by the inline fallback when Redis/Celery is unavailable. The frontend
    streams a real CSV response straight to a file (it only polls a task id when
    the response is JSON with a task_id), so both paths download the same file.
    """
    filename = result.get("filename") or "export.csv"
    return Response(
        content=result.get("content") or "",
        media_type=result.get("media_type") or "text/csv",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )


async def export_csv(celery_task, *args) -> Any:
    """Queue a CSV export task when a broker is reachable, else build it inline.

    Returns ``{"task_id", "status": "queued"}`` for the frontend to poll, or a
    direct CSV ``Response`` when run synchronously. Both are handled by the
    frontend's admin-export download flow.
    """
    if broker_available():
        try:
            async_result = celery_task.delay(*args)
            return {"task_id": async_result.id, "status": "queued"}
        except Exception:
            _mark_broker_down()
    return csv_response(await run_task_inline(celery_task, *args))
