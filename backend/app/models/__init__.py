# Import all models here so Alembic can discover them via Base.metadata
from app.models.parking_availability import ParkingAvailability
from app.models.parking_lot import ParkingLot
from app.models.road_section import RoadAvailability, RoadSection

__all__ = [
    "ParkingLot",
    "ParkingAvailability",
    "RoadSection",
    "RoadAvailability",
]
