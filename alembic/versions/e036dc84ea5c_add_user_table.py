"""add user table

Revision ID: e036dc84ea5c
Revises: ff11ccbd637f
Create Date: 2022-12-13 09:40:19.791197

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e036dc84ea5c'
down_revision = 'ff11ccbd637f'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table("users",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("email", sa.Integer(), nullable=False),
        sa.Column("password", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.TIMESTAMP(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.TIMESTAMP(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("email")
    )
    pass


def downgrade() -> None:
    op.drop_table("users")
    pass