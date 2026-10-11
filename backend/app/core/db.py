"""Database engine, session factory, and the FastAPI dependency.

Sync SQLAlchemy by choice: async adds real complexity (session scoping, greenlet
errors, a second mental model) and buys nothing at this scale. A sync session is
easier to reason about and easier to defend in a viva.
"""

from collections.abc import Iterator

from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session, sessionmaker

from app.core.config import get_settings


def build_engine() -> Engine:
    settings = get_settings()
    return create_engine(
        settings.database_url,
        # Free-tier instances spin down and drop connections; without this the
        # first request after idle fails with a stale-connection error.
        pool_pre_ping=True,
        pool_size=5,
        max_overflow=5,
        echo=settings.debug,
    )


engine = build_engine()
SessionLocal = sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)


def get_db() -> Iterator[Session]:
    """FastAPI dependency. One session per request, always closed."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def check_connection() -> tuple[bool, str | None]:
    """Report database reachability without raising.

    Used by /health/deep: a health endpoint must describe a broken database,
    not become one more thing that returns 500.
    """
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return True, None
    # Deliberately broad: any failure at all - driver, DNS, auth, timeout -
    # is simply 'the database is not reachable' as far as a health check goes.
    except Exception as exc:
        return False, f"{type(exc).__name__}: {exc}"[:200]
