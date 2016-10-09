"""create and populate incidents_updated table

Revision ID: c21533f2fd07
Revises: 1826863c726a
Create Date: 2016-09-17 23:39:00.818737

"""

# revision identifiers, used by Alembic.
revision = 'c21533f2fd07'
down_revision = '1826863c726a'

from alembic import op
import sqlalchemy as sa


def upgrade():
    # create the incidents_updated table
    op.create_table(
        'incidents_updated',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('department_id', sa.Integer(), nullable=False),
        sa.Column('opaque_id', sa.String(length=255), nullable=False),
        sa.Column('incident_type', sa.String(length=32), nullable=False),
        sa.ForeignKeyConstraint(['department_id'], ['departments.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_incidents_updated_opaque_id'), 'incidents_updated', ['opaque_id'], unique=False)


def downgrade():
    op.drop_index(op.f('ix_incidents_updated_opaque_id'), table_name='incidents_updated')
    op.drop_table('incidents_updated')
