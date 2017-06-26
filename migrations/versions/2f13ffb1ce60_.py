"""add bureau and division srpd pursuits

Revision ID: 2f13ffb1ce60
Revises: 14395b9e9208
Create Date: 2017-06-25 23:55:17.512699

"""

# revision identifiers, used by Alembic.
revision = '2f13ffb1ce60'
down_revision = '14395b9e9208'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column('pursuits_srpd', sa.Column('bureau', sa.String(length=255), nullable=True))
    op.add_column('pursuits_srpd', sa.Column('division', sa.String(length=255), nullable=True))


def downgrade():
    op.drop_column('pursuits_srpd', 'division')
    op.drop_column('pursuits_srpd', 'bureau')
