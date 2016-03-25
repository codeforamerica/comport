# -*- coding: utf-8 -*-
from comport.database import (Column, db, Model, SurrogatePK)

class ChartBlock(SurrogatePK, Model):
    __tablename__ = 'chart_blocks'
    department_id = Column(db.Integer, db.ForeignKey('departments.id'), nullable=False)
    title = Column(db.String(255), unique=False, nullable=False)
    caption = Column(db.String(255), unique=False, nullable=True)
    slug = Column(db.String(255), unique=False, nullable=False)
    dataset = Column(db.String(255), unique=False, nullable=False)
    content = Column(db.Text, unique=False, nullable=True)
    date_updated = Column(db.DateTime, nullable=True)
    date_edited = Column(db.DateTime, nullable=True)

    def __init__(self, **kwargs):
        db.Model.__init__(self, **kwargs)
