# -*- coding: utf-8 -*-
from factory import Sequence, PostGenerationMethodCall, LazyAttribute
from factory.fuzzy import FuzzyText, FuzzyNaiveDateTime, FuzzyChoice, BaseFuzzyAttribute, _random, FuzzyInteger
from factory.alchemy import SQLAlchemyModelFactory

from comport.user.models import User
from comport.department.models import Department
from comport.data.models import UseOfForceIncident
from comport.database import db
from comport.utils import random_date, factory_random_string
from datetime import date, datetime, timedelta


import random





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
    service_type = FuzzyChoice(["Arresting", "Call for Service","Code Inforcement", "Interviewing","Restraining", "Transporting", None])
    use_of_force_reason = FuzzyChoice(["Assaulting Citizen(s)","Assaulting Officer","Combative Subject","Damage to City Prop.","Damage to Private Prop.","Non-compliance","Resisting Arrest", None])
    resident_weapon_used = FuzzyChoice(["Gun","Knife","Verbal threats", None])
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
    division = FuzzyChoice([
                ["Chiefs Staff Division","Court Liaison","",""],
                ["Investigative Division","Crime Prevention","C Shift",""],
                ["Investigative Division","Detective Bureau","Auto Theft Unit","Evenings"],
                ["Investigative Division","Detective Bureau","Auto Theft Unit","Off Duty"],
                ["Investigative Division","Detective Bureau","Auto Theft Unit","Rotating"],
                ["Investigative Division","Detective Bureau","Homicide  Unit","Evenings"],
                ["Investigative Division","Detective Bureau","Homicide  Unit","Rotating"],
                ["Investigative Division","First Precinct","A Shift","X21 Zone"],
                ["Investigative Division","First Precinct","A Shift","X22 Zone"],
                ["Investigative Division","First Precinct","B Shift","X26 Zone"],
                ["Investigative Division","Second Precinct","Day Beats","Beat 19"],
                ["Investigative Division","Special Investigations","Computer Crimes","Days"],
                ["Investigative Division","Special Investigations","Computer Crimes","Evenings"],
                ["Investigative Division","Special Investigations","Criminal Intelligence","Days"],
                ["Investigative Division","Special Investigations","Day Beats","Beat 19"],
                ["Investigative Division","Special Investigations","K 9 Unit","Days"],
                ["Investigative Division","Special Investigations","Narcotics","Days"],
                ["Investigative Division","Special Investigations","Vice","Evenings"],
                ["Operational Bureau","First Precinct","C Shift","X25 Zone"],
                ["Operational Bureau","Fourth Precinct","C.O.P. Program","Days"],
                ["Operational Bureau","Fourth Precinct","Unknown","Unknown"],
                ["Operational Bureau","Second Precinct","B Shift","X20 Zone"],
                ["Operational Bureau","Second Precinct","Day Beats","Beat 18"],
                ["Operational Bureau","Second Precinct","Day Beats","Beat 19"],
                ["Operational Bureau","Third Precinct","C Shift","X26 Zone"],
                ["Operational Division","Crime Prevention","B Shift","X27 Zone"],
                ["Operational Division","Detective Bureau","Auto Theft Unit","Days"],
                ["Operational Division","First Precinct","A Shift","X20 Zone"],
                ["Operational Division","First Precinct","A Shift","X22 Zone"],
                ["Operational Division","First Precinct","A Shift","X23 Zone"],
                ["Operational Division","First Precinct","A Shift","X24 Zone"],
                ["Operational Division","First Precinct","A Shift","X25 Zone"],
                ["Operational Division","First Precinct","A Shift","X26 Zone"],
                ["Operational Division","First Precinct","A Shift","X27 Zone"],
                ["Operational Division","First Precinct","B Shift","Beat 20"],
                ["Operational Division","First Precinct","B Shift","X20 Zone"],
                ["Operational Division","First Precinct","B Shift","X21 Zone"],
                ["Operational Division","First Precinct","B Shift","X22 Zone"],
                ["Operational Division","First Precinct","B Shift","X23 Zone"],
                ["Operational Division","First Precinct","B Shift","X24 Zone"],
                ["Operational Division","First Precinct","B Shift","X26 Zone"],
                ["Operational Division","First Precinct","B Shift","X27 Zone"],
                ["Operational Division","First Precinct","B Shift","X28 Zone"],
                ["Operational Division","First Precinct","C Shift","X20 Zone"],
                ["Operational Division","First Precinct","C Shift","X21 Zone"],
                ["Operational Division","First Precinct","C Shift","X23 Zone"],
                ["Operational Division","First Precinct","C Shift","X24 Zone"],
                ["Operational Division","First Precinct","C Shift","X25 Zone"],
                ["Operational Division","Fourth Precinct","A Shift","X20 Zone"],
                ["Operational Division","Fourth Precinct","A Shift","X22 Zone"],
                ["Operational Division","Fourth Precinct","A Shift","X24 Zone"],
                ["Operational Division","Fourth Precinct","B Shift","Beat 23"],
                ["Operational Division","Fourth Precinct","B Shift","X25 Zone"],
                ["Operational Division","Fourth Precinct","B Shift","X27 Zone"],
                ["Operational Division","Fourth Precinct","C Shift","Beat 20"],
                ["Operational Division","Fourth Precinct","C Shift","Beat 23"],
                ["Operational Division","Fourth Precinct","C Shift","X20 Zone"],
                ["Operational Division","Fourth Precinct","C Shift","X21 Zone"],
                ["Operational Division","Fourth Precinct","C Shift","X22 Zone"],
                ["Operational Division","Fourth Precinct","C Shift","X25 Zone"],
                ["Operational Division","Fourth Precinct","C Shift","X27 Zone"],
                ["Operational Division","Fourth Precinct","Commanding Officer","Days"],
                ["Operational Division","Second Precinct","A Shift","Beat 14"],
                ["Operational Division","Second Precinct","A Shift","Beat 17"],
                ["Operational Division","Second Precinct","A Shift","Beat 19"],
                ["Operational Division","Second Precinct","A Shift","X20 Zone"],
                ["Operational Division","Second Precinct","B Shift","X20 Zone"],
                ["Operational Division","Second Precinct","B Shift","X23 Zone"],
                ["Operational Division","Second Precinct","B Shift","X25 Zone"],
                ["Operational Division","Second Precinct","C Shift","X22 Zone"],
                ["Operational Division","Second Precinct","Day Beats",""],
                ["Operational Division","Second Precinct","Day Beats","Beat 15"],
                ["Operational Division","Second Precinct","Day Beats","Beat 19"],
                ["Operational Division","Second Precinct","Day Beats","Beat 20"],
                ["Operational Division","Second Precinct","Days Bikes","Beat 19"],
                ["Operational Division","Second Precinct","Days Bikes","Evenings"],
                ["Operational Division","Second Precinct","Night Beats","Beat 19"],
                ["Operational Division","Second Precinct","Night Beats","Evenings"],
                ["Operational Division","Second Precinct","Oceanfront","Day Bikes"],
                ["Operational Division","Second Precinct","Off Duty / LE","Evenings"],
                ["Operational Division","Special Investigations","B Shift","X20 Zone"],
                ["Operational Division","Special Investigations","Bomb Squad","Beat 20"],
                ["Operational Division","Special Operations","Bomb Squad","Rotating"],
                ["Operational Division","Special Operations","SWAT Team","	"],
                ["Operational Division","Special Operations","SWAT Team","MidNights"],
                ["Operational Division","Special Operations","SWAT Team","Rotating"],
                ["Operational Division","Third Precinct","A Shift","C.O.P."],
                ["Operational Division","Third Precinct","B Shift","X22 Zone"],
                ["Operational Division","Third Precinct","B Shift","X24 Zone"],
                ["Operational Division","Third Precinct","C Shift","X26 Zone"],
                ["Operational Division","Third Precinct","C Shift","X29 Zone"],
                ["Prof. Dev and Training","VBLETA","Instructor","Days"],
                ["Support Division","Logistical Support","A Shift",""],
                [None,None,None,None],
                [None,None,None,None],
                [None,None,None,None],
                [None,None,None,None]]

)
    precinct = None
    shift = None
    beat = None
    disposition = FuzzyChoice([
        "Inactivated",
        "Informational Purpose On",
        "No Violation",
        "Not Sustained",
        "Not within Policy",
        "Partially Sustained",
        "Sustained",
        "Unfounded/Exonerated",
        "Unfounded/False",
        "Unfounded/Not Involved",
        "Unfounded/Unwarranted",
        "Withdrawn",
        "Within policy",
        None
    ])
    officer_force_type = FuzzyChoice([
        "Capstun",
        "Distraction Techniques",
        "Expandable Baton",
        "Hand Cuffed",
        "Hands On",
        "K-9 Utilized",
        "Kicked",
        "Pain Compliance",
        "Pinched",
        "Pressure Points",
        "Punched",
        "Restraints",
        "Sage Impact",
        "Side Handle Baton",
        "Taser",
        "Verbal",
        None
    ])
    resident_resist_type = FuzzyChoice([
        "Active Aggression",
        "Bite",
        "Deadly Force Assualt",
        "Defensive Resistance",
        "Flash Light to the Head",
        "Fled",
        "Kicked",
        "Passive Resistance",
        "Pinched",
        "Psycholog  Intimidation",
        "Punched",
        "Spit",
        "Stricking",
        "Used Knife",
        "Used other object",
        "Verbal Resistance",
        None
    ])
    officer_weapon_used = FuzzyChoice(["Gun","Handcuffs","Physical",None])
    resident_weapon_used = FuzzyChoice(["Gun","Knife","Verbal threats",None])

    arrest_made = FuzzyChoice([True, False, None])
    arrest_charges = LazyAttribute(lambda i: random.choice(["18.2.63 FALE",
        "18.2.64 FALE","18.2.64 Felony Assualt LEO","18.2-60","18.2-60 ASLE",
        "18.2-60 FALE","18.2-64 FALE","18.2-64 FAOLE",
        "18.2-64 Felony assualt LE","Assault of LE Officer","Assault on LE",
        "Assult on L/E (felony)","Felonious assault on LE",
        "Felony assault on LE","Felony Assualt on LE","Resisting Arrest"])
        if i.arrest_made == True else None)
    resident_injured = FuzzyChoice([True, False, None])
    resident_hospitalized =  FuzzyChoice([True, False, None])
    officer_injured = FuzzyChoice([True, False, None])
    officer_hospitalized =  FuzzyChoice([True, False, None])
    resident_race = FuzzyChoice(["Asian","Black","Hispanic","Native Ameri","Polynesian","Unknown","White", None])
    officer_race = FuzzyChoice(["Asian","Black","Hispanic","Native Ameri","Polynesian","Unknown","White", None])
    officer_identifier = FuzzyChoice([factory_random_string(12) for x in range(30)])
    officer_years_of_service = FuzzyInteger(30)

    @classmethod
    def _after_postgeneration(cls, obj,create,results=None):
        tmp = obj.division
        obj.division = tmp[0]
        obj.precinct = tmp[1]
        obj.shift = tmp[2]
        obj.beat = tmp[3]



    class Meta:
        model = UseOfForceIncident
