from unittest.mock import AsyncMock, patch

import pytest
from httpx import AsyncClient

from app.schemas.parking import ParkingLotResponse, RoadSectionResponse

_LOT = ParkingLotResponse(
    id=1,
    external_id="TC001",
    name="台中火車站停車場",
    car_park_type=1,
    address="台中市中區台灣大道一段",
    lat=24.1367,
    lon=120.6850,
    total_spaces=200,
    available_spaces=42,
    charge_description="每小時 30 元",
)

_SECTION = RoadSectionResponse(
    id=1,
    external_id="RS001",
    road_name="台灣大道",
    section_name="一段",
    lat=24.1367,
    lon=120.6850,
    total_spaces=20,
    available_spaces=5,
)


@pytest.mark.asyncio
async def test_list_lots_empty(client: AsyncClient) -> None:
    with patch(
        "app.routers.parking.get_lots",
        new=AsyncMock(return_value=([], 0)),
    ):
        resp = await client.get("/api/v1/parking/lots")
    assert resp.status_code == 200
    body = resp.json()
    assert body["data"] == []
    assert body["total"] == 0


@pytest.mark.asyncio
async def test_list_lots_returns_data(client: AsyncClient) -> None:
    with patch(
        "app.routers.parking.get_lots",
        new=AsyncMock(return_value=([_LOT], 1)),
    ):
        resp = await client.get("/api/v1/parking/lots")
    assert resp.status_code == 200
    body = resp.json()
    assert body["total"] == 1
    assert body["data"][0]["name"] == "台中火車站停車場"
    assert body["data"][0]["available_spaces"] == 42


@pytest.mark.asyncio
async def test_get_lot_by_id_found(client: AsyncClient) -> None:
    with patch(
        "app.routers.parking.get_lot_by_id",
        new=AsyncMock(return_value=_LOT),
    ):
        resp = await client.get("/api/v1/parking/lots/1")
    assert resp.status_code == 200
    assert resp.json()["external_id"] == "TC001"


@pytest.mark.asyncio
async def test_get_lot_by_id_not_found(client: AsyncClient) -> None:
    with patch(
        "app.routers.parking.get_lot_by_id",
        new=AsyncMock(return_value=None),
    ):
        resp = await client.get("/api/v1/parking/lots/999")
    assert resp.status_code == 404


@pytest.mark.asyncio
async def test_list_road_sections_empty(client: AsyncClient) -> None:
    with patch(
        "app.routers.parking.get_road_sections",
        new=AsyncMock(return_value=([], 0)),
    ):
        resp = await client.get("/api/v1/parking/road-sections")
    assert resp.status_code == 200
    assert resp.json()["total"] == 0


@pytest.mark.asyncio
async def test_list_road_sections_with_geo_filter(client: AsyncClient) -> None:
    with patch(
        "app.routers.parking.get_road_sections",
        new=AsyncMock(return_value=([_SECTION], 1)),
    ):
        resp = await client.get(
            "/api/v1/parking/road-sections",
            params={"lat": 24.1367, "lon": 120.685, "radius_m": 500},
        )
    assert resp.status_code == 200
    body = resp.json()
    assert body["total"] == 1
    assert body["data"][0]["road_name"] == "台灣大道"
