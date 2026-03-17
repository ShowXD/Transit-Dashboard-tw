import asyncio

import httpx

from app.database import AsyncSessionLocal
from app.schemas.tdx import (
    CarParkAvailabilitySchema,
    CarParkSchema,
    RoadAvailabilitySchema,
    RoadSectionSchema,
)
from app.services import tdx_client
from app.services.tdx_client import TDXRateLimitError
from app.services.upsert import (
    upsert_parking_availability,
    upsert_parking_lots,
    upsert_road_availability,
    upsert_road_sections,
)
from app.workers.celery_app import celery_app


@celery_app.task(
    name="app.workers.tasks.sync_parking_master_data",
    bind=True,
    max_retries=3,
    default_retry_delay=60,
)
def sync_parking_master_data(self) -> None:  # type: ignore[override]
    """Sync parking lot + road section master data from TDX (runs at 3am daily).

    GET /v2/Parking/OffStreet/CarPark/City/Taichung
    GET /v2/Parking/OnStreet/Road/City/Taichung
    """
    try:
        asyncio.run(_sync_master())
    except TDXRateLimitError as exc:
        raise self.retry(exc=exc, countdown=300)
    except (httpx.HTTPStatusError, httpx.RequestError) as exc:
        raise self.retry(exc=exc)


async def _sync_master() -> None:
    lots = [
        CarParkSchema.model_validate(r)
        for r in await tdx_client.get("/v2/Parking/OffStreet/CarPark/City/Taichung")
    ]
    roads = [
        RoadSectionSchema.model_validate(r)
        for r in await tdx_client.get("/v2/Parking/OnStreet/Road/City/Taichung")
    ]
    async with AsyncSessionLocal() as session:
        await upsert_parking_lots(session, lots)
        await upsert_road_sections(session, roads)


@celery_app.task(
    name="app.workers.tasks.fetch_parking_availability",
    bind=True,
    max_retries=3,
    default_retry_delay=15,
)
def fetch_parking_availability(self) -> None:  # type: ignore[override]
    """Upsert real-time off-street availability every 2 min.

    GET /v2/Parking/OffStreet/CarParkAvailability/City/Taichung
    """
    try:
        asyncio.run(_fetch_parking_avail())
    except TDXRateLimitError as exc:
        raise self.retry(exc=exc, countdown=60)
    except (httpx.HTTPStatusError, httpx.RequestError) as exc:
        raise self.retry(exc=exc)


async def _fetch_parking_avail() -> None:
    items = [
        CarParkAvailabilitySchema.model_validate(r)
        for r in await tdx_client.get(
            "/v2/Parking/OffStreet/CarParkAvailability/City/Taichung"
        )
    ]
    async with AsyncSessionLocal() as session:
        await upsert_parking_availability(session, items)


@celery_app.task(
    name="app.workers.tasks.fetch_road_availability",
    bind=True,
    max_retries=3,
    default_retry_delay=30,
)
def fetch_road_availability(self) -> None:  # type: ignore[override]
    """Upsert real-time on-street road availability every 5 min.

    GET /v2/Parking/OnStreet/RoadSectionAvailability/City/Taichung
    """
    try:
        asyncio.run(_fetch_road_avail())
    except TDXRateLimitError as exc:
        raise self.retry(exc=exc, countdown=120)
    except (httpx.HTTPStatusError, httpx.RequestError) as exc:
        raise self.retry(exc=exc)


async def _fetch_road_avail() -> None:
    items = [
        RoadAvailabilitySchema.model_validate(r)
        for r in await tdx_client.get(
            "/v2/Parking/OnStreet/RoadSectionAvailability/City/Taichung"
        )
    ]
    async with AsyncSessionLocal() as session:
        await upsert_road_availability(session, items)
