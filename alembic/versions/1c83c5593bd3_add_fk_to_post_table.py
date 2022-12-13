"""add FK to post table

Revision ID: 1c83c5593bd3
Revises: e036dc84ea5c
Create Date: 2022-12-13 09:47:32.768354

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1c83c5593bd3'
down_revision = 'e036dc84ea5c'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("posts",sa.Column("owner_id", sa.Integer(), nullable=False))
    op.create_foreign_key("posts_user_fk", source_table="posts", referent_table="users", local_cols=["owner_id"], remote_cols=["id"], ondelete="CASCADE")
    pass


def downgrade() -> None:
    op.drop_constraint("posts_user_fk", table_name="posts")
    op.drop_column("posts", "owner_id")
    pass
