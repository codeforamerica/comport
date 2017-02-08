"""update bpd complaints with new fields, removed unused

Revision ID: 56bb92fb8acc
Revises: 5cb851130ebb
Create Date: 2017-02-07 23:26:09.968323

"""

# revision identifiers, used by Alembic.
revision = '56bb92fb8acc'
down_revision = '5cb851130ebb'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column('citizen_complaints_bpd', sa.Column('case_number', sa.String(length=128), nullable=True))
    op.add_column('citizen_complaints_bpd', sa.Column('completed_date', sa.DateTime(), nullable=True))
    op.add_column('citizen_complaints_bpd', sa.Column('incident_type', sa.String(length=128), nullable=True))
    op.add_column('citizen_complaints_bpd', sa.Column('received_date', sa.DateTime(), nullable=True))
    op.add_column('citizen_complaints_bpd', sa.Column('resident_role', sa.String(length=128), nullable=True))
    op.drop_column('citizen_complaints_bpd', 'division')
    op.drop_column('citizen_complaints_bpd', 'bureau')


def downgrade():
    op.add_column('citizen_complaints_bpd', sa.Column('bureau', sa.VARCHAR(length=255), autoincrement=False, nullable=True))
    op.add_column('citizen_complaints_bpd', sa.Column('division', sa.VARCHAR(length=255), autoincrement=False, nullable=True))
    op.drop_column('citizen_complaints_bpd', 'resident_role')
    op.drop_column('citizen_complaints_bpd', 'received_date')
    op.drop_column('citizen_complaints_bpd', 'incident_type')
    op.drop_column('citizen_complaints_bpd', 'completed_date')
    op.drop_column('citizen_complaints_bpd', 'case_number')
