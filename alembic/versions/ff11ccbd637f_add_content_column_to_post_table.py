"""add content column to post table

Revision ID: ff11ccbd637f
Revises: 38b7034fa7cc
Create Date: 2022-12-13 09:35:03.921086

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ff11ccbd637f'
down_revision = '38b7034fa7cc'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("posts", sa.Column("content", sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column("posts", "content")
    pass
