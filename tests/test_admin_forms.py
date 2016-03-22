# -*- coding: utf-8 -*-
import pytest
from comport.admin.forms import NewDepartmentForm
from comport.department.models import Department

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
