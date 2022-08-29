"""add foreign key to posts



Revision ID: 9e18e115f675
Revises: 1f0103c5e493
Create Date: 2022-08-29 14:50:54.731548

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9e18e115f675'
down_revision = '1f0103c5e493'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('user_id', sa.Integer(), nullable=False))
    op.create_foreign_key('posts_users_fk',
                          source_table='posts',
                          referent_table='users',
                          local_cols=['user_id'],
                          remote_cols=['id'],
                          ondelete='CASCADE')


def downgrade() -> None:
    op.drop_constraint('posts_users_fk', table_name='posts')
    op.drop_column('psots', 'user_id')
    pass
