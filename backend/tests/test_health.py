import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_health_returns_ok(client: AsyncClient) -> None:
    response = await client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert "env" in data


@pytest.mark.asyncio
async def test_parking_lots_endpoint_exists(client: AsyncClient) -> None:
    response = await client.get("/api/v1/parking/lots")
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_road_sections_endpoint_exists(client: AsyncClient) -> None:
    response = await client.get("/api/v1/parking/road-sections")
    assert response.status_code == 200
