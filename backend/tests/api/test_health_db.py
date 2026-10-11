"""Health endpoint behaviour when the database is reachable and when it is not.

The unreachable case is the one worth testing. A health endpoint that returns
500 when the database is down tells you nothing you could not already guess,
and it breaks exactly when you need it most.
"""

from collections.abc import Iterator
from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient

pytestmark = pytest.mark.api


@pytest.fixture
def unreachable_db() -> Iterator[None]:
    with patch(
        "app.api.health.check_connection",
        return_value=(False, "OperationalError: connection refused"),
    ):
        yield


def test_deep_health_reports_database_key(client: TestClient) -> None:
    body = client.get("/api/v1/health/deep").json()
    assert body["database"] in {"connected", "unreachable"}


def test_deep_health_degrades_when_db_is_down(client: TestClient, unreachable_db: None) -> None:
    response = client.get("/api/v1/health/deep")

    # Still 200: the endpoint reports the problem rather than becoming one.
    assert response.status_code == 200

    body = response.json()
    assert body["status"] == "degraded"
    assert body["database"] == "unreachable"
    assert "connection refused" in body["database_error"]


def test_shallow_health_stays_up_when_db_is_down(client: TestClient, unreachable_db: None) -> None:
    """`/health` is the platform's liveness probe and must not depend on the DB.

    If it did, a brief database blip would make the host kill and restart a
    perfectly healthy container.
    """
    assert client.get("/api/v1/health").json() == {"status": "ok"}
