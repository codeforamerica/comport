# -*- coding: utf-8 -*-
import datetime as dt
from comport.database import (
    Column,
    db,
    Model,
    ReferenceCol,
    relationship,
    SurrogatePK,
)
from .csv_utils import csv_utils

from datetime import datetime
from titlecase import titlecase
import types


race_map = {
    "b": "Black"
}

sex_map = {
    "f": "Female",
    "m": "Male"
}

def clean_keys(key):
    return key.lower().strip() if key is not None else None

def abbreviations(word, **kwargs):
   if word.upper() in ('NW', 'SE', 'ED', 'DT', 'FTO', 'ND', 'SW', "DWI"):
     return word.upper()

def capitalize(value):
    if value is None or isinstance(value, list):
        return value
    return titlecase(value.strip(), callback=abbreviations)

def clean_incident(incident, args):
    resident_race = clean_keys(args.pop("resident_race", None))
    resident_sex = clean_keys(args.pop("resident_sex", None))
    precinct = args.pop("precinct", None)
    division = args.pop("division", None)
    shift = args.pop("shift", None)
    beat = args.pop("beat", None)

    if resident_race is not None and resident_race in race_map:
        resident_race = race_map[resident_race]
        incident.resident_race = resident_race
    else:
        incident.resident_race = titlecase(resident_race)

    if resident_sex is not None and resident_sex in sex_map:
        resident_sex = sex_map[resident_sex]
        incident.resident_sex = resident_sex
    else:
        incident.resident_sex = titlecase(resident_sex)

    incident.precinct = capitalize(precinct)
    incident.division = capitalize(division)
    incident.shift = capitalize(shift)
    incident.beat = capitalize(beat)
    return incident

class DenominatorValue(SurrogatePK, Model):
    __tablename__="denominator_values"
    department_id = Column(db.Integer, db.ForeignKey('departments.id'),nullable=False)
    month=Column(db.Integer, unique=False, nullable=False)
    year=Column(db.Integer, unique=False, nullable=False)
    arrests=Column(db.Integer, unique=False, nullable=True)
    calls_for_service=Column(db.Integer, unique=False, nullable=True)
    officer_initiated_calls=Column(db.Integer, unique=False, nullable=True)

    def __init__(self, **kwargs):
        db.Model.__init__(self, **kwargs)

class DemographicValue(SurrogatePK, Model):
    __tablename__="demographic_values"
    department_id = Column(db.Integer, db.ForeignKey('departments.id'),nullable=False)
    race = Column(db.String(255), unique=False, nullable=True)
    gender = Column(db.String(255), unique=False, nullable=True)
    count = Column(db.Integer, unique=False, nullable=True)
    department_value = Column(db.Boolean, nullable=True)

    def __init__(self, **kwargs):
        db.Model.__init__(self, **kwargs)


class UseOfForceIncident(SurrogatePK, Model):
    __tablename__ = 'use_of_force_incidents'
    department_id = Column(db.Integer, db.ForeignKey('departments.id'),nullable=False)
    opaque_id = Column(db.String(255), unique=False, nullable=False)
    occured_date = Column(db.DateTime, nullable=True)
    division = Column(db.String(255), unique=False, nullable=True)
    precinct = Column(db.String(255), unique=False, nullable=True)
    shift = Column(db.String(255), unique=False, nullable=True)
    beat = Column(db.String(255), unique=False, nullable=True)
    disposition = Column(db.String(255), unique=False, nullable=True)
    census_tract = Column(db.String(255), unique=False, nullable=True)
    officer_force_type = Column(db.String(255), unique=False, nullable=True)
    resident_resist_type = Column(db.String(255), unique=False, nullable=True)
    officer_weapon_used = Column(db.String(255), unique=False, nullable=True)
    resident_weapon_used = Column(db.String(255), unique=False, nullable=True)
    service_type = Column(db.String(255), unique=False, nullable=True)
    arrest_made = Column(db.Boolean, nullable=True)
    arrest_charges = Column(db.String(255), unique=False, nullable=True)
    resident_injured = Column(db.Boolean, nullable=True)
    resident_hospitalized = Column(db.Boolean, nullable=True)
    officer_injured = Column(db.Boolean, nullable=True)
    officer_hospitalized = Column(db.Boolean, nullable=True)
    use_of_force_reason = Column(db.String(255), unique=False, nullable=True)
    resident_race = Column(db.String(255), unique=False, nullable=True)
    officer_race = Column(db.String(255), unique=False, nullable=True)
    resident_sex = Column(db.String(255), unique=False, nullable=True)
    officer_sex = Column(db.String(255), unique=False, nullable=True)
    officer_identifier = Column(db.String(255), unique=False, nullable=True)
    officer_years_of_service = Column(db.String(255), unique=False, nullable=True)
    officer_age = Column(db.String(255), unique=False, nullable=True)
    resident_age = Column(db.String(255), unique=False, nullable=True)
    officer_condition = Column(db.String(255), unique=False, nullable=True)
    resident_condition = Column(db.String(255), unique=False, nullable=True)

    def __init__(self, **kwargs):
        cleaned_incident = clean_incident(self, kwargs)
        db.Model.__init__(cleaned_incident, **kwargs)


class CitizenComplaint(SurrogatePK, Model):
    __tablename__ = 'citizen_complaints'
    department_id = Column(db.Integer, db.ForeignKey('departments.id'),nullable=False)
    opaque_id = Column(db.String(255), unique=False, nullable=False)
    occured_date = Column(db.DateTime, nullable=True)
    division = Column(db.String(255), unique=False, nullable=True)
    precinct = Column(db.String(255), unique=False, nullable=True)
    shift = Column(db.String(255), unique=False, nullable=True)
    beat = Column(db.String(255), unique=False, nullable=True)
    disposition = Column(db.String(255), unique=False, nullable=True)
    allegation_type = Column(db.String(255), unique=False, nullable=True)
    allegation = Column(db.String(255), unique=False, nullable=True)
    census_tract = Column(db.String(255), unique=False, nullable=True)
    resident_race = Column(db.String(255), unique=False, nullable=True)
    officer_race = Column(db.String(255), unique=False, nullable=True)
    resident_sex = Column(db.String(255), unique=False, nullable=True)
    officer_sex = Column(db.String(255), unique=False, nullable=True)
    officer_identifier = Column(db.String(255), unique=False, nullable=True)
    officer_years_of_service = Column(db.String(255), unique=False, nullable=True)
    officer_age = Column(db.String(255), unique=False, nullable=True)
    resident_age = Column(db.String(255), unique=False, nullable=True)

    def __init__(self, **kwargs):
        cleaned_incident = clean_incident(self, kwargs)
        db.Model.__init__(cleaned_incident, **kwargs)




class OfficerInvolvedShooting(SurrogatePK, Model):
    __tablename__ = 'officer_involved_shootings'
    department_id = Column(db.Integer, db.ForeignKey('departments.id'),nullable=False)
    opaque_id = Column(db.String(255), unique=False, nullable=False)
    occured_date = Column(db.DateTime, nullable=True)
    division = Column(db.String(255), unique=False, nullable=True)
    precinct = Column(db.String(255), unique=False, nullable=True)
    shift = Column(db.String(255), unique=False, nullable=True)
    beat = Column(db.String(255), unique=False, nullable=True)
    disposition = Column(db.String(255), unique=False, nullable=True)
    census_tract = Column(db.String(255), unique=False, nullable=True)
    officer_force_type = Column(db.String(255), unique=False, nullable=True)
    resident_weapon_used = Column(db.String(255), unique=False, nullable=True)
    service_type = Column(db.String(255), unique=False, nullable=True)
    resident_race = Column(db.String(255), unique=False, nullable=True)
    officer_race = Column(db.String(255), unique=False, nullable=True)
    resident_sex = Column(db.String(255), unique=False, nullable=True)
    officer_sex = Column(db.String(255), unique=False, nullable=True)
    officer_identifier = Column(db.String(255), unique=False, nullable=True)
    officer_years_of_service = Column(db.Integer, unique=False, nullable=True)
    officer_age = Column(db.String(255), unique=False, nullable=True)
    resident_age = Column(db.String(255), unique=False, nullable=True)
    officer_condition = Column(db.String(255), unique=False, nullable=True)
    resident_condition = Column(db.String(255), unique=False, nullable=True)


    def __init__(self, **kwargs):
        cleaned_incident = clean_incident(self, kwargs)
        db.Model.__init__(cleaned_incident, **kwargs)
