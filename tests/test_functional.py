# -*- coding: utf-8 -*-
"""Functional tests using WebTest.

See: http://webtest.readthedocs.org/
"""
import io
import csv
import pytest
from flask import url_for
from comport.user.models import User, Role, Invite_Code
from comport.department.models import Department
from comport.data.models import UseOfForceIncidentIMPD
from .utils import log_in_user

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

    def test_department_not_logged_in_unauthorized(self, testapp):
        # set up department
        department = Department.create(name="Bad Police Department", short_name="BPD", load_defaults=True)
        department.is_public = False

        # make requests to specific front pages
        testapp.get("/department/{}/complaints/".format(department.short_name), status=403)
        testapp.get("/department/{}/useofforce/".format(department.short_name), status=403)
        testapp.get("/department/{}/officerinvolvedshootings/".format(department.short_name), status=403)
        testapp.get("/department/{}/assaultsonofficers/".format(department.short_name), status=403)
        testapp.get("/department/{}/schema/complaints/".format(department.short_name), status=403)
        testapp.get("/department/{}/schema/useofforce/".format(department.short_name), status=403)
        testapp.get("/department/{}/schema/officerinvolvedshootings/".format(department.short_name), status=403)
        testapp.get("/department/{}/schema/assaultsonofficers/".format(department.short_name), status=403)
        testapp.get("/department/{}/complaints.csv".format(department.id), status=403)
        testapp.get("/department/{}/uof.csv".format(department.id), status=403)
        testapp.get("/department/{}/ois.csv".format(department.id), status=403)
        testapp.get("/department/{}/assaultsonofficers.csv".format(department.id), status=403)
        testapp.get("/department/{}/officerCalls.csv".format(department.id), status=403)
        testapp.get("/department/{}/demographics.csv".format(department.id), status=403)

    def test_department_logged_in_authorized(self, testapp):
        # set up department
        department = Department.create(name="Bad Police Department", short_name="BPD", load_defaults=True)
        department.is_public = False

        # set up a user
        log_in_user(testapp, department)

        # make requests to specific front pages
        testapp.get("/department/{}/complaints/".format(department.short_name), status=200)
        testapp.get("/department/{}/useofforce/".format(department.short_name), status=200)
        testapp.get("/department/{}/officerinvolvedshootings/".format(department.short_name), status=200)
        testapp.get("/department/{}/assaultsonofficers/".format(department.short_name), status=200)
        testapp.get("/department/{}/schema/complaints/".format(department.short_name), status=200)
        testapp.get("/department/{}/schema/useofforce/".format(department.short_name), status=200)
        testapp.get("/department/{}/schema/officerinvolvedshootings/".format(department.short_name), status=200)
        testapp.get("/department/{}/schema/assaultsonofficers/".format(department.short_name), status=200)
        testapp.get("/department/{}/complaints.csv".format(department.id), status=200)
        testapp.get("/department/{}/uof.csv".format(department.id), status=200)
        testapp.get("/department/{}/ois.csv".format(department.id), status=200)
        testapp.get("/department/{}/assaultsonofficers.csv".format(department.id), status=200)
        testapp.get("/department/{}/officerCalls.csv".format(department.id), status=200)
        testapp.get("/department/{}/demographics.csv".format(department.id), status=200)

    def test_datset_is_public_by_default(self):
        # create a department
        department = Department.create(name="Good Police Department", short_name="GPD", load_defaults=False)
        assert hasattr(department, "is_public_assaults_on_officers")
        assert hasattr(department, "is_public_officer_involved_shootings")
        assert hasattr(department, "is_public_citizen_complaints")
        assert hasattr(department, "is_public_use_of_force_incidents")
        assert department.is_public_assaults_on_officers is True
        assert department.is_public_officer_involved_shootings is True
        assert department.is_public_citizen_complaints is True
        assert department.is_public_use_of_force_incidents is True

    def test_dataset_can_be_set_private(self):
        # create a department
        department = Department.create(name="Good Police Department", short_name="GPD", load_defaults=False)
        assert hasattr(department, "is_public_assaults_on_officers")
        assert hasattr(department, "is_public_officer_involved_shootings")
        assert hasattr(department, "is_public_citizen_complaints")
        assert hasattr(department, "is_public_use_of_force_incidents")
        department.is_public_assaults_on_officers = False
        department.is_public_officer_involved_shootings = False
        department.is_public_citizen_complaints = False
        department.is_public_use_of_force_incidents = False
        department.save()
        assert department.is_public_assaults_on_officers is False
        assert department.is_public_officer_involved_shootings is False
        assert department.is_public_citizen_complaints is False
        assert department.is_public_use_of_force_incidents is False

    def test_visit_private_dataset_throws_unauth(self, testapp):
        # create a department
        department = Department.create(name="Bad Police Department", short_name="BPD", load_defaults=True)

        # we can access all the datasets except assaults
        testapp.get("/department/{}/complaints/".format(department.short_name), status=200)
        testapp.get("/department/{}/schema/complaints/".format(department.short_name), status=200)
        testapp.get("/department/{}/complaints.csv".format(department.id), status=200)

        testapp.get("/department/{}/useofforce/".format(department.short_name), status=200)
        testapp.get("/department/{}/schema/useofforce/".format(department.short_name), status=200)
        testapp.get("/department/{}/uof.csv".format(department.id), status=200)

        testapp.get("/department/{}/officerinvolvedshootings/".format(department.short_name), status=200)
        testapp.get("/department/{}/schema/officerinvolvedshootings/".format(department.short_name), status=200)
        testapp.get("/department/{}/ois.csv".format(department.id), status=200)

        testapp.get("/department/{}/assaultsonofficers/".format(department.short_name), status=200)
        testapp.get("/department/{}/schema/assaultsonofficers/".format(department.short_name), status=200)
        testapp.get("/department/{}/assaultsonofficers.csv".format(department.id), status=200)

        # set each dataset is_public to false, and verify that they're no longer accessible

        department.is_public_citizen_complaints = False

        testapp.get("/department/{}/complaints/".format(department.short_name), status=403)
        testapp.get("/department/{}/schema/complaints/".format(department.short_name), status=403)
        testapp.get("/department/{}/complaints.csv".format(department.id), status=403)

        department.is_public_use_of_force_incidents = False

        testapp.get("/department/{}/useofforce/".format(department.short_name), status=403)
        testapp.get("/department/{}/schema/useofforce/".format(department.short_name), status=403)
        testapp.get("/department/{}/uof.csv".format(department.id), status=403)

        department.is_public_officer_involved_shootings = False

        testapp.get("/department/{}/officerinvolvedshootings/".format(department.short_name), status=403)
        testapp.get("/department/{}/schema/officerinvolvedshootings/".format(department.short_name), status=403)
        testapp.get("/department/{}/ois.csv".format(department.id), status=403)

        department.is_public_assaults_on_officers = False

        testapp.get("/department/{}/assaultsonofficers/".format(department.short_name), status=403)
        testapp.get("/department/{}/schema/assaultsonofficers/".format(department.short_name), status=403)
        testapp.get("/department/{}/assaultsonofficers.csv".format(department.id), status=403)

        # log in, try again, and they should all be accessible again
        log_in_user(testapp, department)

        testapp.get("/department/{}/complaints/".format(department.short_name), status=200)
        testapp.get("/department/{}/schema/complaints/".format(department.short_name), status=200)
        testapp.get("/department/{}/complaints.csv".format(department.id), status=200)

        testapp.get("/department/{}/useofforce/".format(department.short_name), status=200)
        testapp.get("/department/{}/schema/useofforce/".format(department.short_name), status=200)
        testapp.get("/department/{}/uof.csv".format(department.id), status=200)

        testapp.get("/department/{}/officerinvolvedshootings/".format(department.short_name), status=200)
        testapp.get("/department/{}/schema/officerinvolvedshootings/".format(department.short_name), status=200)
        testapp.get("/department/{}/ois.csv".format(department.id), status=200)

        testapp.get("/department/{}/assaultsonofficers/".format(department.short_name), status=200)
        testapp.get("/department/{}/schema/assaultsonofficers/".format(department.short_name), status=200)
        testapp.get("/department/{}/assaultsonofficers.csv".format(department.id), status=200)

    def test_only_department_user_can_access_non_public_datasets(self, testapp):
        # create a department
        department = Department.create(name="Good Police Department", short_name="GPD", load_defaults=True)
        department.is_public_citizen_complaints = False
        department.is_public_use_of_force_incidents = False
        department.is_public_officer_involved_shootings = False
        department.is_public_assaults_on_officers = False

        # log in under a different department, datasets should not be accessible
        bad_department = Department.create(name="Bad Police Department", short_name="BPD", load_defaults=False)
        log_in_user(testapp, bad_department)

        testapp.get("/department/{}/complaints/".format(department.short_name), status=403)
        testapp.get("/department/{}/schema/complaints/".format(department.short_name), status=403)
        testapp.get("/department/{}/complaints.csv".format(department.id), status=403)

        testapp.get("/department/{}/useofforce/".format(department.short_name), status=403)
        testapp.get("/department/{}/schema/useofforce/".format(department.short_name), status=403)
        testapp.get("/department/{}/uof.csv".format(department.id), status=403)

        testapp.get("/department/{}/officerinvolvedshootings/".format(department.short_name), status=403)
        testapp.get("/department/{}/schema/officerinvolvedshootings/".format(department.short_name), status=403)
        testapp.get("/department/{}/ois.csv".format(department.id), status=403)

        testapp.get("/department/{}/assaultsonofficers/".format(department.short_name), status=403)
        testapp.get("/department/{}/schema/assaultsonofficers/".format(department.short_name), status=403)
        testapp.get("/department/{}/assaultsonofficers.csv".format(department.id), status=403)

@pytest.mark.usefixtures('db')
class TestPagesRespond:

    def test_complaints_schema_edit_page_exists(self, testapp):
        # create a department
        department = Department.create(name="Bad Police Department", short_name="BPD", load_defaults=True)

        # set up a user
        log_in_user(testapp, department)

        # make a request to specific front page
        response = testapp.get("/department/{}/edit/schema/complaints".format(department.id))

        assert response.status_code == 200

    def test_assaults_schema_edit_page_exists(self, testapp):
        # create a department
        department = Department.create(name="Bad Police Department", short_name="BPD", load_defaults=True)

        # set up a user
        log_in_user(testapp, department)

        # make a request to specific front page
        response = testapp.get("/department/{}/edit/schema/assaultsonofficers".format(department.id))

        assert response.status_code == 200

    def test_ois_schema_edit_page_exists(self, testapp):
        # create a department
        department = Department.create(name="Spleen Police Department", short_name="SPD", load_defaults=True)

        # set up a user
        log_in_user(testapp, department)

        # make a request to specific front page
        response = testapp.get("/department/{}/edit/schema/ois".format(department.id))

        assert response.status_code == 200

    def test_useofforce_schema_edit_page_exists(self, testapp):
        # create a department
        department = Department.create(name="Bad Police Department", short_name="BPD", load_defaults=True)

        # set up a user
        log_in_user(testapp, department)

        # make a request to specific front page
        response = testapp.get("/department/{}/edit/schema/useofforce".format(department.id))

        assert response.status_code == 200

    def test_complaints_schema_preview_page_exists(self, testapp):
        # create a department
        department = Department.create(name="Bad Police Department", short_name="BPD", load_defaults=True)

        # set up a user
        log_in_user(testapp, department)

        # make a request to specific front page
        response = testapp.get("/department/{}/preview/schema/complaints".format(department.id))

        assert response.status_code == 200

    def test_useofforce_schema_preview_page_exists(self, testapp):
        # create a department
        department = Department.create(name="Bad Police Department", short_name="BPD", load_defaults=True)

        # set up a user
        log_in_user(testapp, department)

        # make a request to specific front page
        response = testapp.get("/department/{}/preview/schema/useofforce".format(department.id))

        assert response.status_code == 200

    def test_ois_schema_preview_page_exists(self, testapp):
        # create a department
        department = Department.create(name="Bad Police Department", short_name="BPD", load_defaults=True)

        # set up a user
        log_in_user(testapp, department)

        # make a request to specific front page
        response = testapp.get("/department/{}/preview/schema/ois".format(department.id))

        assert response.status_code == 200

    def test_loading_unconfigured_data_type_redirects_to_index(self, testapp):
        # create a department
        department = Department.create(name="Good Police Department", short_name="GPD", load_defaults=False)

        # make a request to a non-public front page
        redirect_response = testapp.get("/department/{}/assaultsonofficers/".format(department.short_name), status=500)
        assert redirect_response.status_code == 500

    def test_assaults_front_page_exists(self, testapp):
        # get a department and intro block from the fixture
        department = Department.create(name="Good Police Department", short_name="GPD", load_defaults=True)

        # make a request to specific front page
        response = testapp.get("/department/{}/assaultsonofficers/".format(department.short_name))

        assert response.status_code == 200

    def test_assaults_schema_page_exists(self, testapp):
        # get a department from the fixture
        department = Department.create(name="Bad Police Department", short_name="BPD", load_defaults=True)

        # make a request to specific front page
        response = testapp.get("/department/{}/schema/assaultsonofficers/".format(department.short_name))

        assert response.status_code == 200

    def test_assaults_schema_preview_page_exists(self, testapp):
        # get a department from the fixture
        department = Department.create(name="Bad Police Department", short_name="BPD", load_defaults=True)

        # set up a user
        log_in_user(testapp, department)

        # make a request to specific front page
        response = testapp.get("/department/{}/preview/schema/assaultsonofficers".format(department.id))

        assert response.status_code == 200

    def test_demographics_csv_endpoint_exists(self, testapp):
        # create a department
        department = Department.create(name="Spleen Police Department", short_name="SPD", load_defaults=False)

        # make a request to specific front page
        response = testapp.get("/department/{}/demographics.csv".format(department.id))

        assert response.status_code == 200

    def test_officer_calls_csv_endpoint_exists(self, testapp):
        # create a department
        department = Department.create(name="Spleen Police Department", short_name="SPD", load_defaults=False)

        # make a request to specific front page
        response = testapp.get("/department/{}/officerCalls.csv".format(department.id))

        assert response.status_code == 200

    def test_assaults_csv_endpoint_exists(self, testapp):
        # create a department
        department = Department.create(name="Spleen Police Department", short_name="SPD", load_defaults=False)

        # make a request to specific front page
        response = testapp.get("/department/{}/assaultsonofficers.csv".format(department.id))

        assert response.status_code == 200

    def test_csv_filtered_by_dept(self, testapp):
        # create a department
        department1 = Department.create(name="Spleen Police Department", short_name="SPD", load_defaults=False)
        department2 = Department.create(name="Random Police Department", short_name="RPD", load_defaults=False)

        UseOfForceIncidentIMPD.create(opaque_id="123ABC", department_id=department1.id)
        UseOfForceIncidentIMPD.create(opaque_id="123XYZ", department_id=department2.id)

        response1 = testapp.get("/department/{}/uof.csv".format(department1.id))
        response2 = testapp.get("/department/{}/uof.csv".format(department2.id))

        incidents1 = list(csv.DictReader(io.StringIO(response1.text)))
        incidents2 = list(csv.DictReader(io.StringIO(response2.text)))

        assert len(incidents1) == 1 and len(incidents2) == 1
        assert incidents1[0]['id'] == '123ABC' and incidents2[0]['id'] == '123XYZ'

    def test_assaults_edit_page_exists(self, testapp):
        # get a department from the fixture
        department = Department.create(name="Bad Police Department", short_name="BPD", load_defaults=True)

        # set up a user
        log_in_user(testapp, department)

        # make a request to specific front page
        response = testapp.get("/department/{}/edit/assaultsonofficers".format(department.id))

        assert response.status_code == 200

    def test_assaults_preview_page_exists(self, testapp):
        # get a department from the fixture
        department = Department.create(name="Bad Police Department", short_name="BPD", load_defaults=True)

        # set up a user
        log_in_user(testapp, department)

        # make a request to the assaults preview page
        response = testapp.get("/department/{}/preview/assaultsonofficers".format(department.id))
        assert response.status_code == 200


@pytest.mark.usefixtures('db')
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

    def test_sees_error_message_if_username_doesnt_exist(self, testapp):
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


@pytest.mark.usefixtures('db')
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


@pytest.mark.usefixtures('db')
class TestRegistering:

    def test_can_register(self, testapp):
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
