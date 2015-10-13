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

class Link(SurrogatePK, Model):
    __tablename__ = 'links'
    department_id = Column(db.Integer, db.ForeignKey('departments.id'),nullable=False)
    title = Column(db.String(255), unique=False, nullable=False)
    url = Column(db.String(2083), unique=False, nullable=False)
    type = Column(db.String(255), unique=False, nullable=False)

    def __init__(self, **kwargs):
        db.Model.__init__(self, **kwargs)

class ChartBlock(SurrogatePK, Model):
    __tablename__ = 'chart_blocks'
    department_id = Column(db.Integer, db.ForeignKey('departments.id'),nullable=False)
    title = Column(db.String(255), unique=False, nullable=False)
    caption = Column(db.String(255), unique=False, nullable=True)
    slug = Column(db.String(255), unique=False, nullable=False)
    dataset = Column(db.String(255), unique=False, nullable=False)
    content = Column(db.Text, unique=False, nullable=True)
    date_updated  = Column(db.DateTime, nullable=True)
    date_edited  = Column(db.DateTime, nullable=True)

    def __init__(self, **kwargs):
        db.Model.__init__(self, **kwargs)
