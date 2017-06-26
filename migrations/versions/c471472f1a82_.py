"""add bureau, division, and officer force type scale to srpd uof

Revision ID: c471472f1a82
Revises: 9d6a8b74b21a
Create Date: 2017-06-25 23:39:53.185468

"""

# revision identifiers, used by Alembic.
revision = 'c471472f1a82'
down_revision = '9d6a8b74b21a'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column('use_of_force_incidents_srpd', sa.Column('bureau', sa.String(length=255), nullable=True))
    op.add_column('use_of_force_incidents_srpd', sa.Column('division', sa.String(length=255), nullable=True))
    op.add_column('use_of_force_incidents_srpd', sa.Column('officer_force_type_scale', sa.String(length=255), nullable=True))

def downgrade():
    op.drop_column('use_of_force_incidents_srpd', 'officer_force_type_scale')
    op.drop_column('use_of_force_incidents_srpd', 'division')
    op.drop_column('use_of_force_incidents_srpd', 'bureau')
