# -*- coding: utf-8 -*-
import pytest
import responses
import json
from datetime import datetime
from comport.department.models import Department, Extractor
from comport.data.models import OfficerInvolvedShootingBPD, UseOfForceIncidentBPD, CitizenComplaintBPD, AssaultOnOfficerBPD
from testclient.JSON_test_client import JSONTestClient
from comport.data.cleaners import Cleaners
from flask import current_app

@pytest.mark.usefixtures('db')
class TestExtractorBPD:

    def test_post_uof_data(self, testapp):
        ''' New UOF data from the extractor is processed as expected.
        '''
        # Set up the extractor
        department = Department.create(name="B Police Department", short_name="BPD", load_defaults=False)
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
        check_uof = UseOfForceIncidentBPD.query.filter_by(opaque_id=sent_uof['opaqueId']).first()
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
        department = Department.create(name="B Police Department", short_name="BPD", load_defaults=False)
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
        check_uof = UseOfForceIncidentBPD.query.filter_by(opaque_id=sent_uof['opaqueId']).first()
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
        department = Department.create(name="B Police Department", short_name="BPD", load_defaults=False)
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
        all_uof = UseOfForceIncidentBPD.query.all()
        assert len(all_uof) == 1

        # check the uof incident in the database against the updated data that was sent
        cleaner = Cleaners()
        sent_uof = updated_uof_data[0]
        check_uof = UseOfForceIncidentBPD.query.filter_by(opaque_id=sent_uof['opaqueId']).first()
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
        department = Department.create(name="B Police Department", short_name="BPD", load_defaults=False)
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
        all_uof = UseOfForceIncidentBPD.query.all()
        assert len(all_uof) == 2
