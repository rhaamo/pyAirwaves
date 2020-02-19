"""Add is_private aircraft owner info

Revision ID: 7dddb7d187c9
Revises: 4a351f950cdd
Create Date: 2019-02-24 11:38:07.778807

"""

# revision identifiers, used by Alembic.
revision = "7dddb7d187c9"
down_revision = "4a351f950cdd"

from alembic import op  # noqa: E402
import sqlalchemy as sa  # noqa: E402


def upgrade():
    op.add_column("aircraft_owner", sa.Column("is_private", sa.Boolean(), nullable=True))


def downgrade():
    op.drop_column("aircraft_owner", "is_private")
