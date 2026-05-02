"""Tradier ``markets/history`` — daily (and other interval) bars."""

from __future__ import annotations

import logging
from datetime import date, timedelta
from typing import Any, Dict, List

from tradier_market.client import get_json

logger = logging.getLogger(__name__)


def parse_history_days(payload: Dict[str, Any]) -> List[Dict[str, Any]]:
    hist = payload.get("history")
    if not hist or not isinstance(hist, dict):
        return []
    day = hist.get("day")
    if day is None:
        return []
    if isinstance(day, dict):
        rows = [day]
    elif isinstance(day, list):
        rows = day
    else:
        return []

    out: List[Dict[str, Any]] = []
    for row in rows:
        if not isinstance(row, dict):
            continue
        ds = row.get("date")
        if ds is None:
            continue
        try:
            if isinstance(ds, date):
                d = ds
            else:
                d = date.fromisoformat(str(ds)[:10])
            o = float(row["open"])
            h = float(row["high"])
            lo = float(row["low"])
            c = float(row["close"])
        except (KeyError, TypeError, ValueError):
            continue
        out.append({"date": d, "open": o, "high": h, "low": lo, "close": c})
    out.sort(key=lambda r: r["date"])
    return out


def fetch_daily_bars(
    symbol: str,
    session_d: date,
    access_token: str,
    *,
    base_url: str = "https://api.tradier.com/v1",
    lookback_calendar_days: int = 28,
    timeout_sec: float = 20.0,
) -> List[Dict[str, Any]]:
    """
    Daily OHLC ending at session_d (inclusive). Each row: date, open, high, low, close.
    Returns [] on HTTP error or parse failure.
    """
    if not access_token or not symbol:
        return []
    start = session_d - timedelta(days=lookback_calendar_days)
    params = {
        "symbol": symbol.upper().replace("$", ""),
        "interval": "daily",
        "start": start.isoformat(),
        "end": session_d.isoformat(),
    }
    try:
        res = get_json(
            base_url=base_url,
            path="markets/history",
            params=params,
            access_token=access_token,
            timeout_s=timeout_sec,
        )
        if res.status_code != 200:
            logger.warning(
                "Tradier daily history HTTP %s for %s",
                res.status_code,
                symbol,
            )
            return []
        payload = res.json_body if isinstance(res.json_body, dict) else {}
    except Exception as exc:
        logger.warning("Tradier daily history request failed: %s", exc)
        return []

    return parse_history_days(payload)
