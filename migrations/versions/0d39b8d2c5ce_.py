"""Add order to chart blocks.

Revision ID: 0d39b8d2c5ce
Revises: 0d78d545906f
Create Date: 2016-07-06 16:52:09.728941

"""

# revision identifiers, used by Alembic.
revision = '0d39b8d2c5ce'
down_revision = '0d78d545906f'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column('chart_blocks', sa.Column('order', sa.Integer(), nullable=True))


def downgrade():
    op.drop_column('chart_blocks', 'order')
