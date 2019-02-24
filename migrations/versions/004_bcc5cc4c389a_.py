"""Add Aircrafts table

Revision ID: bcc5cc4c389a
Revises: 7dddb7d187c9
Create Date: 2019-02-24 14:10:14.608927

"""

# revision identifiers, used by Alembic.
revision = "bcc5cc4c389a"
down_revision = "7dddb7d187c9"

from alembic import op  # noqa: E402
import sqlalchemy as sa  # noqa: E402


def upgrade():
    op.create_table(
        "aircraft",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("icao", sa.String(length=10), nullable=False),
        sa.Column("type", sa.String(length=255), nullable=False),
        sa.Column("manufacturer", sa.String(length=255), nullable=False),
        sa.Column("official_page", sa.String(length=255), nullable=False),
        sa.Column("aircraft_shadow", sa.String(length=255), nullable=True),
        sa.Column("aircraft_description", sa.String(length=255), nullable=True),
        sa.Column("engine_type", sa.String(length=255), nullable=True),
        sa.Column("engine_count", sa.Integer(), nullable=True),
        sa.Column("wake_category", sa.String(length=10), nullable=True),
        sa.Column("mfr", sa.String(length=255), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("icao"),
    )


def downgrade():
    op.drop_table("aircraft")
