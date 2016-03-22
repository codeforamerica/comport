# -*- coding: utf-8 -*-
from comport.department.models import Extractor
from .factories import DepartmentFactory
from .comport_test_client import ComportTestClient
from comport.data.models import OfficerInvolvedShooting, UseOfForceIncident, CitizenComplaint

class TestDataModels:

    def test_heartbeat(self, app):
        ''' Send a valid heartbeat request, get a valid response.
        '''
        # Set up an extractor.
        department = DepartmentFactory()
        department.save()
        extractor = Extractor.create(username='extractor', password='password', email='extractor@example.com', next_month=10, next_year=2006)
        extractor.departments.append(department)
        extractor.save()

        # Post the heartbeat.
        erica = ComportTestClient(app.test_client())
        erica.post_json(path='/data/heartbeat', data={'heartbeat': 'heartbeat'}, username='extractor', password='password')

        # We got a valid response.
        assert erica.status_code == 200
        # The response looks like we expect it to
        assert erica.response_data['nextMonth'] == 10
        assert erica.response_data['nextYear'] == 2006
        assert erica.response_data['received'] == {'heartbeat': 'heartbeat'}
