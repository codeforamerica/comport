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
        sa.Column('updated_date', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['department_id'], ['departments.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_incidents_updated_opaque_id'), 'incidents_updated', ['opaque_id'], unique=False)

    # populate the table from existing records
    db_bind = op.get_bind()
    db_bind.execute(sa.sql.text('''
        INSERT INTO incidents_updated
            (department_id, opaque_id, updated_date)
            (
                SELECT MAX(department_id), opaque_id, CURRENT_DATE
                FROM citizen_complaints_impd GROUP BY opaque_id
                UNION
                SELECT MAX(department_id), opaque_id, CURRENT_DATE
                FROM citizen_complaints_bpd GROUP BY opaque_id
                UNION
                SELECT MAX(department_id), opaque_id, CURRENT_DATE
                FROM officer_involved_shootings_bpd GROUP BY opaque_id
                UNION
                SELECT MAX(department_id), opaque_id, CURRENT_DATE
                FROM officer_involved_shootings_impd GROUP BY opaque_id
                UNION
                SELECT MAX(department_id), opaque_id, CURRENT_DATE
                FROM use_of_force_incidents_bpd GROUP BY opaque_id
                UNION
                SELECT MAX(department_id), opaque_id, CURRENT_DATE
                FROM use_of_force_incidents_impd GROUP BY opaque_id
                UNION
                SELECT MAX(department_id), opaque_id, CURRENT_DATE
                FROM use_of_force_incidents_lmpd GROUP BY opaque_id
            );
    '''))


def downgrade():
    op.drop_index(op.f('ix_incidents_updated_opaque_id'), table_name='incidents_updated')
    op.drop_table('incidents_updated')
