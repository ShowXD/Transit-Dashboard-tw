from sqlalchemy import ForeignKey, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base
from app.models.base import TimestampMixin


class RoadSection(Base, TimestampMixin):
    """On-street road parking section. Synced daily from TDX."""

    __tablename__ = "road_sections"

    id: Mapped[int] = mapped_column(primary_key=True)
    external_id: Mapped[str] = mapped_column(String(64))
    road_name: Mapped[str] = mapped_column(String(128))
    section_name: Mapped[str | None] = mapped_column(String(128))
    total_spaces: Mapped[int | None] = mapped_column()
    lat: Mapped[float | None] = mapped_column()
    lon: Mapped[float | None] = mapped_column()

    __table_args__ = (
        UniqueConstraint("external_id", name="uq_road_section_external_id"),
    )


class RoadAvailability(Base, TimestampMixin):
    """Real-time available spaces per road section. Upserted every ~5 min."""

    __tablename__ = "road_availability"

    id: Mapped[int] = mapped_column(primary_key=True)
    section_id: Mapped[int] = mapped_column(
        ForeignKey("road_sections.id", ondelete="CASCADE")
    )
    available_spaces: Mapped[int] = mapped_column(default=0)

    __table_args__ = (
        UniqueConstraint("section_id", name="uq_road_availability_section"),
    )
