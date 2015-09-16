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
    occured_date = FuzzyNaiveDateTime(start_dt= datetime(2012, 1, 1))
    received_date = LazyAttribute(lambda a: random_date(a.occured_date, a.occured_date + timedelta(days=7)))
    service_type = FuzzyChoice(["Arresting", "Call for Service","Code Inforcement", "Interviewing","Restraining", "Transporting", None])
    use_of_force_reason = FuzzyChoice(["Assaulting Citizen(s)","Assaulting Officer","Combative Subject","Damage to City Prop.","Damage to Private Prop.","Non-compliance","Resisting Arrest", None])
    citizen_weapon = FuzzyChoice(["Gun","Knife","Verbal threats", None])
    census_tract = FuzzyChoice(["3101.03","3101.04","3101.05","3101.06",
        "3101.08","3101.10","3101.11","3102.01","3102.03","3102.04","3103.05",
        "3103.06","3103.08","3103.09","3103.10","3103.12","3201.05","3201.06",
        "3201.07","3201.08","3201.09","3202.02","3202.03","3202.04","3203.01",
        "3203.03","3203.04","3204","3205","3207","3208","3209.01","3209.02",
        "3209.03","3210.01","3210.02","3211","3212","3213","3214","3216","3217",
        "3218","3219","3220","3221","3222","3224","3225","3226","3227",
        "3301.03","3301.05","3301.06","3301.08","3302.02","3302.08","3304.01",
        "3305","3306","3307","3308.03","3308.04","3308.05","3308.06","3309",
        "3310","3401.01","3401.02","3401.08","3401.09","3401.10","3401.11",
        "3401.12","3402.01","3402.02","3403","3404","3405","3406","3407",
        "3409.02","3410","3417","3419.02","3419.03","3419.04","3421.01","3422",
        "3423","3501","3503","3505","3506","3508","3510","3512","3516","3524",
        "3527","3528","3533","3535","3536","3542","3547","3554","3562","3573",
        "3574","3579","3581","3601.01","3601.02","3602.01","3603.01","3603.02",
        "3604.01","3604.02","3604.04","3604.05","3605.01","3605.02","3606.01",
        "3606.02","3608","3609","3611","3614","3702.01","3702.02","3703.01",
        "3801","3802","3803","3804.02","3804.03","3804.04","3805.01","3805.02",
        "3806","3807","3809.02","3810.01","3810.02","3811.01","3811.02","3812.01",
        "3812.03","3812.04","3812.05","3901.02","3902","3904.02","3904.03","3904.04",
        "3904.05","3905","3906","3909","3910", None, None, None, None, None,
        None, None, None, None, None])


    class Meta:
        model = UseOfForceIncident
