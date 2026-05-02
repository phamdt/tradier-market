"""Tradier market endpoints: quotes, option expirations, option chains."""

from __future__ import annotations

from tradier_market.client import TradierResult, get_json

PRODUCTION_BASE = "https://api.tradier.com/v1"
SANDBOX_BASE = "https://sandbox.tradier.com/v1"


def fetch_quote(
    *,
    symbols: list[str],
    token: str,
    base_url: str = PRODUCTION_BASE,
    timeout_s: float = 15.0,
    max_retries: int = 2,
) -> TradierResult:
    """GET /markets/quotes — one or more symbols."""
    return get_json(
        base_url=base_url,
        path="markets/quotes",
        params={"symbols": ",".join(symbols), "greeks": "false"},
        access_token=token,
        timeout_s=timeout_s,
        max_retries=max_retries,
    )


def fetch_option_expirations(
    *,
    symbol: str,
    token: str,
    base_url: str = PRODUCTION_BASE,
    timeout_s: float = 15.0,
    max_retries: int = 2,
) -> TradierResult:
    """GET /markets/options/expirations."""
    return get_json(
        base_url=base_url,
        path="markets/options/expirations",
        params={"symbol": symbol, "includeAllRoots": "true"},
        access_token=token,
        timeout_s=timeout_s,
        max_retries=max_retries,
    )


def fetch_option_chain(
    *,
    symbol: str,
    expiration: str,
    token: str,
    base_url: str = PRODUCTION_BASE,
    greeks: bool = True,
    timeout_s: float = 15.0,
    max_retries: int = 2,
) -> TradierResult:
    """GET /markets/options/chains."""
    return get_json(
        base_url=base_url,
        path="markets/options/chains",
        params={
            "symbol": symbol,
            "expiration": expiration,
            "greeks": "true" if greeks else "false",
        },
        access_token=token,
        timeout_s=timeout_s,
        max_retries=max_retries,
    )
