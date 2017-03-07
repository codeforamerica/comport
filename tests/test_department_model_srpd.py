# -*- coding: utf-8 -*-
import pytest
import importlib
from comport.content.models import ChartBlock
from comport.department.models import Department
from comport.data.models import OfficerInvolvedShootingSRPD, UseOfForceIncidentSRPD, CitizenComplaintSRPD, PursuitSRPD

@pytest.mark.usefixtures('db')
class TestDepartmentModelSRPD:

    def test_get_complaint_blocks(self):
        ''' Set and get complaint chart blocks.
        '''
        department = Department.create(name="SR Police Department", short_name="SRPD", load_defaults=False)

        # create & append chart blocks with the expected slugs
        complaint_intro = ChartBlock(title="INTRO", dataset="", slug="complaints-introduction")
        complaint_bm = ChartBlock(title="BYMONTH", dataset="", slug="complaints-by-month")
        complaint_bal = ChartBlock(title="BYALLEGATION", dataset="", slug="complaints-by-allegation")
        complaint_bd = ChartBlock(title="BYDISPOSITION", dataset="", slug="complaints-by-disposition")
        complaint_bt = ChartBlock(title="BYTEAM", dataset="", slug="complaints-by-team")
        complaint_od = ChartBlock(title="OFFICERDEMOS", dataset="", slug="officer-demographics")

        department.chart_blocks.append(complaint_intro)
        department.chart_blocks.append(complaint_bm)
        department.chart_blocks.append(complaint_bal)
        department.chart_blocks.append(complaint_bd)
        department.chart_blocks.append(complaint_bt)
        department.chart_blocks.append(complaint_od)
        department.save()

        # verify that the blocks are returned in the expected structure
        complaint_blocks = department.get_complaint_blocks()
        assert complaint_blocks['introduction'] == complaint_intro
        assert complaint_blocks['first-block'] == complaint_bm
        assert complaint_blocks['blocks'][0] == complaint_bal
        assert complaint_blocks['blocks'][1] == complaint_bd
        assert complaint_blocks['blocks'][2] == complaint_bt
        assert complaint_blocks['blocks'][3] == complaint_od

    def test_get_complaint_schema_blocks(self):
        ''' Set and get complaint schema chart blocks.
        '''
        department = Department.create(name="SR Police Department", short_name="SRPD", load_defaults=False)

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
        department = Department.create(name="SR Police Department", short_name="SRPD", load_defaults=False)

        # create & append chart blocks with the expected slugs
        uof_intro = ChartBlock(title="INTRO", dataset="intros", slug="uof-introduction")
        uof_bm = ChartBlock(title="BYMONTH", dataset="bymonth", slug="uof-by-month")
        uof_ft = ChartBlock(title="FORCETYPE", dataset="forcetype", slug="uof-incident-force-type")
        uof_bt = ChartBlock(title="BYTEAM", dataset="byteam", slug="uof-by-team")
        uof_od = ChartBlock(title="OFFICERDEMOS", dataset="od", slug="officer-demographics")
        department.chart_blocks.append(uof_intro)
        department.chart_blocks.append(uof_bm)
        department.chart_blocks.append(uof_ft)
        department.chart_blocks.append(uof_bt)
        department.chart_blocks.append(uof_od)
        department.save()

        # verify that the blocks are returned in the expected structure
        uof_blocks = department.get_uof_blocks()
        assert uof_blocks['introduction'] == uof_intro
        assert uof_blocks['first-block'] == uof_bm
        assert uof_blocks['blocks'][0] == uof_ft
        assert uof_blocks['blocks'][1] == uof_bt
        assert uof_blocks['blocks'][2] == uof_od

    def test_get_uof_schema_blocks(self):
        ''' Set and get uof schema chart blocks.
        '''
        department = Department.create(name="SR Police Department", short_name="SRPD", load_defaults=False)

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

    def test_get_ois_blocks(self):
        ''' Set and get ois chart blocks.
        '''
        department = Department.create(name="SR Police Department", short_name="SRPD", load_defaults=False)

        # create & append chart blocks with the expected slugs
        ois_intro = ChartBlock(title="INTRO", dataset="intros", slug="ois-introduction")
        ois_bm = ChartBlock(title="BYMONTH", dataset="bm", slug="ois-by-month")
        ois_bt = ChartBlock(title="BYTEAM", dataset="byteam", slug="ois-by-team")
        ois_od = ChartBlock(title="OFFICERDEMOS", dataset="od", slug="officer-demographics")
        department.chart_blocks.append(ois_intro)
        department.chart_blocks.append(ois_bm)
        department.chart_blocks.append(ois_bt)
        department.chart_blocks.append(ois_od)
        department.save()

        # verify that the blocks are returned in the expected structure
        ois_blocks = department.get_ois_blocks()
        assert ois_blocks['introduction'] == ois_intro
        assert ois_blocks['first-block'] == ois_bm
        assert ois_blocks['blocks'][0] == ois_bt
        assert ois_blocks['blocks'][1] == ois_od

    def test_get_ois_schema_blocks(self):
        ''' Set and get ois schema chart blocks.
        '''
        department = Department.create(name="SR Police Department", short_name="SRPD", load_defaults=False)

        # create & append chart blocks with the expected slugs
        ois_intro = ChartBlock(title="INTRO", dataset="intros", slug="ois-schema-introduction")
        ois_id = ChartBlock(title="FIELDID", dataset="fid", slug="ois-schema-field-id")
        ois_od = ChartBlock(title="OCCURREDDATE", dataset="fod", slug="ois-schema-field-occurred-date")
        ois_div = ChartBlock(title="DIVISION", dataset="div", slug="ois-schema-field-division")
        ois_dis = ChartBlock(title="DISTRICT", dataset="dis", slug="ois-schema-field-district")
        ois_shift = ChartBlock(title="SHIFT", dataset="shift", slug="ois-schema-field-shift")
        ois_footer = ChartBlock(title="FOOTER", dataset="footer", slug="ois-schema-footer")
        ois_disclaimer = ChartBlock(title="DISCLAIMER", dataset="disclaimer", slug="ois-schema-disclaimer")

        department.chart_blocks.append(ois_intro)
        department.chart_blocks.append(ois_id)
        department.chart_blocks.append(ois_od)
        department.chart_blocks.append(ois_div)
        department.chart_blocks.append(ois_dis)
        department.chart_blocks.append(ois_shift)
        department.chart_blocks.append(ois_footer)
        department.chart_blocks.append(ois_disclaimer)
        department.save()

        # verify that the blocks are returned in the expected structure
        ois_blocks = department.get_ois_schema_blocks()
        assert ois_blocks['introduction'] == ois_intro
        assert ois_blocks['footer'] == ois_footer
        assert ois_blocks['disclaimer'] == ois_disclaimer
        assert ois_id in ois_blocks['blocks']
        assert ois_od in ois_blocks['blocks']
        assert ois_div in ois_blocks['blocks']
        assert ois_dis in ois_blocks['blocks']
        assert ois_shift in ois_blocks['blocks']

    def test_get_pursuits_blocks(self):
        ''' Set and get pursuit chart blocks.
        '''
        department = Department.create(name="SR Police Department", short_name="SRPD", load_defaults=False)

        # create & append chart blocks with the expected slugs
        pursuit_intro = ChartBlock(title="INTRO", dataset="intros", slug="pursuits-introduction")
        pursuit_bm = ChartBlock(title="BYMONTH", dataset="bymonth", slug="pursuits-by-month")
        pursuit_bt = ChartBlock(title="BYTEAM", dataset="byteam", slug="pursuits-by-team")
        pursuit_br = ChartBlock(title="BYREASON", dataset="byreason", slug="pursuits-by-reason")
        pursuit_bd = ChartBlock(title="BYDISTANCE", dataset="bydistance", slug="pursuits-by-distance")
        pursuit_bc = ChartBlock(title="BYCONCLUSION", dataset="byconclusion", slug="pursuits-by-conclusion")

        department.chart_blocks.append(pursuit_intro)
        department.chart_blocks.append(pursuit_bm)
        department.chart_blocks.append(pursuit_bt)
        department.chart_blocks.append(pursuit_br)
        department.chart_blocks.append(pursuit_bd)
        department.chart_blocks.append(pursuit_bc)
        department.save()

        # verify that the blocks are returned in the expected structure
        pursuit_blocks = department.get_pursuits_blocks()
        assert pursuit_blocks['introduction'] == pursuit_intro
        assert pursuit_blocks['first-block'] == pursuit_bm
        assert pursuit_blocks['blocks'][0] == pursuit_bt
        assert pursuit_blocks['blocks'][1] == pursuit_br
        assert pursuit_blocks['blocks'][2] == pursuit_bd
        assert pursuit_blocks['blocks'][3] == pursuit_bc

    def test_get_pursuits_schema_blocks(self):
        ''' Set and get pursuit schema chart blocks.
        '''
        department = Department.create(name="SR Police Department", short_name="SRPD", load_defaults=False)

        # create & append chart blocks with the expected slugs
        pursuits_intro = ChartBlock(title="INTRO", dataset="intros", slug="pursuits-schema-introduction")
        pursuits_id = ChartBlock(title="FIELDID", dataset="fid", slug="pursuits-schema-field-id")
        pursuits_od = ChartBlock(title="OCCURREDDATE", dataset="fod", slug="pursuits-schema-field-occurred-date")
        pursuits_div = ChartBlock(title="DIVISION", dataset="div", slug="pursuits-schema-field-division")
        pursuits_dis = ChartBlock(title="DISTRICT", dataset="dis", slug="pursuits-schema-field-district")
        pursuits_shift = ChartBlock(title="SHIFT", dataset="shift", slug="pursuits-schema-field-shift")
        pursuits_footer = ChartBlock(title="FOOTER", dataset="footer", slug="pursuits-schema-footer")
        pursuits_disclaimer = ChartBlock(title="DISCLAIMER", dataset="disclaimer", slug="pursuits-schema-disclaimer")

        department.chart_blocks.append(pursuits_intro)
        department.chart_blocks.append(pursuits_id)
        department.chart_blocks.append(pursuits_od)
        department.chart_blocks.append(pursuits_div)
        department.chart_blocks.append(pursuits_dis)
        department.chart_blocks.append(pursuits_shift)
        department.chart_blocks.append(pursuits_footer)
        department.chart_blocks.append(pursuits_disclaimer)
        department.save()

        # verify that the blocks are returned in the expected structure
        pursuits_blocks = department.get_pursuits_schema_blocks()
        assert pursuits_blocks['introduction'] == pursuits_intro
        assert pursuits_blocks['footer'] == pursuits_footer
        assert pursuits_blocks['disclaimer'] == pursuits_disclaimer
        assert pursuits_id in pursuits_blocks['blocks']
        assert pursuits_od in pursuits_blocks['blocks']
        assert pursuits_div in pursuits_blocks['blocks']
        assert pursuits_dis in pursuits_blocks['blocks']
        assert pursuits_shift in pursuits_blocks['blocks']

    def test_get_dataset_lookup(self):
        ''' The dataset lookup returns usable information
        '''
        # create a department
        department = Department.create(name="SR Police Department", short_name="SRPD", load_defaults=True)

        complaints_lookup = department.get_dataset_lookup("complaints")
        uof_lookup = department.get_dataset_lookup("uof")
        ois_lookup = department.get_dataset_lookup("ois")
        pursuits_lookup = department.get_dataset_lookup("pursuits")

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

        try:
            getattr(department, "is_public_{}".format(ois_lookup["var_suffix"]))
        except AttributeError:
            pytest.fail("Unexpected AttributeError")

        try:
            getattr(department, "is_public_{}".format(pursuits_lookup["var_suffix"]))
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

        try:
            getattr(importlib.import_module("comport.data.models"), "{}{}".format(ois_lookup["class_prefix"], department.short_name))
        except AttributeError:
            pytest.fail("Unexpected AttributeError")

        try:
            getattr(importlib.import_module("comport.data.models"), "{}{}".format(pursuits_lookup["class_prefix"], department.short_name))
        except AttributeError:
            pytest.fail("Unexpected AttributeError")

    def test_dataset_is_public_and_has_data(self):
        ''' We can accurately tell if a dataset is public and has data.
        '''
        # create a department
        department = Department.create(name="SR Police Department", short_name="SRPD", load_defaults=True)

        # none of the datasets have data, so they should all return false
        assert department.dataset_is_public_and_has_data("complaints") == False
        assert department.dataset_is_public_and_has_data("uof") == False
        assert department.dataset_is_public_and_has_data("ois") == False
        assert department.dataset_is_public_and_has_data("pursuits") == False
        # the total count should be zero
        assert department.displayable_dataset_count() == 0

        # create incidents and verify that the datasets are now displayable
        CitizenComplaintSRPD.create(department_id=department.id, opaque_id="12345abcde")
        assert department.dataset_is_public_and_has_data("complaints") == True
        assert department.displayable_dataset_count() == 1

        UseOfForceIncidentSRPD.create(department_id=department.id, opaque_id="23456bcdef")
        assert department.dataset_is_public_and_has_data("uof") == True
        assert department.displayable_dataset_count() == 2

        OfficerInvolvedShootingSRPD.create(department_id=department.id, opaque_id="34567cdefg")
        assert department.dataset_is_public_and_has_data("ois") == True
        assert department.displayable_dataset_count() == 3

        PursuitSRPD.create(department_id=department.id, opaque_id="45678defgh")
        assert department.dataset_is_public_and_has_data("pursuits") == True
        assert department.displayable_dataset_count() == 4

        # now make them all not public, and they should be false again
        department.is_public_citizen_complaints = False
        assert department.dataset_is_public_and_has_data("complaints") == False
        department.is_public_use_of_force_incidents = False
        assert department.dataset_is_public_and_has_data("uof") == False
        department.is_public_officer_involved_shootings = False
        assert department.dataset_is_public_and_has_data("ois") == False
        department.is_public_pursuits = False
        assert department.dataset_is_public_and_has_data("pursuits") == False
        assert department.displayable_dataset_count() == 0
