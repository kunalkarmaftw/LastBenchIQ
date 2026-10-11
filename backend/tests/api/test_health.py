"""API-level tests for the health endpoints."""

import pytest
from fastapi.testclient import TestClient

pytestmark = pytest.mark.api


def test_health_returns_ok(client: TestClient) -> None:
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_deep_health_reports_dependencies(client: TestClient) -> None:
    """EPIC 0: the deployed environment must report what is actually installed."""
    response = client.get("/api/v1/health/deep")
    assert response.status_code == 200

    body = response.json()
    assert "packages" in body
    assert "tesseract_binary" in body
    # Every heavy dependency is reported on, present or not — a silently missing
    # package is exactly the week-7 surprise this endpoint exists to prevent.
    for package in ("sklearn", "pandas", "fitz", "pytesseract"):
        assert package in body["packages"]


def test_openapi_schema_is_generated(client: TestClient) -> None:
    assert client.get("/openapi.json").status_code == 200
