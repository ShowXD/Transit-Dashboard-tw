from unittest.mock import AsyncMock, MagicMock, patch

import pytest

import app.services.tdx_auth as auth_mod


@pytest.fixture(autouse=True)
def reset_redis_singleton():
    """Prevent singleton state leaking between tests."""
    auth_mod._redis = None
    yield
    auth_mod._redis = None


def _make_mock_redis(cached_token: str | None = None) -> AsyncMock:
    r = AsyncMock()
    r.get.return_value = cached_token
    r.setex = AsyncMock()
    r.delete = AsyncMock()
    return r


def _make_mock_http_response(token: str = "fresh_token", expires_in: int = 3600):
    resp = MagicMock()
    resp.raise_for_status = MagicMock()
    resp.json.return_value = {"access_token": token, "expires_in": expires_in}
    return resp


@pytest.mark.asyncio
async def test_returns_cached_token_without_http_call() -> None:
    mock_redis = _make_mock_redis(cached_token="cached_abc")

    with patch("app.services.tdx_auth._get_redis", return_value=mock_redis):
        token = await auth_mod.get_token()

    assert token == "cached_abc"
    mock_redis.get.assert_called_once_with(auth_mod._TOKEN_KEY)


@pytest.mark.asyncio
async def test_fetches_and_caches_token_when_cache_empty() -> None:
    mock_redis = _make_mock_redis(cached_token=None)
    mock_resp = _make_mock_http_response(token="new_token", expires_in=3600)

    mock_http = AsyncMock()
    mock_http.__aenter__.return_value = mock_http
    mock_http.__aexit__.return_value = None
    mock_http.post.return_value = mock_resp

    with (
        patch("app.services.tdx_auth._get_redis", return_value=mock_redis),
        patch("httpx.AsyncClient", return_value=mock_http),
    ):
        token = await auth_mod.get_token()

    assert token == "new_token"
    mock_redis.setex.assert_called_once_with(auth_mod._TOKEN_KEY, 3540, "new_token")


@pytest.mark.asyncio
async def test_ttl_uses_minimum_of_60_seconds() -> None:
    mock_redis = _make_mock_redis(cached_token=None)
    mock_resp = _make_mock_http_response(token="t", expires_in=30)

    mock_http = AsyncMock()
    mock_http.__aenter__.return_value = mock_http
    mock_http.__aexit__.return_value = None
    mock_http.post.return_value = mock_resp

    with (
        patch("app.services.tdx_auth._get_redis", return_value=mock_redis),
        patch("httpx.AsyncClient", return_value=mock_http),
    ):
        await auth_mod.get_token()

    _, args, _ = mock_redis.setex.mock_calls[0]
    assert args[1] == 60  # min TTL floor


@pytest.mark.asyncio
async def test_invalidate_token_deletes_key() -> None:
    mock_redis = _make_mock_redis()

    with patch("app.services.tdx_auth._get_redis", return_value=mock_redis):
        await auth_mod.invalidate_token()

    mock_redis.delete.assert_called_once_with(auth_mod._TOKEN_KEY)
