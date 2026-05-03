# finimal-gamma-service

The gamma microservice should treat **`tradier-market`** as the only place for shared Tradier **market data** HTTP and parsing.

## Pin Predictor (5m RTH candles)

Import from this package instead of keeping a parallel `tradier_timesales` (or similar) module in the gamma repo:

```python
from tradier_market.timesales import fetch_5min_session_candles, parse_series_to_candles
```

- `fetch_5min_session_candles(symbol, session_date, access_token, …)` — GET `markets/timesales` for the regular session window, returns normalized OHLC rows (empty list on failure).
- `parse_series_to_candles(payload)` — pure parse of Tradier `series.data` JSON (used in tests and if you already have a response body).

## Option chains / quotes / expirations

Gamma’s scheduler uses `tradier_market.markets` (`fetch_option_expirations`, `fetch_option_chain`, `fetch_quote`) plus app-specific merging into internal strike maps — that orchestration correctly stays in **finimal-gamma-service** `adapters/`.

## Versioning

Pin a **git `rev`** (or tag) in the consumer’s `pyproject.toml` so CI and Docker builds stay reproducible.
