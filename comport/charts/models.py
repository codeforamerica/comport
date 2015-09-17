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

class ChartBlockDefaults(SurrogatePK, Model):
    __tablename__ = 'chart_block_defaults'
    title = Column(db.String(255), unique=False, nullable=False)
    caption = Column(db.String(255), unique=False, nullable=True)
    slug = Column(db.String(255), unique=False, nullable=False)
    dataset = Column(db.String(255), unique=False, nullable=False)
    content = Column(db.Text( convert_unicode=True), unique=False, nullable=True)

    def __init__(self, **kwargs):
        db.Model.__init__(self, **kwargs)

    def make_real_block(self):
        return ChartBlock(
            title=self.title,
            caption=self.caption,
            slug=self.slug,
            dataset=self.dataset,
            content=self.content)

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
