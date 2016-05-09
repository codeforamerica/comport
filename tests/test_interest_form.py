# -*- coding: utf-8 -*-
import pytest
from comport.interest.forms import InterestForm
from comport.interest.models import Interested

@pytest.mark.usefixtures('app')
class TestInterestForm:

    def test_validate_success(self, db):
        ''' The form validates when properly filled out.
        '''
        form = InterestForm(name="Jean Weaver", agency="Clinton Police Department", location="Clinton, OK", phone="580-970-3338", email="jean.weaver@example.com", comments="I'm interested in Comport as an open-source tool!")
        assert form.validate() is True

    def test_name_required(self):
        ''' The form requires a non-None name.
        '''
        form = InterestForm(name=None, agency="Clinton Police Department", location="Clinton, OK", phone="580-970-3338", email="jean.weaver@example.com", comments="I'm interested in Comport as an open-source tool!")
        assert form.validate() is False
        assert 'This field is required.' in form.name.errors

    def test_agency_required(self):
        ''' The form requires a non-None agency.
        '''
        form = InterestForm(name="Jean Weaver", agency=None, location="Clinton, OK", phone="580-970-3338", email="jean.weaver@example.com", comments="I'm interested in Comport as an open-source tool!")
        assert form.validate() is False
        assert 'This field is required.' in form.agency.errors

    def test_location_required(self):
        ''' The form requires a non-None location.
        '''
        form = InterestForm(name="Jean Weaver", agency="Clinton Police Department", location=None, phone="580-970-3338", email="jean.weaver@example.com", comments="I'm interested in Comport as an open-source tool!")
        assert form.validate() is False
        assert 'This field is required.' in form.location.errors

    def test_phone_required(self):
        ''' The form requires a non-None phone.
        '''
        form = InterestForm(name="Jean Weaver", agency="Clinton Police Department", location="Clinton, OK", phone=None, email="jean.weaver@example.com", comments="I'm interested in Comport as an open-source tool!")
        assert form.validate() is False
        assert 'This field is required.' in form.phone.errors

    def test_email_required(self):
        ''' The form requires a non-None email.
        '''
        form = InterestForm(name="Jean Weaver", agency="Clinton Police Department", location="Clinton, OK", phone="580-970-3338", email=None, comments="I'm interested in Comport as an open-source tool!")
        assert form.validate() is False
        assert 'This field is required.' in form.email.errors

    def test_email_valid(self):
        ''' The form requires a valid email.
        '''
        form = InterestForm(name="Jean Weaver", agency="Clinton Police Department", location="Clinton, OK", phone="580-970-3338", email="jean.weaverexample.com", comments="I'm interested in Comport as an open-source tool!")
        assert form.validate() is False
        assert 'Invalid email address.' in form.email.errors

    def test_comments_not_required(self):
        ''' The form does not require a non-None comment.
        '''
        form = InterestForm(name="Jean Weaver", agency="Clinton Police Department", location="Clinton, OK", phone="580-970-3338", email="jean.weaver@example.com", comments=None)
        assert form.validate() is True
