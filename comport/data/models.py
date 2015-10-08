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

class DenominatorValue(SurrogatePK, Model):
    __tablename__="denominator_values"
    department_id = Column(db.Integer, db.ForeignKey('departments.id'),nullable=False)
    month=Column(db.Integer, unique=False, nullable=False)
    year=Column(db.Integer, unique=False, nullable=False)
    arrests=Column(db.Integer, unique=False, nullable=True)
    calls_for_service=Column(db.Integer, unique=False, nullable=True)
    officer_initiated_calls=Column(db.Integer, unique=False, nullable=True)

    def to_csv_row(self):
        values = [
            csv_utils.coalesce_int(self.month),
            csv_utils.coalesce_int(self.year),
            csv_utils.coalesce_int(self.arrests),
            csv_utils.coalesce_int(self.calls_for_service),
            csv_utils.coalesce_int(self.officer_initiated_calls)
        ]
        return ','.join(values) + "\n"

    def __init__(self, **kwargs):
        db.Model.__init__(self, **kwargs)


class UseOfForceIncident(SurrogatePK, Model):
    __tablename__ = 'use_of_force_incidents'
    department_id = Column(db.Integer, db.ForeignKey('departments.id'),nullable=False)
    opaque_id = Column(db.String(255), unique=True, nullable=False)
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
    officer_years_of_service = Column(db.Integer, unique=False, nullable=True)


    def to_csv_row(self):
        occured_date = csv_utils.coalesce_date(self.occured_date)
        values = [
            self.opaque_id or "",
            occured_date,
            self.division or "",
            self.precinct or "",
            self.shift or "",
            self.beat or "",
            self.disposition or "",
            self.census_tract or "",
            self.officer_force_type or "",
            self.resident_resist_type or "",
            self.officer_weapon_used or "",
            self.resident_weapon_used or "",
            self.service_type or "",
            csv_utils.coalesce_bool(self.arrest_made),
            self.arrest_charges or "",
            csv_utils.coalesce_bool(self.resident_injured),
            csv_utils.coalesce_bool(self.resident_hospitalized),
            csv_utils.coalesce_bool(self.officer_injured),
            csv_utils.coalesce_bool(self.officer_hospitalized),
            self.use_of_force_reason or "",
            self.resident_race or "",
            self.officer_race or "",
            csv_utils.coalesce_int(self.officer_years_of_service),
            self.officer_identifier or ""
        ]

        return ','.join(values) + "\n"

    def __init__(self, **kwargs):
        db.Model.__init__(self, **kwargs)


class CitizenComplaint(SurrogatePK, Model):
    __tablename__ = 'citizen_complaint'
    department_id = Column(db.Integer, db.ForeignKey('departments.id'),nullable=False)
    opaque_id = Column(db.String(255), unique=True, nullable=False)
    occured_date = Column(db.DateTime, nullable=True)
    division = Column(db.String(255), unique=False, nullable=True)
    precinct = Column(db.String(255), unique=False, nullable=True)
    shift = Column(db.String(255), unique=False, nullable=True)
    beat = Column(db.String(255), unique=False, nullable=True)
    disposition = Column(db.String(255), unique=False, nullable=True)
    category = Column(db.String(255), unique=False, nullable=True)
    census_tract = Column(db.String(255), unique=False, nullable=True)
    resident_race = Column(db.String(255), unique=False, nullable=True)
    officer_race = Column(db.String(255), unique=False, nullable=True)
    resident_sex = Column(db.String(255), unique=False, nullable=True)
    officer_sex = Column(db.String(255), unique=False, nullable=True)
    officer_identifier = Column(db.String(255), unique=False, nullable=True)
    officer_years_of_service = Column(db.Integer, unique=False, nullable=True)

    def to_csv_row(self):
        occured_date = csv_utils.coalesce_date(self.occured_date)
        values = [
            self.opaque_id or "",
            occured_date,
            self.division or "",
            self.precinct or "",
            self.shift or "",
            self.beat or "",
            self.disposition or "",
            self.category or "",
            self.census_tract or "",
            self.resident_race or "",
            self.resident_sex or "",
            self.officer_race or "",
            self.officer_sex or "",
            csv_utils.coalesce_int(self.officer_years_of_service),
            self.officer_identifier or ""
        ]

        return ','.join(values) + "\n"

    def __init__(self, **kwargs):
        db.Model.__init__(self, **kwargs)
