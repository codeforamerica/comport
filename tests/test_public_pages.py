import pytest
from comport.department.models import Department
from bs4 import BeautifulSoup
from comport.data.models import OfficerInvolvedShootingBPD, UseOfForceIncidentBPD, CitizenComplaintBPD
from comport.data.models import OfficerInvolvedShootingIMPD, UseOfForceIncidentIMPD, CitizenComplaintIMPD, AssaultOnOfficerIMPD
from comport.data.models import UseOfForceIncidentLMPD


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
        lmpd = Department.create(name="L Police Department", short_name="LMPD", is_public=False)
        UseOfForceIncidentLMPD.create(department_id=lmpd.id, opaque_id="12345abcde")

        response = testapp.get("/", status=200)
        soup = BeautifulSoup(response.text)
        assert soup.find("a", href="/department/IMPD/useofforce") is not None
        assert soup.find("a", href="/department/BPD/useofforce") is not None
        assert soup.find("a", href="/department/LMPD/useofforce") is None

    def test_all_dept_links(self, testapp):
        department = Department.create(name="B Police Department", short_name="BPD", is_public=True)
        CitizenComplaintBPD.create(department_id=department.id, opaque_id="12345abcde")
        UseOfForceIncidentBPD.create(department_id=department.id, opaque_id="23456bcdef")
        OfficerInvolvedShootingBPD.create(department_id=department.id, opaque_id="34567cdefg")

        response = testapp.get("/", status=200)
        soup = BeautifulSoup(response.text)
        with open("scratch.html", "w") as text_file:
            text_file.write(response.text)
        assert soup.find("a", href="/department/BPD/complaints") is not None
        assert soup.find("a", href="/department/BPD/useofforce") is not None
        assert soup.find("a", href="/department/BPD/officerinvolvedshootings") is not None

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
