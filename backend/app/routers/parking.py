from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.schemas.parking import (
    PaginatedResponse,
    ParkingLotResponse,
    RoadSectionResponse,
)
from app.services.parking_query import get_lot_by_id, get_lots, get_road_sections

router = APIRouter(prefix="/parking", tags=["parking"])


@router.get("/lots", response_model=PaginatedResponse[ParkingLotResponse])
async def list_parking_lots(
    lat: float | None = Query(None, description="中心緯度"),
    lon: float | None = Query(None, description="中心經度"),
    radius_m: int = Query(1000, ge=100, le=10_000, description="搜尋半徑（公尺）"),
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
    session: AsyncSession = Depends(get_db),
) -> PaginatedResponse[ParkingLotResponse]:
    items, total = await get_lots(session, lat, lon, radius_m, skip, limit)
    return PaginatedResponse(data=items, total=total, skip=skip, limit=limit)


@router.get("/lots/{lot_id}", response_model=ParkingLotResponse)
async def get_parking_lot(
    lot_id: int,
    session: AsyncSession = Depends(get_db),
) -> ParkingLotResponse:
    lot = await get_lot_by_id(session, lot_id)
    if lot is None:
        raise HTTPException(status_code=404, detail="Parking lot not found")
    return lot


@router.get("/road-sections", response_model=PaginatedResponse[RoadSectionResponse])
async def list_road_sections(
    lat: float | None = Query(None, description="中心緯度"),
    lon: float | None = Query(None, description="中心經度"),
    radius_m: int = Query(500, ge=100, le=10_000, description="搜尋半徑（公尺）"),
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
    session: AsyncSession = Depends(get_db),
) -> PaginatedResponse[RoadSectionResponse]:
    items, total = await get_road_sections(session, lat, lon, radius_m, skip, limit)
    return PaginatedResponse(data=items, total=total, skip=skip, limit=limit)
