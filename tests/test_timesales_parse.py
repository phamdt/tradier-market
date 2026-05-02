from __future__ import annotations

from tradier_market.timesales import parse_series_to_candles


def test_parse_series_to_candles_list_row():
    payload = {
        "series": {
            "data": [
                {
                    "time": "2026-05-01T10:30:00",
                    "open": 100.0,
                    "high": 101.0,
                    "low": 99.0,
                    "close": 100.5,
                    "volume": 1000,
                }
            ]
        }
    }
    candles = parse_series_to_candles(payload)
    assert len(candles) == 1
    assert candles[0]["open"] == 100.0
    assert candles[0]["close"] == 100.5
    assert "2026-05-01" in candles[0]["time"]


def test_parse_series_single_dict_row():
    payload = {
        "series": {
            "data": {
                "time": "2026-05-01T10:35:00",
                "open": 1,
                "high": 2,
                "low": 0.5,
                "close": 1.5,
            }
        }
    }
    assert len(parse_series_to_candles(payload)) == 1
