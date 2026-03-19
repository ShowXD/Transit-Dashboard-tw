import asyncio

import httpx
import redis.asyncio as aioredis

from app.config import settings

_redis: aioredis.Redis | None = None
_redis_loop: asyncio.AbstractEventLoop | None = None
_TOKEN_KEY = "tdx:access_token"


def _get_redis() -> aioredis.Redis:
    global _redis, _redis_loop
    try:
        current_loop = asyncio.get_event_loop()
    except RuntimeError:
        current_loop = None
    if _redis is None or _redis_loop is not current_loop:
        _redis = aioredis.from_url(settings.redis_url, decode_responses=True)
        _redis_loop = current_loop
    return _redis


async def get_token() -> str:
    cached = await _get_redis().get(_TOKEN_KEY)
    if cached:
        return cached
    return await _fetch_token()


async def invalidate_token() -> None:
    await _get_redis().delete(_TOKEN_KEY)


async def _fetch_token() -> str:
    async with httpx.AsyncClient() as client:
        resp = await client.post(
            settings.tdx_auth_url,
            data={
                "grant_type": "client_credentials",
                "client_id": settings.tdx_client_id,
                "client_secret": settings.tdx_client_secret,
            },
        )
        resp.raise_for_status()

    data = resp.json()
    token: str = data["access_token"]
    ttl: int = max(data.get("expires_in", 3600) - 60, 60)
    await _get_redis().setex(_TOKEN_KEY, ttl, token)
    return token
