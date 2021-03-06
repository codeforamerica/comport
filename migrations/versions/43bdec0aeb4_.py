"""empty message

Revision ID: 43bdec0aeb4
Revises: 1392585412d
Create Date: 2015-09-02 10:43:25.250039

"""

# revision identifiers, used by Alembic.
revision = '43bdec0aeb4'
down_revision = '1392585412d'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('invite_codes',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('department_id', sa.Integer(), nullable=True),
    sa.Column('code', sa.String(length=36), nullable=False),
    sa.Column('used', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['department_id'], ['departments.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('code')
    )
    op.create_index(op.f('ix_invite_codes_id'), 'invite_codes', ['id'], unique=False)
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_invite_codes_id'), table_name='invite_codes')
    op.drop_table('invite_codes')
    ### end Alembic commands ###
