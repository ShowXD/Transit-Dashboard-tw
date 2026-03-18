from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.parking_availability import ParkingAvailability
from app.models.parking_lot import ParkingLot
from app.models.road_section import RoadAvailability, RoadSection
from app.schemas.parking import ParkingLotResponse, RoadSectionResponse

# Earth radius in metres
_EARTH_RADIUS_M = 6_371_000.0


def _haversine_dist(lat_col, lon_col, lat: float, lon: float):
    """SQLAlchemy expression for approximate distance in metres (Haversine)."""
    dlat = func.radians(lat_col - lat)
    dlon = func.radians(lon_col - lon)
    lat1 = func.radians(lat)
    lat2 = func.radians(lat_col)
    a = (
        func.pow(func.sin(dlat / 2), 2)
        + func.cos(lat1) * func.cos(lat2) * func.pow(func.sin(dlon / 2), 2)
    )
    return 2 * _EARTH_RADIUS_M * func.asin(func.sqrt(a))


async def get_lots(
    session: AsyncSession,
    lat: float | None,
    lon: float | None,
    radius_m: int,
    skip: int,
    limit: int,
) -> tuple[list[ParkingLotResponse], int]:
    base_q = (
        select(
            ParkingLot,
            ParkingAvailability.available_spaces,
        )
        .outerjoin(
            ParkingAvailability,
            ParkingAvailability.lot_id == ParkingLot.id,
        )
    )

    if lat is not None and lon is not None:
        dist = _haversine_dist(ParkingLot.lat, ParkingLot.lon, lat, lon)
        base_q = base_q.where(dist <= radius_m)

    total = (await session.execute(
        select(func.count()).select_from(base_q.subquery())
    )).scalar_one()

    rows = (await session.execute(base_q.offset(skip).limit(limit))).all()

    items = [
        ParkingLotResponse(
            **{c.key: getattr(lot, c.key) for c in ParkingLot.__table__.columns},
            available_spaces=avail,
        )
        for lot, avail in rows
    ]
    return items, total


async def get_lot_by_id(
    session: AsyncSession,
    lot_id: int,
) -> ParkingLotResponse | None:
    row = (await session.execute(
        select(ParkingLot, ParkingAvailability.available_spaces)
        .outerjoin(ParkingAvailability, ParkingAvailability.lot_id == ParkingLot.id)
        .where(ParkingLot.id == lot_id)
    )).first()

    if row is None:
        return None

    lot, avail = row
    return ParkingLotResponse(
        **{c.key: getattr(lot, c.key) for c in ParkingLot.__table__.columns},
        available_spaces=avail,
    )


async def get_road_sections(
    session: AsyncSession,
    lat: float | None,
    lon: float | None,
    radius_m: int,
    skip: int,
    limit: int,
) -> tuple[list[RoadSectionResponse], int]:
    base_q = (
        select(
            RoadSection,
            RoadAvailability.available_spaces,
        )
        .outerjoin(
            RoadAvailability,
            RoadAvailability.section_id == RoadSection.id,
        )
    )

    if lat is not None and lon is not None:
        dist = _haversine_dist(RoadSection.lat, RoadSection.lon, lat, lon)
        base_q = base_q.where(dist <= radius_m)

    total = (await session.execute(
        select(func.count()).select_from(base_q.subquery())
    )).scalar_one()

    rows = (await session.execute(base_q.offset(skip).limit(limit))).all()

    items = [
        RoadSectionResponse(
            **{c.key: getattr(section, c.key) for c in RoadSection.__table__.columns},
            available_spaces=avail,
        )
        for section, avail in rows
    ]
    return items, total
