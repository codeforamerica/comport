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

class Month(SurrogatePK, Model):
    __tablename__ = 'months'
    month = Column(db.Integer)
    year = Column(db.Integer)
    department_id = Column(db.Integer, db.ForeignKey('departments.id'),nullable=True)
    service_types = relationship("ServiceType", backref="month")

    def to_json(self):
        return {"month":self.month, "year":self.year}

    def __init__(self, **kwargs):
        db.Model.__init__(self, **kwargs)

class ServiceType(SurrogatePK, Model):
    __tablename__ = 'serviceTypes'
    month_id = Column(db.Integer, db.ForeignKey('months.id'),nullable=True)
    service_type = Column(db.String(36), unique=False, nullable=False)
    count = Column(db.Integer)

    def __init__(self, **kwargs):
        db.Model.__init__(self, **kwargs)
