"""fix capitalization for 'allegation'

Revision ID: 43c4c512514
Revises: ab97630e71ce
Create Date: 2016-11-28 18:36:26.344090

"""

# revision identifiers, used by Alembic.
revision = '43c4c512514'
down_revision = 'ab97630e71ce'

from comport.data.cleaners import Cleaners
from comport.data.models import CitizenComplaintIMPD

def upgrade():
    complaints = CitizenComplaintIMPD.query.all()
    cleaner = Cleaners()
    for complaint in complaints:
        new_allegation = cleaner.capitalize(complaint.allegation)
        if complaint.allegation != new_allegation:
            complaint.update(allegation=new_allegation)

def downgrade():
    pass
