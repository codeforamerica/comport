# -*- coding: utf-8 -*-
import datetime as dt

import pytest

from comport.data.models import OfficerInvolvedShooting, UseOfForceIncident, CitizenComplaint
from .factories import UseOfForceIncidentFactory
import uuid

@pytest.mark.usefixtures('db')
class TestDataModels:
        def test_allow_no_race(self):
            complaint = CitizenComplaint(resident_race=None)
            assert complaint.resident_race == None

        def test_allow_valid_race(self):
            complaint = CitizenComplaint(resident_race="Black")
            assert complaint.resident_race == "Black"

        def test_cleaning_race_b(self):
            complaint = CitizenComplaint(resident_race="b")
            assert complaint.resident_race == "Black"

        def test_cleaning_race_B(self):
            complaint = CitizenComplaint(resident_race="B")
            assert complaint.resident_race == "Black"

        def test_cleaning_race_B_and_space(self):
            complaint = CitizenComplaint(resident_race="B     ")
            assert complaint.resident_race == "Black"

        def test_allow_no_sex(self):
            complaint = CitizenComplaint(resident_sex=None)
            assert complaint.resident_sex == None

        def test_cleaning_sex_f(self):
            complaint = CitizenComplaint(resident_sex="f")
            assert complaint.resident_sex == "Female"

        def test_cleaning_sex_F(self):
            complaint = CitizenComplaint(resident_sex="F")
            assert complaint.resident_sex == "Female"

        def test_cleaning_sex_M(self):
            complaint = CitizenComplaint(resident_sex="M")
            assert complaint.resident_sex == "Male"

        def test_cleaning_sex_F_and_space(self):
            complaint = CitizenComplaint(resident_sex="F     ")
            assert complaint.resident_sex == "Female"

        def test_cleaning_precinct(self):
            complaint = CitizenComplaint(precinct="TRAINING BUREAU")
            assert complaint.precinct == "Training Bureau"

        def test_cleaning_no_precinct(self):
            complaint = CitizenComplaint(precinct=None)
            assert complaint.precinct == None

        def test_cleaning_geo_abbrevs(self):
            complaint = CitizenComplaint(precinct="NW DAY SHIFT")
            assert complaint.precinct == "NW Day Shift"

        def test_cleaning_on_ois(self):
            ois = OfficerInvolvedShooting(precinct="NW DAY SHIFT", resident_sex="f", resident_race='b')
            assert ois.precinct == "NW Day Shift"
            assert ois.resident_sex == "Female"
            assert ois.resident_race == "Black"
