"""add received & completed date to bpd ois

Revision ID: 01c18862cf4a
Revises: 56bb92fb8acc
Create Date: 2017-02-08 12:53:11.998789

"""

# revision identifiers, used by Alembic.
revision = '01c18862cf4a'
down_revision = '56bb92fb8acc'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column('officer_involved_shootings_bpd', sa.Column('completed_date', sa.DateTime(), nullable=True))
    op.add_column('officer_involved_shootings_bpd', sa.Column('received_date', sa.DateTime(), nullable=True))


def downgrade():
    op.drop_column('officer_involved_shootings_bpd', 'received_date')
    op.drop_column('officer_involved_shootings_bpd', 'completed_date')
