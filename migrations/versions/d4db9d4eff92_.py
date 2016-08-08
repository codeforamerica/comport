"""Rename the incident tables so they all have _impd at the end.

Revision ID: d4db9d4eff92
Revises: 0d39b8d2c5ce
Create Date: 2016-08-04 14:34:33.900556

"""

# revision identifiers, used by Alembic.
revision = 'd4db9d4eff92'
down_revision = '0d39b8d2c5ce'

from alembic import op

def upgrade():
    op.rename_table('use_of_force_incidents', 'use_of_force_incidents_impd')
    op.execute('ALTER SEQUENCE use_of_force_incidents_id_seq RENAME TO use_of_force_incidents_impd_id_seq')
    op.execute('ALTER INDEX use_of_force_incidents_pkey RENAME TO use_of_force_incidents_impd_pkey')
    op.execute('ALTER TABLE use_of_force_incidents_impd RENAME CONSTRAINT "use_of_force_incidents_department_id_fkey" TO "use_of_force_incidents_impd_department_id_fkey"')

    op.rename_table('citizen_complaints', 'citizen_complaints_impd')
    op.execute('ALTER SEQUENCE citizen_complaints_id_seq RENAME TO citizen_complaints_impd_id_seq')
    op.execute('ALTER INDEX citizen_complaints_pkey RENAME TO citizen_complaints_impd_pkey')
    op.execute('ALTER TABLE citizen_complaints_impd RENAME CONSTRAINT "citizen_complaints_department_id_fkey" TO "citizen_complaints_impd_department_id_fkey"')

    op.rename_table('assaults_on_officers', 'assaults_on_officers_impd')
    op.execute('ALTER SEQUENCE assaults_on_officers_id_seq RENAME TO assaults_on_officers_impd_id_seq')
    op.execute('ALTER INDEX assaults_on_officers_pkey RENAME TO assaults_on_officers_impd_pkey')
    op.execute('ALTER TABLE assaults_on_officers_impd RENAME CONSTRAINT "assaults_on_officers_department_id_fkey" TO "assaults_on_officers_impd_department_id_fkey"')

    op.rename_table('officer_involved_shootings', 'officer_involved_shootings_impd')
    op.execute('ALTER SEQUENCE officer_involved_shootings_id_seq RENAME TO officer_involved_shootings_impd_id_seq')
    op.execute('ALTER INDEX officer_involved_shootings_pkey RENAME TO officer_involved_shootings_impd_pkey')
    op.execute('ALTER TABLE officer_involved_shootings_impd RENAME CONSTRAINT "officer_involved_shootings_department_id_fkey" TO "officer_involved_shootings_impd_department_id_fkey"')

def downgrade():
    op.rename_table('use_of_force_incidents_impd', 'use_of_force_incidents')
    op.execute('ALTER SEQUENCE use_of_force_incidents_impd_id_seq RENAME TO use_of_force_incidents_id_seq')
    op.execute('ALTER INDEX use_of_force_incidents_impd_pkey RENAME TO use_of_force_incidents_pkey')
    op.execute('ALTER TABLE use_of_force_incidents RENAME CONSTRAINT "use_of_force_incidents_impd_department_id_fkey" TO "use_of_force_incidents_department_id_fkey"')

    op.rename_table('citizen_complaints_impd', 'citizen_complaints')
    op.execute('ALTER SEQUENCE citizen_complaints_impd_id_seq RENAME TO citizen_complaints_id_seq')
    op.execute('ALTER INDEX citizen_complaints_impd_pkey RENAME TO citizen_complaints_pkey')
    op.execute('ALTER TABLE citizen_complaints RENAME CONSTRAINT "citizen_complaints_impd_department_id_fkey" TO "citizen_complaints_department_id_fkey"')

    op.rename_table('assaults_on_officers_impd', 'assaults_on_officers')
    op.execute('ALTER SEQUENCE assaults_on_officers_impd_id_seq RENAME TO assaults_on_officers_id_seq')
    op.execute('ALTER INDEX assaults_on_officers_impd_pkey RENAME TO assaults_on_officers_pkey')
    op.execute('ALTER TABLE assaults_on_officers RENAME CONSTRAINT "assaults_on_officers_impd_department_id_fkey" TO "assaults_on_officers_department_id_fkey"')

    op.rename_table('officer_involved_shootings_impd', 'officer_involved_shootings')
    op.execute('ALTER SEQUENCE officer_involved_shootings_impd_id_seq RENAME TO officer_involved_shootings_id_seq')
    op.execute('ALTER INDEX officer_involved_shootings_impd_pkey RENAME TO officer_involved_shootings_pkey')
    op.execute('ALTER TABLE officer_involved_shootings RENAME CONSTRAINT "officer_involved_shootings_impd_department_id_fkey" TO "officer_involved_shootings_department_id_fkey"')
