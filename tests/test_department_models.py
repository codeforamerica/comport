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
        department = Department.create(name="IM Police Department", short_name="IMPD", load_defaults=True)

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

    def test_get_blocks_by_slugs_order(self):
        ''' We can get blocks sorted by order or in the order the slugs were passed.
        '''
        department = Department.create(name="IM Police Department", short_name="IMPD", load_defaults=True)

        # get some complaint schema blocks
        blocks = department.get_complaint_schema_blocks()['blocks']
        assert len(blocks) >= 6
        blocks = blocks[:6]

        # make sure our test will be valid
        orders = [b.order for b in blocks]
        assert orders == sorted(orders)

        # make a list of slugs out of order
        ordered_slugs = [b.slug for b in blocks]
        mixedup_slugs = ordered_slugs.copy()
        mixedup_slugs = [ordered_slugs[i] for i in [5, 3, 1, 0, 2, 4]]
        assert ordered_slugs != mixedup_slugs

        # now request an ordered list of chart blocks from the mixed up list
        check_ordered_blocks = department.get_blocks_by_slugs(mixedup_slugs, sort_by_order=True)
        check_ordered_slugs = [b.slug for b in check_ordered_blocks]
        assert len(check_ordered_blocks) == 6
        assert check_ordered_slugs == ordered_slugs
        assert check_ordered_slugs != mixedup_slugs

        # and request a list of chart blocks in the order the slugs are passed
        check_mixedup_blocks = department.get_blocks_by_slugs(mixedup_slugs, sort_by_order=False)
        check_mixedup_slugs = [b.slug for b in check_mixedup_blocks]
        assert len(check_mixedup_slugs) == 6
        assert check_mixedup_slugs != ordered_slugs
        assert check_mixedup_slugs == mixedup_slugs
