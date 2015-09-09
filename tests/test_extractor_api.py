# -*- coding: utf-8 -*-
"""Functional tests using WebTest.

See: http://webtest.readthedocs.org/
"""
import pytest
from flask import url_for

from comport.department.models import Department, Extractor
from .factories import UserFactory

class TestHeartbeat:

    def test_non_existant_extractor_user_is_a_401(self, testapp):
        testapp.authorization = ('Basic', ('bad', 'fake'))
        res = testapp.post("/data/heartbeat", expect_errors=True)
        assert res.status_code == 401

    def test_bad_extractor_password_is_a_401(self, testapp):
        Extractor.create(username='good',email='good@good.com',password="valid")
        testapp.authorization = ('Basic', ('good', 'fake'))
        res = testapp.post("/data/heartbeat", expect_errors=True)
        assert res.status_code == 401

    def test_valid_login_replies_with_request(self, testapp):
        right_department = Department.create(name="good2")

        Extractor.create(username='good4',email='good4@good.com',password="valid", department_id = right_department.id)
        testapp.authorization = ('Basic', ('good4', 'valid'))

        res = testapp.post_json("/data/heartbeat", params={"json":"yep"},expect_errors=True )
        assert res.status_code == 200
