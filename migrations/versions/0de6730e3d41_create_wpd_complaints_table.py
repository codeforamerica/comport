"""Create WPD complaints table

Revision ID: 0de6730e3d41
Revises: 2f13ffb1ce60
Create Date: 2017-11-29 21:58:00.624361

"""

# revision identifiers, used by Alembic.
revision = '0de6730e3d41'
down_revision = '2f13ffb1ce60'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table(
        'citizen_complaints_wpd',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('department_id', sa.Integer(), sa.ForeignKey('departments.id'), nullable=False),
        sa.Column('incident_id', sa.String(255), unique=False, nullable=True),
        sa.Column('received_date', sa.DateTime, unique=False, nullable=True),
        sa.Column('division', sa.String(255), unique=False, nullable=True),
        sa.Column('bureau', sa.String(255), unique=False, nullable=True),
        sa.Column('shift', sa.String(255), unique=False, nullable=True),
        sa.Column('service_type', sa.String(255), unique=False, nullable=True),
        sa.Column('source', sa.String(255), unique=False, nullable=True),
        sa.Column('incident_type', sa.String(255), unique=False, nullable=True),
        sa.Column('allegation', sa.String(255), unique=False, nullable=True),
        sa.Column('finding', sa.String(255), unique=False, nullable=True),
        sa.Column('disposition', sa.String(255), unique=False, nullable=True),
        sa.Column('citizen_id', sa.String(255), unique=False, nullable=True),
        sa.Column('citizen_race', sa.String(255), unique=False, nullable=True),
        sa.Column('citizen_sex', sa.String(255), unique=False, nullable=True),
        sa.Column('citizen_age', sa.String(255), unique=False, nullable=True),
        sa.Column('officer_id', sa.String(255), unique=False, nullable=True),
        sa.Column('officer_race', sa.String(255), unique=False, nullable=True),
        sa.Column('officer_sex', sa.String(255), unique=False, nullable=True),
        sa.Column('officer_age', sa.String(255), unique=False, nullable=True),
        sa.Column('officer_years_of_service', sa.String(255), unique=False, nullable=True),
        sa.ForeignKeyConstraint(['department_id'], ['departments.id']),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade():
    op.drop_table('citizen_complaints_wpd')
