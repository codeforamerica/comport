"""Change the BPD OIS varchar disposition column to a boolean has_disposition column.

Revision ID: 7f4ae427dcf6
Revises: 513f93441476
Create Date: 2016-11-15 15:00:10.729390

"""

# revision identifiers, used by Alembic.
revision = '7f4ae427dcf6'
down_revision = '513f93441476'

from alembic import op
import sqlalchemy as sa


def upgrade():
    # create the has_disposition column
    op.add_column('officer_involved_shootings_bpd', sa.Column('has_disposition', sa.Boolean(), nullable=True))

    # update the has_disposition column based on values in the disposition column
    db_bind = op.get_bind()
    db_bind.execute(sa.sql.text('''
        UPDATE officer_involved_shootings_bpd SET has_disposition = (disposition != '' AND disposition IS NOT NULL)
    '''))

    # drop the disposition column
    op.drop_column('officer_involved_shootings_bpd', 'disposition')


def downgrade():
    op.add_column('officer_involved_shootings_bpd', sa.Column('disposition', sa.VARCHAR(length=255), autoincrement=False, nullable=True))
    op.drop_column('officer_involved_shootings_bpd', 'has_disposition')
