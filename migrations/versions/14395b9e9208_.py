"""add bureau, division, and discharge type to srpd ois

Revision ID: 14395b9e9208
Revises: c471472f1a82
Create Date: 2017-06-25 23:49:23.700985

"""

# revision identifiers, used by Alembic.
revision = '14395b9e9208'
down_revision = 'c471472f1a82'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column('officer_involved_shootings_srpd', sa.Column('bureau', sa.String(length=255), nullable=True))
    op.add_column('officer_involved_shootings_srpd', sa.Column('discharge_type', sa.String(length=255), nullable=True))
    op.add_column('officer_involved_shootings_srpd', sa.Column('division', sa.String(length=255), nullable=True))


def downgrade():
    op.drop_column('officer_involved_shootings_srpd', 'division')
    op.drop_column('officer_involved_shootings_srpd', 'discharge_type')
    op.drop_column('officer_involved_shootings_srpd', 'bureau')
