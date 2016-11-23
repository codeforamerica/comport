"""add case_number column to the BPD officer-involved shooting table

Revision ID: ab97630e71ce
Revises: cff7a8d7f106
Create Date: 2016-11-17 15:08:24.107164

"""

# revision identifiers, used by Alembic.
revision = 'ab97630e71ce'
down_revision = 'cff7a8d7f106'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column('officer_involved_shootings_bpd', sa.Column('case_number', sa.String(length=255), nullable=True))


def downgrade():
    op.drop_column('officer_involved_shootings_bpd', 'case_number')
