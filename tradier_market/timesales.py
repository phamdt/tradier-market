"""Tradier ``markets/timesales`` — intraday bars (e.g. 5m RTH for Pin Predictor)."""

from __future__ import annotations

import logging
from datetime import date, datetime, time
from typing import Any, Dict, List, Optional

from tradier_market.client import get_json

logger = logging.getLogger(__name__)


def _et_open_close_strings(session_d: date, end_dt_et: Optional[datetime] = None) -> tuple[str, str]:
    """Build Tradier start/end as 'YYYY-MM-DD HH:MM' in America/New_York wall time."""
    from zoneinfo import ZoneInfo

    et = ZoneInfo("America/New_York")
    start_local = datetime.combine(session_d, time(9, 30), tzinfo=et)
    start_s = start_local.strftime("%Y-%m-%d %H:%M")
    if end_dt_et is None:
        end_dt_et = datetime.now(et)
    end_s = end_dt_et.strftime("%Y-%m-%d %H:%M")
    return start_s, end_s


def parse_series_to_candles(payload: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Map Tradier JSON (series.data) to [{time, open, high, low, close}, ...]."""
    series = payload.get("series")
    if not series or not isinstance(series, dict):
        return []
    data = series.get("data")
    if data is None:
        return []
    if isinstance(data, dict):
        rows = [data]
    elif isinstance(data, list):
        rows = data
    else:
        return []

    out: List[Dict[str, Any]] = []
    for row in rows:
        if not isinstance(row, dict):
            continue
        t = row.get("time")
        if t is None:
            continue
        try:
            o = float(row["open"])
            h = float(row["high"])
            lo = float(row["low"])
            c = float(row["close"])
        except (KeyError, TypeError, ValueError):
            continue
        time_str = t if isinstance(t, str) else str(t)
        out.append({"time": time_str, "open": o, "high": h, "low": lo, "close": c})
    return out


def fetch_5min_session_candles(
    symbol: str,
    session_date: date,
    access_token: str,
    *,
    base_url: str = "https://api.tradier.com/v1",
    end_dt_et: Optional[datetime] = None,
    timeout_sec: float = 30.0,
) -> List[Dict[str, Any]]:
    """
    GET Tradier timesales (5min, regular session) and map to candle rows.

    Returns [] on HTTP error, empty payload, or parse failure (caller hides candle layer).
    """
    if not access_token or not symbol:
        return []

    start_s, end_s = _et_open_close_strings(session_date, end_dt_et)
    params = {
        "symbol": symbol.upper(),
        "interval": "5min",
        "start": start_s,
        "end": end_s,
        "session_filter": "open",
    }
    try:
        res = get_json(
            base_url=base_url,
            path="markets/timesales",
            params=params,
            access_token=access_token,
            timeout_s=timeout_sec,
        )
        if res.status_code != 200:
            return []
        payload = res.json_body if isinstance(res.json_body, dict) else {}
    except Exception as exc:
        logger.warning("Tradier timesales request failed: %s", exc)
        return []

    return parse_series_to_candles(payload)


def fetch_timesales(
    symbol: str,
    *,
    interval: str,
    start: str,
    end: str,
    access_token: str,
    session_filter: str = "open",
    base_url: str = "https://api.tradier.com/v1",
    timeout_sec: float = 30.0,
) -> dict[str, Any]:
    """GET timesales; returns parsed JSON dict (raises on HTTP error)."""
    params = {
        "symbol": symbol.upper(),
        "interval": interval,
        "start": start,
        "end": end,
        "session_filter": session_filter,
    }
    res = get_json(
        base_url=base_url,
        path="markets/timesales",
        params=params,
        access_token=access_token,
        timeout_s=timeout_sec,
    )
    return res.json_body if isinstance(res.json_body, dict) else {}
