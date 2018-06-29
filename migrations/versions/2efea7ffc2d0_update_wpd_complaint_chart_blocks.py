"""Update WPD complaint chart blocks

Revision ID: 2efea7ffc2d0
Revises: 4d1cde26d807
Create Date: 2018-06-29 13:22:12.102836

"""

# revision identifiers, used by Alembic.
revision = '2efea7ffc2d0'
down_revision = '4d1cde26d807'

from alembic import op
import sqlalchemy as sa
from comport.department.models import Department


def upgrade():
    wpd = Department.query.filter_by(short_name='WPD').first()
    connection = op.get_bind()
    connection.execute("UPDATE chart_blocks SET slug = 'complaints-by-officer-with-cap' WHERE department_id = " + str(wpd.id) + " and slug = 'complaints-by-officer'")

def downgrade():
    wpd = Department.query.filter_by(short_name='WPD').first()
    connection = op.get_bind()
    connection.execute("UPDATE chart_blocks SET slug = 'complaints-by-officer' WHERE department_id = " + str(wpd.id) + " and slug = 'complaints-by-officer-with-cap'")
    pass
