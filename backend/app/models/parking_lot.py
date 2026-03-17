from enum import IntEnum

from sqlalchemy import String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base
from app.models.base import TimestampMixin


class CarParkType(IntEnum):
    PUBLIC = 1      # 路外公共停車場
    PRIVATE = 2     # 路外專用停車場
    ON_STREET = 3   # 路邊停車


class ParkingLot(Base, TimestampMixin):
    """Off-street parking lot. Synced daily from TDX."""

    __tablename__ = "parking_lots"

    id: Mapped[int] = mapped_column(primary_key=True)
    external_id: Mapped[str] = mapped_column(String(64))
    name: Mapped[str] = mapped_column(String(128))
    car_park_type: Mapped[int | None] = mapped_column()
    address: Mapped[str | None] = mapped_column(String(255))
    lat: Mapped[float | None] = mapped_column()
    lon: Mapped[float | None] = mapped_column()
    total_spaces: Mapped[int | None] = mapped_column()
    charge_description: Mapped[str | None] = mapped_column(String(512))

    __table_args__ = (
        UniqueConstraint("external_id", name="uq_parking_lot_external_id"),
    )
