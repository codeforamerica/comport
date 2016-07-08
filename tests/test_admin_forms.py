# -*- coding: utf-8 -*-
import pytest
from urllib.parse import urlparse
from comport.admin.forms import NewDepartmentForm
from comport.department.models import Department, Extractor, User
from comport.content.models import ChartBlock
from .utils import log_in_user
from bs4 import BeautifulSoup

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

    def test_edit_and_preview_links_on_department_admin_page(sefl, testapp):
        ''' There are links to preview & edit main and schema pages from the department admin page.
        '''
        department = Department.create(name="Bad Police Department", short_name="BPD", load_defaults=True)

        # set up a user
        log_in_user(testapp, department)

        # make a request to specific front page
        response = testapp.get("/department/{}".format(department.id))
        assert response.status_code == 200
        soup = BeautifulSoup(response.text)
        assert soup.find("a", href="{}/preview/useofforce".format(department.id)) is not None
        assert soup.find("a", href="{}/preview/complaints".format(department.id)) is not None
        assert soup.find("a", href="{}/preview/ois".format(department.id)) is not None
        assert soup.find("a", href="{}/preview/assaultsonofficers".format(department.id)) is not None
        assert soup.find("a", href="{}/edit/useofforce".format(department.id)) is not None
        assert soup.find("a", href="{}/edit/complaints".format(department.id)) is not None
        assert soup.find("a", href="{}/edit/ois".format(department.id)) is not None
        assert soup.find("a", href="{}/edit/assaultsonofficers".format(department.id)) is not None
        assert soup.find("a", href="{}/preview/schema/useofforce".format(department.id)) is not None
        assert soup.find("a", href="{}/preview/schema/complaints".format(department.id)) is not None
        assert soup.find("a", href="{}/preview/schema/ois".format(department.id)) is not None
        assert soup.find("a", href="{}/preview/schema/assaultsonofficers".format(department.id)) is not None
        assert soup.find("a", href="{}/edit/schema/useofforce".format(department.id)) is not None
        assert soup.find("a", href="{}/edit/schema/complaints".format(department.id)) is not None
        assert soup.find("a", href="{}/edit/schema/ois".format(department.id)) is not None
        assert soup.find("a", href="{}/edit/schema/assaultsonofficers".format(department.id)) is not None

    def test_ois_schema_edit_forms_exist(self, testapp):
        ''' Edit forms exist for the complaints schema page.
        '''
        department = Department.create(name="Bad Police Department", short_name="BPD", load_defaults=True)

        # set up a user
        log_in_user(testapp, department)

        # make a request to specific front page
        response = testapp.get("/department/{}/edit/schema/ois".format(department.id))
        assert response.status_code == 200

        # assert that the intro, footer, disclaimer forms are there
        assert 'editIntro' in response.forms
        assert 'editFooter' in response.forms
        assert 'editDisclaimer' in response.forms

        # assert that the field forms are there
        assert 'editIdTitleContentAndOrder' in response.forms
        assert 'editOccurredDateTitleContentAndOrder' in response.forms
        assert 'editDivisionTitleContentAndOrder' in response.forms
        assert 'editDistrictTitleContentAndOrder' in response.forms
        assert 'editShiftTitleContentAndOrder' in response.forms

    def test_useofforce_schema_edit_forms_exist(self, testapp):
        ''' Edit forms exist for the complaints schema page.
        '''
        department = Department.create(name="Bad Police Department", short_name="BPD", load_defaults=True)

        # set up a user
        log_in_user(testapp, department)

        # make a request to specific front page
        response = testapp.get("/department/{}/edit/schema/useofforce".format(department.id))
        assert response.status_code == 200

        # assert that the intro, footer, disclaimer forms are there
        assert 'editIntro' in response.forms
        assert 'editFooter' in response.forms
        assert 'editDisclaimer' in response.forms

        # assert that the field forms are there
        assert 'editIdTitleContentAndOrder' in response.forms
        assert 'editOccurredDateTitleContentAndOrder' in response.forms
        assert 'editDivisionTitleContentAndOrder' in response.forms
        assert 'editDistrictTitleContentAndOrder' in response.forms
        assert 'editShiftTitleContentAndOrder' in response.forms
        assert 'editBeatTitleContentAndOrder' in response.forms
        assert 'editUseOfForceReasonTitleContentAndOrder' in response.forms
        assert 'editOfficerForceTypeTitleContentAndOrder' in response.forms
        assert 'editDispositionTitleContentAndOrder' in response.forms
        assert 'editServiceTypeTitleContentAndOrder' in response.forms
        assert 'editArrestMadeTitleContentAndOrder' in response.forms
        assert 'editArrestChargesTitleContentAndOrder' in response.forms
        assert 'editResidentInjuredTitleContentAndOrder' in response.forms
        assert 'editResidentHospitalizedTitleContentAndOrder' in response.forms
        assert 'editResidentConditionTitleContentAndOrder' in response.forms
        assert 'editOfficerInjuredTitleContentAndOrder' in response.forms
        assert 'editOfficerHospitalizedTitleContentAndOrder' in response.forms
        assert 'editOfficerConditionTitleContentAndOrder' in response.forms
        assert 'editResidentRaceTitleContentAndOrder' in response.forms
        assert 'editResidentSexTitleContentAndOrder' in response.forms
        assert 'editResidentAgeTitleContentAndOrder' in response.forms
        assert 'editOfficerRaceTitleContentAndOrder' in response.forms
        assert 'editOfficerSexTitleContentAndOrder' in response.forms
        assert 'editOfficerAgeTitleContentAndOrder' in response.forms
        assert 'editOfficerYearsOfServiceTitleContentAndOrder' in response.forms
        assert 'editOfficerIdentifierTitleContentAndOrder' in response.forms

    def test_assaults_schema_edit_forms_exist(self, testapp):
        ''' Edit forms exist for the complaints schema page.
        '''
        department = Department.create(name="Bad Police Department", short_name="BPD", load_defaults=True)

        # set up a user
        log_in_user(testapp, department)

        # make a request to specific front page
        response = testapp.get("/department/{}/edit/schema/assaultsonofficers".format(department.id))
        assert response.status_code == 200

        # assert that the intro, footer, disclaimer forms are there
        assert 'editIntro' in response.forms
        assert 'editFooter' in response.forms
        assert 'editDisclaimer' in response.forms

        # assert that the field forms are there
        assert 'editIdTitleContentAndOrder' in response.forms
        assert 'editOfficerIdentifierTitleContentAndOrder' in response.forms
        assert 'editServiceTypeTitleContentAndOrder' in response.forms
        assert 'editForceTypeTitleContentAndOrder' in response.forms
        assert 'editAssignmentTitleContentAndOrder' in response.forms
        assert 'editArrestMadeTitleContentAndOrder' in response.forms
        assert 'editOfficerInjuredTitleContentAndOrder' in response.forms
        assert 'editReportFiledTitleContentAndOrder' in response.forms

    def test_complaints_schema_edit_forms_exist(self, testapp):
        ''' Edit forms exist for the complaints schema page.
        '''
        department = Department.create(name="Bad Police Department", short_name="BPD", load_defaults=True)

        # set up a user
        log_in_user(testapp, department)

        # make a request to specific front page
        response = testapp.get("/department/{}/edit/schema/complaints".format(department.id))
        assert response.status_code == 200

        # assert that the intro, footer, disclaimer forms are there
        assert 'editIntro' in response.forms
        assert 'editFooter' in response.forms
        assert 'editDisclaimer' in response.forms

        # assert that the field forms are there
        assert 'editIdTitleContentAndOrder' in response.forms
        assert 'editOccurredDateTitleContentAndOrder' in response.forms
        assert 'editDivisionTitleContentAndOrder' in response.forms
        assert 'editDistrictTitleContentAndOrder' in response.forms
        assert 'editShiftTitleContentAndOrder' in response.forms

    def test_changing_schema_field_order_reorders_other_fields(self, testapp):
        ''' Changing the order value of a schema field will re-order the other fields to make room.
        '''
        department = Department.create(name="Bad Police Department", short_name="BPD", load_defaults=True)

        # set up a user
        log_in_user(testapp, department)

        for incident_type in [("complaints", "complaints"), ("assaults", "assaultsonofficers"), ("ois", "ois"), ("uof", "useofforce")]:
            # make a request to specific front page
            response = testapp.get("/department/{}/edit/schema/{}".format(department.id, incident_type[1]))
            assert response.status_code == 200

            schema_field_prefix = "{}-schema-field-".format(incident_type[0])
            schema_fields = department.get_blocks_by_slug_startswith(schema_field_prefix)

            assert schema_fields[0].order < schema_fields[1].order
            assert schema_fields[1].order < schema_fields[2].order
            assert schema_fields[2].order < schema_fields[3].order

            form_name = "edit{}TitleContentAndOrder".format(schema_fields[2].slug.replace(schema_field_prefix, "").replace("-", " ").title().replace(" ", ""))
            assert form_name in response.forms
            form = response.forms[form_name]
            new_order = schema_fields[0].order
            form['chart_order'] = new_order
            response = form.submit().follow()
            assert response.status_code == 200

            check_fields = department.get_blocks_by_slug_startswith(schema_field_prefix)
            assert check_fields[0].order < check_fields[1].order
            assert check_fields[1].order < check_fields[2].order
            assert check_fields[2].order < check_fields[3].order

    def test_changing_order_number_to_a_valid_range(self, testapp):
        ''' Changing the order value of a schema field will re-order the other fields to make room.
        '''
        department = Department.create(name="Bad Police Department", short_name="BPD", load_defaults=True)

        # set up a user
        log_in_user(testapp, department)

        for incident_type in [("complaints", "complaints"), ("assaults", "assaultsonofficers"), ("ois", "ois"), ("uof", "useofforce")]:
            # make a request to specific front page
            response = testapp.get("/department/{}/edit/schema/{}".format(department.id, incident_type[1]))
            assert response.status_code == 200

            schema_field_prefix = "{}-schema-field-".format(incident_type[0])
            schema_fields = department.get_blocks_by_slug_startswith(schema_field_prefix)
            fields_length = len(schema_fields)

            assert schema_fields[0].order < schema_fields[1].order
            assert schema_fields[1].order < schema_fields[2].order
            assert schema_fields[2].order < schema_fields[3].order

            # Testing overtly high order numbers
            form_name = "edit{}TitleContentAndOrder".format(schema_fields[2].slug.replace(schema_field_prefix, "").replace("-", " ").title().replace(" ", ""))
            assert form_name in response.forms
            form = response.forms[form_name]
            new_order = fields_length + 10
            form['chart_order'] = new_order
            response = form.submit().follow()
            assert response.status_code == 200

            check_fields = department.get_blocks_by_slug_startswith(schema_field_prefix)
            assert check_fields[-1].order == len(check_fields) - 1
            assert len(check_fields) == fields_length
            assert check_fields[-1].slug == schema_fields[2].slug

            # make a request to specific front page
            response = testapp.get("/department/{}/edit/schema/{}".format(department.id, incident_type[1]))
            assert response.status_code == 200

            schema_fields = department.get_blocks_by_slug_startswith(schema_field_prefix)
            fields_length = len(schema_fields)

            # Testing negative order numbers
            form_name = "edit{}TitleContentAndOrder".format(schema_fields[2].slug.replace(schema_field_prefix, "").replace("-", " ").title().replace(" ", ""))
            assert form_name in response.forms
            form = response.forms[form_name]
            new_order = -10
            form['chart_order'] = new_order
            response = form.submit().follow()
            assert response.status_code == 200

            check_fields = department.get_blocks_by_slug_startswith(schema_field_prefix)
            assert check_fields[0].slug == schema_fields[2].slug
            assert len(check_fields) == fields_length
            assert check_fields[0].order == 0

    def test_editing_complaints_schema_field_value(self, testapp):
        ''' Submitting the form to edit a schema field changes the correct value in the database
        '''
        department = Department.create(name="Bad Police Department", short_name="BPD", load_defaults=True)

        # set up a user
        log_in_user(testapp, department)

        # make a request to specific front page
        response = testapp.get("/department/{}/edit/schema/complaints".format(department.id))
        assert response.status_code == 200

        assert 'editShiftTitleContentAndOrder' in response.forms
        form = response.forms['editShiftTitleContentAndOrder']
        new_title = "A New Data Field Title"
        new_content = "A Short Definition of this Data Field"
        new_order = 99
        form['chart_title'] = new_title
        form['chart_content'] = new_content
        form['chart_order'] = new_order
        response = form.submit().follow()
        assert response.status_code == 200

        checkblock = ChartBlock.query.filter_by(slug="complaints-schema-field-shift", department_id=department.id).first()
        assert checkblock.title == new_title
        assert checkblock.content == new_content
        assert checkblock.order == len(department.get_blocks_by_slug_startswith("complaints-schema-field-")) - 1

    def test_submit_non_numberic_value_to_order(self, testapp):
        ''' Submitting the form to change the order of a schmea field with a non-numeric value doesn't change anything.
        '''
        department = Department.create(name="Bad Police Department", short_name="BPD", load_defaults=True)

        # set up a user
        log_in_user(testapp, department)

        # get the order of a schema field
        check_order = ChartBlock.query.filter_by(slug="complaints-schema-field-shift", department_id=department.id).first().order

        # make a request to specific front page
        response = testapp.get("/department/{}/edit/schema/complaints".format(department.id))
        assert response.status_code == 200

        assert 'editShiftTitleContentAndOrder' in response.forms
        form = response.forms['editShiftTitleContentAndOrder']
        new_order = "I'm not a number"
        form['chart_order'] = new_order
        response = form.submit().follow()
        assert response.status_code == 200

        checkblock = ChartBlock.query.filter_by(slug="complaints-schema-field-shift", department_id=department.id).first()
        assert checkblock.order == check_order

    def test_submitting_schema_intro_field_value(self, testapp):
        ''' Submitting the form to edit a schema intro field changes the expected value in the database and not others
        '''
        department = Department.create(name="Bad Police Department", short_name="BPD", load_defaults=True)

        # set up a user
        log_in_user(testapp, department)

        # make a request to specific front page
        response = testapp.get("/department/{}/edit/schema/complaints".format(department.id))
        assert response.status_code == 200

        assert 'editIntro' in response.forms
        form = response.forms['editIntro']
        new_content = "A Short Definition of this Data Field"
        form['chart_content'] = new_content
        checkblock = ChartBlock.query.filter_by(slug="complaints-schema-introduction", department_id=department.id).first()
        title = checkblock.title
        order = checkblock.order
        response = form.submit().follow()

        assert response.status_code == 200

        checkblock2 = ChartBlock.query.filter_by(slug="complaints-schema-introduction", department_id=department.id).first()

        assert checkblock.content == new_content
        assert title == checkblock2.title
        assert order == checkblock2.order

    def test_editing_assaults_schema_field_value(self, testapp):
        ''' Submitting the form to edit a schema field changes the correct value in the database
        '''
        department = Department.create(name="Bad Police Department", short_name="BPD", load_defaults=True)

        # set up a user
        log_in_user(testapp, department)

        # make a request to specific front page
        response = testapp.get("/department/{}/edit/schema/assaultsonofficers".format(department.id))
        assert response.status_code == 200

        assert 'editForceTypeTitleContentAndOrder' in response.forms
        form = response.forms['editForceTypeTitleContentAndOrder']
        new_title = "A New Data Field Title"
        new_content = "A Short Definition of this Data Field"
        new_order = 99
        form['chart_title'] = new_title
        form['chart_content'] = new_content
        form['chart_order'] = new_order
        response = form.submit().follow()
        assert response.status_code == 200

        checkblock = ChartBlock.query.filter_by(slug="assaults-schema-field-force-type").first()
        assert checkblock.title == new_title
        assert checkblock.content == new_content
        assert checkblock.order == len(department.get_blocks_by_slug_startswith("assaults-schema-field-")) - 1

    def test_editing_ois_schema_field_value(self, testapp):
        ''' Submitting the form to edit a schema field changes the correct value in the database
        '''
        department = Department.create(name="Bad Police Department", short_name="BPD", load_defaults=True)

        # set up a user
        log_in_user(testapp, department)

        # make a request to specific front page
        response = testapp.get("/department/{}/edit/schema/ois".format(department.id))
        assert response.status_code == 200

        assert 'editShiftTitleContentAndOrder' in response.forms
        form = response.forms['editShiftTitleContentAndOrder']
        new_title = "A New Data Field Title"
        new_content = "A Short Definition of this Data Field"
        new_order = 99
        form['chart_title'] = new_title
        form['chart_content'] = new_content
        form['chart_order'] = new_order
        response = form.submit().follow()
        assert response.status_code == 200

        checkblock = ChartBlock.query.filter_by(slug="ois-schema-field-shift").first()
        assert checkblock.title == new_title
        assert checkblock.content == new_content
        assert checkblock.order == len(department.get_blocks_by_slug_startswith("ois-schema-field-")) - 1

    def test_editing_useofforce_schema_field_value(self, testapp):
        ''' Submitting the form to edit a schema field changes the correct value in the database
        '''
        department = Department.create(name="Bad Police Department", short_name="BPD", load_defaults=True)

        # set up a user
        log_in_user(testapp, department)

        # make a request to specific front page
        response = testapp.get("/department/{}/edit/schema/useofforce".format(department.id))
        assert response.status_code == 200

        assert 'editShiftTitleContentAndOrder' in response.forms
        form = response.forms['editShiftTitleContentAndOrder']
        new_title = "A New Data Field Title"
        new_content = "A Short Definition of this Data Field"
        new_order = 99
        form['chart_title'] = new_title
        form['chart_content'] = new_content
        form['chart_order'] = new_order
        response = form.submit().follow()
        assert response.status_code == 200

        checkblock = ChartBlock.query.filter_by(slug="uof-schema-field-shift").first()
        assert checkblock.title == new_title
        assert checkblock.content == new_content
        assert checkblock.order == len(department.get_blocks_by_slug_startswith("uof-schema-field-")) - 1

    def test_submitting_schema_edit_form_redirects_to_preview(self, testapp):
        ''' Submitting the form to edit a schema field changes the correct value in the database
        '''
        department = Department.create(name="Bad Police Department", short_name="BPD", load_defaults=True)

        # set up a user
        log_in_user(testapp, department)

        # make a request to specific front page
        response = testapp.get("/department/{}/edit/schema/complaints".format(department.id))
        assert response.status_code == 200

        # submit new title & content
        assert 'editShiftTitleContentAndOrder' in response.forms
        form = response.forms['editShiftTitleContentAndOrder']
        new_title = "A New Data Field Title"
        new_content = "A Short Definition of this Data Field"
        new_order = 99
        form['chart_title'] = new_title
        form['chart_content'] = new_content
        form['chart_order'] = new_order
        response = form.submit()

        # the response should be a redirect
        assert response.status_code == 302
        # the location of the redirect should be the preview page
        parsed = urlparse(response.location)
        assert parsed.path == "/department/{}/preview/schema/complaints".format(department.id)
