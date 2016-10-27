"""fix capitalization for 'allegation'

Revision ID: 300d0c0b7f6
Revises: 513f93441476
Create Date: 2016-10-27 17:48:09.758346

"""

# revision identifiers, used by Alembic.
revision = '300d0c0b7f6'
down_revision = '513f93441476'

from alembic import op
import sqlalchemy as sa
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
   