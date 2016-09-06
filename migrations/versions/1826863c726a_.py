"""create LMPD uof incident table

Revision ID: 1826863c726a
Revises: bd713215655e
Create Date: 2016-09-06 01:41:02.344115

"""

# revision identifiers, used by Alembic.
revision = '1826863c726a'
down_revision = 'bd713215655e'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table(
        'use_of_force_incidents_lmpd',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('department_id', sa.Integer(), nullable=False),
        sa.Column('opaque_id', sa.String(length=255), nullable=False),
        sa.Column('occured_date', sa.DateTime(), nullable=True),
        sa.Column('bureau', sa.String(length=255), nullable=True),
        sa.Column('division', sa.String(length=255), nullable=True),
        sa.Column('unit', sa.String(length=255), nullable=True),
        sa.Column('platoon', sa.String(length=255), nullable=True),
        sa.Column('disposition', sa.String(length=255), nullable=True),
        sa.Column('use_of_force_reason', sa.String(length=255), nullable=True),
        sa.Column('officer_force_type', sa.String(length=255), nullable=True),
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
    op.drop_table('use_of_force_incidents_lmpd')
