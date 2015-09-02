# -*- coding: utf-8 -*-
import pytest

from comport.admin.forms import NewDepartmentForm
from comport.department.models import Department


class TestNewDepartmentForm:

    def test_department_name_required(self):
        # Enters username that is already registered
        form = NewDepartmentForm(department_name=None)

        assert form.validate() is False
        assert 'This field is required.' in form.department_name.errors

    def test_department_name_unique_required(self, db):
        Department.create(name="name")
        # Enters username that is already registered
        form = NewDepartmentForm(department_name="name")

        assert form.validate() is False
        assert 'Department name already registered.' in form.department_name.errors

    def test_validate_success(self,db):
        form = NewDepartmentForm(department_name='newdeptname')
        assert form.validate() is True
