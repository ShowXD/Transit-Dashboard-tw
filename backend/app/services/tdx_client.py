import httpx

from app.config import settings
from app.services.tdx_auth import get_token, invalidate_token


class TDXRateLimitError(Exception):
    pass


async def get(path: str, params: dict | None = None) -> list[dict]:
    """GET a TDX endpoint, handling token refresh and rate-limit errors."""
    async with httpx.AsyncClient(
        base_url=settings.tdx_base_url,
        timeout=httpx.Timeout(30.0),
    ) as client:
        resp = await _request(client, path, params)

        if resp.status_code == 401:
            await invalidate_token()
            resp = await _request(client, path, params)

        if resp.status_code == 429:
            raise TDXRateLimitError(path)

        resp.raise_for_status()
        return resp.json()


async def _request(
    client: httpx.AsyncClient,
    path: str,
    params: dict | None,
) -> httpx.Response:
    token = await get_token()
    return await client.get(
        path,
        headers={"Authorization": f"Bearer {token}"},
        params=params,
    )
