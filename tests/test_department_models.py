# -*- coding: utf-8 -*-
import pytest
from comport.content.models import ChartBlock
from comport.department.models import Extractor
from .factories import DepartmentFactory
import uuid

@pytest.mark.usefixtures('db')
class TestExtractors:
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

    def test_get_complaint_blocks(self):
        ''' Set and get complaint chart blocks.
        '''
        department = DepartmentFactory()
        department.save()

        # create & append chart blocks with the expected slugs
        complaint_intro = ChartBlock(title="INTRO", dataset="intros", slug="complaints-introduction")
        complaint_bm = ChartBlock(title="BYMONTH", dataset="bymonth", slug="complaints-by-month")
        complaint_bya = ChartBlock(title="BYALLEGATION", dataset="bya", slug="complaints-by-allegation")
        complaint_byat = ChartBlock(title="BYALLEGATIONTYPE", dataset="byat", slug="complaints-by-allegation-type")
        complaint_bdis = ChartBlock(title="BYDISPOSITION", dataset="bdis", slug="complaints-by-disposition")
        complaint_bpre = ChartBlock(title="BYPRECINCT", dataset="bpre", slug="complaints-by-precinct")
        complaint_od = ChartBlock(title="OFFICERDEMOS", dataset="od", slug="officer-demographics")
        complaint_bde = ChartBlock(title="BYDEMO", dataset="bde", slug="complaints-by-demographic")
        complaint_bof = ChartBlock(title="BYOFFICER", dataset="bof", slug="complaints-by-officer")

        department.chart_blocks.append(complaint_intro)
        department.chart_blocks.append(complaint_bm)
        department.chart_blocks.append(complaint_bya)
        department.chart_blocks.append(complaint_byat)
        department.chart_blocks.append(complaint_bdis)
        department.chart_blocks.append(complaint_bpre)
        department.chart_blocks.append(complaint_od)
        department.chart_blocks.append(complaint_bde)
        department.chart_blocks.append(complaint_bof)
        department.save()

        # verify that the blocks are returned in the expected structure
        complaint_blocks = department.get_complaint_blocks()
        assert complaint_blocks['introduction'] == complaint_intro
        assert complaint_blocks['first-block'] == complaint_bm
        assert complaint_blocks['blocks'][0] == complaint_bya
        assert complaint_blocks['blocks'][1] == complaint_byat
        assert complaint_blocks['blocks'][2] == complaint_bdis
        assert complaint_blocks['blocks'][3] == complaint_bpre
        assert complaint_blocks['blocks'][4] == complaint_od
        assert complaint_blocks['blocks'][5] == complaint_bde
        assert complaint_blocks['blocks'][6] == complaint_bof

    def test_get_uof_blocks(self):
        ''' Set and get uof chart blocks.
        '''
        department = DepartmentFactory()
        department.save()

        # create & append chart blocks with the expected slugs
        uof_intro = ChartBlock(title="INTRO", dataset="intros", slug="uof-introduction")
        uof_ft = ChartBlock(title="FORCETYPE", dataset="forcetype", slug="uof-force-type")
        uof_bid = ChartBlock(title="BYINCDISTRICT", dataset="bid", slug="uof-by-inc-district")
        uof_od = ChartBlock(title="OFFICERDEMOS", dataset="od", slug="officer-demographics")
        uof_race = ChartBlock(title="RACE", dataset="race", slug="uof-race")
        department.chart_blocks.append(uof_intro)
        department.chart_blocks.append(uof_ft)
        department.chart_blocks.append(uof_bid)
        department.chart_blocks.append(uof_od)
        department.chart_blocks.append(uof_race)
        department.save()

        # verify that the blocks are returned in the expected structure
        uof_blocks = department.get_uof_blocks()
        assert uof_blocks['introduction'] == uof_intro
        assert uof_blocks['first-block'] == uof_ft
        assert uof_blocks['blocks'][0] == uof_bid
        assert uof_blocks['blocks'][1] == uof_od
        assert uof_blocks['blocks'][2] == uof_race

    def test_get_ois_blocks(self):
        ''' Set and get ois chart blocks.
        '''
        department = DepartmentFactory()
        department.save()

        # create & append chart blocks with the expected slugs
        ois_intro = ChartBlock(title="INTRO", dataset="intros", slug="ois-introduction")
        ois_bid = ChartBlock(title="BYINCDISTRICT", dataset="bid", slug="ois-by-inc-district")
        ois_wt = ChartBlock(title="WEAPONTYPE", dataset="weapontype", slug="ois-weapon-type")
        ois_od = ChartBlock(title="OFFICERDEMOS", dataset="od", slug="officer-demographics")
        ois_race = ChartBlock(title="RACE", dataset="race", slug="ois-race")
        department.chart_blocks.append(ois_intro)
        department.chart_blocks.append(ois_bid)
        department.chart_blocks.append(ois_wt)
        department.chart_blocks.append(ois_od)
        department.chart_blocks.append(ois_race)
        department.save()

        # verify that the blocks are returned in the expected structure
        ois_blocks = department.get_ois_blocks()
        assert ois_blocks['introduction'] == ois_intro
        assert ois_blocks['first-block'] == ois_bid
        assert ois_blocks['blocks'][0] == ois_wt
        assert ois_blocks['blocks'][1] == ois_od
        assert ois_blocks['blocks'][2] == ois_race
