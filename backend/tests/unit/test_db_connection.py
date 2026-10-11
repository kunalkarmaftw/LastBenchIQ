"""`check_connection` must report failure, never raise.

/health/deep calls this. A health check that raises when the database is down
is worse than useless - it fails exactly when you are trying to find out why.
"""

from unittest.mock import patch

import pytest

from app.core.db import check_connection, get_db

pytestmark = pytest.mark.unit


def test_check_connection_returns_false_instead_of_raising() -> None:
    with patch("app.core.db.engine.connect", side_effect=OSError("network unreachable")):
        ok, error = check_connection()

    assert ok is False
    assert error is not None
    assert "OSError" in error
    assert "network unreachable" in error


def test_connection_error_is_truncated() -> None:
    """A driver can emit a very long error; the health payload stays bounded."""
    with patch("app.core.db.engine.connect", side_effect=OSError("x" * 5000)):
        _, error = check_connection()

    assert error is not None
    assert len(error) <= 200


def test_get_db_closes_the_session_even_on_error() -> None:
    """A session leaked per failed request exhausts the pool within minutes."""
    generator = get_db()
    session = next(generator)

    with patch.object(session, "close") as closed:
        generator.close()
        closed.assert_called_once()
