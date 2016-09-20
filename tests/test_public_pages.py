import io
import csv
import pytest
import importlib
from flask import url_for
from comport.user.models import User, Role, Invite_Code
from comport.department.models import Department
from comport.data.models import UseOfForceIncidentIMPD
from .utils import log_in_user
from bs4 import BeautifulSoup


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
        Department.create(name="Public1 PD", short_name="P1PD", is_public=True)
        Department.create(name="Public2 PD", short_name="P2PD", is_public=True)
        Department.create(name="Not Ready PD", short_name="NPD", is_public=False)

        response = testapp.get("/", status=200)
        soup = BeautifulSoup(response.text)
        assert soup.find("a", href="/department/P1PD/complaints") is not None
        assert soup.find("a", href="/department/P2PD/complaints") is not None
        assert soup.find("a", href="/department/NPD/complaints") is None

   
 