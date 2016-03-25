# -*- coding: utf-8 -*-
import datetime as dt

from flask_login import UserMixin
from comport.extensions import bcrypt
from comport.database import (Column, db, Model, ReferenceCol, relationship, SurrogatePK)


class Role(SurrogatePK, Model):
    __tablename__ = 'roles'
    name = Column(db.String(80), unique=False, nullable=False)
    user_id = ReferenceCol('users', nullable=True)
    user = relationship('User', backref='roles')

    def __init__(self, name, **kwargs):
        db.Model.__init__(self, name=name, **kwargs)

    def __repr__(self):
        return '<Role({name})>'.format(name=self.name)


class Invite_Code(SurrogatePK, Model):
    __tablename__ = 'invite_codes'
    id = Column(db.Integer, primary_key=True, index=True)
    department_id = Column(db.Integer, db.ForeignKey('departments.id'))
    code = Column(db.String(36), unique=True, nullable=False)
    used = Column(db.Boolean(), default=False)

    def __init__(self, **kwargs):
        db.Model.__init__(self, **kwargs)


class User(UserMixin, SurrogatePK, Model):

    __tablename__ = 'users'
    id = Column(db.Integer, primary_key=True, index=True)
    username = Column(db.String(80), unique=True, nullable=False)
    email = Column(db.String(80), unique=False, nullable=False)
    #: The hashed password
    password = Column(db.String(128), nullable=True)
    created_at = Column(db.DateTime, nullable=False, default=dt.datetime.utcnow)
    first_name = Column(db.String(30), nullable=True)
    last_name = Column(db.String(30), nullable=True)
    active = Column(db.Boolean(), default=False)
    department_id = Column(db.Integer, db.ForeignKey('departments.id'), nullable=True)
    type = Column(db.String(50))
    password_reset_uuid = Column(db.String(36), unique=True, nullable=True)

    __mapper_args__ = {
        'polymorphic_on': type
    }

    def __init__(self, username, email, is_admin=False, password=None, **kwargs):
        db.Model.__init__(self, username=username, email=email, **kwargs)

        if is_admin:
            admin_role = Role(name='admin')
            admin_role.save()
            self.roles.append(admin_role)

        if password:
            self.set_password(password)
        else:
            self.password = None

    def set_password(self, password):
        self.password = bcrypt.generate_password_hash(password)

    def check_password(self, value):
        return bcrypt.check_password_hash(self.password, value)

    def is_admin(self):
        def names(role):
            return role.name
        return "admin" in map(names, self.roles)

    def has_department(self, department_id):

        def department_ids(department):
            return department.id

        return department_id in map(department_ids, self.departments)

    def first_department(self):
        if len(self.departments) > 0:
            return self.departments[0]
        else:
            return None

    @property
    def full_name(self):
        return "{0} {1}".format(self.first_name, self.last_name)

    def __repr__(self):
        return '<User({username!r})>'.format(username=self.username)
