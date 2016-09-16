# -*- coding: utf-8 -*-
import factory
from factory.fuzzy import FuzzyText, FuzzyDate, FuzzyChoice
from factory.alchemy import SQLAlchemyModelFactory

from comport.user.models import User
from comport.department.models import Department
from comport.data.models import UseOfForceIncidentLMPD
from comport.database import db
import datetime

class BaseFactory(SQLAlchemyModelFactory):

    class Meta:
        abstract = True
        sqlalchemy_session = db.session

class DepartmentFactory(BaseFactory):
    name = factory.Sequence(lambda n: "Factory{0} Police Department".format(n))
    short_name = factory.Sequence(lambda n: "F{0}PD".format(n))
    load_defaults = False

    class Meta:
        model = Department

class UserFactory(BaseFactory):
    username = factory.Sequence(lambda n: "user{0}".format(n))
    email = factory.Sequence(lambda n: "user{0}@example.com".format(n))
    password = factory.PostGenerationMethodCall('set_password', 'example')
    active = True

    class Meta:
        model = User

class UseOfForceIncidentLMPDFactory(BaseFactory):
    ''' Generate a fake LMPD uof incident. Must pass a department_id when using.
    '''
    opaque_id = FuzzyText(length=32)
    occured_date = FuzzyDate(datetime.date(2015, 1, 1))
    bureau = FuzzyText(length=16)
    division = FuzzyText(length=16)
    unit = FuzzyText(length=16)
    platoon = FuzzyText(length=16)
    disposition = FuzzyText(length=16)
    use_of_force_reason = FuzzyText(length=16)
    officer_force_type = FuzzyText(length=16)
    service_type = FuzzyText(length=16)
    arrest_made = FuzzyChoice([True, False])
    arrest_charges = FuzzyText(length=16)
    resident_injured = FuzzyChoice([True, False])
    resident_hospitalized = FuzzyChoice([True, False])
    resident_condition = FuzzyText(length=16)
    officer_injured = FuzzyChoice([True, False])
    officer_hospitalized = FuzzyChoice([True, False])
    officer_condition = FuzzyText(length=16)
    resident_identifier = FuzzyText(length=32)
    resident_weapon_used = FuzzyText(length=16)
    resident_race = FuzzyText(length=16)
    resident_sex = FuzzyText(length=16)
    resident_age = FuzzyText(length=16)
    officer_race = FuzzyText(length=16)
    officer_sex = FuzzyText(length=16)
    officer_age = FuzzyText(length=16)
    officer_years_of_service = FuzzyText(length=16)
    officer_identifier = FuzzyText(length=32)

    class Meta:
        model = UseOfForceIncidentLMPD
