# -*- coding: utf-8 -*-
import datetime as dt

import pytest

from comport.user.models import User, Role
from comport.department.models import Extractor, Department
from .factories import UserFactory, DepartmentFactory
import uuid

@pytest.mark.usefixtures('db')
class TestExtactors:
    def test_extractors_from_department_and_password(self):
        department = DepartmentFactory()
        department.save()

        password = str(uuid.uuid4())

        extractor, envs = Extractor.from_department_and_password(department=department, password=password)

        assert department == extractor.department
        assert extractor.check_password(password) is True
        assert password in envs

    def test_get_extractor_from_department(self):
        department = DepartmentFactory()
        department.save()
        assert (" " in department.name) is True


        password = str(uuid.uuid4())

        extractor, envs = Extractor.from_department_and_password(department=department, password=password)
        extractor.save()

        assert department.get_extractor() == extractor
        assert (" " in extractor.username) is False

    def test_regen_extractor_envs(self):
        department = DepartmentFactory()
        department.save()

        password = str(uuid.uuid4())

        extractor, envs = Extractor.from_department_and_password(department=department, password=password)
        extractor.save()
        new_password = str(uuid.uuid4())

        extractor.set_password(new_password)

        assert extractor.check_password(new_password) is True
        assert new_password in extractor.generate_envs(new_password)
        assert "http://localhost:5000" in extractor.generate_envs(new_password)

    def test_get_extractor_from_department_without_extractor(self):
        department = DepartmentFactory()
        department.save()

        assert department.get_extractor() == None
