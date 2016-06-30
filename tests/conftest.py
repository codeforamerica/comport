# -*- coding: utf-8 -*-
"""Defines fixtures available to all tests."""
import pytest
from webtest import TestApp

from comport.settings import TestConfig
from comport.app import create_app
from comport.database import db as _db
from comport.content.models import ChartBlock
from comport.department.models import Department

from .factories import UserFactory, DepartmentFactory


@pytest.yield_fixture(scope='function')
def app():
    _app = create_app(TestConfig)
    ctx = _app.test_request_context()
    ctx.push()

    yield _app

    ctx.pop()


@pytest.fixture(scope='function')
def testapp(app):
    """A Webtest app."""
    return TestApp(app)

@pytest.fixture(scope='function')
def db(app):
    _db.app = app
    _db.drop_all()
    _db.create_all()
    return _db


@pytest.fixture
def user(db):
    department = DepartmentFactory()
    department.save()
    user = UserFactory(password='myprecious')
    user.departments.append(department)
    user.save()
    db.session.commit()
    return user

@pytest.fixture
def preconfigured_department():
    # create a department
    department = Department.create(name="Good Police Department", short_name="GPD", load_defaults=False)

    # create & append assaults chart blocks with the expected slugs
    assaults_intro = ChartBlock(title="INTRO", dataset="intros", slug="assaults-introduction", content="AAAAAAAAAAAAAA")
    assaults_bst = ChartBlock(title="BYSERVICETYPE", dataset="byservicetype", slug="assaults-by-service-type", content="AAAAAAAAAAAAAA")
    assaults_bft = ChartBlock(title="BYFORCETYPE", dataset="byforcetype", slug="assaults-by-force-type", content="AAAAAAAAAAAAAA")
    assaults_bof = ChartBlock(title="BYOFFICER", dataset="byofficer", slug="assaults-by-officer", content="AAAAAAAAAAAAAA")

    department.chart_blocks.append(assaults_intro)
    department.chart_blocks.append(assaults_bst)
    department.chart_blocks.append(assaults_bft)
    department.chart_blocks.append(assaults_bof)

    assaults_schema_intro = ChartBlock(title="INTRO", dataset="intros", slug="assaults-schema-introduction", content="CCCCCCCCCCCCC")
    assaults_schema_footer = ChartBlock(title="FOOTER", dataset="footer", slug="assaults-schema-footer", content="CCCCCCCCCCCCC")
    assaults_schema_disclaimer = ChartBlock(title="DISCLAIMER", dataset="disclaimer", slug="assaults-schema-disclaimer", content="CCCCCCCCCCCCC")

    # define the field blocks
    field_block_slugs = ['id', 'officer-identifier', 'service-type', 'force-type', 'assignment', 'arrest-made', 'officer-injured', 'officer-killed', 'report-filed']
    field_blocks = []
    for slug in field_block_slugs:
        field_blocks.append(ChartBlock(title="{}".format(slug.replace("-", " ").upper()), dataset=slug.replace("-", ""), slug="assaults-schema-field-{}".format(slug), content="CCCCCCCCCCCCC"))

    department.chart_blocks.append(assaults_schema_intro)
    department.chart_blocks.append(assaults_schema_footer)
    department.chart_blocks.append(assaults_schema_disclaimer)
    for block in field_blocks:
        department.chart_blocks.append(block)

    # create & append complaint chart blocks with the expected slugs
    complaint_intro = ChartBlock(title="INTRO", dataset="intros", slug="complaints-introduction", content="BBBBBBBBBBBBB")
    complaint_bm = ChartBlock(title="BYMONTH", dataset="bymonth", slug="complaints-by-month", content="BBBBBBBBBBBBB")
    complaint_bya = ChartBlock(title="BYALLEGATION", dataset="bya", slug="complaints-by-allegation", content="BBBBBBBBBBBBB")
    complaint_byat = ChartBlock(title="BYALLEGATIONTYPE", dataset="byat", slug="complaints-by-allegation-type", content="BBBBBBBBBBBBB")
    complaint_bdis = ChartBlock(title="BYDISPOSITION", dataset="bdis", slug="complaints-by-disposition", content="BBBBBBBBBBBBB")
    complaint_bpre = ChartBlock(title="BYPRECINCT", dataset="bpre", slug="complaints-by-precinct", content="BBBBBBBBBBBBB")
    complaint_od = ChartBlock(title="OFFICERDEMOS", dataset="od", slug="officer-demographics", content="BBBBBBBBBBBBB")
    complaint_bde = ChartBlock(title="BYDEMO", dataset="bde", slug="complaints-by-demographic", content="BBBBBBBBBBBBB")
    complaint_bof = ChartBlock(title="BYOFFICER", dataset="bof", slug="complaints-by-officer", content="BBBBBBBBBBBBB")

    department.chart_blocks.append(complaint_intro)
    department.chart_blocks.append(complaint_bm)
    department.chart_blocks.append(complaint_bya)
    department.chart_blocks.append(complaint_byat)
    department.chart_blocks.append(complaint_bdis)
    department.chart_blocks.append(complaint_bpre)
    department.chart_blocks.append(complaint_od)
    department.chart_blocks.append(complaint_bde)
    department.chart_blocks.append(complaint_bof)

    complaint_schema_intro = ChartBlock(title="INTRO", dataset="intros", slug="complaints-schema-introduction", content="CCCCCCCCCCCCC")
    complaint_schema_footer = ChartBlock(title="FOOTER", dataset="footer", slug="complaints-schema-footer", content="CCCCCCCCCCCCC")
    complaint_schema_disclaimer = ChartBlock(title="DISCLAIMER", dataset="disclaimer", slug="complaints-schema-disclaimer", content="CCCCCCCCCCCCC")

    # define the field blocks
    field_block_slugs = ['id', 'occured-date', 'division', 'district', 'shift']
    field_blocks = []
    for slug in field_block_slugs:
        field_blocks.append(ChartBlock(title="{}".format(slug.replace("-", " ").upper()), dataset=slug.replace("-", ""), slug="complaints-schema-field-{}".format(slug), content="CCCCCCCCCCCCC"))

    department.chart_blocks.append(complaint_schema_intro)
    department.chart_blocks.append(complaint_schema_footer)
    department.chart_blocks.append(complaint_schema_disclaimer)
    for block in field_blocks:
        department.chart_blocks.append(block)

    # create & append use of force chart blocks with the expected slugs
    uof_intro = ChartBlock(title="INTRO", dataset="intros", slug="uof-introduction", content="CCCCCCCCCCCCCC")
    uof_ft = ChartBlock(title="FORCETYPE", dataset="forcetype", slug="uof-force-type", content="CCCCCCCCCCCCCC")
    uof_bid = ChartBlock(title="BYINCDISTRICT", dataset="bid", slug="uof-by-inc-district", content="CCCCCCCCCCCCCC")
    uof_od = ChartBlock(title="OFFICERDEMOS", dataset="od", slug="officer-demographics", content="CCCCCCCCCCCCCC")
    uof_race = ChartBlock(title="RACE", dataset="race", slug="uof-race", content="CCCCCCCCCCCCCC")

    department.chart_blocks.append(uof_intro)
    department.chart_blocks.append(uof_ft)
    department.chart_blocks.append(uof_bid)
    department.chart_blocks.append(uof_od)
    department.chart_blocks.append(uof_race)

    uof_schema_intro = ChartBlock(title="INTRO", dataset="intros", slug="uof-schema-introduction", content="CCCCCCCCCCCCC")
    uof_schema_footer = ChartBlock(title="FOOTER", dataset="footer", slug="uof-schema-footer", content="CCCCCCCCCCCCC")
    uof_schema_disclaimer = ChartBlock(title="DISCLAIMER", dataset="disclaimer", slug="uof-schema-disclaimer", content="CCCCCCCCCCCCC")

    # define the field blocks
    field_block_slugs = ['id', 'occurred-date', 'division', 'district', 'shift', 'beat', 'use-of-force-reason', 'office-force-type', 'disposition', 'service-type', 'arrest-made', 'arrest-charges', 'resident-injured', 'resident-hospitalized', 'resident-condition', 'officer-injured', 'officer-hospitalized', 'officer-condition', 'resident-race', 'resident-sex', 'resident-age', 'officer-race', 'officer-sex', 'officer-age', 'officer-years-of-service', 'officer-identifier']
    field_blocks = []
    for slug in field_block_slugs:
        field_blocks.append(ChartBlock(title="{}".format(slug.replace("-", " ").upper()), dataset=slug.replace("-", ""), slug="uof-schema-field-{}".format(slug), content="CCCCCCCCCCCCC"))

    department.chart_blocks.append(uof_schema_intro)
    department.chart_blocks.append(uof_schema_footer)
    department.chart_blocks.append(uof_schema_disclaimer)
    for block in field_blocks:
        department.chart_blocks.append(block)

    # create & append officer involved shooting chart blocks with the expected slugs
    ois_intro = ChartBlock(title="INTRO", dataset="intros", slug="ois-introduction", content="DDDDDDDDDDDDDDD")
    ois_bid = ChartBlock(title="BYINCDISTRICT", dataset="bid", slug="ois-by-inc-district", content="DDDDDDDDDDDDDDD")
    ois_wt = ChartBlock(title="WEAPONTYPE", dataset="weapontype", slug="ois-weapon-type", content="DDDDDDDDDDDDDDD")
    ois_od = ChartBlock(title="OFFICERDEMOS", dataset="od", slug="officer-demographics", content="DDDDDDDDDDDDDDD")
    ois_race = ChartBlock(title="RACE", dataset="race", slug="ois-race", content="DDDDDDDDDDDDDDD")

    department.chart_blocks.append(ois_intro)
    department.chart_blocks.append(ois_bid)
    department.chart_blocks.append(ois_wt)
    department.chart_blocks.append(ois_od)
    department.chart_blocks.append(ois_race)

    department.save()
    return department, assaults_intro
