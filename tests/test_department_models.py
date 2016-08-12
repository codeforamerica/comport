# -*- coding: utf-8 -*-
import pytest
from comport.department.models import Extractor, Department
from .factories import DepartmentFactory
import uuid

@pytest.mark.usefixtures('db')
class TestDepartmentModel:
    def test_extractors_from_department_and_password(self):
        department = DepartmentFactory()
        department.save()

        password = str(uuid.uuid4())

        extractor, envs = Extractor.from_department_and_password(department=department, password=password)

        assert department == extractor.departments[0]
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

    def test_get_extractor_from_department_without_extractor(self):
        department = DepartmentFactory()
        department.save()

        assert department.get_extractor() == None

    def test_schema_chart_block_order(self):
        ''' Set and get complaint chart blocks.
        '''
        department = Department.create(name="Inner Mongolia Police Department", short_name="IMPD", load_defaults=True)

        # get complaint schema blocks
        before_blocks = department.get_complaint_schema_blocks()

        # make sure our test will be valid
        assert len(before_blocks['blocks']) > 2
        assert before_blocks['blocks'][0].order < before_blocks['blocks'][1].order
        assert before_blocks['blocks'][1].order < 100
        assert before_blocks['blocks'][-1].order < 100

        # change the order of the first block to 100
        block = before_blocks['blocks'][0]
        block.order = 100
        block.save()

        # get the blocks again and test the order
        after_blocks = department.get_complaint_schema_blocks()
        assert before_blocks['blocks'][1].order == after_blocks['blocks'][0].order
        assert before_blocks['blocks'][1].slug == after_blocks['blocks'][0].slug
        assert after_blocks['blocks'][-1].order == 100
        assert before_blocks['blocks'][0].slug == after_blocks['blocks'][-1].slug
