"""Remove resident_weapon_used from LMPD UOF incidents

Revision ID: 513f93441476
Revises: c21533f2fd07
Create Date: 2016-10-12 16:47:01.587229

"""

# revision identifiers, used by Alembic.
revision = '513f93441476'
down_revision = 'c21533f2fd07'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.drop_column('use_of_force_incidents_lmpd', 'resident_weapon_used')


def downgrade():
    op.add_column('use_of_force_incidents_lmpd', sa.Column('resident_weapon_used', sa.VARCHAR(length=255), autoincrement=False, nullable=True))
