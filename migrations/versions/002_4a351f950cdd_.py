"""Add AircraftModeS and AircraftOwner

Revision ID: 4a351f950cdd
Revises: 7f5c2634ef59
Create Date: 2019-02-24 10:50:44.337330

"""

# revision identifiers, used by Alembic.
revision = "4a351f950cdd"
down_revision = "7f5c2634ef59"

from alembic import op  # noqa: E402
import sqlalchemy as sa  # noqa: E402


def upgrade():
    op.create_table(
        "aircraft_modes",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("first_created", sa.DateTime(), nullable=True),
        sa.Column("last_modified", sa.DateTime(), nullable=True),
        sa.Column("mode_s", sa.String(length=6), nullable=False),
        sa.Column("mode_s_country", sa.String(length=40), nullable=True),
        sa.Column("registration", sa.String(length=20), nullable=True),
        sa.Column("icao_type_code", sa.String(length=4), nullable=True),
        sa.Column("type_flight", sa.String(length=50), nullable=True),
        sa.Column("source", sa.String(length=255), nullable=True),
        sa.Column("source_type", sa.String(length=255), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "aircraft_owner",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("registration", sa.String(length=255), nullable=False),
        sa.Column("base", sa.String(length=255), nullable=True),
        sa.Column("owner", sa.String(length=255), nullable=True),
        sa.Column("date_first_reg", sa.DateTime(), nullable=True),
        sa.Column("source", sa.String(length=255), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade():
    op.drop_table("aircraft_owner")
    op.drop_table("aircraft_modes")
