"""Add 'is_public' flags for datasets

Revision ID: 0d78d545906f
Revises: 6d30846080b2
Create Date: 2016-06-27 15:30:14.415519

"""

# revision identifiers, used by Alembic.
revision = '0d78d545906f'
down_revision = '6d30846080b2'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column('departments', sa.Column('is_public_assaults_on_officers', sa.Boolean(), server_default=sa.true(), nullable=False))
    op.add_column('departments', sa.Column('is_public_citizen_complaints', sa.Boolean(), server_default=sa.true(), nullable=False))
    op.add_column('departments', sa.Column('is_public_officer_involved_shootings', sa.Boolean(), server_default=sa.true(), nullable=False))
    op.add_column('departments', sa.Column('is_public_use_of_force_incidents', sa.Boolean(), server_default=sa.true(), nullable=False))


def downgrade():
    op.drop_column('departments', 'is_public_use_of_force_incidents')
    op.drop_column('departments', 'is_public_officer_involved_shootings')
    op.drop_column('departments', 'is_public_citizen_complaints')
    op.drop_column('departments', 'is_public_assaults_on_officers')
