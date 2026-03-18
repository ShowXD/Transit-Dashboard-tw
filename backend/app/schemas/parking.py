from typing import Generic, TypeVar

from pydantic import BaseModel

T = TypeVar("T")


class ParkingLotResponse(BaseModel):
    id: int
    external_id: str
    name: str
    car_park_type: int | None
    address: str | None
    lat: float | None
    lon: float | None
    total_spaces: int | None
    available_spaces: int | None
    charge_description: str | None

    model_config = {"from_attributes": True}


class RoadSectionResponse(BaseModel):
    id: int
    external_id: str
    road_name: str
    section_name: str | None
    lat: float | None
    lon: float | None
    total_spaces: int | None
    available_spaces: int | None

    model_config = {"from_attributes": True}


class PaginatedResponse(BaseModel, Generic[T]):
    data: list[T]
    total: int
    skip: int
    limit: int
