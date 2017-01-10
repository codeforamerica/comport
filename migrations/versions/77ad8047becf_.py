"""add case_number, completed_date, received_date; remove division, bureau, resident_weapon_used on BPD UOF table

Revision ID: 77ad8047becf
Revises: 43c4c512514
Create Date: 2017-01-09 23:48:43.764788

"""

# revision identifiers, used by Alembic.
revision = '77ad8047becf'
down_revision = '43c4c512514'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column('use_of_force_incidents_bpd', sa.Column('case_number', sa.String(length=128), nullable=True))
    op.add_column('use_of_force_incidents_bpd', sa.Column('completed_date', sa.DateTime(), nullable=True))
    op.add_column('use_of_force_incidents_bpd', sa.Column('received_date', sa.DateTime(), nullable=True))

    op.drop_column('use_of_force_incidents_bpd', 'division')
    op.drop_column('use_of_force_incidents_bpd', 'bureau')
    op.drop_column('use_of_force_incidents_bpd', 'resident_weapon_used')

def downgrade():
    op.add_column('use_of_force_incidents_bpd', sa.Column('resident_weapon_used', sa.VARCHAR(length=255), autoincrement=False, nullable=True))
    op.add_column('use_of_force_incidents_bpd', sa.Column('bureau', sa.VARCHAR(length=255), autoincrement=False, nullable=True))
    op.add_column('use_of_force_incidents_bpd', sa.Column('division', sa.VARCHAR(length=255), autoincrement=False, nullable=True))

    op.drop_column('use_of_force_incidents_bpd', 'received_date')
    op.drop_column('use_of_force_incidents_bpd', 'completed_date')
    op.drop_column('use_of_force_incidents_bpd', 'case_number')
