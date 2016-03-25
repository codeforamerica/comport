#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from flask_script import Manager, Shell, Server, prompt_pass
from flask_migrate import MigrateCommand, upgrade
from comport.content.defaults import ChartBlockDefaults


from comport.app import create_app
from comport.user.models import User, Role
from comport.department.models import Department, Extractor
from comport.settings import DevConfig, ProdConfig, Config
from comport.database import db
from comport.utils import parse_csv_date
from comport.data.models import UseOfForceIncident, CitizenComplaint, DenominatorValue, DemographicValue, OfficerInvolvedShooting
import glob
import csv
import hashlib
from testclient.JSON_test_client import JSONTestClient

if os.environ.get("COMPORT_ENV") == 'prod':
    app = create_app(ProdConfig)
else:
    app = create_app(DevConfig)

HERE = os.path.abspath(os.path.dirname(__file__))
TEST_PATH = os.path.join(HERE, 'tests')

manager = Manager(app)


def _make_context():
    """Return context dict for a shell session so you can access
    app, db, and the User model by default.
    """
    return {'app': app, 'db': db, 'User': User, 'Department': Department, 'Extractor': Extractor, 'UseOfForceIncident': UseOfForceIncident, "CitizenComplaint": CitizenComplaint, "OfficerInvolvedShooting": OfficerInvolvedShooting}


@manager.command
def test():
    """Run the tests."""
    import pytest
    exit_code = pytest.main([TEST_PATH, '-x', '--verbose'])
    return exit_code


@manager.command
def make_admin_user():
    password = prompt_pass("Password")
    user = User.create(username="admin", email="email@example.com", password=password, active=True)
    admin_role = Role(name='admin')
    admin_role.save()
    user.roles.append(admin_role)
    user.save()

@manager.command
def load_test_data():
    department = Department.query.filter_by(name="Indianapolis Metropolitan Police Department", short_name="IMPD").first()
    if not department:
        department = Department.create(name="Indianapolis Metropolitan Police Department", short_name="IMPD")
    if not User.query.filter_by(username="user").first():
        User.create(username="user", email="email2@example.com", password="password", active=True, department_id=department.id)

    for filename in glob.glob('data/testdata/complaints/complaints.csv'):
        with open(filename, 'rt') as f:
            reader = csv.DictReader(f)
            for complaint in reader:
                officer_identifier = hashlib.md5((complaint.get("OFFNUM", None) + Config.SECRET_KEY).encode('UTF-8')).hexdigest()
                opaque_id = hashlib.md5((complaint.get("INCNUM", None) + Config.SECRET_KEY).encode('UTF-8')).hexdigest()

                CitizenComplaint.create(
                    opaque_id=opaque_id,
                    department_id=department.id,
                    occured_date=parse_csv_date(complaint.get("OCCURRED_DT", None)),
                    division=complaint.get("UDTEXT24A", None),
                    precinct=complaint.get("UDTEXT24B", None),
                    shift=complaint.get("UDTEXT24C", None),
                    beat=complaint.get("UDTEXT24D", None),
                    disposition=complaint.get("FINDING", None),
                    allegation_type=complaint.get("ALG_CLASS", None),
                    allegation=complaint.get("ALLEGATION", None),
                    census_tract=None,
                    resident_race=complaint.get("RACE", None),
                    officer_race=complaint.get("OFF_RACE", None),
                    resident_sex=complaint.get("SEX", None),
                    officer_sex=complaint.get("OFF_SEX", None),
                    officer_identifier=officer_identifier,
                    officer_years_of_service=complaint.get("OFF_YR_EMPLOY", None),
                    officer_age=complaint.get("OFF_AGE", None),
                    resident_age=complaint.get("CIT_AGE", None)
                )

    for filename in glob.glob('data/testdata/uof/uof.csv'):
        with open(filename, 'rt') as f:
            reader = csv.DictReader(f)
            for incident in reader:
                officer_identifier = hashlib.md5((incident.get("OFFNUM", None) + Config.SECRET_KEY).encode('UTF-8')).hexdigest()
                opaque_id = hashlib.md5((incident.get("INCNUM", None) + Config.SECRET_KEY).encode('UTF-8')).hexdigest()

                UseOfForceIncident.create(
                    department_id=department.id,
                    opaque_id=opaque_id,
                    occured_date=parse_csv_date(incident.get("OCCURRED_DT", None)),
                    division=incident.get("UDTEXT24A", None),
                    precinct=incident.get("UDTEXT24B", None),
                    shift=incident.get("UDTEXT24C", None),
                    beat=incident.get("UDTEXT24D", None),
                    disposition=incident.get("DISPOSITION", None),
                    census_tract=None,
                    officer_force_type=incident.get("UOF_FORCE_TYPE", None),
                    resident_resist_type=None,
                    officer_weapon_used=None,
                    resident_weapon_used=None,
                    service_type=incident.get("SERVICE_TYPE", None),
                    arrest_made=incident.get("CIT_ARRESTED", None),
                    arrest_charges=incident.get("CITCHARGE_TYPE", None),
                    resident_injured=incident.get("CIT_INJURED", None),
                    resident_hospitalized=incident.get("CIT_HOSPITAL", None),
                    officer_injured=incident.get("OFF_INJURED", None),
                    officer_hospitalized=incident.get("OFF_HOSPITAL", None),
                    use_of_force_reason=incident.get("UOF_REASON", None),
                    resident_race=incident.get("RACE", None),
                    officer_race=incident.get("OFF_RACE", None),
                    resident_sex=incident.get("SEX", None),
                    officer_sex=incident.get("OFF_SEX", None),
                    officer_identifier=officer_identifier,
                    officer_years_of_service=incident.get("OFF_YR_EMPLOY", None),
                    officer_age=incident.get("OFF_AGE", None),
                    resident_age=incident.get("CIT_AGE", None),
                    officer_condition=incident.get("OFF_COND_TYPE", None),
                    resident_condition=incident.get("CIT_COND_TYPE", None)
                )

    for filename in glob.glob('data/testdata/ois/ois.csv'):
        with open(filename, 'rt') as f:
            reader = csv.DictReader(f)
            for incident in reader:
                officer_identifier = hashlib.md5((incident.get("OFFNUM", None) + Config.SECRET_KEY).encode('UTF-8')).hexdigest()
                opaque_id = hashlib.md5((incident.get("INCNUM", None) + Config.SECRET_KEY).encode('UTF-8')).hexdigest()

                OfficerInvolvedShooting.create(
                    department_id=department.id,
                    opaque_id=opaque_id,
                    occured_date=parse_csv_date(incident.get("OCCURRED_DT", None)),
                    division=incident.get("UDTEXT24A", None),
                    precinct=incident.get("UDTEXT24B", None),
                    shift=incident.get("UDTEXT24C", None),
                    beat=incident.get("UDTEXT24D", None),
                    disposition=incident.get("DISPOSITION", None),
                    census_tract=None,
                    officer_weapon_used=incident.get("WEAPON_TYPE", None),
                    resident_weapon_used=incident.get("CIT_WEAPON_TYPE", None),
                    service_type=incident.get("SERVICE_TYPE", None),
                    resident_race=incident.get("RACE", None),
                    officer_race=incident.get("OFF_RACE", None),
                    resident_sex=incident.get("SEX", None),
                    officer_sex=incident.get("OFF_SEX", None),
                    officer_identifier=officer_identifier,
                    officer_years_of_service=incident.get("OFF_YR_EMPLOY", None),
                    officer_age=incident.get("OFF_AGE", None),
                    resident_age=incident.get("CIT_AGE", None),
                    officer_condition=incident.get("OFF_COND_TYPE", None),
                    resident_condition=incident.get("CIT_COND_TYPE", None)
                )

    for filename in glob.glob('data/testdata/denominators/denominators.csv'):
        with open(filename, 'rt') as f:
            reader = csv.DictReader(f)
            for month in reader:
                DenominatorValue.create(
                    department_id=department.id,
                    month=month.get("month", None),
                    year=month.get("year", None),
                    officers_out_on_service=month.get("officers out on service", None)
                )

    for filename in glob.glob('data/testdata/demographics/demographics.csv'):
        with open(filename, 'rt') as f:
            reader = csv.DictReader(f)
            for value in reader:
                DemographicValue.create(
                    department_id=department.id,
                    race=value.get("race", None),
                    count=value.get("count", None),
                    department_value=value.get("cityOrDepartment", None) == "department"
                )

@manager.command
def delete_everything():
    db.reflect()
    db.drop_all()
    upgrade()

@manager.command
def add_new_blocks():
    for department in Department.query.all():
        for block in ChartBlockDefaults.defaults:
            if block.slug not in [x.slug for x in department.chart_blocks]:
                print("adding %s to %s", [block.slug, department.name])
                department.chart_blocks.append(block)
                department.save()
    db.session.commit()


@manager.command
def test_client():
    delete_everything()
    department = Department.create(name="Busy Town Police Department", short_name="BTPD", load_defaults=True)
    user = User.create(username="user", email="email2@example.com", password="password", active=True, is_admin=True)
    user.departments.append(department)
    user.save()

    test_client = JSONTestClient()
    # missing_data_mutator = MissingDataMutator()
    # fuzzed_data_mutator = FuzzedDataMutator()
    # known_bad_data_mutator = KnownBadDataMutator()
    # empty_data_mutator = EmptyDataMutator()
    # casing_mutator = CasingMutator()
    # condenisng_date_mutator = CondenisngDateMutator()
    # gap_date_mutator = GapDateMutator()

    test_client.run(department, [])


manager.add_command('server', Server())
manager.add_command('shell', Shell(make_context=_make_context))
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
