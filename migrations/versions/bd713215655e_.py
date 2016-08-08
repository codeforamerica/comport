"""Create BPD incident tables

Revision ID: bd713215655e
Revises: d4db9d4eff92
Create Date: 2016-08-08 00:56:37.412428

"""

# revision identifiers, used by Alembic.
revision = 'bd713215655e'
down_revision = 'd4db9d4eff92'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table(
        'officer_involved_shootings_bpd',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('department_id', sa.Integer(), nullable=False),
        sa.Column('opaque_id', sa.String(length=255), nullable=False),
        sa.Column('occured_date', sa.DateTime(), nullable=True),
        sa.Column('bureau', sa.String(length=255), nullable=True),
        sa.Column('division', sa.String(length=255), nullable=True),
        sa.Column('assignment', sa.String(length=255), nullable=True),
        sa.Column('disposition', sa.String(length=255), nullable=True),
        sa.Column('resident_weapon_used', sa.String(length=255), nullable=True),
        sa.Column('officer_weapon_used', sa.String(length=255), nullable=True),
        sa.Column('service_type', sa.String(length=255), nullable=True),
        sa.Column('resident_condition', sa.String(length=255), nullable=True),
        sa.Column('officer_condition', sa.String(length=255), nullable=True),
        sa.Column('resident_identifier', sa.String(length=255), nullable=True),
        sa.Column('resident_race', sa.String(length=255), nullable=True),
        sa.Column('resident_sex', sa.String(length=255), nullable=True),
        sa.Column('resident_age', sa.String(length=255), nullable=True),
        sa.Column('officer_race', sa.String(length=255), nullable=True),
        sa.Column('officer_sex', sa.String(length=255), nullable=True),
        sa.Column('officer_age', sa.String(length=255), nullable=True),
        sa.Column('officer_years_of_service', sa.Integer(), nullable=True),
        sa.Column('officer_identifier', sa.String(length=255), nullable=True),
        sa.ForeignKeyConstraint(['department_id'], ['departments.id'], ),
        sa.PrimaryKeyConstraint('id')
    )

    op.create_table(
        'citizen_complaints_bpd',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('department_id', sa.Integer(), nullable=False),
        sa.Column('opaque_id', sa.String(length=255), nullable=False),
        sa.Column('occured_date', sa.DateTime(), nullable=True),
        sa.Column('bureau', sa.String(length=255), nullable=True),
        sa.Column('division', sa.String(length=255), nullable=True),
        sa.Column('assignment', sa.String(length=255), nullable=True),
        sa.Column('service_type', sa.String(length=255), nullable=True),
        sa.Column('source', sa.String(length=255), nullable=True),
        sa.Column('allegation', sa.String(length=255), nullable=True),
        sa.Column('disposition', sa.String(length=255), nullable=True),
        sa.Column('resident_identifier', sa.String(length=255), nullable=True),
        sa.Column('resident_race', sa.String(length=255), nullable=True),
        sa.Column('resident_sex', sa.String(length=255), nullable=True),
        sa.Column('resident_age', sa.String(length=255), nullable=True),
        sa.Column('officer_identifier', sa.String(length=255), nullable=True),
        sa.Column('officer_race', sa.String(length=255), nullable=True),
        sa.Column('officer_sex', sa.String(length=255), nullable=True),
        sa.Column('officer_age', sa.String(length=255), nullable=True),
        sa.Column('officer_years_of_service', sa.String(length=255), nullable=True),
        sa.ForeignKeyConstraint(['department_id'], ['departments.id'], ),
        sa.PrimaryKeyConstraint('id')
    )

    op.create_table(
        'use_of_force_incidents_bpd',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('department_id', sa.Integer(), nullable=False),
        sa.Column('opaque_id', sa.String(length=255), nullable=False),
        sa.Column('occured_date', sa.DateTime(), nullable=True),
        sa.Column('bureau', sa.String(length=255), nullable=True),
        sa.Column('division', sa.String(length=255), nullable=True),
        sa.Column('assignment', sa.String(length=255), nullable=True),
        sa.Column('use_of_force_reason', sa.String(length=255), nullable=True),
        sa.Column('officer_force_type', sa.String(length=255), nullable=True),
        sa.Column('disposition', sa.String(length=255), nullable=True),
        sa.Column('service_type', sa.String(length=255), nullable=True),
        sa.Column('arrest_made', sa.Boolean(), nullable=True),
        sa.Column('arrest_charges', sa.String(length=255), nullable=True),
        sa.Column('resident_injured', sa.Boolean(), nullable=True),
        sa.Column('resident_hospitalized', sa.Boolean(), nullable=True),
        sa.Column('resident_condition', sa.String(length=255), nullable=True),
        sa.Column('officer_injured', sa.Boolean(), nullable=True),
        sa.Column('officer_hospitalized', sa.Boolean(), nullable=True),
        sa.Column('officer_condition', sa.String(length=255), nullable=True),
        sa.Column('resident_identifier', sa.String(length=255), nullable=True),
        sa.Column('resident_weapon_used', sa.String(length=255), nullable=True),
        sa.Column('resident_race', sa.String(length=255), nullable=True),
        sa.Column('resident_sex', sa.String(length=255), nullable=True),
        sa.Column('resident_age', sa.String(length=255), nullable=True),
        sa.Column('officer_race', sa.String(length=255), nullable=True),
        sa.Column('officer_sex', sa.String(length=255), nullable=True),
        sa.Column('officer_age', sa.String(length=255), nullable=True),
        sa.Column('officer_years_of_service', sa.String(length=255), nullable=True),
        sa.Column('officer_identifier', sa.String(length=255), nullable=True),
        sa.ForeignKeyConstraint(['department_id'], ['departments.id'], ),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade():
    op.drop_table('use_of_force_incidents_bpd')
    op.drop_table('citizen_complaints_bpd')
    op.drop_table('officer_involved_shootings_bpd')
