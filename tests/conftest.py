# -*- coding: utf-8 -*-
"""Defines fixtures available to all tests."""
import pytest
from webtest import TestApp

from comport.settings import TestConfig
from comport.app import create_app
from comport.database import db as _db
from comport.content.models import ChartBlock
from comport.department.models import Department

from .factories import UserFactory, DepartmentFactory


@pytest.yield_fixture(scope='function')
def app():
    _app = create_app(TestConfig)
    ctx = _app.test_request_context()
    ctx.push()

    yield _app

    ctx.pop()


@pytest.fixture(scope='function')
def testapp(app):
    """A Webtest app."""
    return TestApp(app)

@pytest.fixture(scope='function')
def db(app):
    _db.app = app
    _db.drop_all()
    _db.create_all()
    return _db


@pytest.fixture
def user(db):
    department = DepartmentFactory()
    department.save()
    user = UserFactory(password='myprecious')
    user.departments.append(department)
    user.save()
    db.session.commit()
    return user
