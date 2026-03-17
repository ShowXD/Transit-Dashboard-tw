from unittest.mock import AsyncMock, MagicMock, patch

import httpx
import pytest

from app.services.tdx_client import TDXRateLimitError, get


def _mock_response(status_code: int = 200, json_data: list | None = None) -> MagicMock:
    resp = MagicMock(spec=httpx.Response)
    resp.status_code = status_code
    resp.json.return_value = json_data or []
    resp.raise_for_status = MagicMock(
        side_effect=None if status_code < 400 else httpx.HTTPStatusError(
            "error", request=MagicMock(), response=resp
        )
    )
    return resp


def _mock_client(responses: list) -> AsyncMock:
    client = AsyncMock(spec=httpx.AsyncClient)
    client.__aenter__.return_value = client
    client.__aexit__.return_value = None
    client.get.side_effect = responses
    return client


@pytest.mark.asyncio
async def test_successful_get_returns_json() -> None:
    payload = [{"CarParkID": "A001", "AvailableSpaces": 10}]
    client = _mock_client([_mock_response(200, payload)])

    with (
        patch("app.services.tdx_client.get_token", new=AsyncMock(return_value="tok")),
        patch("httpx.AsyncClient", return_value=client),
    ):
        result = await get("/v2/Parking/OffStreet/CarPark/City/Taichung")

    assert result == payload


@pytest.mark.asyncio
async def test_401_invalidates_token_and_retries() -> None:
    payload = [{"CarParkID": "A001"}]
    client = _mock_client([
        _mock_response(401),
        _mock_response(200, payload),
    ])

    mock_invalidate = AsyncMock()
    with (
        patch("app.services.tdx_client.get_token", new=AsyncMock(return_value="tok")),
        patch("app.services.tdx_client.invalidate_token", mock_invalidate),
        patch("httpx.AsyncClient", return_value=client),
    ):
        result = await get("/some/path")

    mock_invalidate.assert_called_once()
    assert result == payload


@pytest.mark.asyncio
async def test_429_raises_rate_limit_error() -> None:
    client = _mock_client([_mock_response(429)])

    with (
        patch("app.services.tdx_client.get_token", new=AsyncMock(return_value="tok")),
        patch("httpx.AsyncClient", return_value=client),
    ):
        with pytest.raises(TDXRateLimitError):
            await get("/some/path")
