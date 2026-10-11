"""FastAPI application entrypoint.

Deliberately thin. Routers validate and delegate; business logic lives in
`app/services/` so it stays testable without an HTTP client.
"""

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from typing import Any

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.auth import router as auth_router
from app.api.health import router as health_router
from app.core.config import get_settings


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    settings = get_settings()
    settings.validate_production()
    # ML models are loaded once here, not per request (TECH_SPEC §5.2).
    app.state.ml_models = {}
    yield


def create_app() -> FastAPI:
    settings = get_settings()
    app = FastAPI(
        title="LastBenchIQ API",
        version="0.1.0",
        docs_url="/docs",
        lifespan=lifespan,
    )
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.include_router(health_router, prefix="/api/v1")
    app.include_router(auth_router, prefix="/api/v1")
    return app


app = create_app()


@app.get("/")
def root() -> dict[str, Any]:
    return {"service": "LastBenchIQ", "docs": "/docs"}
