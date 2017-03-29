import pytest
from flask import url_for
from comport.department.models import Extractor, Department
from bs4 import BeautifulSoup
from comport.data.models import OfficerInvolvedShootingBPD, UseOfForceIncidentBPD, CitizenComplaintBPD
from comport.data.models import OfficerInvolvedShootingIMPD, UseOfForceIncidentIMPD, CitizenComplaintIMPD, AssaultOnOfficerIMPD
from comport.data.models import PursuitSRPD
from comport.data.models import UseOfForceIncidentLMPD
from .utils import create_and_log_in_user
import datetime

@pytest.mark.usefixtures('db')
class TestPublicPages:

    def test_home_page_exists(self, testapp):
        testapp.get("/", status=200)

    def test_home_page_links_to_about(self, testapp):
        response = testapp.get("/", status=200)
        soup = BeautifulSoup(response.text)
        assert soup.find("a", href="/about/") is not None

    def test_about_page_exists(self, testapp):
        response = testapp.get("/about/", status=200)
        soup = BeautifulSoup(response.text)
        assert soup.find("a", href="https://www.codeforamerica.org") is not None

    def test_multiple_depts_display(self, testapp):
        impd = Department.create(name="I Police Department", short_name="IMPD", is_public=True)
        UseOfForceIncidentIMPD.create(department_id=impd.id, opaque_id="12345abcde")
        bpd = Department.create(name="B Police Department", short_name="BPD", is_public=True)
        UseOfForceIncidentBPD.create(department_id=bpd.id, opaque_id="12345abcde")
        lmpd = Department.create(name="LM Police Department", short_name="LMPD", is_public=False)
        UseOfForceIncidentLMPD.create(department_id=lmpd.id, opaque_id="12345abcde")

        response = testapp.get("/", status=200)
        soup = BeautifulSoup(response.text)
        assert soup.find("a", href="/department/IMPD/useofforce") is not None
        assert soup.find("a", href="/department/BPD/useofforce") is not None
        assert soup.find("a", href="/department/LMPD/useofforce") is None

    def test_non_public_depts_display_for_users_with_access(self, testapp):
        ''' Users can see links to datasets they're allowed to access on the front page
        '''
        impd = Department.create(name="I Police Department", short_name="IMPD", is_public=True)
        UseOfForceIncidentIMPD.create(department_id=impd.id, opaque_id="12345abcde")
        bpd = Department.create(name="B Police Department", short_name="BPD", is_public=False)
        UseOfForceIncidentBPD.create(department_id=bpd.id, opaque_id="12345abcde")
        lmpd = Department.create(name="LM Police Department", short_name="LMPD", is_public=False)
        UseOfForceIncidentLMPD.create(department_id=lmpd.id, opaque_id="12345abcde")

        # A non logged-in user can only see the public department
        response = testapp.get("/", status=200)
        soup = BeautifulSoup(response.text)
        assert soup.find("a", href="/department/IMPD/useofforce") is not None
        assert soup.find("a", href="/department/BPD/useofforce") is None
        assert soup.find("a", href="/department/LMPD/useofforce") is None

        # A user associated with a particular department can see that department's
        # available datasets when logged in
        create_and_log_in_user(testapp=testapp, department=bpd, username="user1")
        response = testapp.get("/", status=200)
        soup = BeautifulSoup(response.text)
        assert soup.find("a", href="/department/IMPD/useofforce") is not None
        assert soup.find("a", href="/department/BPD/useofforce") is not None
        assert soup.find("a", href="/department/LMPD/useofforce") is None

        # A user with admin access can see all departments' available datasets
        create_and_log_in_user(testapp=testapp, department=impd, rolename='admin', username="user2")
        response = testapp.get("/", status=200)
        soup = BeautifulSoup(response.text)
        assert soup.find("a", href="/department/IMPD/useofforce") is not None
        assert soup.find("a", href="/department/BPD/useofforce") is not None
        assert soup.find("a", href="/department/LMPD/useofforce") is not None

        # Log out and only the public department should be visible
        testapp.get(url_for('public.logout')).follow()
        response = testapp.get("/", status=200)
        soup = BeautifulSoup(response.text)
        assert soup.find("a", href="/department/IMPD/useofforce") is not None
        assert soup.find("a", href="/department/BPD/useofforce") is None
        assert soup.find("a", href="/department/LMPD/useofforce") is None

    def test_all_dept_links(self, testapp):
        department = Department.create(name="B Police Department", short_name="BPD", is_public=True)
        CitizenComplaintBPD.create(department_id=department.id, opaque_id="12345abcde")
        UseOfForceIncidentBPD.create(department_id=department.id, opaque_id="23456bcdef")
        OfficerInvolvedShootingBPD.create(department_id=department.id, opaque_id="34567cdefg")
        SRDepartment = Department.create(name="SR Police Department", short_name="SRPD", is_public=True)
        PursuitSRPD.create(department_id=SRDepartment.id, opaque_id="45678defgh")

        response = testapp.get("/", status=200)
        soup = BeautifulSoup(response.text)
        assert soup.find("a", href="/department/BPD/complaints") is not None
        assert soup.find("a", href="/department/BPD/useofforce") is not None
        assert soup.find("a", href="/department/BPD/officerinvolvedshootings") is not None
        assert soup.find("a", href="/department/SRPD/pursuits") is not None

    def test_data_status(self, testapp):
        department = Department.create(name="B Police Department", short_name="BPD", is_public=True)
        CitizenComplaintBPD.create(department_id=department.id, opaque_id="12345abcde")
        OfficerInvolvedShootingBPD.create(department_id=department.id, opaque_id="34567cdefg")
        department.is_public_officer_involved_shootings = False

        response = testapp.get("/", status=200)
        soup = BeautifulSoup(response.text)
        assert soup.find("a", href="/department/BPD/complaints") is not None
        assert soup.find("a", href="/department/BPD/useofforce") is None
        assert soup.find("a", href="/department/BPD/officerinvolvedshootings") is None

    def test_updated_text_on_schema_pages(self, testapp):
        ''' The notice of the last time a dataset was updated is on all schema pages
        '''
        department = Department.create(name="B Police Department", short_name="BPD", is_public=True)
        CitizenComplaintBPD.create(department_id=department.id, opaque_id="12345abcde")
        UseOfForceIncidentBPD.create(department_id=department.id, opaque_id="23456bcdef")
        OfficerInvolvedShootingBPD.create(department_id=department.id, opaque_id="34567cdefg")

        SRDepartment = Department.create(name="SR Police Department", short_name="SRPD", is_public=True)
        PursuitSRPD.create(department_id=SRDepartment.id, opaque_id="45678defgh")

        extractor_password = 'password'
        bpd_extractor, envs = Extractor.from_department_and_password(department=department, password=extractor_password)
        bpd_extractor.last_contact = datetime.datetime(2012, 9, 16)
        srpd_extractor, envs = Extractor.from_department_and_password(department=SRDepartment, password=extractor_password)
        srpd_extractor.last_contact = datetime.datetime(2014, 11, 2)

        response = testapp.get("/department/BPD/schema/complaints/")
        soup = BeautifulSoup(response.text)
        updated_span = soup.find("span", {"class": "updated"})
        assert updated_span is not None
        assert "Last Updated September 16, 2012" == updated_span.text

        response = testapp.get("/department/BPD/schema/useofforce/")
        soup = BeautifulSoup(response.text)
        updated_span = soup.find("span", {"class": "updated"})
        assert updated_span is not None
        assert "Last Updated September 16, 2012" == updated_span.text

        response = testapp.get("/department/BPD/schema/officerinvolvedshootings/")
        soup = BeautifulSoup(response.text)
        updated_span = soup.find("span", {"class": "updated"})
        assert updated_span is not None
        assert "Last Updated September 16, 2012" == updated_span.text

        response = testapp.get("/department/SRPD/schema/pursuits/")
        soup = BeautifulSoup(response.text)
        updated_span = soup.find("span", {"class": "updated"})
        assert updated_span is not None
        assert "Last Updated November 02, 2014" == updated_span.text
