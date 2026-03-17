"""Integration tests for upsert helpers — require a running PostgreSQL (via docker compose).

Run with: docker compose exec api pytest tests/test_upsert.py
"""

import pytest
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import AsyncSessionLocal
from app.models.parking_availability import ParkingAvailability
from app.models.parking_lot import ParkingLot
from app.schemas.tdx import CarParkAvailabilitySchema, CarParkSchema, _LocalizedName, _Position
from app.services.upsert import upsert_parking_availability, upsert_parking_lots


@pytest.fixture
async def db() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        yield session
        await session.rollback()  # clean up after each test


def _make_lot(external_id: str, name: str = "Test Lot", total: int = 100) -> CarParkSchema:
    return CarParkSchema(
        CarParkID=external_id,
        CarParkName={"Zh_tw": name},
        CarParkType=1,
        Address="台中市某路1號",
        CarParkPosition={"PositionLat": 24.148, "PositionLon": 120.674},
        TotalSpaces=total,
        ChargeDescription=None,
    )


def _make_avail(external_id: str, spaces: int) -> CarParkAvailabilitySchema:
    return CarParkAvailabilitySchema(CarParkID=external_id, AvailableSpaces=spaces)


@pytest.mark.asyncio
async def test_upsert_parking_lots_inserts_new_row(db: AsyncSession) -> None:
    await upsert_parking_lots(db, [_make_lot("TEST001", "停車場甲", 50)])

    result = await db.execute(
        select(ParkingLot).where(ParkingLot.external_id == "TEST001")
    )
    lot = result.scalar_one()
    assert lot.name == "停車場甲"
    assert lot.total_spaces == 50


@pytest.mark.asyncio
async def test_upsert_parking_lots_updates_existing_row(db: AsyncSession) -> None:
    await upsert_parking_lots(db, [_make_lot("TEST002", "舊名稱", 80)])
    await upsert_parking_lots(db, [_make_lot("TEST002", "新名稱", 90)])

    result = await db.execute(
        select(ParkingLot).where(ParkingLot.external_id == "TEST002")
    )
    lots = result.scalars().all()
    assert len(lots) == 1
    assert lots[0].name == "新名稱"
    assert lots[0].total_spaces == 90


@pytest.mark.asyncio
async def test_upsert_parking_availability_updates_spaces(db: AsyncSession) -> None:
    await upsert_parking_lots(db, [_make_lot("TEST003", "停車場丙", 100)])

    await upsert_parking_availability(db, [_make_avail("TEST003", 42)])
    await upsert_parking_availability(db, [_make_avail("TEST003", 15)])

    lot = (await db.execute(
        select(ParkingLot).where(ParkingLot.external_id == "TEST003")
    )).scalar_one()
    avail = (await db.execute(
        select(ParkingAvailability).where(ParkingAvailability.lot_id == lot.id)
    )).scalar_one()
    assert avail.available_spaces == 15


@pytest.mark.asyncio
async def test_upsert_availability_skips_unknown_external_ids(db: AsyncSession) -> None:
    await upsert_parking_availability(db, [_make_avail("NONEXISTENT_ID", 5)])
    # Should not raise — unknown IDs are silently skipped
