"""add content column

Revision ID: ac2a6892467c
Revises: 121146aea722
Create Date: 2022-08-29 14:13:56.121897

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ac2a6892467c'
down_revision = '121146aea722'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))


def downgrade() -> None:
    op.drop_column('posts', 'content')
