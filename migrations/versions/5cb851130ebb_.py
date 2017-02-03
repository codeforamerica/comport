"""add officer age & years of service to SRPD incidents

Revision ID: 5cb851130ebb
Revises: c5e276c0d67f
Create Date: 2017-02-02 16:31:22.915785

"""

# revision identifiers, used by Alembic.
revision = '5cb851130ebb'
down_revision = 'c5e276c0d67f'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column('citizen_complaints_srpd', sa.Column('officer_age', sa.String(length=255), nullable=True))
    op.add_column('citizen_complaints_srpd', sa.Column('officer_years_of_service', sa.String(length=255), nullable=True))
    op.add_column('officer_involved_shootings_srpd', sa.Column('officer_age', sa.String(length=255), nullable=True))
    op.add_column('officer_involved_shootings_srpd', sa.Column('officer_years_of_service', sa.String(length=255), nullable=True))
    op.add_column('pursuits_srpd', sa.Column('officer_age', sa.String(length=255), nullable=True))
    op.add_column('pursuits_srpd', sa.Column('officer_years_of_service', sa.String(length=255), nullable=True))
    op.add_column('use_of_force_incidents_srpd', sa.Column('officer_age', sa.String(length=255), nullable=True))
    op.add_column('use_of_force_incidents_srpd', sa.Column('officer_years_of_service', sa.String(length=255), nullable=True))

def downgrade():
    op.drop_column('use_of_force_incidents_srpd', 'officer_years_of_service')
    op.drop_column('use_of_force_incidents_srpd', 'officer_age')
    op.drop_column('pursuits_srpd', 'officer_years_of_service')
    op.drop_column('pursuits_srpd', 'officer_age')
    op.drop_column('officer_involved_shootings_srpd', 'officer_years_of_service')
    op.drop_column('officer_involved_shootings_srpd', 'officer_age')
    op.drop_column('citizen_complaints_srpd', 'officer_years_of_service')
    op.drop_column('citizen_complaints_srpd', 'officer_age')
