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

from datetime import datetime

class UseOfForceIncident(SurrogatePK, Model):
    __tablename__ = 'useOfForceIncidents'
    opaque_id = Column(db.String(255), unique=True, nullable=False)
    occured_date = Column(db.DateTime, nullable=True)
    received_date = Column(db.DateTime, nullable=True)
    month = Column(db.Integer)
    year = Column(db.Integer)
    department_id = Column(db.Integer, db.ForeignKey('departments.id'),nullable=True)
    status = Column(db.String(255), unique=False, nullable=True)
    disposition = Column(db.String(255), unique=False, nullable=True)
    service_type = Column(db.String(255), unique=False, nullable=True)
    day_of_week = Column(db.String(255), unique=False, nullable=True)
    hour = Column(db.Integer)
    arrest_made = Column(db.Boolean, nullable=True)
    arrest_charges = Column(db.String(255), unique=False, nullable=True)
    citizen_hospitalized = Column(db.Boolean, nullable=True)
    citizen_injured = Column(db.Boolean, nullable=True)
    officer_injured = Column(db.Boolean, nullable=True)
    officer_hospitalized = Column(db.Boolean, nullable=True)
    use_of_force_reason = Column(db.String(255), unique=False, nullable=True)

    def coalesce_date(self, date):
        return "" if date == None else datetime.strftime(date, '%Y-%m-%d %H:%M:%S')

    def to_csv_row(self):
        occured_date = self.coalesce_date(self.occured_date)
        received_date = self.coalesce_date(self.received_date)
        return ','.join([
            self.opaque_id,
            self.service_type or "",
            occured_date,
            received_date,
            self.use_of_force_reason  or ""
            ]) + "\n"

    def __init__(self, **kwargs):
        db.Model.__init__(self, **kwargs)
