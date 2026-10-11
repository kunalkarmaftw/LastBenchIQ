"""Health and readiness endpoints.

`/health/deep` exists for EPIC 0: it reports whether the heavy dependencies and
the Tesseract system binary are actually present in the deployed environment.
That is the week-1 question the audit flagged as the project's second-biggest
risk, answered by a URL instead of by hoping.
"""

import importlib.util
import shutil
from typing import Any

from fastapi import APIRouter

router = APIRouter(tags=["health"])

_HEAVY_DEPENDENCIES = ("sklearn", "pandas", "numpy", "fitz", "pytesseract")


@router.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@router.get("/health/deep")
def health_deep() -> dict[str, Any]:
    """Report what is genuinely installed, so deploy problems surface in week 1."""
    packages = {name: importlib.util.find_spec(name) is not None for name in _HEAVY_DEPENDENCIES}
    tesseract_path = shutil.which("tesseract")
    return {
        "status": "ok" if all(packages.values()) else "degraded",
        "packages": packages,
        "tesseract_binary": tesseract_path or "MISSING",
    }
