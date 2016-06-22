# -*- coding: utf-8 -*-
"""Functional tests using WebTest.

See: http://webtest.readthedocs.org/
"""
import io
import csv
import pytest
from flask import url_for
from comport.content.models import ChartBlock
from comport.user.models import User, Role, Invite_Code
from comport.department.models import Department
from comport.data.models import UseOfForceIncident

@pytest.fixture
def preconfigured_department():
    # create a department
    department = Department.create(name="Good Police Department", short_name="GPD", load_defaults=False)

    # create & append assaults chart blocks with the expected slugs
    assaults_intro = ChartBlock(title="INTRO", dataset="intros", slug="assaults-introduction", content="AAAAAAAAAAAAAA")
    assaults_bst = ChartBlock(title="BYSERVICETYPE", dataset="byservicetype", slug="assaults-by-service-type", content="AAAAAAAAAAAAAA")
    assaults_bft = ChartBlock(title="BYFORCETYPE", dataset="byforcetype", slug="assaults-by-force-type", content="AAAAAAAAAAAAAA")
    assaults_bof = ChartBlock(title="BYOFFICER", dataset="byofficer", slug="assaults-by-officer", content="AAAAAAAAAAAAAA")

    department.chart_blocks.append(assaults_intro)
    department.chart_blocks.append(assaults_bst)
    department.chart_blocks.append(assaults_bft)
    department.chart_blocks.append(assaults_bof)

    # create & append assaults chart blocks with the expected slugs
    complaint_intro = ChartBlock(title="INTRO", dataset="intros", slug="complaints-introduction", content="BBBBBBBBBBBBB")
    complaint_bm = ChartBlock(title="BYMONTH", dataset="bymonth", slug="complaints-by-month", content="BBBBBBBBBBBBB")
    complaint_bya = ChartBlock(title="BYALLEGATION", dataset="bya", slug="complaints-by-allegation", content="BBBBBBBBBBBBB")
    complaint_byat = ChartBlock(title="BYALLEGATIONTYPE", dataset="byat", slug="complaints-by-allegation-type", content="BBBBBBBBBBBBB")
    complaint_bdis = ChartBlock(title="BYDISPOSITION", dataset="bdis", slug="complaints-by-disposition", content="BBBBBBBBBBBBB")
    complaint_bpre = ChartBlock(title="BYPRECINCT", dataset="bpre", slug="complaints-by-precinct", content="BBBBBBBBBBBBB")
    complaint_od = ChartBlock(title="OFFICERDEMOS", dataset="od", slug="officer-demographics", content="BBBBBBBBBBBBB")
    complaint_bde = ChartBlock(title="BYDEMO", dataset="bde", slug="complaints-by-demographic", content="BBBBBBBBBBBBB")
    complaint_bof = ChartBlock(title="BYOFFICER", dataset="bof", slug="complaints-by-officer", content="BBBBBBBBBBBBB")

    department.chart_blocks.append(complaint_intro)
    department.chart_blocks.append(complaint_bm)
    department.chart_blocks.append(complaint_bya)
    department.chart_blocks.append(complaint_byat)
    department.chart_blocks.append(complaint_bdis)
    department.chart_blocks.append(complaint_bpre)
    department.chart_blocks.append(complaint_od)
    department.chart_blocks.append(complaint_bde)
    department.chart_blocks.append(complaint_bof)

    uof_intro = ChartBlock(title="INTRO", dataset="intros", slug="uof-introduction", content="CCCCCCCCCCCCCC")
    uof_ft = ChartBlock(title="FORCETYPE", dataset="forcetype", slug="uof-force-type", content="CCCCCCCCCCCCCC")
    uof_bid = ChartBlock(title="BYINCDISTRICT", dataset="bid", slug="uof-by-inc-district", content="CCCCCCCCCCCCCC")
    uof_od = ChartBlock(title="OFFICERDEMOS", dataset="od", slug="officer-demographics", content="CCCCCCCCCCCCCC")
    uof_race = ChartBlock(title="RACE", dataset="race", slug="uof-race", content="CCCCCCCCCCCCCC")

    department.chart_blocks.append(uof_intro)
    department.chart_blocks.append(uof_ft)
    department.chart_blocks.append(uof_bid)
    department.chart_blocks.append(uof_od)
    department.chart_blocks.append(uof_race)

    ois_intro = ChartBlock(title="INTRO", dataset="intros", slug="ois-introduction", content="DDDDDDDDDDDDDDD")
    ois_bid = ChartBlock(title="BYINCDISTRICT", dataset="bid", slug="ois-by-inc-district", content="DDDDDDDDDDDDDDD")
    ois_wt = ChartBlock(title="WEAPONTYPE", dataset="weapontype", slug="ois-weapon-type", content="DDDDDDDDDDDDDDD")
    ois_od = ChartBlock(title="OFFICERDEMOS", dataset="od", slug="officer-demographics", content="DDDDDDDDDDDDDDD")
    ois_race = ChartBlock(title="RACE", dataset="race", slug="ois-race", content="DDDDDDDDDDDDDDD")

    department.chart_blocks.append(ois_intro)
    department.chart_blocks.append(ois_bid)
    department.chart_blocks.append(ois_wt)
    department.chart_blocks.append(ois_od)
    department.chart_blocks.append(ois_race)

    department.save()
    return department, assaults_intro

def log_in_user(testapp, department):
    # set up a user
    user = User.create(username="user", email="user@example.com", password="password")
    user.departments.append(department)
    user.active = True
    user.save()
    # login
    response = testapp.get("/login/")
    form = response.forms['loginForm']
    form['username'] = user.username
    form['password'] = 'password'
    response = form.submit().follow()
    return user

@pytest.mark.usefixtures('db')
class TestConditionalAccess:

    def test_department_is_public_by_default(self):
        # create a department
        department = Department.create(name="Good Police Department", short_name="GPD", load_defaults=False)
        assert department.is_public

    def test_department_can_be_set_private(self):
        # create a department
        department = Department.create(name="Good Police Department", short_name="GPD", is_public=False, load_defaults=False)
        assert not department.is_public

    def test_department_not_logged_in_unauthorized(self, testapp, preconfigured_department):
        # set up department
        department, _ = preconfigured_department
        department.is_public = False

        # make requests to specific front pages
        testapp.get("/department/GPD/complaints/", status=403)
        testapp.get("/department/GPD/useofforce/", status=403)
        testapp.get("/department/GPD/officerinvolvedshootings/", status=403)
        testapp.get("/department/GPD/assaultsonofficers/", status=403)
        testapp.get("/department/GPD/schema/complaints/", status=403)
        testapp.get("/department/GPD/schema/useofforce/", status=403)
        testapp.get("/department/GPD/schema/officerinvolvedshootings/", status=403)
        testapp.get("/department/GPD/schema/assaultsonofficers/", status=403)
        testapp.get("/department/{}/complaints.csv".format(department.id), status=403)
        testapp.get("/department/{}/uof.csv".format(department.id), status=403)
        testapp.get("/department/{}/ois.csv".format(department.id), status=403)
        testapp.get("/department/{}/assaultsonofficers.csv".format(department.id), status=403)

    def test_department_logged_in_authorized(self, testapp, preconfigured_department):
        # set up department
        department, _ = preconfigured_department
        department.is_public = False

        # set up a user
        log_in_user(testapp, department)

        # make requests to specific front pages
        testapp.get("/department/GPD/complaints/", status=200)
        testapp.get("/department/GPD/useofforce/", status=200)
        testapp.get("/department/GPD/officerinvolvedshootings/", status=200)
        testapp.get("/department/GPD/assaultsonofficers/", status=200)
        testapp.get("/department/GPD/schema/complaints/", status=200)
        testapp.get("/department/GPD/schema/useofforce/", status=200)
        testapp.get("/department/GPD/schema/officerinvolvedshootings/", status=200)
        testapp.get("/department/GPD/schema/assaultsonofficers/", status=200)
        testapp.get("/department/{}/complaints.csv".format(department.id), status=200)
        testapp.get("/department/{}/uof.csv".format(department.id), status=200)
        testapp.get("/department/{}/ois.csv".format(department.id), status=200)
        testapp.get("/department/{}/assaultsonofficers.csv".format(department.id), status=200)

@pytest.mark.usefixtures('db')
class TestPagesRespond:

    def test_complaints_schema_preview_page_exists(self, testapp):
        # create a department
        department = Department.create(name="Spleen Police Department", short_name="SPD", load_defaults=False)

        # set up a user
        log_in_user(testapp, department)

        # make a resquest to specific front page
        response = testapp.get("/department/{}/preview/schema/complaints".format(department.id))

        assert response.status_code == 200

    def test_assaults_front_page_exists(self, testapp, preconfigured_department):
        # get a department and intro block from the fixture
        department, assaults_intro = preconfigured_department

        # make a resquest to specific front page
        response = testapp.get("/department/GPD/assaultsonofficers/")

        assaults_blocks = department.get_assaults_blocks()

        assert assaults_blocks['introduction'] == assaults_intro
        assert response.status_code == 200

    def test_assaults_schema_page_exists(self, testapp):
        # create a department
        Department.create(name="Spleen Police Department", short_name="SPD", load_defaults=False)

        # make a resquest to specific front page
        response = testapp.get("/department/SPD/schema/assaultsonofficers/")

        assert response.status_code == 200

    def test_assaults_schema_preview_page_exists(self, testapp):
        # create a department
        department = Department.create(name="Spleen Police Department", short_name="SPD", load_defaults=False)

        # set up a user
        log_in_user(testapp, department)

        # make a resquest to specific front page
        response = testapp.get("/department/{}/preview/schema/assaultsonofficers".format(department.id))

        assert response.status_code == 200

    def test_assaults_csv_endpoint_exists(self, testapp):
        # create a department
        department = Department.create(name="Spleen Police Department", short_name="SPD", load_defaults=False)

        # make a resquest to specific front page
        response = testapp.get("/department/{}/assaultsonofficers.csv".format(department.id))

        assert response.status_code == 200

    def test_csv_filtered_by_dept(self, testapp):
        # create a department
        department1 = Department.create(name="Spleen Police Department", short_name="SPD", load_defaults=False)
        department2 = Department.create(name="Random Police Department", short_name="RPD", load_defaults=False)

        UseOfForceIncident.create(opaque_id="123ABC", department_id=department1.id)
        UseOfForceIncident.create(opaque_id="123XYZ", department_id=department2.id)

        response1 = testapp.get("/department/{}/uof.csv".format(department1.id))
        response2 = testapp.get("/department/{}/uof.csv".format(department2.id))

        incidents1 = list(csv.DictReader(io.StringIO(response1.text)))
        incidents2 = list(csv.DictReader(io.StringIO(response2.text)))

        assert len(incidents1) == 1 and len(incidents2) == 1
        assert incidents1[0]['id'] == '123ABC' and incidents2[0]['id'] == '123XYZ'

    def test_assaults_edit_page_exists(self, testapp, preconfigured_department):
        # get a department from the fixture
        department, _ = preconfigured_department

        # set up a user
        log_in_user(testapp, department)

        # make a resquest to specific front page
        response = testapp.get("/department/{}/edit/assaultsonofficers".format(department.id))

        assert response.status_code == 200

    def test_assaults_preview_page_exists(self, testapp, preconfigured_department):
        # get a department from the fixture
        department, _ = preconfigured_department

        # set up a user
        log_in_user(testapp, department)

        # make a request to the assaults preview page
        response = testapp.get("/department/{}/preview/assaultsonofficers".format(department.id))
        assert response.status_code == 200


class TestLoggingIn:

    def test_can_log_in_returns_200(self, user, testapp):
        # Goes to homepage
        res = testapp.get("/login/")
        # Fills out login form in navbar
        form = res.forms['loginForm']
        form['username'] = user.username
        form['password'] = 'myprecious'
        # Submits
        res = form.submit().follow()
        assert res.status_code == 200

    def test_sees_alert_on_log_out(self, user, testapp):
        res = testapp.get("/login/")
        # Fills out login form in navbar
        form = res.forms['loginForm']
        form['username'] = user.username
        form['password'] = 'myprecious'
        # Submits
        res = form.submit().follow()
        res = testapp.get(url_for('public.logout')).follow()
        # sees alert
        assert 'You are logged out.' in res

    def test_sees_error_message_if_password_is_incorrect(self, user, testapp):
        # Goes to homepage
        res = testapp.get("/login/")
        # Fills out login form, password incorrect
        form = res.forms['loginForm']
        form['username'] = user.username
        form['password'] = 'wrong'
        # Submits
        res = form.submit()
        # sees error
        assert "Invalid password" in res

    def test_sees_error_message_if_username_doesnt_exist(self, user, testapp):
        # Goes to homepage
        res = testapp.get("/login/")
        # Fills out login form, password incorrect
        form = res.forms['loginForm']
        form['username'] = 'unknown'
        form['password'] = 'myprecious'
        # Submits
        res = form.submit()
        # sees error
        assert "Unknown user" in res


class TestUserRoles:

    def test_access(self, user, testapp):
        admin_role = Role.create(name="admin")
        user.roles.append(admin_role)
        user.save()
        TestLoggingIn.test_can_log_in_returns_200(self, user=user, testapp=testapp)
        res = testapp.get("/admin").follow()

        assert res.status_code == 200
        assert "Admin Dashboard" in res

    def test_department_access(self, user, testapp):
        department = Department.create(name="Busy Town Public Safety", short_name="BTPD", load_defaults=False)
        user.departments.append(department)
        user.save()
        TestLoggingIn.test_can_log_in_returns_200(self, user=user, testapp=testapp)
        res = testapp.get("/department/6").follow()

        assert res.status_code == 200
        assert "You do not have sufficient permissions to do that" in res


class TestRegistering:

    def test_can_register(self, user, testapp):
        ''' A new user can register.
        '''
        # The new user's credentials
        test_username = 'cato'
        test_email = 'cato@example.com'
        test_password = 'pistol_and_ball'
        test_invite_code = 'coffin_warehouses'

        # create a department and an invite code
        department = Department.create(name="Spleen Police Department", short_name="SPD", load_defaults=False)
        Invite_Code.create(department_id=department.id, code=test_invite_code)

        # establish that the user doesn't exist yet
        old_user_count = len(User.query.all())
        assert len(department.users) == 0
        assert User.query.filter_by(username=test_username).first() is None

        # Goes to register page
        response = testapp.get("/register/")
        # Fills out the form
        form = response.forms["registerForm"]
        form['username'] = test_username
        form['email'] = test_email
        form['password'] = test_password
        form['confirm'] = test_password
        form['invite_code'] = test_invite_code
        # Submits
        response = form.submit().follow()
        assert response.status_code == 200

        # The new user was created
        assert len(User.query.all()) == old_user_count + 1
        assert len(department.users) == 1
        check_user = User.query.filter_by(username=test_username).first()
        assert check_user is not None
        assert check_user.email == test_email
        assert check_user.check_password(test_password) is True
