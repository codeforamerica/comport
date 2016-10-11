# -*- coding: utf-8 -*-
import pytest
from comport.department.models import Department, Extractor
from comport.data.models import IncidentsUpdated, UseOfForceIncidentLMPD
from testclient.JSON_test_client import JSONTestClient

@pytest.mark.usefixtures('db')
class TestExtractorLMPD:

    def test_post_uof_data(self, testapp):
        ''' New and updated UOF data from the extractor is processed as expected.
        '''
        # Set up the extractor
        department = Department.create(name="B Police Department", short_name="LMPD", load_defaults=False)
        extractor, _ = Extractor.from_department_and_password(department=department, password="password")

        # Set the correct authorization
        testapp.authorization = ('Basic', (extractor.username, 'password'))

        # post to the heartbeat URL to start the update
        response = testapp.post_json("/data/heartbeat", params={"heartbeat": "heartbeat"})

        # Post 5 fake incidents to the UOF endpoint
        uof_count = 5
        test_client = JSONTestClient()
        uof_data = test_client.make_uof(count=uof_count, short_name=department.short_name)
        response = testapp.post_json("/data/UOF", params={'month': 0, 'year': 0, 'data': uof_data})

        # assert that we got the expected reponse
        assert response.status_code == 200

        # there are 5 incident rows in the database
        check_uofs = UseOfForceIncidentLMPD.query.all()
        assert len(check_uofs) == uof_count

        for incident in uof_data:
            # verify that the opaqueIDs posted match those in the database
            assert UseOfForceIncidentLMPD.query.filter_by(opaque_id=incident['opaqueId']).first() is not None
            # verify that the opaqueIds are recorded in IncidentsUpdated tables
            record_updated = IncidentsUpdated.query.filter_by(opaque_id=incident['opaqueId']).first()
            assert record_updated is not None
            assert record_updated.department_id == department.id
            assert record_updated.incident_type == "uof"

        # post to the heartbeat URL to start the new update
        response = testapp.post_json("/data/heartbeat", params={"heartbeat": "heartbeat"})

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
        check_uofs = UseOfForceIncidentLMPD.query.all()
        assert len(check_uofs) == uof_count

        # verify that the opaqueIDs posted match those in the database
        for incident in uof_data:
            assert UseOfForceIncidentLMPD.query.filter_by(opaque_id=incident['opaqueId']).first() is not None

        # Create 5 more fake incidents
        new_data = test_client.make_uof(count=uof_count, short_name=department.short_name)
        # give them the same opaqueIds as the first batch
        for idx, _ in enumerate(new_data):
            new_data[idx]['opaqueId'] = uof_data[idx]['opaqueId']

        # post the new incident rows without starting a new update
        response = testapp.post_json("/data/UOF", params={'month': 0, 'year': 0, 'data': new_data})

        # assert that we got the expected reponse
        assert response.status_code == 200

        # there are 10 incident rows in the database
        check_uofs = UseOfForceIncidentLMPD.query.all()
        assert len(check_uofs) == uof_count * 2

    def test_all_uof_records_destroyed_when_new_record_posted(self, testapp):
        ''' Posting a new record with an id that matches a set of past records destroys all of them.
        '''
        # Set up the extractor
        department = Department.create(name="B Police Department", short_name="LMPD", load_defaults=False)
        extractor, _ = Extractor.from_department_and_password(department=department, password="password")

        # Set the correct authorization
        testapp.authorization = ('Basic', (extractor.username, 'password'))

        # post to the heartbeat URL to start the update
        response = testapp.post_json("/data/heartbeat", params={"heartbeat": "heartbeat"})

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
        check_uofs = UseOfForceIncidentLMPD.query.all()
        assert len(check_uofs) == uof_count

        # all the records in the database have the same opaqueId
        uof_records = UseOfForceIncidentLMPD.query.filter_by(opaque_id=use_id).all()
        assert len(uof_records) == uof_count
        # verify that the opaqueId is recorded in an IncidentsUpdated table
        record_updated = IncidentsUpdated.query.filter_by(opaque_id=use_id).first()
        assert record_updated is not None
        assert record_updated.incident_type == "uof"
        assert record_updated.department_id == department.id

        # post to the heartbeat URL to start a new update
        response = testapp.post_json("/data/heartbeat", params={"heartbeat": "heartbeat"})

        # Create 1 new fake incident
        new_data = test_client.make_uof(count=1, short_name=department.short_name)
        # give it the same opaqueId as the first batch
        new_data[0]['opaqueId'] = use_id

        # post the new incident row
        response = testapp.post_json("/data/UOF", params={'month': 0, 'year': 0, 'data': new_data})

        # assert that we got the expected reponse
        assert response.status_code == 200

        # there is now only 1 incident row in the database
        check_uofs = UseOfForceIncidentLMPD.query.all()
        assert len(check_uofs) == 1

        # verify that the opaqueID posted matches that in the database
        assert check_uofs[0].opaque_id == use_id

        # verify that the opaqueId is recorded in an IncidentsUpdated table
        record_updated = IncidentsUpdated.query.filter_by(opaque_id=use_id).first()
        assert record_updated is not None
        assert record_updated.incident_type == "uof"
        assert record_updated.department_id == department.id
