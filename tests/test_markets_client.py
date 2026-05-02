from __future__ import annotations

from unittest.mock import MagicMock, patch

import pytest

from tradier_market.client import TradierResult
from tradier_market.markets import PRODUCTION_BASE, fetch_quote


def _mock_response(status: int, body: dict) -> MagicMock:
    r = MagicMock()
    r.status_code = status
    r.url = "https://api.tradier.com/v1/markets/quotes?symbols=SPX"
    r.json.return_value = body
    r.raise_for_status = MagicMock()
    return r


@patch("tradier_market.client.httpx.Client")
def test_fetch_quote_returns_result(mock_client_cls: MagicMock) -> None:
    body = {"quotes": {"quote": {"symbol": "SPX", "last": 5500.0}}}
    mock_client_cls.return_value.__enter__.return_value.get.return_value = _mock_response(200, body)

    result = fetch_quote(symbols=["SPX"], token="tok", base_url=PRODUCTION_BASE)

    assert isinstance(result, TradierResult)
    assert result.status_code == 200
    assert result.json_body == body


@patch("tradier_market.client.httpx.Client")
def test_fetch_quote_raises_on_http_error(mock_client_cls: MagicMock) -> None:
    mock_resp = _mock_response(401, {})
    mock_resp.raise_for_status.side_effect = Exception("401 Unauthorized")
    mock_client_cls.return_value.__enter__.return_value.get.return_value = mock_resp

    with pytest.raises(Exception, match="401"):
        fetch_quote(symbols=["SPX"], token="bad-token", base_url=PRODUCTION_BASE)
