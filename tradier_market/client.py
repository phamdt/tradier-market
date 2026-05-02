"""Low-level HTTP GET with Bearer auth and simple 429 retry."""

from __future__ import annotations

import time
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any

import httpx


@dataclass(frozen=True)
class TradierResult:
    url: str
    status_code: int
    took_ms: int
    json_body: Any


def get_json(
    *,
    base_url: str,
    path: str,
    params: dict[str, Any],
    access_token: str,
    timeout_s: float = 30.0,
    max_retries: int = 2,
) -> TradierResult:
    """
    GET ``{base_url}/{path}`` with Bearer token.

    Retries on HTTP 429 with exponential backoff. Raises on final non-success.
    """
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Accept": "application/json",
    }
    root = base_url.rstrip("/")
    rel = path.lstrip("/")
    url = f"{root}/{rel}"
    last_exc: Exception | None = None

    for attempt in range(max_retries + 1):
        with httpx.Client(timeout=timeout_s) as client:
            start = datetime.now(timezone.utc)
            r = client.get(url, params=params, headers=headers)
            took_ms = int((datetime.now(timezone.utc) - start).total_seconds() * 1000)

        if r.status_code == 429:
            wait = min(60.0, 2.0 * (attempt + 1))
            time.sleep(wait)
            if attempt < max_retries:
                continue

        try:
            r.raise_for_status()
            return TradierResult(
                url=str(r.url),
                status_code=r.status_code,
                took_ms=took_ms,
                json_body=r.json(),
            )
        except Exception as exc:
            last_exc = exc
            if r.status_code == 429 and attempt < max_retries:
                continue
            raise

    assert last_exc is not None
    raise last_exc
