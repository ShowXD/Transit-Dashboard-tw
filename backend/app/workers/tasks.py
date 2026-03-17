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
    # TODO: Phase 2


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
    # TODO: Phase 2


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
    # TODO: Phase 2
