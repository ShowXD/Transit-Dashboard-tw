"""init schema: parking_lots, parking_availability, road_sections, road_availability

Revision ID: 0001
Revises:
Create Date: 2026-03-17
"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "0001"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ── parking_lots ──────────────────────────────────────────────────────────
    op.create_table(
        "parking_lots",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("external_id", sa.String(64), nullable=False),
        sa.Column("name", sa.String(128), nullable=False),
        sa.Column("car_park_type", sa.Integer(), nullable=True),
        sa.Column("address", sa.String(255), nullable=True),
        sa.Column("lat", sa.Float(), nullable=True),
        sa.Column("lon", sa.Float(), nullable=True),
        sa.Column("total_spaces", sa.Integer(), nullable=True),
        sa.Column("charge_description", sa.String(512), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            onupdate=sa.func.now(),
            nullable=False,
        ),
        sa.UniqueConstraint("external_id", name="uq_parking_lot_external_id"),
    )
    op.create_index("ix_parking_lots_lat_lon", "parking_lots", ["lat", "lon"])

    # ── parking_availability ──────────────────────────────────────────────────
    op.create_table(
        "parking_availability",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column(
            "lot_id",
            sa.Integer(),
            sa.ForeignKey("parking_lots.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column(
            "available_spaces", sa.Integer(), nullable=False, server_default="0"
        ),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            onupdate=sa.func.now(),
            nullable=False,
        ),
        sa.UniqueConstraint("lot_id", name="uq_parking_availability_lot"),
    )

    # ── road_sections ─────────────────────────────────────────────────────────
    op.create_table(
        "road_sections",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("external_id", sa.String(64), nullable=False),
        sa.Column("road_name", sa.String(128), nullable=False),
        sa.Column("section_name", sa.String(128), nullable=True),
        sa.Column("total_spaces", sa.Integer(), nullable=True),
        sa.Column("lat", sa.Float(), nullable=True),
        sa.Column("lon", sa.Float(), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            onupdate=sa.func.now(),
            nullable=False,
        ),
        sa.UniqueConstraint("external_id", name="uq_road_section_external_id"),
    )
    op.create_index("ix_road_sections_road_name", "road_sections", ["road_name"])

    # ── road_availability ─────────────────────────────────────────────────────
    op.create_table(
        "road_availability",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column(
            "section_id",
            sa.Integer(),
            sa.ForeignKey("road_sections.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column(
            "available_spaces", sa.Integer(), nullable=False, server_default="0"
        ),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            onupdate=sa.func.now(),
            nullable=False,
        ),
        sa.UniqueConstraint("section_id", name="uq_road_availability_section"),
    )


def downgrade() -> None:
    op.drop_table("road_availability")
    op.drop_table("road_sections")
    op.drop_table("parking_availability")
    op.drop_table("parking_lots")
