#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import datetime
from copy import deepcopy
from dateutil.relativedelta import relativedelta
from random import randint
from flask_script import Manager, Shell, Server, prompt_pass, prompt_bool
from flask_migrate import MigrateCommand, upgrade
from comport.content.defaults import ChartBlockDefaults
from comport.app import create_app
from comport.user.models import User, Role
from comport.department.models import Department, Extractor
from comport.settings import DevConfig, ProdConfig
from comport.database import db
from comport.data.models import DenominatorValue, DemographicValue
from testclient.JSON_test_client import JSONTestClient
import importlib

# set environment variables from the .env file
if os.path.exists('.env'):
    for line in open('.env'):
        var = [item.strip() for item in line.strip().split('=')]
        if len(var) == 2:
            os.environ[var[0]] = var[1]

# pick a configuration object
if os.environ.get("COMPORT_ENV") == 'prod':
    config_object = ProdConfig
else:
    # No Slack webhook URL for testing
    if 'SLACK_WEBHOOK_URL' in os.environ:
        del(os.environ['SLACK_WEBHOOK_URL'])
    config_object = DevConfig

# create the app
app = create_app(config_object)

HERE = os.path.abspath(os.path.dirname(__file__))
TEST_PATH = os.path.join(HERE, 'tests')

manager = Manager(app)

def _make_context():
    ''' Return context dict for a shell session.
    '''
    # generate a list of all the incident classes
    short_names = ["IMPD"]
    incident_prefixes = ["UseOfForceIncident", "AssaultOnOfficer", "CitizenComplaint", "OfficerInvolvedShooting"]
    incident_classes = {}
    for name in short_names:
        for prefix in incident_prefixes:
            class_name = prefix + name
            incident_classes[class_name] = getattr(importlib.import_module("comport.data.models"), class_name)

    context = {'app': app, 'db': db, 'User': User, 'Department': Department, 'Extractor': Extractor}
    # update the context with the incident classes
    context.update(incident_classes)

    return context


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
def delete_everything():
    db.reflect()
    db.drop_all()
    upgrade()

@manager.command
def add_new_blocks():
    for department in Department.query.all():
        for block in ChartBlockDefaults.defaults:
            if block.slug not in [x.slug for x in department.chart_blocks]:
                print("adding {} to {}".format(block.slug, department.name))
                # Attempting to save had removed identical chart blocks from previously
                # iterated departments. Passing in a deep copy here prevents that.
                department.chart_blocks.append(deepcopy(block))
                department.save()
    db.session.commit()


@manager.command
def test_client():
    ''' Erase the database and load in a full suite of test data
    '''
    if not prompt_bool("Are you sure you want to destroy and recreate Comport's database?"):
        return

    delete_everything()

    # create a fake PD and admin user
    department = Department.create(name="Izquierda Metropolitan Police Department", short_name="IMPD", load_defaults=True)
    user = User.create(username="user", email="user@example.com", password="password", active=True, is_admin=True)
    user.departments.append(department)
    user.save()

    # create some fake officer out on service data
    date_now = datetime.datetime.now()
    date_step = date_now - relativedelta(months=30)
    while date_step.year < date_now.year or date_step.month < date_now.month:
        DenominatorValue.create(
            department_id=department.id,
            month=date_step.month,
            year=date_step.year,
            officers_out_on_service=(100000 + (randint(0, 46000) - 23000))
        )
        date_step = date_step + relativedelta(months=1)

    # create some fake demographic data
    demo_template = [
        dict(race="Asian", city_factor=0.0194, dept_factor=0.0013),
        dict(race="Black", city_factor=0.2452, dept_factor=0.1402),
        dict(race="Hispanic", city_factor=0.0861, dept_factor=0.0253),
        dict(race="Other", city_factor=0.0699, dept_factor=0.0101),
        dict(race="White", city_factor=0.5794, dept_factor=0.8231)
    ]

    # for the city
    city_population = 100000 + round(100000 * ((randint(0, 16) / 100) - .08))
    for value in demo_template:
        DemographicValue.create(
            department_id=department.id,
            race=value["race"],
            count=round(city_population * value["city_factor"]),
            department_value=False
        )

    # for the department
    dept_population = 1500 + round(1500 * ((randint(0, 16) / 100) - .08))
    for value in demo_template:
        DemographicValue.create(
            department_id=department.id,
            race=value["race"],
            count=round(dept_population * value["dept_factor"]),
            department_value=True
        )

    # create a JSON test client and run it
    test_client = JSONTestClient()
    mutations = []
    # mutations.append(MissingDataMutator())
    # mutations.append(FuzzedDataMutator())
    # mutations.append(KnownBadDataMutator())
    # mutations.append(EmptyDataMutator())
    # mutations.append(CasingMutator())
    # mutations.append(CondenisngDateMutator())
    # mutations.append(GapDateMutator())

    test_client.run(department, mutations)


manager.add_command('server', Server())
manager.add_command('shell', Shell(make_context=_make_context))
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
