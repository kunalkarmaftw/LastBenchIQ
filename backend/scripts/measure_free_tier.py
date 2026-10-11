"""Measure what the free tier actually does (EPIC 0.4).

The plan assumes things about cold starts, memory and rate limits that nobody
has verified. This script replaces each assumption with a number.

    python scripts/measure_free_tier.py --url https://lastbenchiq-api.onrender.com

It measures; it does not fix. Record the output in docs/KNOWLEDGE_BASE.md and
flag any NFR the numbers contradict.
"""

from __future__ import annotations

import argparse
import json
import statistics
import sys
import time
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import urlparse
from urllib.request import Request, urlopen

# From TECH_SPEC section 6. Measured values are compared against these.
NFR_DASHBOARD_SECONDS = 1.0
NFR_ANALYSIS_SECONDS = 30.0


def _require_http_url(url: str) -> str:
    """Reject anything that is not http(s).

    urlopen will happily open file:// and other schemes, so an unvalidated
    --url turns this script into a file reader. Checking the scheme is the fix;
    silencing the linter is not.
    """
    scheme = urlparse(url).scheme
    if scheme not in {"http", "https"}:
        raise ValueError(f"--url must be http or https, got {scheme or 'no scheme'!r}")
    return url


def _get(url: str, timeout: float = 90.0) -> tuple[float, int, dict[str, Any] | None]:
    """Return (elapsed_seconds, status_code, parsed_body)."""
    _require_http_url(url)
    started = time.perf_counter()
    try:
        # S310: the scheme is validated by _require_http_url above, which ruff
        # cannot see through. The check is real; the warning is static-only.
        request = Request(url, headers={"User-Agent": "lastbenchiq-measure"})  # noqa: S310
        with urlopen(request, timeout=timeout) as r:  # noqa: S310
            raw = r.read()
            status = r.status
    except HTTPError as exc:
        return time.perf_counter() - started, exc.code, None
    except (URLError, TimeoutError) as exc:
        print(f"  request failed: {exc}")
        return time.perf_counter() - started, 0, None

    elapsed = time.perf_counter() - started
    try:
        return elapsed, status, json.loads(raw)
    except json.JSONDecodeError:
        return elapsed, status, None


def measure_warm_latency(base: str, samples: int = 8) -> None:
    print(f"\n[2] Warm latency over {samples} requests")
    timings = []
    for _ in range(samples):
        elapsed, status, _ = _get(f"{base}/api/v1/health")
        if status == 200:
            timings.append(elapsed)
        time.sleep(0.3)

    if not timings:
        print("  no successful requests")
        return

    median = statistics.median(timings)
    worst = max(timings)
    print(f"  median {median * 1000:7.0f} ms")
    print(f"  worst  {worst * 1000:7.0f} ms")
    verdict = "OK" if worst < NFR_DASHBOARD_SECONDS else "VIOLATES NFR"
    print(f"  NFR dashboard < {NFR_DASHBOARD_SECONDS}s -> {verdict}")


def measure_cold_start(base: str, idle_minutes: float) -> None:
    print(f"\n[3] Cold start after {idle_minutes:g} minutes idle")
    if idle_minutes <= 0:
        print("  skipped (pass --idle-minutes 16 to measure; Render sleeps at ~15)")
        return

    print(f"  sleeping {idle_minutes:g} min so the instance spins down...")
    time.sleep(idle_minutes * 60)

    elapsed, status, _ = _get(f"{base}/api/v1/health")
    print(f"  first request after idle: {elapsed:.1f}s (status {status})")
    if elapsed > 5:
        print("  NOTE: this is what a student meets when they open the app after")
        print("        a quiet period. Budget for it in the UI, or keep it warm.")


def check_dependencies(base: str) -> bool:
    print("\n[1] Deployed dependencies (/health/deep)")
    elapsed, status, body = _get(f"{base}/api/v1/health/deep")
    if status != 200 or body is None:
        print(f"  FAILED - status {status}. The deploy is not healthy.")
        return False

    print(f"  responded in {elapsed:.1f}s with status '{body.get('status')}'")
    for name, present in (body.get("packages") or {}).items():
        print(f"    {'OK  ' if present else 'MISS'} {name}")
    print(
        f"    {'OK  ' if body.get('tesseract_binary') != 'MISSING' else 'MISS'} "
        f"tesseract -> {body.get('tesseract_binary')}"
    )
    print(
        f"    {'OK  ' if body.get('database') == 'connected' else 'MISS'} "
        f"database -> {body.get('database')}"
    )
    if body.get("database_error"):
        print(f"      {body['database_error']}")

    if body.get("status") != "ok":
        print("\n  >>> STOP. A degraded deploy means the free tier cannot carry")
        print("      this dependency tree. Fix it now - that is what EPIC 0 is for.")
        return False
    return True


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", required=True, help="deployed API base URL")
    parser.add_argument("--idle-minutes", type=float, default=0.0)
    parser.add_argument("--samples", type=int, default=8)
    args = parser.parse_args()

    try:
        base = _require_http_url(args.url.rstrip("/"))
    except ValueError as exc:
        print(f"error: {exc}")
        return 2
    print("=" * 62)
    print(f"Free-tier measurement - {base}")
    print("=" * 62)

    healthy = check_dependencies(base)
    measure_warm_latency(base, args.samples)
    measure_cold_start(base, args.idle_minutes)

    print("\n" + "=" * 62)
    print("Record these numbers in docs/KNOWLEDGE_BASE.md section 6.")
    print("Still to measure by hand (needs an API key):")
    print("  - Groq rate limit: send requests until a real 429, note the limit")
    print("  - Memory headroom: Render dashboard, under load")
    print("  - Time to process one 20-question paper end to end")
    print("=" * 62)
    return 0 if healthy else 1


if __name__ == "__main__":
    sys.exit(main())
