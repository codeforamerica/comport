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

class UseOfForceIncident(SurrogatePK, Model):
    __tablename__ = 'useOfForceIncidents'
    opaque_id = Column(db.String(255), unique=True, nullable=False)
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

    def __init__(self, **kwargs):
        db.Model.__init__(self, **kwargs)
