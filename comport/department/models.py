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

from comport.user.models import User


class Department(SurrogatePK, Model):
    __tablename__ = 'departments'
    id = Column(db.Integer, primary_key=True, index=True)
    name = Column(db.String(80), unique=True, nullable=False)
    invite_codes = relationship("Invite_Code", backref="department")
    users = relationship("User", backref="department")

    def __init__(self, name, **kwargs):
        db.Model.__init__(self, name=name, **kwargs)

    def __repr__(self):
        return '<Department({name})>'.format(name=self.name)


class Extractor(User):
    __tablename__ = 'extractors'
    id = Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)

    __mapper_args__ = {
        'polymorphic_identity':'extractors',
        'inherit_condition': (id==User.id)
    }
