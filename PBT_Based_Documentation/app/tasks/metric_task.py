from celery_app import celery_app
from fastapi.encoders import jsonable_encoder
from fastapi import status
import legacy_backend

# Helper function
def legacy_error(exc: Exception) -> dict:
    """Return a JSON-serializable error shape for Celery result storage."""
    status_code = status.HTTP_400_BAD_REQUEST if isinstance(exc, ValueError) else status.HTTP_500_INTERNAL_SERVER_ERROR
    return {"error": str(exc), "status_code": status_code}


def task_result(result) -> dict:
    """Convert legacy metric output into a Celery JSON-backend friendly payload."""
    return jsonable_encoder(result)

@celery_app.task 
def calculate_metrics_celery(payload: dict):
    """Drop-in replacement for server.py's /api/metrics endpoint."""
    try:
        return task_result(legacy_backend.generate_metrics(payload))
    except Exception as exc:
        return legacy_error(exc)
    

@celery_app.task 
def calculate_mutation_analysis_celery(payload: dict):
    """Analyze mutation survivors for one generated Hypothesis test."""
    try:
        return task_result(legacy_backend.generate_mutation_analysis(payload))
    except Exception as exc:
        return legacy_error(exc)
    

@celery_app.task
def rerun_generated_test_celery(payload: dict):
    """Re-run one generated test and return the metric object."""
    try:
        return task_result(legacy_backend.rerun_test(payload))
    except Exception as exc:
        return legacy_error(exc)
    

@celery_app.task
def calculate_documentation_coverage_celery(payload: dict):
    """Map generated documentation claims back to source-code evidence."""
    try:
        return task_result(legacy_backend.generate_coverage(payload))
    except Exception as exc:
        return legacy_error(exc)
    
