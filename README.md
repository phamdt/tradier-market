# tradier-market

Small **Python** client for [Tradier](https://documentation.tradier.com/) **market data** REST endpoints only (`markets/timesales`, `markets/history`, `markets/quotes`, `markets/options/*`). It does **not** implement brokerage account APIs (orders, balances, OAuth).

Used by `finimal-gamma-service` (Pin Predictor bundle) and `spx-gex` (live price timesales, etc.). **Do not** add Tradier to `schwab-core` — that package keeps Schwab response normalization only.

**Finimal** (`../finimal`) still owns **Tradier broker OAuth** (`app/services/tradier_oauth.py`) for linking user accounts; that is not market data and is not part of this library.

## Install

Declare a [Poetry git dependency](https://python-poetry.org/docs/dependency-specification/#git-dependencies) (no local path):

```toml
tradier-market = { git = "https://github.com/phamdt/tradier-market.git", branch = "main" }
```

Pin a tag or commit for reproducible builds:

```toml
tradier-market = { git = "https://github.com/phamdt/tradier-market.git", tag = "v0.1.0" }
# or: rev = "abc123..."
```

Replace the URL with your fork/org if different.

## Auth

Pass a **Bearer access token** (same value Tradier documents for API access). Env naming is left to each app (`TRADIER_ACCESS_TOKEN`, `TRADIER_TOKEN`, etc.).

## Windows

Use PowerShell at the repo root: `python3 -m poetry install` then `python3 -m poetry run pytest`.
