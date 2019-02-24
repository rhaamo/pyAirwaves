"""Create ACARS translation table

Revision ID: 7f5c2634ef59
Revises: None
Create Date: 2019-02-24 09:58:19.032683

"""

# revision identifiers, used by Alembic.
revision = "7f5c2634ef59"
down_revision = None

from alembic import op  # noqa: E402
import sqlalchemy as sa  # noqa: E402


def upgrade():
    op.create_table(
        "translation",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("reg", sa.String(length=20), nullable=True),
        sa.Column("reg_correct", sa.String(length=20), nullable=True),
        sa.Column("operator", sa.String(length=20), nullable=True),
        sa.Column("operator_correct", sa.String(length=20), nullable=True),
        sa.Column("source", sa.String(length=255), nullable=True),
        sa.Column("date_added", sa.DateTime(), nullable=True),
        sa.Column("date_modified", sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade():
    op.drop_table("translation")
