"""Registration and sign-in, against a real database.

The enrollment number is the account's identity, so the tests that matter most
are the ones proving it is genuinely unique and that one student's token can
never read another student's record.
"""

from collections.abc import Iterator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import text

from app.core.db import engine
from app.main import create_app

pytestmark = pytest.mark.api

API = "/api/v1"


@pytest.fixture
def client() -> Iterator[TestClient]:
    """A clean users table per test, so one test cannot pass because of another."""
    with engine.begin() as conn:
        conn.execute(text("TRUNCATE TABLE users CASCADE"))
    with TestClient(create_app()) as c:
        yield c


def _signup(client: TestClient, enrollment: str = "03514902024", **over: object) -> dict:
    # The email is derived from the digits only: an enrollment number typed
    # with spaces or dashes would otherwise produce an invalid address.
    digits = "".join(c for c in enrollment if c.isdigit())
    body = {
        "enrollment_number": enrollment,
        "email": f"s{digits}@example.edu",
        "password": "correct horse battery",
        "name": "Test Student",
        "college": "Maharaja Surajmal Institute",
        "branch": "BCA",
        "graduation_year": 2027,
    }
    body.update(over)  # type: ignore[arg-type]
    return client.post(f"{API}/auth/register", json=body).json()


# --------------------------------------------------------------------------
# registration
# --------------------------------------------------------------------------


def test_register_returns_token_and_user(client: TestClient) -> None:
    r = client.post(
        f"{API}/auth/register",
        json={
            "enrollment_number": "03514902024",
            "email": "karma@example.edu",
            "password": "correct horse battery",
            "name": "Kunal Verma",
            "branch": "BCA",
        },
    )
    assert r.status_code == 201
    body = r.json()
    assert body["token_type"] == "bearer"
    assert body["access_token"]
    assert body["user"]["enrollment_number"] == "03514902024"
    assert body["user"]["name"] == "Kunal Verma"


def test_password_is_never_returned(client: TestClient) -> None:
    body = _signup(client)
    assert "password" not in body["user"]
    assert "password_hash" not in body["user"]


def test_enrollment_number_must_be_unique(client: TestClient) -> None:
    """The point of using enrollment numbers: one number, one account."""
    _signup(client, "03514902024")
    r = client.post(
        f"{API}/auth/register",
        json={
            "enrollment_number": "03514902024",
            "email": "someone.else@example.edu",
            "password": "a different password",
            "name": "Someone Else",
        },
    )
    assert r.status_code == 409
    assert r.json()["detail"]["code"] == "enrollment_taken"


def test_email_must_be_unique(client: TestClient) -> None:
    _signup(client, "03514902024", email="shared@example.edu")
    r = client.post(
        f"{API}/auth/register",
        json={
            "enrollment_number": "08914902022",
            "email": "shared@example.edu",
            "password": "a different password",
            "name": "Someone Else",
        },
    )
    assert r.status_code == 409
    assert r.json()["detail"]["code"] == "email_taken"


def test_enrollment_number_is_normalised(client: TestClient) -> None:
    """Students copy the number off an ID card, spaces and dashes included."""
    body = _signup(client, "0351-4902 024")
    assert body["user"]["enrollment_number"] == "03514902024"


@pytest.mark.parametrize("bad", ["12345", "abcdefghijk", "0351490202412345678", ""])
def test_malformed_enrollment_number_is_rejected(client: TestClient, bad: str) -> None:
    r = client.post(
        f"{API}/auth/register",
        json={
            "enrollment_number": bad,
            "email": "x@example.edu",
            "password": "correct horse battery",
            "name": "X",
        },
    )
    assert r.status_code == 422


def test_short_password_is_rejected(client: TestClient) -> None:
    r = client.post(
        f"{API}/auth/register",
        json={
            "enrollment_number": "03514902024",
            "email": "x@example.edu",
            "password": "short",
            "name": "X",
        },
    )
    assert r.status_code == 422


# --------------------------------------------------------------------------
# sign-in
# --------------------------------------------------------------------------


def test_login_with_enrollment_number(client: TestClient) -> None:
    _signup(client, "03514902024")
    r = client.post(
        f"{API}/auth/login",
        json={
            "enrollment_number": "03514902024",
            "password": "correct horse battery",
        },
    )
    assert r.status_code == 200
    assert r.json()["access_token"]


def test_wrong_password_is_rejected(client: TestClient) -> None:
    _signup(client, "03514902024")
    r = client.post(
        f"{API}/auth/login",
        json={
            "enrollment_number": "03514902024",
            "password": "not the password",
        },
    )
    assert r.status_code == 401


def test_unknown_and_wrong_password_look_identical(client: TestClient) -> None:
    """Different messages would let anyone test which enrollment numbers exist."""
    _signup(client, "03514902024")
    wrong = client.post(
        f"{API}/auth/login",
        json={"enrollment_number": "03514902024", "password": "not the password"},
    ).json()
    unknown = client.post(
        f"{API}/auth/login",
        json={"enrollment_number": "09999999999", "password": "not the password"},
    ).json()
    assert wrong["detail"] == unknown["detail"]


# --------------------------------------------------------------------------
# protected routes
# --------------------------------------------------------------------------


def test_me_requires_a_token(client: TestClient) -> None:
    assert client.get(f"{API}/auth/me").status_code == 401


def test_me_rejects_a_garbage_token(client: TestClient) -> None:
    r = client.get(f"{API}/auth/me", headers={"Authorization": "Bearer not-a-jwt"})
    assert r.status_code == 401


def test_me_returns_the_signed_in_student(client: TestClient) -> None:
    token = _signup(client, "03514902024")["access_token"]
    r = client.get(f"{API}/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert r.status_code == 200
    assert r.json()["enrollment_number"] == "03514902024"


def test_one_students_token_returns_only_their_own_record(client: TestClient) -> None:
    """Two accounts, two tokens: each must see itself and never the other."""
    a = _signup(client, "03514902024", name="Student A")
    b = _signup(client, "08914902022", name="Student B")

    me_a = client.get(
        f"{API}/auth/me", headers={"Authorization": f"Bearer {a['access_token']}"}
    ).json()
    me_b = client.get(
        f"{API}/auth/me", headers={"Authorization": f"Bearer {b['access_token']}"}
    ).json()

    assert me_a["enrollment_number"] == "03514902024"
    assert me_a["name"] == "Student A"
    assert me_b["enrollment_number"] == "08914902022"
    assert me_a["id"] != me_b["id"]
