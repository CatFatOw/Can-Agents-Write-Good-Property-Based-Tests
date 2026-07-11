"""Smoke tests for the FastAPI application boundary."""

from fastapi.testclient import TestClient

from app.main import app


def test_health_endpoint_reports_ready_status():
    response = TestClient(app).get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
