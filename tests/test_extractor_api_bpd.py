# -*- coding: utf-8 -*-
import pytest
import responses
import json
from datetime import datetime, time, timedelta
from comport.department.models import Department, Extractor
from comport.data.models import IncidentsUpdated, OfficerInvolvedShootingBPD, UseOfForceIncidentBPD, CitizenComplaintBPD
from testclient.JSON_test_client import JSONTestClient
from comport.data.cleaners import Cleaners
from flask import current_app

@pytest.mark.usefixtures('db')
class TestExtractorBPD:

    def test_post_uof_data(self, testapp):
        ''' New and updated UOF data from the extractor is processed as expected.
        '''
        # Set up the extractor
        department = Department.create(name="B Police Department", short_name="BPD", load_defaults=False)
        extractor, envs = Extractor.from_department_and_password(department=department, password="password")

        # Set the correct authorization
        testapp.authorization = ('Basic', (extractor.username, 'password'))

        # Post 5 fake incidents to the UOF endpoint
        uof_count = 5
        test_client = JSONTestClient()
        uof_data = test_client.make_uof(count=uof_count, short_name=department.short_name)
        response = testapp.post_json("/data/UOF", params={'month': 0, 'year': 0, 'data': uof_data})

        # assert that we got the expected reponse
        assert response.status_code == 200

        # there are 5 incident rows in the database
        check_uofs = UseOfForceIncidentBPD.query.all()
        assert len(check_uofs) == uof_count

        # make a valid updated date
        today = datetime.combine(datetime.today(), time())
        for incident in uof_data:
            # verify that the opaqueIDs posted match those in the database
            assert UseOfForceIncidentBPD.query.filter_by(opaque_id=incident['opaqueId']).first() is not None
            # verify that the opaqueIds are recorded in IncidentsUpdated tables
            record_updated = IncidentsUpdated.query.filter_by(opaque_id=incident['opaqueId']).first()
            assert record_updated is not None
            assert record_updated.updated_date == today
            # now set the updated dates back a day, so the records will be replaced
            # when we post new incidents with the same ids
            record_updated.update(updated_date=today - timedelta(days=1))

        # Create 5 more fake incidents
        new_data = test_client.make_uof(count=uof_count, short_name=department.short_name)
        # give them the same opaqueIds as the first batch
        for idx, _ in enumerate(new_data):
            new_data[idx]['opaqueId'] = uof_data[idx]['opaqueId']

        # post the new incident rows
        response = testapp.post_json("/data/UOF", params={'month': 0, 'year': 0, 'data': new_data})

        # assert that we got the expected reponse
        assert response.status_code == 200

        # there are 5 incident rows in the database
        check_uofs = UseOfForceIncidentBPD.query.all()
        assert len(check_uofs) == uof_count

        # verify that the opaqueIDs posted match those in the database
        for incident in uof_data:
            assert UseOfForceIncidentBPD.query.filter_by(opaque_id=incident['opaqueId']).first() is not None

    def test_all_records_destroyed_when_new_record_posted(self, testapp):
        ''' Posting a new record with an id that matches a set of past records destroys all of them.
        '''
        # Set up the extractor
        department = Department.create(name="B Police Department", short_name="BPD", load_defaults=False)
        extractor, envs = Extractor.from_department_and_password(department=department, password="password")

        # Set the correct authorization
        testapp.authorization = ('Basic', (extractor.username, 'password'))

        # Post 5 fake incidents with an identical opaqueId to the UOF endpoint
        uof_count = 5
        test_client = JSONTestClient()
        uof_data = test_client.make_uof(count=uof_count, short_name=department.short_name)
        use_id = uof_data[0]['opaqueId']
        for idx, _ in enumerate(uof_data):
            uof_data[idx]['opaqueId'] = use_id
        response = testapp.post_json("/data/UOF", params={'month': 0, 'year': 0, 'data': uof_data})

        # assert that we got the expected reponse
        assert response.status_code == 200

        # there are 5 incident rows in the database
        check_uofs = UseOfForceIncidentBPD.query.all()
        assert len(check_uofs) == uof_count

        # make a valid updated date
        today = datetime.combine(datetime.today(), time())
        # all the records in the database have the same id
        uof_records = UseOfForceIncidentBPD.query.filter_by(opaque_id=use_id).all()
        assert len(uof_records) == 5
        # verify that the opaqueId is recorded in an IncidentsUpdated table
        record_updated = IncidentsUpdated.query.filter_by(opaque_id=use_id).first()
        assert record_updated is not None
        assert record_updated.updated_date == today
        # now set the updated date back a day, so the records will be replaced
        # when we post a new incident with the same id
        record_updated.update(updated_date=today - timedelta(days=1))

        # Create 1 new fake incident
        new_data = test_client.make_uof(count=1, short_name=department.short_name)
        # give it the same opaqueId as the first batch
        new_data[0]['opaqueId'] = use_id

        # post the new incident
        response = testapp.post_json("/data/UOF", params={'month': 0, 'year': 0, 'data': new_data})

        # assert that we got the expected reponse
        assert response.status_code == 200

        # there is 1 incident row in the database
        check_uofs = UseOfForceIncidentBPD.query.all()
        assert len(check_uofs) == 1

        # verify that the opaqueID posted matches that in the database
        assert check_uofs[0].opaque_id == use_id

        # verify that the opaqueId is recorded in an IncidentsUpdated table
        record_updated = IncidentsUpdated.query.filter_by(opaque_id=use_id).first()
        assert record_updated is not None
        assert record_updated.updated_date == today
