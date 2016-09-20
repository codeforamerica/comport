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
