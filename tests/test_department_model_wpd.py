# -*- coding: utf-8 -*-
import pytest
import importlib
from comport.content.models import ChartBlock
from comport.department.models import Department
from comport.data.models import UseOfForceIncidentWPD, CitizenComplaintWPD

@pytest.mark.usefixtures('db')
class TestDepartmentModelWPD:

    def test_get_complaint_blocks(self):
        ''' Set and get complaint chart blocks.
        '''
        department = Department.create(name="W Police Department", short_name="WPD", load_defaults=False)

        # create & append chart blocks with the expected slugs
        complaint_intro = ChartBlock(title="INTRO", dataset="intros", slug="complaints-introduction")
        complaint_bm = ChartBlock(title="BYMONTH", dataset="bymonth", slug="complaints-by-month")
        complaint_byat = ChartBlock(title="BYALLEGATIONTYPE", dataset="byat", slug="complaints-by-allegation-type")
        complaint_bdis = ChartBlock(title="BYDISPOSITION", dataset="bdis", slug="complaints-by-finding")
        complaint_bpre = ChartBlock(title="BYPRECINCT", dataset="bpre", slug="complaints-by-precinct")
        complaint_od = ChartBlock(title="OFFICERDEMOS", dataset="od", slug="officer-demographics")
        complaint_bde = ChartBlock(title="BYDEMO", dataset="bde", slug="complaints-by-demographic")

        department.chart_blocks.append(complaint_intro)
        department.chart_blocks.append(complaint_bm)
        department.chart_blocks.append(complaint_byat)
        department.chart_blocks.append(complaint_bdis)
        department.chart_blocks.append(complaint_bpre)
        department.chart_blocks.append(complaint_od)
        department.chart_blocks.append(complaint_bde)
        department.save()

        # verify that the blocks are returned in the expected structure
        complaint_blocks = department.get_complaint_blocks()
        assert complaint_blocks['introduction'] == complaint_intro
        assert complaint_blocks['first-block'] == complaint_bm
        assert complaint_blocks['blocks'][0] == complaint_byat
        assert complaint_blocks['blocks'][1] == complaint_bdis
        assert complaint_blocks['blocks'][2] == complaint_bpre
        assert complaint_blocks['blocks'][3] == complaint_od
        assert complaint_blocks['blocks'][4] == complaint_bde

    def test_get_complaint_schema_blocks(self):
        ''' Set and get complaint schema chart blocks.
        '''
        department = Department.create(name="W Police Department", short_name="WPD", load_defaults=False)

        # create & append chart blocks with the expected slugs
        complaint_intro = ChartBlock(title="INTRO", dataset="intros", slug="complaints-schema-introduction")
        complaint_id = ChartBlock(title="FIELDID", dataset="fid", slug="complaints-schema-field-id")
        complaint_od = ChartBlock(title="OCCURREDDATE", dataset="fod", slug="complaints-schema-field-occurred-date")
        complaint_div = ChartBlock(title="DIVISION", dataset="div", slug="complaints-schema-field-division")
        complaint_dis = ChartBlock(title="DISTRICT", dataset="dis", slug="complaints-schema-field-district")
        complaint_shift = ChartBlock(title="SHIFT", dataset="shift", slug="complaints-schema-field-shift")
        complaint_footer = ChartBlock(title="FOOTER", dataset="footer", slug="complaints-schema-footer")
        complaint_disclaimer = ChartBlock(title="DISCLAIMER", dataset="disclaimer", slug="complaints-schema-disclaimer")

        department.chart_blocks.append(complaint_intro)
        department.chart_blocks.append(complaint_id)
        department.chart_blocks.append(complaint_od)
        department.chart_blocks.append(complaint_div)
        department.chart_blocks.append(complaint_dis)
        department.chart_blocks.append(complaint_shift)
        department.chart_blocks.append(complaint_footer)
        department.chart_blocks.append(complaint_disclaimer)
        department.save()

        # verify that the blocks are returned in the expected structure
        complaint_blocks = department.get_complaint_schema_blocks()
        assert complaint_blocks['introduction'] == complaint_intro
        assert complaint_blocks['footer'] == complaint_footer
        assert complaint_blocks['disclaimer'] == complaint_disclaimer
        assert complaint_id in complaint_blocks['blocks']
        assert complaint_od in complaint_blocks['blocks']
        assert complaint_div in complaint_blocks['blocks']
        assert complaint_dis in complaint_blocks['blocks']
        assert complaint_shift in complaint_blocks['blocks']

    def test_get_uof_blocks(self):
        ''' Set and get uof chart blocks.
        '''
        department = Department.create(name="W Police Department", short_name="WPD", load_defaults=False)

        # create & append chart blocks with the expected slugs
        uof_intro = ChartBlock(title="INTRO", dataset="intros", slug="uof-introduction")
        uof_ft = ChartBlock(title="FORCETYPE", dataset="forcetype", slug="uof-force-type")
        uof_bid = ChartBlock(title="BYASSIGNMENT", dataset="bid", slug="uof-by-inc-district")
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

    def test_get_uof_schema_blocks(self):
        ''' Set and get uof schema chart blocks.
        '''
        department = Department.create(name="W Police Department", short_name="WPD", load_defaults=False)

        # create & append chart blocks with the expected slugs
        uof_intro = ChartBlock(title="INTRO", dataset="intros", slug="uof-schema-introduction")
        uof_id = ChartBlock(title="FIELDID", dataset="fid", slug="uof-schema-field-id")
        uof_od = ChartBlock(title="OCCURREDDATE", dataset="fod", slug="uof-schema-field-occurred-date")
        uof_div = ChartBlock(title="DIVISION", dataset="div", slug="uof-schema-field-division")
        uof_dis = ChartBlock(title="DISTRICT", dataset="dis", slug="uof-schema-field-district")
        uof_shift = ChartBlock(title="SHIFT", dataset="shift", slug="uof-schema-field-shift")
        uof_footer = ChartBlock(title="FOOTER", dataset="footer", slug="uof-schema-footer")
        uof_disclaimer = ChartBlock(title="DISCLAIMER", dataset="disclaimer", slug="uof-schema-disclaimer")

        department.chart_blocks.append(uof_intro)
        department.chart_blocks.append(uof_id)
        department.chart_blocks.append(uof_od)
        department.chart_blocks.append(uof_div)
        department.chart_blocks.append(uof_dis)
        department.chart_blocks.append(uof_shift)
        department.chart_blocks.append(uof_footer)
        department.chart_blocks.append(uof_disclaimer)
        department.save()

        # verify that the blocks are returned in the expected structure
        uof_blocks = department.get_uof_schema_blocks()
        assert uof_blocks['introduction'] == uof_intro
        assert uof_blocks['footer'] == uof_footer
        assert uof_blocks['disclaimer'] == uof_disclaimer
        assert uof_id in uof_blocks['blocks']
        assert uof_od in uof_blocks['blocks']
        assert uof_div in uof_blocks['blocks']
        assert uof_dis in uof_blocks['blocks']
        assert uof_shift in uof_blocks['blocks']

    def test_get_dataset_lookup(self):
        ''' The dataset lookup returns usable information
        '''
        # create a department
        department = Department.create(name="W Police Department", short_name="WPD", load_defaults=True)

        complaints_lookup = department.get_dataset_lookup("complaints")
        uof_lookup = department.get_dataset_lookup("uof")

        # TODO: how to test that paths are valid?

        # test that the var suffixes are valid
        try:
            getattr(department, "is_public_{}".format(complaints_lookup["var_suffix"]))
        except AttributeError:
            pytest.fail("Unexpected AttributeError")

        try:
            getattr(department, "is_public_{}".format(uof_lookup["var_suffix"]))
        except AttributeError:
            pytest.fail("Unexpected AttributeError")

        # test that the class prefixes are valid
        try:
            getattr(importlib.import_module("comport.data.models"), "{}{}".format(complaints_lookup["class_prefix"], department.short_name))
        except AttributeError:
            pytest.fail("Unexpected AttributeError")

        try:
            getattr(importlib.import_module("comport.data.models"), "{}{}".format(uof_lookup["class_prefix"], department.short_name))
        except AttributeError:
            pytest.fail("Unexpected AttributeError")

    def test_dataset_is_public_and_has_data(self):
        ''' We can accurately tell if a dataset is public and has data.
        '''
        # create a department
        department = Department.create(name="W Police Department", short_name="WPD", load_defaults=True)

        # none of the datasets have data, so they should all return false
        assert department.dataset_is_public_and_has_data("complaints") == False
        assert department.dataset_is_public_and_has_data("uof") == False
        # the total count should be zero
        assert department.displayable_dataset_count() == 0

        # create incidents and verify that the datasets are now displayable
        CitizenComplaintWPD.create(department_id=department.id, opaque_id="12345abcde")
        assert department.dataset_is_public_and_has_data("complaints") == True
        assert department.displayable_dataset_count() == 1

        UseOfForceIncidentWPD.create(department_id=department.id, opaque_id="23456bcdef")
        assert department.dataset_is_public_and_has_data("uof") == True
        assert department.displayable_dataset_count() == 2

        # now make them all not public, and they should be false again
        department.is_public_citizen_complaints = False
        assert department.dataset_is_public_and_has_data("complaints") == False
        department.is_public_use_of_force_incidents = False
        assert department.dataset_is_public_and_has_data("uof") == False
        assert department.displayable_dataset_count() == 0
