"""Adds SRPD and four datasets

Revision ID: c5e276c0d67f
Revises: 77ad8047becf
Create Date: 2017-01-20 03:58:12.333638

"""

# revision identifiers, used by Alembic.
revision = 'c5e276c0d67f'
down_revision = '77ad8047becf'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table(
        'use_of_force_incidents_srpd',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('department_id', sa.Integer(), nullable=False),
        sa.Column('opaque_id', sa.String(length=255), nullable=False),
        sa.Column('case_number', sa.String(length=128), nullable=True),
        sa.Column('file_number', sa.String(length=128), nullable=True),
        sa.Column('occurred_date', sa.DateTime(), nullable=True),
        sa.Column('team', sa.String(length=255), nullable=True),
        sa.Column('assignment', sa.String(length=255), nullable=True),
        sa.Column('service_type', sa.String(length=255), nullable=True),
        sa.Column('use_of_force_reason', sa.String(length=255), nullable=True),
        sa.Column('aggravating_factors', sa.String(length=255), nullable=True),
        sa.Column('arrest_made', sa.Boolean(), nullable=True),
        sa.Column('resident_injured', sa.Boolean(), nullable=True),
        sa.Column('resident_hospitalized', sa.Boolean(), nullable=True),
        sa.Column('officer_injured', sa.Boolean(), nullable=True),
        sa.Column('officer_hospitalized', sa.Boolean(), nullable=True),
        sa.Column('officer_force_type', sa.String(length=255), nullable=True),
        sa.ForeignKeyConstraint(['department_id'], ['departments.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_table(
        'officer_involved_shootings_srpd',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('department_id', sa.Integer(), nullable=False),
        sa.Column('opaque_id', sa.String(length=255), nullable=False),
        sa.Column('case_number', sa.String(length=128), nullable=True),
        sa.Column('occurred_date', sa.DateTime(), nullable=True),
        sa.Column('team', sa.String(length=255), nullable=True),
        sa.Column('assignment', sa.String(length=255), nullable=True),
        sa.Column('resident_race', sa.String(length=255), nullable=True),
        sa.Column('resident_sex', sa.String(length=255), nullable=True),
        sa.Column('resident_age', sa.String(length=255), nullable=True),
        sa.Column('service_type', sa.String(length=255), nullable=True),
        sa.Column('officer_weapon_used', sa.String(length=255), nullable=True),
        sa.Column('intentional', sa.Boolean(), nullable=True),
        sa.Column('resident_condition', sa.String(length=255), nullable=True),
        sa.Column('officer_condition', sa.String(length=255), nullable=True),
        sa.Column('disposition', sa.String(length=255), nullable=True),
        sa.ForeignKeyConstraint(['department_id'], ['departments.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_table(
        'citizen_complaints_srpd',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('department_id', sa.Integer(), nullable=False),
        sa.Column('opaque_id', sa.String(length=255), nullable=False),
        sa.Column('case_number', sa.String(length=128), nullable=True),
        sa.Column('file_number', sa.String(length=128), nullable=True),
        sa.Column('occurred_date', sa.DateTime(), nullable=True),
        sa.Column('team', sa.String(length=255), nullable=True),
        sa.Column('assignment', sa.String(length=255), nullable=True),
        sa.Column('bureau', sa.String(length=255), nullable=True),
        sa.Column('division', sa.String(length=255), nullable=True),
        sa.Column('resident_race', sa.String(length=255), nullable=True),
        sa.Column('resident_sex', sa.String(length=255), nullable=True),
        sa.Column('resident_age', sa.String(length=255), nullable=True),
        sa.Column('allegation', sa.String(length=255), nullable=True),
        sa.Column('disposition', sa.String(length=255), nullable=True),
        sa.Column('service_type', sa.String(length=255), nullable=True),
        sa.Column('source', sa.String(length=255), nullable=True),
        sa.ForeignKeyConstraint(['department_id'], ['departments.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_table(
        'pursuits_srpd',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('department_id', sa.Integer(), nullable=False),
        sa.Column('opaque_id', sa.String(length=255), nullable=False),
        sa.Column('case_number', sa.String(length=128), nullable=True),
        sa.Column('pursuit_number', sa.String(length=128), nullable=True),
        sa.Column('occurred_date', sa.DateTime(), nullable=True),
        sa.Column('team', sa.String(length=255), nullable=True),
        sa.Column('assignment', sa.String(length=255), nullable=True),
        sa.Column('aborted', sa.Boolean(), nullable=True),
        sa.Column('accident', sa.Boolean(), nullable=True),
        sa.Column('arrest_made', sa.Boolean(), nullable=True),
        sa.Column('distance', sa.String(length=255), nullable=True),
        sa.Column('reason', sa.String(length=255), nullable=True),
        sa.Column('vehicle_type', sa.String(length=255), nullable=True),
        sa.Column('max_speed', sa.String(length=255), nullable=True),
        sa.Column('resident_race', sa.String(length=255), nullable=True),
        sa.Column('resident_sex', sa.String(length=255), nullable=True),
        sa.Column('resident_age', sa.String(length=255), nullable=True),
        sa.Column('copter_available', sa.Boolean(), nullable=True),
        sa.Column('copter_used', sa.Boolean(), nullable=True),
        sa.Column('dui_arrest', sa.Boolean(), nullable=True),
        sa.Column('stop_device_used', sa.Boolean(), nullable=True),
        sa.Column('stop_device', sa.String(length=255), nullable=True),
        sa.Column('follow_policy', sa.Boolean(), nullable=True),
        sa.Column('weather_condition', sa.String(length=255), nullable=True),
        sa.Column('location_began', sa.String(length=255), nullable=True),
        sa.Column('location_ended', sa.String(length=255), nullable=True),
        sa.Column('in_car_cam_available', sa.Boolean(), nullable=True),
        sa.Column('in_car_cam_used', sa.Boolean(), nullable=True),
        sa.Column('total_time_minutes', sa.String(length=255), nullable=True),
        sa.Column('influencing_factor', sa.String(length=255), nullable=True),
        sa.Column('aborted_by', sa.String(length=255), nullable=True),
        sa.Column('concluded_by', sa.String(length=255), nullable=True),
        sa.Column('damage_type', sa.String(length=255), nullable=True),
        sa.Column('injury_type', sa.String(length=255), nullable=True),
        sa.Column('initiated_by_agency', sa.String(length=255), nullable=True),
        sa.Column('concluded_by_agency', sa.String(length=255), nullable=True),
        sa.Column('liability_claim', sa.Boolean(), nullable=True),
        sa.Column('associated_officer_count', sa.String(length=255), nullable=True),
        sa.Column('violation', sa.String(length=255), nullable=True),
        sa.Column('justified', sa.Boolean(), nullable=True),
        sa.Column('officer_condition', sa.String(length=255), nullable=True),
        sa.ForeignKeyConstraint(['department_id'], ['departments.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.add_column('departments', sa.Column('is_public_pursuits', sa.Boolean(), server_default=sa.true(), nullable=False))


def downgrade():
    op.drop_column('departments', 'is_public_pursuits')
    op.drop_table('pursuits_srpd')
    op.drop_table('citizen_complaints_srpd')
    op.drop_table('officer_involved_shootings_srpd')
    op.drop_table('use_of_force_incidents_srpd')
