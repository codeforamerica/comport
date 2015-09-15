# -*- coding: utf-8 -*-
from factory import Sequence, PostGenerationMethodCall, LazyAttribute
from factory.fuzzy import FuzzyText, FuzzyNaiveDateTime, FuzzyChoice
from factory.alchemy import SQLAlchemyModelFactory

from comport.user.models import User
from comport.department.models import Department
from comport.data.models import UseOfForceIncident
from comport.database import db
from comport.utils import random_date
from datetime import date, datetime, timedelta





class BaseFactory(SQLAlchemyModelFactory):

    class Meta:
        abstract = True
        sqlalchemy_session = db.session

class DepartmentFactory(BaseFactory):
    name = Sequence(lambda n: "Department {0}".format(n))

    class Meta:
        model = Department

class UserFactory(BaseFactory):
    username = Sequence(lambda n: "user{0}".format(n))
    email = Sequence(lambda n: "user{0}@example.com".format(n))
    password = PostGenerationMethodCall('set_password', 'example')
    active = True

    class Meta:
        model = User

class UseOfForceIncidentFactory(BaseFactory):
    opaque_id = FuzzyText(length=12)
    occured_date = FuzzyNaiveDateTime(start_dt= datetime(2008, 1, 1))
    received_date = LazyAttribute(lambda a: random_date(a.occured_date, a.occured_date + timedelta(days=7)))
    service_type = FuzzyChoice(["Arresting", "Call for Service","Code Inforcement", "Interviewing","Restraining", "Transporting", None])
    use_of_force_reason = FuzzyChoice(["Assaulting Citizen(s)","Assaulting Officer","Combative Subject","Damage to City Prop.","Damage to Private Prop.","Non-compliance","Resisting Arrest", None])


    class Meta:
        model = UseOfForceIncident
