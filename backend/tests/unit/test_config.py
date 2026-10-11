"""Settings normalisation.

The driver prefix is the single most likely thing to go wrong when moving this
project to a new machine or to Render, and the failure is a `ModuleNotFoundError:
psycopg2` that never names the URL. These tests pin the fix.
"""

import pytest

from app.core.config import Settings

pytestmark = pytest.mark.unit

HOST = "user:pw@ep-x.aws.neon.tech/neondb?sslmode=require"
EXPECTED = f"postgresql+psycopg://{HOST}"


@pytest.mark.parametrize(
    "given",
    [
        # What Neon, Render and Supabase actually print in their dashboards.
        f"postgresql://{HOST}",
        # What Heroku-style providers print.
        f"postgres://{HOST}",
        # A URL copied from a tutorial written for psycopg2.
        f"postgresql+psycopg2://{HOST}",
    ],
)
def test_provider_urls_are_rewritten_to_psycopg3(given: str) -> None:
    assert Settings(database_url=given).database_url == EXPECTED


def test_an_already_correct_url_is_left_alone() -> None:
    assert Settings(database_url=EXPECTED).database_url == EXPECTED


def test_query_string_and_credentials_survive_the_rewrite() -> None:
    """Rewriting the scheme must not disturb the password or sslmode."""
    url = Settings(database_url=f"postgresql://{HOST}").database_url
    assert url.endswith("?sslmode=require")
    assert "user:pw@" in url


def test_a_non_postgres_url_is_not_touched() -> None:
    """The rewrite is scoped to Postgres; it must not mangle anything else."""
    assert Settings(database_url="sqlite:///./x.db").database_url == "sqlite:///./x.db"
