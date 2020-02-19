"""Add missing performance index

Revision ID: 23e0cd74b0aa
Revises: cb6b54abcdb3
Create Date: 2020-02-12 22:29:07.056507

"""

# revision identifiers, used by Alembic.
revision = "23e0cd74b0aa"
down_revision = "cb6b54abcdb3"

from alembic import op  # noqa: E402


def upgrade():
    op.create_index(op.f("ix_aircraft_modes_icao_type_code"), "aircraft_modes", ["icao_type_code"], unique=False)
    op.create_index(op.f("ix_aircraft_modes_mode_s"), "aircraft_modes", ["mode_s"], unique=False)
    op.create_index(op.f("ix_aircraft_modes_mode_s_country"), "aircraft_modes", ["mode_s_country"], unique=False)
    op.create_index(op.f("ix_aircraft_modes_registration"), "aircraft_modes", ["registration"], unique=False)
    op.create_index(op.f("ix_aircraft_owner_registration"), "aircraft_owner", ["registration"], unique=False)
    op.create_index(op.f("ix_aircraft_registration_country"), "aircraft_registration", ["country"], unique=False)


def downgrade():
    op.drop_index(op.f("ix_aircraft_registration_country"), table_name="aircraft_registration")
    op.drop_index(op.f("ix_aircraft_owner_registration"), table_name="aircraft_owner")
    op.drop_index(op.f("ix_aircraft_modes_registration"), table_name="aircraft_modes")
    op.drop_index(op.f("ix_aircraft_modes_mode_s_country"), table_name="aircraft_modes")
    op.drop_index(op.f("ix_aircraft_modes_mode_s"), table_name="aircraft_modes")
    op.drop_index(op.f("ix_aircraft_modes_icao_type_code"), table_name="aircraft_modes")
