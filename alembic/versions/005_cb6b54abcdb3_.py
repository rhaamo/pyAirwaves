"""Add Aircraft Registrations

Revision ID: cb6b54abcdb3
Revises: bcc5cc4c389a
Create Date: 2019-02-26 09:47:25.263327

"""

# revision identifiers, used by Alembic.
revision = "cb6b54abcdb3"
down_revision = "bcc5cc4c389a"

from alembic import op  # noqa: E402
import sqlalchemy as sa  # noqa: E402


def upgrade():
    op.create_table(
        "aircraft_registration",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("country", sa.String(length=255), nullable=False),
        sa.Column("prefix", sa.String(length=10), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade():
    op.drop_table("aircraft_registration")
