from typing import Annotated

from pydantic import BaseModel, BeforeValidator, ConfigDict, Field


def _zh_tw(v: object) -> str:
    if isinstance(v, dict):
        return v.get("Zh_tw", "")
    return str(v) if v else ""


LocalizedStr = Annotated[str, BeforeValidator(_zh_tw)]


class _Position(BaseModel):
    model_config = ConfigDict(extra="ignore")
    lat: float | None = Field(None, alias="PositionLat")
    lon: float | None = Field(None, alias="PositionLon")


class CarParkSchema(BaseModel):
    """GET /v2/Parking/OffStreet/CarPark/City/Taichung — one item."""

    model_config = ConfigDict(extra="ignore", populate_by_name=True)

    car_park_id: str = Field(alias="CarParkID")
    name: LocalizedStr = Field(alias="CarParkName")
    car_park_type: int | None = Field(None, alias="CarParkType")
    address: str | None = Field(None, alias="Address")
    position: _Position | None = Field(None, alias="CarParkPosition")
    total_spaces: int | None = Field(None, alias="TotalSpaces")
    charge_description: str | None = Field(None, alias="ChargeDescription")


class CarParkAvailabilitySchema(BaseModel):
    """GET /v2/Parking/OffStreet/CarParkAvailability/City/Taichung — one item."""

    model_config = ConfigDict(extra="ignore", populate_by_name=True)

    car_park_id: str = Field(alias="CarParkID")
    available_spaces: int = Field(0, alias="AvailableSpaces")


class RoadSectionSchema(BaseModel):
    """GET /v2/Parking/OnStreet/Road/City/Taichung — one item."""

    model_config = ConfigDict(extra="ignore", populate_by_name=True)

    road_section_id: str = Field(alias="RoadSectionID")
    road_name: str = Field(alias="RoadName")
    section_name: str | None = Field(None, alias="SectionName")
    total_spaces: int | None = Field(None, alias="TotalSpaces")
    lat: float | None = Field(None, alias="PositionLat")
    lon: float | None = Field(None, alias="PositionLon")


class RoadAvailabilitySchema(BaseModel):
    """GET /v2/Parking/OnStreet/RoadSectionAvailability/City/Taichung — one item."""

    model_config = ConfigDict(extra="ignore", populate_by_name=True)

    road_section_id: str = Field(alias="RoadSectionID")
    available_spaces: int = Field(0, alias="AvailableSpaces")
