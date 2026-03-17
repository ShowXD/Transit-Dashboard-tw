from sqlalchemy import func, select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.parking_availability import ParkingAvailability
from app.models.parking_lot import ParkingLot
from app.models.road_section import RoadAvailability, RoadSection
from app.schemas.tdx import (
    CarParkAvailabilitySchema,
    CarParkSchema,
    RoadAvailabilitySchema,
    RoadSectionSchema,
)


async def upsert_parking_lots(
    session: AsyncSession, lots: list[CarParkSchema]
) -> None:
    if not lots:
        return
    stmt = insert(ParkingLot).values(
        [
            {
                "external_id": lot.car_park_id,
                "name": lot.name.zh_tw,
                "car_park_type": lot.car_park_type,
                "address": lot.address,
                "lat": lot.position.lat if lot.position else None,
                "lon": lot.position.lon if lot.position else None,
                "total_spaces": lot.total_spaces,
                "charge_description": lot.charge_description,
            }
            for lot in lots
        ]
    )
    await session.execute(
        stmt.on_conflict_do_update(
            index_elements=["external_id"],
            set_={
                "name": stmt.excluded.name,
                "car_park_type": stmt.excluded.car_park_type,
                "address": stmt.excluded.address,
                "lat": stmt.excluded.lat,
                "lon": stmt.excluded.lon,
                "total_spaces": stmt.excluded.total_spaces,
                "charge_description": stmt.excluded.charge_description,
                "updated_at": func.now(),
            },
        )
    )
    await session.commit()


async def upsert_parking_availability(
    session: AsyncSession, items: list[CarParkAvailabilitySchema]
) -> None:
    if not items:
        return
    id_map = await _lot_id_map(session, [i.car_park_id for i in items])
    rows = [
        {"lot_id": id_map[i.car_park_id], "available_spaces": i.available_spaces}
        for i in items
        if i.car_park_id in id_map
    ]
    if not rows:
        return
    stmt = insert(ParkingAvailability).values(rows)
    await session.execute(
        stmt.on_conflict_do_update(
            index_elements=["lot_id"],
            set_={
                "available_spaces": stmt.excluded.available_spaces,
                "updated_at": func.now(),
            },
        )
    )
    await session.commit()


async def upsert_road_sections(
    session: AsyncSession, sections: list[RoadSectionSchema]
) -> None:
    if not sections:
        return
    stmt = insert(RoadSection).values(
        [
            {
                "external_id": s.road_section_id,
                "road_name": s.road_name,
                "section_name": s.section_name,
                "total_spaces": s.total_spaces,
                "lat": s.lat,
                "lon": s.lon,
            }
            for s in sections
        ]
    )
    await session.execute(
        stmt.on_conflict_do_update(
            index_elements=["external_id"],
            set_={
                "road_name": stmt.excluded.road_name,
                "section_name": stmt.excluded.section_name,
                "total_spaces": stmt.excluded.total_spaces,
                "lat": stmt.excluded.lat,
                "lon": stmt.excluded.lon,
                "updated_at": func.now(),
            },
        )
    )
    await session.commit()


async def upsert_road_availability(
    session: AsyncSession, items: list[RoadAvailabilitySchema]
) -> None:
    if not items:
        return
    id_map = await _section_id_map(session, [i.road_section_id for i in items])
    rows = [
        {"section_id": id_map[i.road_section_id], "available_spaces": i.available_spaces}
        for i in items
        if i.road_section_id in id_map
    ]
    if not rows:
        return
    stmt = insert(RoadAvailability).values(rows)
    await session.execute(
        stmt.on_conflict_do_update(
            index_elements=["section_id"],
            set_={
                "available_spaces": stmt.excluded.available_spaces,
                "updated_at": func.now(),
            },
        )
    )
    await session.commit()


async def _lot_id_map(
    session: AsyncSession, external_ids: list[str]
) -> dict[str, int]:
    result = await session.execute(
        select(ParkingLot.id, ParkingLot.external_id).where(
            ParkingLot.external_id.in_(external_ids)
        )
    )
    return {row.external_id: row.id for row in result}


async def _section_id_map(
    session: AsyncSession, external_ids: list[str]
) -> dict[str, int]:
    result = await session.execute(
        select(RoadSection.id, RoadSection.external_id).where(
            RoadSection.external_id.in_(external_ids)
        )
    )
    return {row.external_id: row.id for row in result}
