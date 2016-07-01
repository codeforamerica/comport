"""empty message

Revision ID: 51524883509
Revises: 16b50a2c53b
Create Date: 2015-12-21 15:33:48.694126

"""

# revision identifiers, used by Alembic.
revision = '51524883509'
down_revision = '16b50a2c53b'

from alembic import op
import sqlalchemy as sa
from sqlalchemy.orm import Session
from sqlalchemy import text


def upgrade():
    bind = op.get_bind()
    session = Session(bind=bind)

    department_query = text("SELECT * FROM departments")
    for department in session.execute(department_query):
        short_name = "".join([x[0] for x in department.name.split(" ")])
        department.short_name = short_name
    session.commit()

    op.alter_column('departments', 'short_name', existing_type=sa.VARCHAR(length=80), nullable=False)


def downgrade():
    op.alter_column('departments', 'short_name', existing_type=sa.VARCHAR(length=80), nullable=True)
