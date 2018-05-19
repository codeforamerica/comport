"""Create WPD UOF table

Revision ID: 4d1cde26d807
Revises: 0de6730e3d41
Create Date: 2018-02-23 07:00:38.367128

"""

# revision identifiers, used by Alembic.
revision = '4d1cde26d807'
down_revision = '0de6730e3d41'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table(
        'use_of_force_incidents_wpd',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('department_id', sa.Integer(), sa.ForeignKey('departments.id'), nullable=False),
        sa.Column('incident_id', sa.String(255), unique=False, nullable=True),
        sa.Column('occurred_date', sa.DateTime, unique=False, nullable=True),
        sa.Column('division', sa.String(255), unique=False, nullable=True),
        sa.Column('bureau', sa.String(255), unique=False, nullable=True),
        sa.Column('shift', sa.String(255), unique=False, nullable=True),
        sa.Column('use_of_force_reason', sa.String(255), unique=False, nullable=True),
        sa.Column('citizen_resist_type', sa.String(255), unique=False, nullable=True),
        sa.Column('citizen_resistance', sa.String(255), unique=False, nullable=True),
        sa.Column('officer_force_type', sa.String(255), unique=False, nullable=True),
        sa.Column('arrest_charges', sa.String(255), unique=False, nullable=True),
        sa.Column('disposition', sa.String(255), unique=False, nullable=True),
        sa.Column('service_type', sa.String(255), unique=False, nullable=True),
        sa.Column('arrest_made', sa.String(255), unique=False, nullable=True),
        sa.Column('citizen_id', sa.String(255), unique=False, nullable=True),
        sa.Column('citizen_injured', sa.String(255), unique=False, nullable=True),
        sa.Column('citizen_hospitalized', sa.String(255), unique=False, nullable=True),
        sa.Column('citizen_condition', sa.String(255), unique=False, nullable=True),
        sa.Column('citizen_race', sa.String(255), unique=False, nullable=True),
        sa.Column('citizen_sex', sa.String(255), unique=False, nullable=True),
        sa.Column('citizen_age', sa.String(255), unique=False, nullable=True),
        sa.Column('officer_id', sa.String(255), unique=False, nullable=True),
        sa.Column('officer_injured', sa.String(255), unique=False, nullable=True),
        sa.Column('officer_hospitalized', sa.String(255), unique=False, nullable=True),
        sa.Column('officer_race', sa.String(255), unique=False, nullable=True),
        sa.Column('officer_sex', sa.String(255), unique=False, nullable=True),
        sa.Column('officer_age', sa.String(255), unique=False, nullable=True),
        sa.Column('officer_years_of_service', sa.String(255), unique=False, nullable=True),
        sa.ForeignKeyConstraint(['department_id'], ['departments.id']),
        sa.PrimaryKeyConstraint('id')
    )

def downgrade():
    op.drop_table('use_of_force_incidents_wpd')
