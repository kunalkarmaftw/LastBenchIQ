"""Application settings, loaded from the environment.

Every secret arrives through here. Nothing is hardcoded, and `.env` is gitignored,
so there is one place to audit before the repo is ever shared or submitted.
"""

from functools import lru_cache
from typing import Literal

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

# A deliberate sentinel, not a credential: `validate_production()` refuses to start
# if this value survives into production. Named once so the security linter has a
# single, reviewable place to be told so.
DEV_SECRET_SENTINEL = "dev-only-not-a-real-secret"  # noqa: S105

# Hosted Postgres providers (Neon, Render, Supabase, Heroku) hand out URLs starting
# `postgres://` or `postgresql://`. SQLAlchemy reads that prefix as "use psycopg2",
# a driver this project does not install, and fails at import with a stack trace
# that never mentions the URL. The project uses psycopg 3, so the prefix is
# normalised here instead of being a step a human has to remember - on a laptop at
# 2am, and again in the Render dashboard on deploy day.
_DRIVER = "postgresql+psycopg"
_REWRITE_PREFIXES = ("postgres://", "postgresql://", "postgresql+psycopg2://")


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    environment: Literal["local", "ci", "production"] = "local"
    debug: bool = False

    # --- database -----------------------------------------------------------
    database_url: str = "postgresql+psycopg://lastbench:lastbench@localhost:5432/lastbenchiq"

    # --- auth ---------------------------------------------------------------
    # Default is a throwaway for local/CI only. Production refuses to start
    # without a real value — see `validate_production()`.
    secret_key: str = DEV_SECRET_SENTINEL
    access_token_expire_minutes: int = 60 * 24

    # --- LLM ----------------------------------------------------------------
    llm_api_key: str = ""
    llm_model: str = "llama-3.3-70b-versatile"

    # --- limits -------------------------------------------------------------
    max_upload_mb: int = 20
    agent_max_iterations: int = 8
    agent_timeout_seconds: int = 90

    # --- analysis thresholds (DATA_MODEL: minimum data rule) ----------------
    min_papers_for_analysis: int = 3
    min_questions_for_analysis: int = 50

    cors_origins: list[str] = Field(default_factory=lambda: ["http://localhost:5173"])

    @field_validator("database_url")
    @classmethod
    def normalise_driver(cls, v: str) -> str:
        for prefix in _REWRITE_PREFIXES:
            if v.startswith(prefix):
                return f"{_DRIVER}://{v[len(prefix) :]}"
        return v

    def validate_production(self) -> None:
        """Fail fast rather than deploy with the development secret."""
        if self.environment != "production":
            return
        if self.secret_key == DEV_SECRET_SENTINEL:
            raise RuntimeError("SECRET_KEY must be set in production")
        if not self.llm_api_key:
            raise RuntimeError("LLM_API_KEY must be set in production")


@lru_cache
def get_settings() -> Settings:
    return Settings()
