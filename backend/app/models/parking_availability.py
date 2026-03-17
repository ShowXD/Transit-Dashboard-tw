from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base
from app.models.base import TimestampMixin


class ParkingAvailability(Base, TimestampMixin):
    """Real-time available spaces per off-street lot. Upserted every ~2 min."""

    __tablename__ = "parking_availability"

    id: Mapped[int] = mapped_column(primary_key=True)
    lot_id: Mapped[int] = mapped_column(ForeignKey("parking_lots.id", ondelete="CASCADE"))
    available_spaces: Mapped[int] = mapped_column(default=0)

    __table_args__ = (UniqueConstraint("lot_id", name="uq_parking_availability_lot"),)
