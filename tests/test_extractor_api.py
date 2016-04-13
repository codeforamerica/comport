# -*- coding: utf-8 -*-
"""Functional tests using WebTest.

See: http://webtest.readthedocs.org/
"""
import pytest
from comport.department.models import Department, Extractor
from comport.data.models import OfficerInvolvedShooting, UseOfForceIncident, CitizenComplaint
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

    def test_post_complaint_data(self, testapp):
        ''' New complaint data from the extractor is processed as expected.
        '''
        # Set up the extractor
        department = Department.create(name="Good Police Department", short_name="GPD", load_defaults=False)
        extractor, envs = Extractor.from_department_and_password(department=department, password="password")

        # Set the correct authorization
        testapp.authorization = ('Basic', (extractor.username, 'password'))

        # Get a generated list of complaint descriptions from the JSON test client
        test_client = JSONTestClient()
        complaint_count = 1
        complaint_data = test_client.get_prebaked_complaints(last=complaint_count)
        # post the json to the complaint URL
        response = testapp.post_json("/data/complaints", params={'month': 0, 'year': 0, 'data': complaint_data})

        # assert that we got the expected reponse
        assert response.status_code == 200
        assert response.json_body['updated'] == 0
        assert response.json_body['added'] == complaint_count

        # check the complaint incident in the database against the data that was sent
        cleaner = Cleaners()
        sent_complaint = cleaner.capitalize_incident(complaint_data[0])
        check_complaint = CitizenComplaint.query.filter_by(opaque_id=sent_complaint['opaqueId']).first()
        assert check_complaint.occured_date.strftime('%Y-%m-%d %-H:%-M:%S') == sent_complaint['occuredDate']
        assert check_complaint.division == sent_complaint['division']
        assert check_complaint.precinct == sent_complaint['precinct']
        assert check_complaint.shift == sent_complaint['shift']
        assert check_complaint.beat == sent_complaint['beat']
        assert check_complaint.disposition == sent_complaint['disposition']
        assert check_complaint.service_type == sent_complaint['serviceType']
        assert check_complaint.source == sent_complaint['source']
        assert check_complaint.allegation_type == sent_complaint['allegationType']
        assert check_complaint.allegation == sent_complaint['allegation']
        assert check_complaint.resident_race == cleaner.race(sent_complaint['residentRace'])
        assert check_complaint.resident_sex == cleaner.sex(sent_complaint['residentSex'])
        assert check_complaint.resident_age == cleaner.number_to_string(sent_complaint['residentAge'])
        assert check_complaint.officer_identifier == sent_complaint['officerIdentifier']
        assert check_complaint.officer_race == cleaner.race(sent_complaint['officerRace'])
        assert check_complaint.officer_sex == cleaner.sex(sent_complaint['officerSex'])
        assert check_complaint.officer_age == cleaner.number_to_string(sent_complaint['officerAge'])
        assert check_complaint.officer_years_of_service == cleaner.number_to_string(sent_complaint['officerYearsOfService'])

    def test_post_mistyped_complaint_data(self, testapp):
        ''' New complaint data from the extractor with wrongly typed data is processed as expected.
        '''
        # Set up the extractor
        department = Department.create(name="Good Police Department", short_name="GPD", load_defaults=False)
        extractor, envs = Extractor.from_department_and_password(department=department, password="password")

        # Set the correct authorization
        testapp.authorization = ('Basic', (extractor.username, 'password'))

        # Get a generated list of complaint descriptions from the JSON test client
        test_client = JSONTestClient()
        complaint_count = 1
        complaint_data = test_client.get_prebaked_complaints(last=complaint_count)

        # The app expects number values to be transmitted as strings. Let's change them to integers.
        complaint_data[0]['residentAge'] = 28
        complaint_data[0]['officerAge'] = 46
        complaint_data[0]['officerYearsOfService'] = 17

        # post the json to the complaint URL
        response = testapp.post_json("/data/complaints", params={'month': 0, 'year': 0, 'data': complaint_data})

        # assert that we got the expected reponse
        assert response.status_code == 200
        assert response.json_body['updated'] == 0
        assert response.json_body['added'] == complaint_count

        # check the complaint incident in the database against the data that was sent
        cleaner = Cleaners()
        sent_complaint = cleaner.capitalize_incident(complaint_data[0])
        check_complaint = CitizenComplaint.query.filter_by(opaque_id=sent_complaint['opaqueId']).first()
        assert check_complaint.occured_date.strftime('%Y-%m-%d %-H:%-M:%S') == sent_complaint['occuredDate']
        assert check_complaint.division == sent_complaint['division']
        assert check_complaint.precinct == sent_complaint['precinct']
        assert check_complaint.shift == sent_complaint['shift']
        assert check_complaint.beat == sent_complaint['beat']
        assert check_complaint.disposition == sent_complaint['disposition']
        assert check_complaint.service_type == sent_complaint['serviceType']
        assert check_complaint.source == sent_complaint['source']
        assert check_complaint.allegation_type == sent_complaint['allegationType']
        assert check_complaint.allegation == sent_complaint['allegation']
        assert check_complaint.resident_race == cleaner.race(sent_complaint['residentRace'])
        assert check_complaint.resident_sex == cleaner.sex(sent_complaint['residentSex'])
        assert check_complaint.resident_age == cleaner.number_to_string(sent_complaint['residentAge'])
        assert check_complaint.officer_identifier == sent_complaint['officerIdentifier']
        assert check_complaint.officer_race == cleaner.race(sent_complaint['officerRace'])
        assert check_complaint.officer_sex == cleaner.sex(sent_complaint['officerSex'])
        assert check_complaint.officer_age == cleaner.number_to_string(sent_complaint['officerAge'])
        assert check_complaint.officer_years_of_service == cleaner.number_to_string(sent_complaint['officerYearsOfService'])

    def test_update_complaint_data(self, testapp):
        ''' Updated complaint data from the extractor is processed as expected.
        '''
        # Set up the extractor
        department = Department.create(name="Good Police Department", short_name="GPD", load_defaults=False)
        extractor, envs = Extractor.from_department_and_password(department=department, password="password")

        # Set the correct authorization
        testapp.authorization = ('Basic', (extractor.username, 'password'))

        # Get a generated list of complaint descriptions from the JSON test client
        test_client = JSONTestClient()
        complaint_data = test_client.get_prebaked_complaints(last=1)
        # post the json to the complaint URL
        response = testapp.post_json("/data/complaints", params={'month': 0, 'year': 0, 'data': complaint_data})

        # assert that we got the expected reponse
        assert response.status_code == 200
        assert response.json_body['updated'] == 0
        assert response.json_body['added'] == 1

        # Get the second pre-baked complaint
        updated_complaint_data = test_client.get_prebaked_complaints(first=1, last=2)
        # Swap in the opaque ID from the first complaint
        updated_complaint_data[0]["opaqueId"] = complaint_data[0]["opaqueId"]
        # The complaint won't be a match unless these fields are the same
        updated_complaint_data[0]["allegationType"] = complaint_data[0]["allegationType"]
        updated_complaint_data[0]["allegation"] = complaint_data[0]["allegation"]
        updated_complaint_data[0]["officerIdentifier"] = complaint_data[0]["officerIdentifier"]
        updated_complaint_data[0]["residentRace"] = complaint_data[0]["residentRace"]
        updated_complaint_data[0]["residentSex"] = complaint_data[0]["residentSex"]
        updated_complaint_data[0]["residentAge"] = complaint_data[0]["residentAge"]
        # post the json to the complaint URL
        response = testapp.post_json("/data/complaints", params={'month': 0, 'year': 0, 'data': updated_complaint_data})

        # assert that we got the expected reponse
        assert response.status_code == 200
        assert response.json_body['updated'] == 1
        assert response.json_body['added'] == 0

        # There's only one complaint in the database.
        all_complaints = CitizenComplaint.query.all()
        assert len(all_complaints) == 1

        # check the complaint incident in the database against the updated data that was sent
        cleaner = Cleaners()
        sent_complaint = cleaner.capitalize_incident(updated_complaint_data[0])
        check_complaint = CitizenComplaint.query.filter_by(opaque_id=sent_complaint['opaqueId']).first()
        assert check_complaint.occured_date.strftime('%Y-%m-%d %-H:%-M:%S') == sent_complaint['occuredDate']
        assert check_complaint.division == sent_complaint['division']
        assert check_complaint.precinct == sent_complaint['precinct']
        assert check_complaint.shift == sent_complaint['shift']
        assert check_complaint.beat == sent_complaint['beat']
        assert check_complaint.disposition == sent_complaint['disposition']
        assert check_complaint.service_type == sent_complaint['serviceType']
        assert check_complaint.source == sent_complaint['source']
        assert check_complaint.allegation_type == sent_complaint['allegationType']
        assert check_complaint.allegation == sent_complaint['allegation']
        assert check_complaint.resident_race == cleaner.race(sent_complaint['residentRace'])
        assert check_complaint.resident_sex == cleaner.sex(sent_complaint['residentSex'])
        assert check_complaint.resident_age == cleaner.number_to_string(sent_complaint['residentAge'])
        assert check_complaint.officer_identifier == sent_complaint['officerIdentifier']
        assert check_complaint.officer_race == cleaner.race(sent_complaint['officerRace'])
        assert check_complaint.officer_sex == cleaner.sex(sent_complaint['officerSex'])
        assert check_complaint.officer_age == cleaner.number_to_string(sent_complaint['officerAge'])
        assert check_complaint.officer_years_of_service == cleaner.number_to_string(sent_complaint['officerYearsOfService'])

    def test_skip_multiple_complaint_data(self, testapp):
        ''' Multiple complaint data from the extractor is skipped.
        '''
        # Set up the extractor
        department = Department.create(name="Good Police Department", short_name="GPD", load_defaults=False)
        extractor, envs = Extractor.from_department_and_password(department=department, password="password")

        # Set the correct authorization
        testapp.authorization = ('Basic', (extractor.username, 'password'))

        # Get a generated list of complaint descriptions from the JSON test client
        test_client = JSONTestClient()
        complaint_data = test_client.get_prebaked_complaints(last=1)
        # post the json to the complaint URL
        response = testapp.post_json("/data/complaints", params={'month': 0, 'year': 0, 'data': complaint_data})

        # assert that we got the expected reponse
        assert response.status_code == 200
        assert response.json_body['updated'] == 0
        assert response.json_body['added'] == 1

        # Get the second pre-baked complaint
        multiple_complaint_data = test_client.get_prebaked_complaints(first=1, last=2)
        # Swap in the opaque ID from the first complaint
        multiple_complaint_data[0]["opaqueId"] = complaint_data[0]["opaqueId"]
        # The complaint will be skipped as a 'multiple' if these fields are the same
        multiple_complaint_data[0]["allegationType"] = complaint_data[0]["allegationType"]
        multiple_complaint_data[0]["allegation"] = complaint_data[0]["allegation"]
        multiple_complaint_data[0]["officerIdentifier"] = complaint_data[0]["officerIdentifier"]
        # post the json to the complaint URL
        response = testapp.post_json("/data/complaints", params={'month': 0, 'year': 0, 'data': multiple_complaint_data})

        # assert that we got the expected reponse
        assert response.status_code == 200
        assert response.json_body['updated'] == 0
        assert response.json_body['added'] == 0

        # There is one complaint in the database.
        all_complaints = CitizenComplaint.query.all()
        assert len(all_complaints) == 1

    def test_post_complaint_data_near_match_does_not_update(self, testapp):
        ''' Complaint data with the same ID but different details creates a new record.
        '''
        # Set up the extractor
        department = Department.create(name="Good Police Department", short_name="GPD", load_defaults=False)
        extractor, envs = Extractor.from_department_and_password(department=department, password="password")

        # Set the correct authorization
        testapp.authorization = ('Basic', (extractor.username, 'password'))

        # Get a generated list of complaint descriptions from the JSON test client
        test_client = JSONTestClient()
        complaint_data = test_client.get_prebaked_complaints(last=1)
        # post the json to the complaint URL
        response = testapp.post_json("/data/complaints", params={'month': 0, 'year': 0, 'data': complaint_data})

        # assert that we got the expected reponse
        assert response.status_code == 200
        assert response.json_body['updated'] == 0
        assert response.json_body['added'] == 1

        # Get the second pre-baked complaint
        updated_complaint_data = test_client.get_prebaked_complaints(first=1, last=2)
        # Swap in the opaque ID from the first complaint
        updated_complaint_data[0]["opaqueId"] = complaint_data[0]["opaqueId"]
        # post the json to the complaint URL
        response = testapp.post_json("/data/complaints", params={'month': 0, 'year': 0, 'data': updated_complaint_data})

        # assert that we got the expected reponse
        assert response.status_code == 200
        assert response.json_body['updated'] == 0
        assert response.json_body['added'] == 1

        # There are two complaints in the database.
        all_complaints = CitizenComplaint.query.all()
        assert len(all_complaints) == 2

    def test_post_uof_data(self, testapp):
        ''' New UOF data from the extractor is processed as expected.
        '''
        # Set up the extractor
        department = Department.create(name="Good Police Department", short_name="GPD", load_defaults=False)
        extractor, envs = Extractor.from_department_and_password(department=department, password="password")

        # Set the correct authorization
        testapp.authorization = ('Basic', (extractor.username, 'password'))

        # Get a generated list of UOF descriptions from the JSON test client
        test_client = JSONTestClient()
        uof_count = 1
        uof_data = test_client.get_prebaked_uof(last=uof_count)
        # post the json to the UOF URL
        response = testapp.post_json("/data/UOF", params={'month': 0, 'year': 0, 'data': uof_data})

        # assert that we got the expected reponse
        assert response.status_code == 200
        assert response.json_body['updated'] == 0
        assert response.json_body['added'] == uof_count

        # check the uof incident in the database against the data that was sent
        cleaner = Cleaners()
        sent_uof = uof_data[0]
        check_uof = UseOfForceIncident.query.filter_by(opaque_id=sent_uof['opaqueId']).first()
        assert check_uof.occured_date.strftime('%Y-%m-%d %-H:%-M:%S') == sent_uof['occuredDate']
        assert check_uof.division == cleaner.capitalize(sent_uof['division'])
        assert check_uof.precinct == cleaner.capitalize(sent_uof['precinct'])
        assert check_uof.shift == cleaner.capitalize(sent_uof['shift'])
        assert check_uof.beat == cleaner.capitalize(sent_uof['beat'])
        assert check_uof.disposition == sent_uof['disposition']
        assert check_uof.officer_force_type == cleaner.officer_force_type(sent_uof['officerForceType'])
        assert check_uof.use_of_force_reason == sent_uof['useOfForceReason']
        assert check_uof.service_type == sent_uof['serviceType']
        assert check_uof.arrest_made == sent_uof['arrestMade']
        assert check_uof.arrest_charges == sent_uof['arrestCharges']
        assert check_uof.resident_weapon_used == sent_uof['residentWeaponUsed']
        assert check_uof.resident_injured == sent_uof['residentInjured']
        assert check_uof.resident_hospitalized == sent_uof['residentHospitalized']
        assert check_uof.officer_injured == sent_uof['officerInjured']
        assert check_uof.officer_hospitalized == sent_uof['officerHospitalized']
        assert check_uof.resident_race == cleaner.race(sent_uof['residentRace'])
        assert check_uof.resident_sex == cleaner.sex(sent_uof['residentSex'])
        assert check_uof.resident_age == cleaner.number_to_string(sent_uof['residentAge'])
        assert check_uof.resident_condition == sent_uof['residentCondition']
        assert check_uof.officer_identifier == sent_uof['officerIdentifier']
        assert check_uof.officer_race == cleaner.race(sent_uof['officerRace'])
        assert check_uof.officer_sex == cleaner.sex(sent_uof['officerSex'])
        assert check_uof.officer_age == cleaner.number_to_string(sent_uof['officerAge'])
        assert check_uof.officer_years_of_service == cleaner.number_to_string(sent_uof['officerYearsOfService'])
        assert check_uof.officer_condition == sent_uof['officerCondition']

    def test_post_mistyped_uof_data(self, testapp):
        ''' New UOF data from the extractor is processed as expected.
        '''
        # Set up the extractor
        department = Department.create(name="Good Police Department", short_name="GPD", load_defaults=False)
        extractor, envs = Extractor.from_department_and_password(department=department, password="password")

        # Set the correct authorization
        testapp.authorization = ('Basic', (extractor.username, 'password'))

        # Get a generated list of UOF descriptions from the JSON test client
        test_client = JSONTestClient()
        uof_count = 1
        uof_data = test_client.get_prebaked_uof(last=uof_count)

        # The app expects number values to be transmitted as strings. Let's change them to integers.
        uof_data[0]['residentAge'] = 28
        uof_data[0]['officerAge'] = 46
        uof_data[0]['officerYearsOfService'] = 17

        # post the json to the UOF URL
        response = testapp.post_json("/data/UOF", params={'month': 0, 'year': 0, 'data': uof_data})

        # assert that we got the expected reponse
        assert response.status_code == 200
        assert response.json_body['updated'] == 0
        assert response.json_body['added'] == uof_count

        # check the uof incident in the database against the data that was sent
        cleaner = Cleaners()
        sent_uof = uof_data[0]
        check_uof = UseOfForceIncident.query.filter_by(opaque_id=sent_uof['opaqueId']).first()
        assert check_uof.occured_date.strftime('%Y-%m-%d %-H:%-M:%S') == sent_uof['occuredDate']
        assert check_uof.division == cleaner.capitalize(sent_uof['division'])
        assert check_uof.precinct == cleaner.capitalize(sent_uof['precinct'])
        assert check_uof.shift == cleaner.capitalize(sent_uof['shift'])
        assert check_uof.beat == cleaner.capitalize(sent_uof['beat'])
        assert check_uof.disposition == sent_uof['disposition']
        assert check_uof.officer_force_type == cleaner.officer_force_type(sent_uof['officerForceType'])
        assert check_uof.use_of_force_reason == sent_uof['useOfForceReason']
        assert check_uof.service_type == sent_uof['serviceType']
        assert check_uof.arrest_made == sent_uof['arrestMade']
        assert check_uof.arrest_charges == sent_uof['arrestCharges']
        assert check_uof.resident_weapon_used == sent_uof['residentWeaponUsed']
        assert check_uof.resident_injured == sent_uof['residentInjured']
        assert check_uof.resident_hospitalized == sent_uof['residentHospitalized']
        assert check_uof.officer_injured == sent_uof['officerInjured']
        assert check_uof.officer_hospitalized == sent_uof['officerHospitalized']
        assert check_uof.resident_race == cleaner.race(sent_uof['residentRace'])
        assert check_uof.resident_sex == cleaner.sex(sent_uof['residentSex'])
        assert check_uof.resident_age == cleaner.number_to_string(sent_uof['residentAge'])
        assert check_uof.resident_condition == sent_uof['residentCondition']
        assert check_uof.officer_identifier == sent_uof['officerIdentifier']
        assert check_uof.officer_race == cleaner.race(sent_uof['officerRace'])
        assert check_uof.officer_sex == cleaner.sex(sent_uof['officerSex'])
        assert check_uof.officer_age == cleaner.number_to_string(sent_uof['officerAge'])
        assert check_uof.officer_years_of_service == cleaner.number_to_string(sent_uof['officerYearsOfService'])
        assert check_uof.officer_condition == sent_uof['officerCondition']

    def test_update_uof_data(self, testapp):
        ''' Updated UOF data from the extractor is processed as expected.
        '''
        # Set up the extractor
        department = Department.create(name="Good Police Department", short_name="GPD", load_defaults=False)
        extractor, envs = Extractor.from_department_and_password(department=department, password="password")

        # Set the correct authorization
        testapp.authorization = ('Basic', (extractor.username, 'password'))

        # Get a generated list of UOF descriptions from the JSON test client
        test_client = JSONTestClient()
        uof_data = test_client.get_prebaked_uof(last=1)
        # post the json to the UOF URL
        response = testapp.post_json("/data/UOF", params={'month': 0, 'year': 0, 'data': uof_data})

        # assert that we got the expected reponse
        assert response.status_code == 200
        assert response.json_body['updated'] == 0
        assert response.json_body['added'] == 1

        # Get the second pre-baked uof incident
        updated_uof_data = test_client.get_prebaked_uof(first=1, last=2)
        # Swap in the opaque ID from the first uof incident
        updated_uof_data[0]["opaqueId"] = uof_data[0]["opaqueId"]
        # The uof incident won't be a match unless these fields are the same
        updated_uof_data[0]["officerIdentifier"] = uof_data[0]["officerIdentifier"]
        updated_uof_data[0]["officerForceType"] = uof_data[0]["officerForceType"]
        # post the json to the uof URL
        response = testapp.post_json("/data/UOF", params={'month': 0, 'year': 0, 'data': updated_uof_data})

        # assert that we got the expected reponse
        assert response.status_code == 200
        assert response.json_body['updated'] == 1
        assert response.json_body['added'] == 0

        # There's only one complaint in the database.
        all_uof = UseOfForceIncident.query.all()
        assert len(all_uof) == 1

        # check the uof incident in the database against the updated data that was sent
        cleaner = Cleaners()
        sent_uof = updated_uof_data[0]
        check_uof = UseOfForceIncident.query.filter_by(opaque_id=sent_uof['opaqueId']).first()
        assert check_uof.occured_date.strftime('%Y-%m-%d %-H:%-M:%S') == sent_uof['occuredDate']
        assert check_uof.division == cleaner.capitalize(sent_uof['division'])
        assert check_uof.precinct == cleaner.capitalize(sent_uof['precinct'])
        assert check_uof.shift == cleaner.capitalize(sent_uof['shift'])
        assert check_uof.beat == cleaner.capitalize(sent_uof['beat'])
        assert check_uof.disposition == sent_uof['disposition']
        assert check_uof.officer_force_type == cleaner.officer_force_type(sent_uof['officerForceType'])
        assert check_uof.use_of_force_reason == sent_uof['useOfForceReason']
        assert check_uof.service_type == sent_uof['serviceType']
        assert check_uof.arrest_made == sent_uof['arrestMade']
        assert check_uof.arrest_charges == sent_uof['arrestCharges']
        assert check_uof.resident_weapon_used == sent_uof['residentWeaponUsed']
        assert check_uof.resident_injured == sent_uof['residentInjured']
        assert check_uof.resident_hospitalized == sent_uof['residentHospitalized']
        assert check_uof.officer_injured == sent_uof['officerInjured']
        assert check_uof.officer_hospitalized == sent_uof['officerHospitalized']
        assert check_uof.resident_race == cleaner.race(sent_uof['residentRace'])
        assert check_uof.resident_sex == cleaner.sex(sent_uof['residentSex'])
        assert check_uof.resident_age == cleaner.number_to_string(sent_uof['residentAge'])
        assert check_uof.resident_condition == sent_uof['residentCondition']
        assert check_uof.officer_identifier == sent_uof['officerIdentifier']
        assert check_uof.officer_race == cleaner.race(sent_uof['officerRace'])
        assert check_uof.officer_sex == cleaner.sex(sent_uof['officerSex'])
        assert check_uof.officer_age == cleaner.number_to_string(sent_uof['officerAge'])
        assert check_uof.officer_years_of_service == cleaner.number_to_string(sent_uof['officerYearsOfService'])
        assert check_uof.officer_condition == sent_uof['officerCondition']

    def test_post_uof_data_near_match_does_not_update(self, testapp):
        ''' UOF data with the same ID but different details creates a new record.
        '''
        # Set up the extractor
        department = Department.create(name="Good Police Department", short_name="GPD", load_defaults=False)
        extractor, envs = Extractor.from_department_and_password(department=department, password="password")

        # Set the correct authorization
        testapp.authorization = ('Basic', (extractor.username, 'password'))

        # Get a generated list of UOF descriptions from the JSON test client
        test_client = JSONTestClient()
        uof_data = test_client.get_prebaked_uof(last=1)
        # post the json to the UOF URL
        response = testapp.post_json("/data/UOF", params={'month': 0, 'year': 0, 'data': uof_data})

        # assert that we got the expected reponse
        assert response.status_code == 200
        assert response.json_body['updated'] == 0
        assert response.json_body['added'] == 1

        # Get the second pre-baked uof incident
        updated_uof_data = test_client.get_prebaked_uof(first=1, last=2)
        # Swap in the opaque ID from the first uof incident
        updated_uof_data[0]["opaqueId"] = uof_data[0]["opaqueId"]
        # post the json to the uof URL
        response = testapp.post_json("/data/UOF", params={'month': 0, 'year': 0, 'data': updated_uof_data})

        # assert that we got the expected reponse
        assert response.status_code == 200
        assert response.json_body['updated'] == 0
        assert response.json_body['added'] == 1

        # There's only one complaint in the database.
        all_uof = UseOfForceIncident.query.all()
        assert len(all_uof) == 2

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
        ois_data = test_client.get_prebaked_ois(last=ois_count)
        # post the json to the OIS URL
        response = testapp.post_json("/data/OIS", params={'month': 0, 'year': 0, 'data': ois_data})

        # assert that we got the expected reponse
        assert response.status_code == 200
        assert response.json_body['updated'] == 0
        assert response.json_body['added'] == ois_count

        # check the ois incident in the database against the data that was sent
        cleaner = Cleaners()
        sent_ois = ois_data[0]
        check_ois = OfficerInvolvedShooting.query.filter_by(opaque_id=sent_ois['opaqueId']).first()
        assert check_ois.occured_date.strftime('%Y-%m-%d %-H:%-M:%S') == sent_ois['occuredDate']
        assert check_ois.division == cleaner.capitalize(sent_ois['division'])
        assert check_ois.precinct == cleaner.capitalize(sent_ois['precinct'])
        assert check_ois.shift == cleaner.capitalize(sent_ois['shift'])
        assert check_ois.beat == cleaner.capitalize(sent_ois['beat'])
        assert check_ois.disposition == sent_ois['disposition']
        assert check_ois.resident_race == cleaner.race(sent_ois['residentRace'])
        assert check_ois.resident_sex == cleaner.sex(sent_ois['residentSex'])
        assert check_ois.resident_age == cleaner.number_to_string(sent_ois['residentAge'])
        assert check_ois.resident_weapon_used == cleaner.resident_weapon_used(sent_ois['residentWeaponUsed'])
        assert check_ois.resident_condition == sent_ois['residentCondition']
        assert check_ois.officer_identifier == sent_ois['officerIdentifier']
        assert check_ois.officer_weapon_used == sent_ois['officerForceType']
        assert check_ois.officer_race == cleaner.race(sent_ois['officerRace'])
        assert check_ois.officer_sex == cleaner.sex(sent_ois['officerSex'])
        assert check_ois.officer_age == cleaner.number_to_string(sent_ois['officerAge'])
        assert check_ois.officer_years_of_service == cleaner.string_to_integer(sent_ois['officerYearsOfService'])
        assert check_ois.officer_condition == sent_ois['officerCondition']

    def test_post_mistyped_ois_data(self, testapp):
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
        ois_data = test_client.get_prebaked_ois(last=ois_count)

        # The app expects number values to be transmitted as strings. Let's change them to integers.
        ois_data[0]['residentAge'] = 28
        ois_data[0]['officerAge'] = 46
        # And it expects this number value to be transmitted as a number, so let's make it a string.
        ois_data[0]['officerYearsOfService'] = "17"

        # post the json to the OIS URL
        response = testapp.post_json("/data/OIS", params={'month': 0, 'year': 0, 'data': ois_data})

        # assert that we got the expected reponse
        assert response.status_code == 200
        assert response.json_body['updated'] == 0
        assert response.json_body['added'] == ois_count

        # check the ois incident in the database against the data that was sent
        cleaner = Cleaners()
        sent_ois = ois_data[0]
        check_ois = OfficerInvolvedShooting.query.filter_by(opaque_id=sent_ois['opaqueId']).first()
        assert check_ois.occured_date.strftime('%Y-%m-%d %-H:%-M:%S') == sent_ois['occuredDate']
        assert check_ois.division == cleaner.capitalize(sent_ois['division'])
        assert check_ois.precinct == cleaner.capitalize(sent_ois['precinct'])
        assert check_ois.shift == cleaner.capitalize(sent_ois['shift'])
        assert check_ois.beat == cleaner.capitalize(sent_ois['beat'])
        assert check_ois.disposition == sent_ois['disposition']
        assert check_ois.resident_race == cleaner.race(sent_ois['residentRace'])
        assert check_ois.resident_sex == cleaner.sex(sent_ois['residentSex'])
        assert check_ois.resident_age == cleaner.number_to_string(sent_ois['residentAge'])
        assert check_ois.resident_weapon_used == cleaner.resident_weapon_used(sent_ois['residentWeaponUsed'])
        assert check_ois.resident_condition == sent_ois['residentCondition']
        assert check_ois.officer_identifier == sent_ois['officerIdentifier']
        assert check_ois.officer_weapon_used == sent_ois['officerForceType']
        assert check_ois.officer_race == cleaner.race(sent_ois['officerRace'])
        assert check_ois.officer_sex == cleaner.sex(sent_ois['officerSex'])
        assert check_ois.officer_age == cleaner.number_to_string(sent_ois['officerAge'])
        assert check_ois.officer_years_of_service == cleaner.string_to_integer(sent_ois['officerYearsOfService'])
        assert check_ois.officer_condition == sent_ois['officerCondition']

    def test_update_ois_data(self, testapp):
        ''' Updated OIS data from the extractor is processed as expected.
        '''
        # Set up the extractor
        department = Department.create(name="Good Police Department", short_name="GPD", load_defaults=False)
        extractor, envs = Extractor.from_department_and_password(department=department, password="password")

        # Set the correct authorization
        testapp.authorization = ('Basic', (extractor.username, 'password'))

        # Get a generated list of OIS descriptions from the JSON test client
        test_client = JSONTestClient()
        ois_data = test_client.get_prebaked_ois(last=1)
        # post the json to the OIS URL
        response = testapp.post_json("/data/OIS", params={'month': 0, 'year': 0, 'data': ois_data})

        # assert that we got the expected reponse
        assert response.status_code == 200
        assert response.json_body['updated'] == 0
        assert response.json_body['added'] == 1

        # Get the second pre-baked ois incident
        updated_ois_data = test_client.get_prebaked_ois(first=1, last=2)
        # Swap in the opaque ID from the first ois incident
        updated_ois_data[0]["opaqueId"] = ois_data[0]["opaqueId"]
        # The ois incident won't be a match unless this field is the same
        updated_ois_data[0]["officerIdentifier"] = ois_data[0]["officerIdentifier"]
        # post the json to the ois URL
        response = testapp.post_json("/data/OIS", params={'month': 0, 'year': 0, 'data': updated_ois_data})

        # assert that we got the expected reponse
        assert response.status_code == 200
        assert response.json_body['updated'] == 1
        assert response.json_body['added'] == 0

        # There's only one complaint in the database.
        all_ois = OfficerInvolvedShooting.query.all()
        assert len(all_ois) == 1

        # check the ois incident in the database against the updated data that was sent
        cleaner = Cleaners()
        sent_ois = updated_ois_data[0]
        check_ois = OfficerInvolvedShooting.query.filter_by(opaque_id=sent_ois['opaqueId']).first()
        assert check_ois.occured_date.strftime('%Y-%m-%d %-H:%-M:%S') == sent_ois['occuredDate']
        assert check_ois.division == cleaner.capitalize(sent_ois['division'])
        assert check_ois.precinct == cleaner.capitalize(sent_ois['precinct'])
        assert check_ois.shift == cleaner.capitalize(sent_ois['shift'])
        assert check_ois.beat == cleaner.capitalize(sent_ois['beat'])
        assert check_ois.disposition == sent_ois['disposition']
        assert check_ois.resident_race == cleaner.race(sent_ois['residentRace'])
        assert check_ois.resident_sex == cleaner.sex(sent_ois['residentSex'])
        assert check_ois.resident_age == cleaner.number_to_string(sent_ois['residentAge'])
        assert check_ois.resident_weapon_used == cleaner.resident_weapon_used(sent_ois['residentWeaponUsed'])
        assert check_ois.resident_condition == sent_ois['residentCondition']
        assert check_ois.officer_identifier == sent_ois['officerIdentifier']
        assert check_ois.officer_weapon_used == sent_ois['officerForceType']
        assert check_ois.officer_race == cleaner.race(sent_ois['officerRace'])
        assert check_ois.officer_sex == cleaner.sex(sent_ois['officerSex'])
        assert check_ois.officer_age == cleaner.number_to_string(sent_ois['officerAge'])
        assert check_ois.officer_years_of_service == cleaner.string_to_integer(sent_ois['officerYearsOfService'])
        assert check_ois.officer_condition == sent_ois['officerCondition']

    def test_post_ois_data_near_match_does_not_update(self, testapp):
        ''' OIS data with the same ID but different details creates a new record.
        '''
        # Set up the extractor
        department = Department.create(name="Good Police Department", short_name="GPD", load_defaults=False)
        extractor, envs = Extractor.from_department_and_password(department=department, password="password")

        # Set the correct authorization
        testapp.authorization = ('Basic', (extractor.username, 'password'))

        # Get a generated list of OIS descriptions from the JSON test client
        test_client = JSONTestClient()
        ois_data = test_client.get_prebaked_ois(last=1)
        # post the json to the OIS URL
        response = testapp.post_json("/data/OIS", params={'month': 0, 'year': 0, 'data': ois_data})

        # assert that we got the expected reponse
        assert response.status_code == 200
        assert response.json_body['updated'] == 0
        assert response.json_body['added'] == 1

        # Get the second pre-baked ois incident
        updated_ois_data = test_client.get_prebaked_ois(first=1, last=2)
        # Swap in the opaque ID from the first ois incident
        updated_ois_data[0]["opaqueId"] = ois_data[0]["opaqueId"]
        # post the json to the ois URL
        response = testapp.post_json("/data/OIS", params={'month': 0, 'year': 0, 'data': updated_ois_data})

        # assert that we got the expected reponse
        assert response.status_code == 200
        assert response.json_body['updated'] == 0
        assert response.json_body['added'] == 1

        # There's only one complaint in the database.
        all_ois = OfficerInvolvedShooting.query.all()
        assert len(all_ois) == 2
