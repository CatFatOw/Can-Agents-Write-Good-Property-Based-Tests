"""File handles the metric calculations.

FOLLOWING ROUTES
1. Calculate soundness + validity
2. Calculate mutation
3. Generate mutation + summary
4. Get the soundness/validity metric, get mutation and mutation summary

Note, rewrite this alot of functionaility via redis + celery
"""
from app.celery_app import celery_app
import sys
from app.tasks.metric_task import calculate_metrics_celery, calculate_mutation_analysis_celery, rerun_generated_test_celery, calculate_documentation_coverage_celery
from app.task_runner import dispatch_json
from fastapi import APIRouter, HTTPException, status, Depends, Response
from fastapi.responses import JSONResponse
from starlette.concurrency import run_in_threadpool
from sqlalchemy.orm import Session
from app import database, legacy_backend, models
from app.database import get_db
# To be used when calculating metrics
from tempfile import TemporaryDirectory
from pathlib import Path
from celery.result import AsyncResult

METRICS_DIR = Path(__file__).resolve().parents[2] / "metrics"
if str(METRICS_DIR) not in sys.path:
    sys.path.append(str(METRICS_DIR))

from metric_code import (
    evaluate_mutation_testing,
    evaluate_pytest,
    evaluate_validity_soundness,
    score_validity_soundness_mutation,
)

router = APIRouter(prefix="/metrics", tags=["metrics"])
api_router = APIRouter(prefix="/api", tags=["legacy metrics api"])


def legacy_error(exc: Exception) -> JSONResponse:
    """Return the same JSON error shape that the frontend expected from server.py."""
    status_code = status.HTTP_400_BAD_REQUEST if isinstance(exc, ValueError) else status.HTTP_500_INTERNAL_SERVER_ERROR
    return JSONResponse(status_code=status_code, content={"error": str(exc)})


def celery_result_payload(job_id: str) -> dict:
    result = AsyncResult(job_id, app=celery_app)
    payload = {
        "job_id": job_id,
        "status": result.status,
        "ready": result.ready(),
        "result": None,
    }
    if result.ready():
        if result.failed():
            payload["result"] = {"error": str(result.result)}
        else:
            payload["result"] = result.result
    return payload


# Celery decode/get job id 
@router.get("/{job_id}")
async def get_job_id(job_id):
    """Function decodes unique celery job_id and gets value """
    return celery_result_payload(job_id)


# Queue to Celery when Redis is up; otherwise run inline so the metrics
# pipeline still works (the frontend handles both the task_id and direct shapes).
@api_router.post("/metrics")
async def calculate_metrics(payload: dict):
    """Drop-in replacement for server.py's /api/metrics endpoint."""
    try:
        return await dispatch_json(calculate_metrics_celery, legacy_backend.generate_metrics, payload)
    except Exception as exc:
        return legacy_error(exc)


@api_router.post("/mutation-analysis")
async def calculate_mutation_analysis(payload: dict):
    """Analyze mutation survivors for one generated Hypothesis test."""
    try:
        return await dispatch_json(calculate_mutation_analysis_celery, legacy_backend.generate_mutation_analysis, payload)
    except Exception as exc:
        return legacy_error(exc)


@api_router.post("/rerun-test")
async def rerun_generated_test(payload: dict):
    """Re-run one generated test and return the metric object."""
    try:
        return await dispatch_json(rerun_generated_test_celery, legacy_backend.rerun_test, payload)
    except Exception as exc:
        return legacy_error(exc)


@api_router.post("/coverage")
async def calculate_documentation_coverage(payload: dict):
    """Map generated documentation claims back to source-code evidence."""
    try:
        return await dispatch_json(calculate_documentation_coverage_celery, legacy_backend.generate_coverage, payload)
    except Exception as exc:
        return legacy_error(exc)
