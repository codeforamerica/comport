"""remove bureau and division from BPD officer-invovled shootings

Revision ID: cff7a8d7f106
Revises: 7f4ae427dcf6
Create Date: 2016-11-17 14:50:09.068379

"""

# revision identifiers, used by Alembic.
revision = 'cff7a8d7f106'
down_revision = '7f4ae427dcf6'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.drop_column('officer_involved_shootings_bpd', 'bureau')
    op.drop_column('officer_involved_shootings_bpd', 'division')


def downgrade():
    op.add_column('officer_involved_shootings_bpd', sa.Column('division', sa.VARCHAR(length=255), autoincrement=False, nullable=True))
    op.add_column('officer_involved_shootings_bpd', sa.Column('bureau', sa.VARCHAR(length=255), autoincrement=False, nullable=True))
