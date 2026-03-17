from fastapi import APIRouter

router = APIRouter(prefix="/parking", tags=["parking"])


@router.get("/lots", summary="停車場列表與即時車位")
async def get_parking_lots(
    lat: float | None = None,
    lon: float | None = None,
    radius_m: int = 1000,
) -> dict:
    """Return off-street parking lots with real-time available spaces.

    Query params:
    - **lat / lon**: center point for proximity filter
    - **radius_m**: search radius in metres (default 1000m)
    """
    # TODO: Phase 2 — query ParkingLot JOIN ParkingAvailability via service layer
    return {"data": [], "total": 0}


@router.get("/lots/{lot_id}", summary="停車場詳細資訊")
async def get_parking_lot(lot_id: int) -> dict:
    """Return details and current availability for a single parking lot."""
    # TODO: Phase 2
    return {"data": None}


@router.get("/road-sections", summary="路邊停車路段與即時車位")
async def get_road_sections(
    lat: float | None = None,
    lon: float | None = None,
    radius_m: int = 500,
) -> dict:
    """Return on-street road parking sections with real-time available spaces.

    Query params:
    - **lat / lon**: center point for proximity filter
    - **radius_m**: search radius in metres (default 500m)
    """
    # TODO: Phase 2 — query RoadSection JOIN RoadAvailability via service layer
    return {"data": [], "total": 0}
