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
    
    def __init__(self, name, **kwargs):
        db.Model.__init__(self, name=name, **kwargs)

    def __repr__(self):
        return '<Month({name})>'.format(name=self.name)
