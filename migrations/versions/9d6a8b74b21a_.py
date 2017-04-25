"""remove officer age from all srpd datasets

Revision ID: 9d6a8b74b21a
Revises: 01c18862cf4a
Create Date: 2017-04-25 01:08:34.383679

"""

# revision identifiers, used by Alembic.
revision = '9d6a8b74b21a'
down_revision = '01c18862cf4a'

from alembic import op
import sqlalchemy as sa

def upgrade():
    op.drop_column('citizen_complaints_srpd', 'officer_age')
    op.drop_column('officer_involved_shootings_srpd', 'officer_age')
    op.drop_column('pursuits_srpd', 'officer_age')
    op.drop_column('use_of_force_incidents_srpd', 'officer_age')

def downgrade():
    op.add_column('use_of_force_incidents_srpd', sa.Column('officer_age', sa.VARCHAR(length=255), autoincrement=False, nullable=True))
    op.add_column('pursuits_srpd', sa.Column('officer_age', sa.VARCHAR(length=255), autoincrement=False, nullable=True))
    op.add_column('officer_involved_shootings_srpd', sa.Column('officer_age', sa.VARCHAR(length=255), autoincrement=False, nullable=True))
    op.add_column('citizen_complaints_srpd', sa.Column('officer_age', sa.VARCHAR(length=255), autoincrement=False, nullable=True))
