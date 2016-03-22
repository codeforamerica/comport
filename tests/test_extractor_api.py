# -*- coding: utf-8 -*-
"""Functional tests using WebTest.

See: http://webtest.readthedocs.org/
"""
import pytest
from comport.department.models import Department, Extractor
from comport.data.models import OfficerInvolvedShooting
from testclient.JSON_test_client import JSONTestClient
from comport.data.cleaners import Cleaners

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

    def test_post_ois_data(self, testapp):
        ''' New OIS data from the extractor is processed as expected.
        '''
        # Set up the extractor
        department = Department.create(name="Good Police Department", short_name="GPD", load_defaults=False)
        extractor, envs = Extractor.from_department_and_password(department=department, password="password")

        # Set the correct authorization
        testapp.authorization = ('Basic', (extractor.username, 'password'))

        # Get a generated list of OIS descriptions from the JSON test client
        test_client = JSONTestClient()
        ois_count = 1
        ois_data = test_client.make_ois(count=ois_count)
        # post the json to the OIS URL
        response = testapp.post_json("/data/OIS", params={'month': 0, 'year': 0, 'data': ois_data})

        # assert that we got the expected reponse
        assert response.status_code == 200
        assert response.json_body['updated'] == 0
        assert response.json_body['added'] == ois_count

        # check the ois incident in the database against the data that was sent
        sent_ois = ois_data[0]
        check_ois = OfficerInvolvedShooting.query.filter_by(opaque_id=sent_ois['opaqueId']).first()
        assert check_ois.occured_date.strftime('%Y-%m-%d %-H:%-M:%S') == sent_ois['occuredDate']
        assert check_ois.division == Cleaners.capitalize(sent_ois['division'])
        assert check_ois.precinct == Cleaners.capitalize(sent_ois['precinct'])
        assert check_ois.shift == Cleaners.capitalize(sent_ois['shift'])
        assert check_ois.beat == Cleaners.capitalize(sent_ois['beat'])
        assert check_ois.disposition == sent_ois['disposition']
        assert check_ois.resident_race == Cleaners.race(sent_ois['residentRace'])
        assert check_ois.resident_sex == Cleaners.sex(sent_ois['residentSex'])
        assert check_ois.resident_age == sent_ois['residentAge']
        assert check_ois.resident_weapon_used == Cleaners.resident_weapon_used(sent_ois['residentWeaponUsed'])
        assert check_ois.resident_condition == sent_ois['residentCondition']
        assert check_ois.officer_identifier == sent_ois['officerIdentifier']
        assert check_ois.officer_weapon_used == sent_ois['officerForceType']
        assert check_ois.officer_race == Cleaners.race(sent_ois['officerRace'])
        assert check_ois.officer_sex == Cleaners.sex(sent_ois['officerSex'])
        assert check_ois.officer_age == sent_ois['officerAge']
        assert check_ois.officer_years_of_service == sent_ois['officerYearsOfService']
        assert check_ois.officer_condition == sent_ois['officerCondition']
