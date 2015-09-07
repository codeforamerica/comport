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
        res = testapp.post("/department/1/heartbeat", expect_errors=True)
        assert res.status_code == 401

    def test_bad_extractor_password_is_a_401(self, testapp):
        Extractor.create(username='good',email='good@good.com',password="valid")
        testapp.authorization = ('Basic', ('good', 'fake'))
        res = testapp.post("/department/1/heartbeat", expect_errors=True)
        assert res.status_code == 401

    def test_bad_department_slug_is_a_404(self, testapp):
        Extractor.create(username='good2',email='good2@good.com',password="valid")
        testapp.authorization = ('Basic', ('good2', 'valid'))
        res = testapp.post("/department/999999999999/heartbeat", expect_errors=True)
        assert res.status_code == 404

    def test_wrong_department_slug_is_a_403(self, testapp):
        right_department = Department.create(name="good")
        wrong_department = Department.create(name="ill")

        Extractor.create(username='good3',email='good3@good.com',password="valid", department_id = right_department.id)
        testapp.authorization = ('Basic', ('good3', 'valid'))
        res = testapp.post("/department/%s/heartbeat" % wrong_department.id, expect_errors=True)
        assert res.status_code == 403

    def test_valid_login_replies_with_request(self, testapp):
        right_department = Department.create(name="good2")

        Extractor.create(username='good4',email='good4@good.com',password="valid", department_id = right_department.id)
        testapp.authorization = ('Basic', ('good4', 'valid'))

        res = testapp.post_json("/department/%s/heartbeat" % right_department.id, params={"json":"yep"},expect_errors=True )
        assert res.status_code == 200
