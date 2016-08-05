# -*- coding: utf-8 -*-
from factory import Sequence, PostGenerationMethodCall
from factory.fuzzy import FuzzyInteger
from factory.alchemy import SQLAlchemyModelFactory

from comport.user.models import User
from comport.department.models import Department
from comport.data.models import DenominatorValue
from comport.database import db
from datetime import datetime
from dateutil.relativedelta import relativedelta

class BaseFactory(SQLAlchemyModelFactory):

    class Meta:
        abstract = True
        sqlalchemy_session = db.session

class DepartmentFactory(BaseFactory):
    name = Sequence(lambda n: "Department {0}".format(n))
    short_name = Sequence(lambda n: "DPD{0}".format(n))
    load_defaults = False

    class Meta:
        model = Department

class UserFactory(BaseFactory):
    username = Sequence(lambda n: "user{0}".format(n))
    email = Sequence(lambda n: "user{0}@example.com".format(n))
    password = PostGenerationMethodCall('set_password', 'example')
    active = True

    class Meta:
        model = User

class DenominatorValueFactory(BaseFactory):
    month = Sequence(lambda n: datetime(2012, 1, 1) + relativedelta(months=n))
    officers_out_on_service = FuzzyInteger(200, 500)

    class Meta:
        model = DenominatorValue

    @classmethod
    def _after_postgeneration(cls, obj, create, results=None):
        tmp = obj.month
        obj.month = tmp.month
        obj.year = tmp.year
