# -*- coding: utf-8 -*-
import pytest
from urllib.parse import urlparse
from comport.admin.forms import NewDepartmentForm
from comport.department.models import Department, Extractor, User
from comport.content.models import ChartBlock
from .utils import log_in_user

@pytest.mark.usefixtures('app')
class TestNewDepartmentForm:

    def test_validate_success(self, db):
        ''' The form validates when properly filled out.
        '''
        form = NewDepartmentForm(department_name="Any Police Department", department_short_name="APD")
        assert form.validate() is True

    def test_department_name_required(self):
        ''' The form requires a non-None department name.
        '''
        form = NewDepartmentForm(department_name=None, department_short_name="APD")
        assert form.validate() is False
        assert 'This field is required.' in form.department_name.errors

    def test_department_short_name_required(self):
        ''' The form requires a non-None department short name.
        '''
        form = NewDepartmentForm(department_name="Any Police Department", department_short_name=None)
        assert form.validate() is False
        assert 'This field is required.' in form.department_short_name.errors

    def test_department_name_unique_required(self, db):
        ''' The form won't allow creation of a duplicate department name.
        '''
        test_name = "Any Police Department"
        test_short_name = "APD"
        Department.create(name=test_name, short_name=test_short_name)
        form = NewDepartmentForm(department_name=test_name, department_short_name=test_short_name)
        assert form.validate() is False
        assert 'The department name "{}" is already registered.'.format(test_name) in form.department_name.errors

    def test_department_short_name_unique_required(self, db):
        ''' The form won't allow creation of a duplicate department short name.
        '''
        test_name = "Any Police Department"
        test_short_name = "APD"
        Department.create(name=test_name, short_name=test_short_name)
        form = NewDepartmentForm(department_name="Another Police Department", department_short_name=test_short_name)
        assert form.validate() is False
        assert 'The department short name "{}" is already registered.'.format(test_short_name) in form.department_short_name.errors


@pytest.mark.usefixtures('app')
class TestStartExtractorForm:

    def test_can_set_extractor_start_date(self, testapp):
        ''' Can set an extraction start date.
        '''
        # set up the department
        department = Department.create(name="Good Police Department", short_name="GPD", load_defaults=False)

        # set up a user
        user = User.create(username="moby", email="moby@example.com", password="password")
        user.departments.append(department)
        user.active = True
        user.save()
        # login
        response = testapp.get("/login/")
        form = response.forms['loginForm']
        form['username'] = user.username
        form['password'] = 'password'
        response = form.submit().follow()

        # create an extractor account
        extractor_password = "password"
        extractor, _ = Extractor.from_department_and_password(department=department, password=extractor_password)

        # submit the extractor start date form
        response = testapp.get("/department/{}".format(department.id))
        form = response.forms["extractionStartForm"]
        submit_month = 10
        submit_year = 2006
        form['month'] = str(submit_month)
        form['year'] = str(submit_year)
        response = form.submit('submit').follow()

        # the new date was set
        assert extractor.next_month == submit_month
        assert extractor.next_year == submit_year

@pytest.mark.usefixtures('db')
class TestAdminEditForms:

    def test_ois_schema_edit_forms_exist(self, preconfigured_department, testapp):
        ''' Edit forms exist for the complaints schema page.
        '''
        department, _ = preconfigured_department

        # set up a user
        log_in_user(testapp, department)

        # make a request to specific front page
        response = testapp.get("/department/{}/edit/schema/ois".format(department.id))
        assert response.status_code == 200

        # assert that the intro, footer, disclaimer forms are there
        assert 'editIntro' in response.forms
        assert 'editFooter' in response.forms
        assert 'editDisclaimer' in response.forms

        # assert that the field forms are there (as defined in conftest.py)
        assert 'editIdTitleAndContent' in response.forms
        assert 'editOccuredDateTitleAndContent' in response.forms
        assert 'editDivisionTitleAndContent' in response.forms
        assert 'editDistrictTitleAndContent' in response.forms
        assert 'editShiftTitleAndContent' in response.forms

    def test_useofforce_schema_edit_forms_exist(self, preconfigured_department, testapp):
        ''' Edit forms exist for the complaints schema page.
        '''
        department, _ = preconfigured_department

        # set up a user
        log_in_user(testapp, department)

        # make a request to specific front page
        response = testapp.get("/department/{}/edit/schema/useofforce".format(department.id))
        assert response.status_code == 200

        # assert that the intro, footer, disclaimer forms are there
        assert 'editIntro' in response.forms
        assert 'editFooter' in response.forms
        assert 'editDisclaimer' in response.forms

        # assert that the field forms are there (as defined in conftest.py)
        assert 'editIdTitleAndContent' in response.forms
        assert 'editOccuredDateTitleAndContent' in response.forms
        assert 'editDivisionTitleAndContent' in response.forms
        assert 'editDistrictTitleAndContent' in response.forms
        assert 'editShiftTitleAndContent' in response.forms

    def test_assaults_schema_edit_forms_exist(self, preconfigured_department, testapp):
        ''' Edit forms exist for the complaints schema page.
        '''
        department, _ = preconfigured_department

        # set up a user
        log_in_user(testapp, department)

        # make a request to specific front page
        response = testapp.get("/department/{}/edit/schema/assaultsonofficers".format(department.id))
        assert response.status_code == 200

        # assert that the intro, footer, disclaimer forms are there
        assert 'editIntro' in response.forms
        assert 'editFooter' in response.forms
        assert 'editDisclaimer' in response.forms

        # assert that the field forms are there (as defined in conftest.py)
        assert 'editIdTitleAndContent' in response.forms
        assert 'editOccuredDateTitleAndContent' in response.forms
        assert 'editDivisionTitleAndContent' in response.forms
        assert 'editDistrictTitleAndContent' in response.forms
        assert 'editShiftTitleAndContent' in response.forms

    def test_complaints_schema_edit_forms_exist(self, preconfigured_department, testapp):
        ''' Edit forms exist for the complaints schema page.
        '''
        department, _ = preconfigured_department

        # set up a user
        log_in_user(testapp, department)

        # make a request to specific front page
        response = testapp.get("/department/{}/edit/schema/complaints".format(department.id))
        assert response.status_code == 200

        # assert that the intro, footer, disclaimer forms are there
        assert 'editIntro' in response.forms
        assert 'editFooter' in response.forms
        assert 'editDisclaimer' in response.forms

        # assert that the field forms are there (as defined in conftest.py)
        assert 'editIdTitleAndContent' in response.forms
        assert 'editOccuredDateTitleAndContent' in response.forms
        assert 'editDivisionTitleAndContent' in response.forms
        assert 'editDistrictTitleAndContent' in response.forms
        assert 'editShiftTitleAndContent' in response.forms

    def test_editing_complaints_schema_field_value(self, preconfigured_department, testapp):
        ''' Submitting the form to edit a schema field changes the correct value in the database
        '''
        department, _ = preconfigured_department

        # set up a user
        log_in_user(testapp, department)

        # make a request to specific front page
        response = testapp.get("/department/{}/edit/schema/complaints".format(department.id))
        assert response.status_code == 200

        assert 'editShiftTitleAndContent' in response.forms
        form = response.forms['editShiftTitleAndContent']
        new_title = "A New Data Field Title"
        new_content = "A Short Definition of this Data Field"
        form['chart_title'] = new_title
        form['chart_content'] = new_content
        response = form.submit().follow()
        assert response.status_code == 200

        checkblock = ChartBlock.query.filter_by(slug="complaints-schema-field-shift").first()
        assert checkblock.title == new_title
        assert checkblock.content == new_content

    def test_editing_assaults_schema_field_value(self, preconfigured_department, testapp):
        ''' Submitting the form to edit a schema field changes the correct value in the database
        '''
        department, _ = preconfigured_department

        # set up a user
        log_in_user(testapp, department)

        # make a request to specific front page
        response = testapp.get("/department/{}/edit/schema/assaultsonofficers".format(department.id))
        assert response.status_code == 200

        assert 'editShiftTitleAndContent' in response.forms
        form = response.forms['editShiftTitleAndContent']
        new_title = "A New Data Field Title"
        new_content = "A Short Definition of this Data Field"
        form['chart_title'] = new_title
        form['chart_content'] = new_content
        response = form.submit().follow()
        assert response.status_code == 200

        checkblock = ChartBlock.query.filter_by(slug="assaults-schema-field-shift").first()
        assert checkblock.title == new_title
        assert checkblock.content == new_content

    def test_editing_ois_schema_field_value(self, preconfigured_department, testapp):
        ''' Submitting the form to edit a schema field changes the correct value in the database
        '''
        department, _ = preconfigured_department

        # set up a user
        log_in_user(testapp, department)

        # make a request to specific front page
        response = testapp.get("/department/{}/edit/schema/ois".format(department.id))
        assert response.status_code == 200

        assert 'editShiftTitleAndContent' in response.forms
        form = response.forms['editShiftTitleAndContent']
        new_title = "A New Data Field Title"
        new_content = "A Short Definition of this Data Field"
        form['chart_title'] = new_title
        form['chart_content'] = new_content
        response = form.submit().follow()
        assert response.status_code == 200

        checkblock = ChartBlock.query.filter_by(slug="ois-schema-field-shift").first()
        assert checkblock.title == new_title
        assert checkblock.content == new_content

    def test_editing_useofforce_schema_field_value(self, preconfigured_department, testapp):
        ''' Submitting the form to edit a schema field changes the correct value in the database
        '''
        department, _ = preconfigured_department

        # set up a user
        log_in_user(testapp, department)

        # make a request to specific front page
        response = testapp.get("/department/{}/edit/schema/useofforce".format(department.id))
        assert response.status_code == 200

        assert 'editShiftTitleAndContent' in response.forms
        form = response.forms['editShiftTitleAndContent']
        new_title = "A New Data Field Title"
        new_content = "A Short Definition of this Data Field"
        form['chart_title'] = new_title
        form['chart_content'] = new_content
        response = form.submit().follow()
        assert response.status_code == 200

        checkblock = ChartBlock.query.filter_by(slug="useofforce-schema-field-shift").first()
        assert checkblock.title == new_title
        assert checkblock.content == new_content

    def test_submitting_schema_edit_form_redirects_to_preview(self, preconfigured_department, testapp):
        ''' Submitting the form to edit a schema field changes the correct value in the database
        '''
        department, _ = preconfigured_department

        # set up a user
        log_in_user(testapp, department)

        # make a request to specific front page
        response = testapp.get("/department/{}/edit/schema/complaints".format(department.id))
        assert response.status_code == 200

        # submit new title & content
        assert 'editShiftTitleAndContent' in response.forms
        form = response.forms['editShiftTitleAndContent']
        new_title = "A New Data Field Title"
        new_content = "A Short Definition of this Data Field"
        form['chart_title'] = new_title
        form['chart_content'] = new_content
        response = form.submit()

        # the response should be a redirect
        assert response.status_code == 302
        # the location of the redirect should be the preview page
        parsed = urlparse(response.location)
        assert parsed.path == "/department/{}/preview/schema/complaints".format(department.id)
