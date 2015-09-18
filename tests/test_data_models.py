# -*- coding: utf-8 -*-
import datetime as dt

import pytest

from comport.data.models import UseOfForceIncident
from .factories import UseOfForceIncidentFactory
import uuid

@pytest.mark.usefixtures('db')
class TestDataModels:
        def test_get_csv_row_from_incident_when_column_is_none(self):
            incident = UseOfForceIncident()
            incident.officer_race = None
            incident.officerInjured = False
            incident.to_csv_row()
