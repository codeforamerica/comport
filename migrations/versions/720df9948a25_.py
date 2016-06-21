"""Create the assaults on officers table

Revision ID: 720df9948a25
Revises: 4e98ea7e43d
Create Date: 2016-06-15 15:47:59.913618

"""

# revision identifiers, used by Alembic.
revision = '720df9948a25'
down_revision = '4e98ea7e43d'

from alembic import op
import sqlalchemy as sa

def upgrade():
    op.create_table(
        'assaults_on_officers',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('department_id', sa.Integer(), nullable=False),
        sa.Column('opaque_id', sa.String(length=255), nullable=False),
        sa.Column('officer_identifier', sa.String(length=255), nullable=True),
        sa.Column('service_type', sa.String(length=255), nullable=True),
        sa.Column('force_type', sa.String(length=255), nullable=True),
        sa.Column('assignment', sa.String(length=255), nullable=True),
        sa.Column('arrest_made', sa.Boolean(), nullable=True),
        sa.Column('officer_injured', sa.Boolean(), nullable=True),
        sa.Column('officer_killed', sa.Boolean(), nullable=True),
        sa.Column('report_filed', sa.Boolean(), nullable=True),
        sa.ForeignKeyConstraint(['department_id'], ['departments.id'], ),
        sa.PrimaryKeyConstraint('id')
    )

def downgrade():
    op.drop_table('assaults_on_officers')
