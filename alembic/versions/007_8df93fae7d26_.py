"""Add future table for ADSB history

Revision ID: 8df93fae7d26
Revises: 23e0cd74b0aa
Create Date: 2020-02-12 22:30:19.539620

"""

# revision identifiers, used by Alembic.
revision = "8df93fae7d26"
down_revision = "23e0cd74b0aa"

from alembic import op  # noqa: E402
import sqlalchemy as sa  # noqa: E402


def upgrade():
    op.create_table(
        "archive_adsb_message",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("message_type", sa.String(length=5), nullable=False),
        sa.Column("transmission_type", sa.Integer(), nullable=False),
        sa.Column("session_id", sa.String(length=20), nullable=True),
        sa.Column("aircraft_id", sa.String(length=20), nullable=True),
        sa.Column("hex_ident", sa.String(length=20), nullable=True),
        sa.Column("flight_id", sa.String(length=20), nullable=True),
        sa.Column("date_msg_gen", sa.String(length=20), nullable=True),
        sa.Column("time_msg_gen", sa.String(length=20), nullable=True),
        sa.Column("msg_gen", sa.DateTime(), nullable=True),
        sa.Column("date_msg_log", sa.String(length=20), nullable=True),
        sa.Column("time_msg_log", sa.String(length=20), nullable=True),
        sa.Column("msg_log", sa.DateTime(), nullable=True),
        sa.Column("callsign", sa.String(length=20), nullable=True),
        sa.Column("altitude", sa.Integer(), nullable=True),
        sa.Column("ground_speed", sa.Integer(), nullable=True),
        sa.Column("track", sa.String(length=20), nullable=True),
        sa.Column("latitude", sa.Float(), nullable=True),
        sa.Column("longitude", sa.Float(), nullable=True),
        sa.Column("vertical_rate", sa.Integer(), nullable=True),
        sa.Column("squawk", sa.Integer(), nullable=True),
        sa.Column("alert", sa.String(length=20), nullable=True),
        sa.Column("emergency", sa.String(length=20), nullable=True),
        sa.Column("spi_ident", sa.String(length=20), nullable=True),
        sa.Column("is_on_ground", sa.Boolean(), nullable=True),
        sa.Column("src", sa.String(length=255), nullable=True),
        sa.Column("client_name", sa.String(length=255), nullable=True),
        sa.Column("data_origin", sa.String(length=255), nullable=True),
        sa.Column("entry_point", sa.String(length=255), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade():
    op.drop_table("archive_adsb_message")
