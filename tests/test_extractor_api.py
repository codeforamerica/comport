# -*- coding: utf-8 -*-
"""Functional tests using WebTest.

See: http://webtest.readthedocs.org/
"""
import pytest
from comport.department.models import Department, Extractor

@pytest.mark.usefixtures('db')
class TestHeartbeat:

    def test_reject_nonexistent_extractor_post(self, testapp):
        ''' An extractor login that doesn't exist is rejected.
        '''
        testapp.authorization = ('Basic', ('extractor', 'nonexistent'))
        response = testapp.post("/data/heartbeat", expect_errors=True)
        assert response.status_code == 401
        assert response.text == 'No extractor with that username!'

    def test_reject_extractor_post_with_wrong_password(self, testapp):
        ''' An extractor login with the wrong password is rejected.
        '''
        Extractor.create(username='extractor', email='extractor@example.com', password="password")
        testapp.authorization = ('Basic', ('extractor', 'drowssap'))
        response = testapp.post("/data/heartbeat", expect_errors=True)
        assert response.status_code == 401
        assert response.text == 'Extractor authorization failed!'

    def test_successful_extractor_post(self, testapp):
        ''' Send a valid heartbeat post, get a valid response.
        '''
        # set up the extractor
        department = Department.create(name="Good Police Department", short_name="GPD", load_defaults=False)
        Extractor.create(username='extractor', email='extractor@example.com', password="password", department_id=department.id, next_month=10, next_year=2006)

        # set the correct authorization
        testapp.authorization = ('Basic', ('extractor', 'password'))

        # post a sample json object to the heartbeat URL
        response = testapp.post_json("/data/heartbeat", params={"heartbeat": "heartbeat"})
        # assert that we got the expected response
        assert response.status_code == 200
        assert response.json_body['nextMonth'] == 10
        assert response.json_body['nextYear'] == 2006
        assert response.json_body['received'] == {'heartbeat': 'heartbeat'}
