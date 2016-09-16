# -*- coding: utf-8 -*-
import pytest
import datetime
import csv
import io
from comport.content.models import ChartBlock
from comport.department.models import Department
from comport.data.models import UseOfForceIncidentLMPD

@pytest.mark.usefixtures('db')
class TestDepartmentModelLMPD:

    def test_get_complaint_blocks(self):
        ''' Set and get complaint chart blocks.
        '''
        department = Department.create(name="LM Police Department", short_name="LMPD", load_defaults=False)

        # create & append chart blocks with the expected slugs
        complaint_intro = ChartBlock(title="INTRO", dataset="intros", slug="complaints-introduction")
        complaint_bm = ChartBlock(title="BYMONTH", dataset="bymonth", slug="complaints-by-month")
        complaint_bya = ChartBlock(title="BYALLEGATION", dataset="bya", slug="complaints-by-allegation")
        complaint_byat = ChartBlock(title="BYALLEGATIONTYPE", dataset="byat", slug="complaints-by-allegation-type")
        complaint_bdis = ChartBlock(title="BYDISPOSITION", dataset="bdis", slug="complaints-by-finding")
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

    def test_get_complaint_schema_blocks(self):
        ''' Set and get complaint schema chart blocks.
        '''
        department = Department.create(name="LM Police Department", short_name="LMPD", load_defaults=False)

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
        department = Department.create(name="LM Police Department", short_name="LMPD", load_defaults=False)

        # create & append chart blocks with the expected slugs
        uof_intro = ChartBlock(title="INTRO", dataset="intros", slug="uof-introduction")
        uof_bm = ChartBlock(title="BYMONTH", dataset="bymonth", slug="uof-by-month")
        uof_ft = ChartBlock(title="FORCETYPE", dataset="forcetype", slug="uof-force-type")
        uof_bd = ChartBlock(title="BYDIVISION", dataset="bd", slug="uof-by-division")
        uof_od = ChartBlock(title="OFFICERDEMOS", dataset="od", slug="officer-demographics")
        uof_race = ChartBlock(title="RACE", dataset="race", slug="uof-race")
        department.chart_blocks.append(uof_intro)
        department.chart_blocks.append(uof_bm)
        department.chart_blocks.append(uof_ft)
        department.chart_blocks.append(uof_bd)
        department.chart_blocks.append(uof_od)
        department.chart_blocks.append(uof_race)
        department.save()

        # verify that the blocks are returned in the expected structure
        uof_blocks = department.get_uof_blocks()
        assert uof_blocks['introduction'] == uof_intro
        assert uof_blocks['first-block'] == uof_bm
        assert uof_blocks['blocks'][0] == uof_ft
        assert uof_blocks['blocks'][1] == uof_bd
        assert uof_blocks['blocks'][2] == uof_od
        assert uof_blocks['blocks'][3] == uof_race

    def test_get_uof_schema_blocks(self):
        ''' Set and get uof schema chart blocks.
        '''
        department = Department.create(name="LM Police Department", short_name="LMPD", load_defaults=False)

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
        department = Department.create(name="LM Police Department", short_name="LMPD", load_defaults=False)

        # create & append chart blocks with the expected slugs
        ois_intro = ChartBlock(title="INTRO", dataset="intros", slug="ois-introduction")
        ois_bid = ChartBlock(title="BYASSIGNMENT", dataset="bid", slug="ois-by-inc-district")
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

    def test_get_ois_schema_blocks(self):
        ''' Set and get ois schema chart blocks.
        '''
        department = Department.create(name="LM Police Department", short_name="LMPD", load_defaults=False)

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

    def test_get_assaults_blocks(self):
        ''' Set and get ois chart blocks.
        '''
        department = Department.create(name="LM Police Department", short_name="LMPD", load_defaults=False)

        # create & append chart blocks with the expected slugs
        assault_intro = ChartBlock(title="INTRO", dataset="intros", slug="assaults-introduction")
        assault_bst = ChartBlock(title="BYINCDISTRICT", dataset="bst", slug="assaults-by-service-type")
        assault_bft = ChartBlock(title="WEAPONTYPE", dataset="bft", slug="assaults-by-force-type")
        assault_bo = ChartBlock(title="OFFICERDEMOS", dataset="bo", slug="assaults-by-officer")
        department.chart_blocks.append(assault_intro)
        department.chart_blocks.append(assault_bst)
        department.chart_blocks.append(assault_bft)
        department.chart_blocks.append(assault_bo)
        department.save()

        # verify that the blocks are returned in the expected structure
        assault_blocks = department.get_assaults_blocks()
        assert assault_blocks['introduction'] == assault_intro
        assert assault_blocks['first-block'] == assault_bst
        assert assault_blocks['blocks'][0] == assault_bft
        assert assault_blocks['blocks'][1] == assault_bo

    def test_get_assaults_schema_blocks(self):
        ''' Set and get assaults schema chart blocks.
        '''
        department = Department.create(name="LM Police Department", short_name="LMPD", load_defaults=False)

        # create & append chart blocks with the expected slugs
        assaults_intro = ChartBlock(title="INTRO", dataset="intros", slug="assaults-schema-introduction")
        assaults_fid = ChartBlock(title="FIELDID", dataset="fid", slug="assaults-schema-field-id")
        assaults_foi = ChartBlock(title="OCCURREDDATE", dataset="fod", slug="assaults-schema-field-officer-identifier")
        assaults_fst = ChartBlock(title="DIVISION", dataset="div", slug="assaults-schema-field-service-type")
        assaults_fft = ChartBlock(title="DISTRICT", dataset="dis", slug="assaults-schema-field-force-type")
        assaults_ffa = ChartBlock(title="SHIFT", dataset="shift", slug="assaults-schema-field-assignment")
        assaults_footer = ChartBlock(title="FOOTER", dataset="footer", slug="assaults-schema-footer")
        assaults_disclaimer = ChartBlock(title="DISCLAIMER", dataset="disclaimer", slug="assaults-schema-disclaimer")

        department.chart_blocks.append(assaults_intro)
        department.chart_blocks.append(assaults_fid)
        department.chart_blocks.append(assaults_foi)
        department.chart_blocks.append(assaults_fst)
        department.chart_blocks.append(assaults_fft)
        department.chart_blocks.append(assaults_ffa)
        department.chart_blocks.append(assaults_footer)
        department.chart_blocks.append(assaults_disclaimer)
        department.save()

        # verify that the blocks are returned in the expected structure
        assaults_blocks = department.get_assaults_schema_blocks()
        assert assaults_blocks['introduction'] == assaults_intro
        assert assaults_blocks['footer'] == assaults_footer
        assert assaults_blocks['disclaimer'] == assaults_disclaimer
        assert assaults_fid in assaults_blocks['blocks']
        assert assaults_foi in assaults_blocks['blocks']
        assert assaults_fst in assaults_blocks['blocks']
        assert assaults_fft in assaults_blocks['blocks']
        assert assaults_ffa in assaults_blocks['blocks']

    def test_csv_response(self, testapp):
        # create a department and an LMPD uof incident
        department = Department.create(name="LM Police Department", short_name="LMPD", load_defaults=False)

        uof_check = dict(department_id=department.id, opaque_id="Check Opaque ID", occured_date=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), bureau="Check Bureau", division="Check Division", unit="Check Unit", platoon="Check Platoon", disposition="Check Disposition", use_of_force_reason="Check UOF Reason", officer_force_type="Check Officer Force Type", service_type="Check Service Type", arrest_made=False, arrest_charges="Check Arrest Charges", resident_injured=True, resident_hospitalized=False, resident_condition="Check Resident Condition", officer_injured=False, officer_hospitalized=False, officer_condition="Check Officer Condition", resident_identifier="Check Resident Identifier", resident_weapon_used="Check Resident Weapon Used", resident_race="Check Resident Race", resident_sex="Check Resident Sex", resident_age="Check Resident Age", officer_race="Check Officer Race", officer_sex="Check Officer Sex", officer_age="Check Officer Age", officer_years_of_service="Check Officer Years Of Service", officer_identifier="Check Officer Identifier")

        UseOfForceIncidentLMPD.create(**uof_check)

        response = testapp.get("/department/{}/uof.csv".format(department.id))

        incidents = list(csv.DictReader(io.StringIO(response.text)))

        # build a variable to csv header lookup from the csv schema
        csv_schema = UseOfForceIncidentLMPD.get_csv_schema()
        schema_lookup = dict(zip([col[1] for col in csv_schema], [col[0] for col in csv_schema]))

        assert len(incidents) == 1
        for check_key in uof_check.keys():
            if check_key == 'department_id':
                continue
            assert str(uof_check[check_key]) == incidents[0][schema_lookup[check_key]]
