# -*- coding: utf-8 -*-
from comport.database import (Column, db, Model, relationship, SurrogatePK)
from comport.content.defaults import ChartBlockDefaults
from .page_block_lookup import PageBlockLookup
from flask import abort
from comport.utils import coalesce_date
from comport.user.models import User, Role
from comport.content.models import ChartBlock
import csv
import io
import json
import copy
import importlib

user_department_relationship_table = db.Table(
    'user_department_relationship_table',
    db.Column('department_id', db.Integer, db.ForeignKey('departments.id'), nullable=False),
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'), nullable=False),
    db.PrimaryKeyConstraint('department_id', 'user_id')
)

class Department(SurrogatePK, Model):
    __tablename__ = 'departments'
    id = Column(db.Integer, primary_key=True, index=True)
    name = Column(db.String(80), unique=True, nullable=False)
    short_name = Column(db.String(80), unique=True, nullable=False)
    is_public = Column(db.Boolean, default=True, nullable=False)
    is_public_use_of_force_incidents = Column(db.Boolean, default=True, nullable=False)
    is_public_citizen_complaints = Column(db.Boolean, default=True, nullable=False)
    is_public_officer_involved_shootings = Column(db.Boolean, default=True, nullable=False)
    is_public_assaults_on_officers = Column(db.Boolean, default=True, nullable=False)
    invite_codes = relationship("Invite_Code", backref="department")
    users = relationship("User", secondary=user_department_relationship_table, backref="departments")
    chart_blocks = relationship("ChartBlock", backref="department")
    denominator_values = relationship("DenominatorValue", backref="department")
    demographic_values = relationship("DemographicValue", backref="department")

    def __init__(self, name, load_defaults=True, **kwargs):
        db.Model.__init__(self, name=name, **kwargs)
        if load_defaults:
            for default_chart_block in ChartBlockDefaults.defaults:
                self.chart_blocks.append(copy.deepcopy(default_chart_block))
            self.save()

    @classmethod
    def get_dataset_lookup(cls, dataset_name):
        ''' Look up the name for particular aspects of a dataset.
        '''
        lookup = [
            {"in": ["complaints", "citizen_complaints"], "var_suffix": "citizen_complaints", "class_prefix": "CitizenComplaint", "path": "department.public_complaints"},
            {"in": ["uof", "use_of_force_incidents"], "var_suffix": "use_of_force_incidents", "class_prefix": "UseOfForceIncident", "path": "department.public_uof"},
            {"in": ["ois", "officer_involved_shootings"], "var_suffix": "officer_involved_shootings", "class_prefix": "OfficerInvolvedShooting", "path": "department.public_ois"},
            {"in": ["assaults", "assaults_on_officers"], "var_suffix": "assaults_on_officers", "class_prefix": "AssaultOnOfficer", "path": "department.public_assaults"}
        ]

        found = False
        for check in lookup:
            if dataset_name in check["in"]:
                var_suffix = check["var_suffix"]
                class_prefix = check["class_prefix"]
                path = check["path"]
                found = True
                break

        if not found:
            return {}

        return {"var_suffix": var_suffix, "class_prefix": class_prefix, "path": path}

    def dataset_is_public_and_has_data(self, dataset_name):
        ''' Return true if the dataset is public and has data.
        '''
        # look up what dataset we're looking for
        lookup = self.get_dataset_lookup(dataset_name)

        # if we didn't recognize it, just return false
        if not lookup:
            return False

        # get the current is_public value
        is_public = getattr(self, "is_public_{}".format(lookup["var_suffix"]))

        # check to see whether the model exists
        try:
            model_class = getattr(importlib.import_module("comport.data.models"), "{}{}".format(lookup["class_prefix"], self.short_name))
        except AttributeError:
            # this department doesn't have this dataset
            return False

        # check to see whether there's data in the dataset
        first_record = model_class.query.first()

        return (is_public and first_record is not None)

    def get_uof_blocks(self):
        blocks = PageBlockLookup.get_uof_blocks(self.short_name)
        return {
            'introduction': self.get_block_by_slug(blocks['introduction']),
            'first-block': self.get_block_by_slug(blocks['first-block']),
            'blocks': self.get_blocks_by_slugs(blocks['blocks'])
        }

    def get_ois_blocks(self):
        blocks = PageBlockLookup.get_ois_blocks(self.short_name)
        return {
            'introduction': self.get_block_by_slug(blocks['introduction']),
            'first-block': self.get_block_by_slug(blocks['first-block']),
            'blocks': self.get_blocks_by_slugs(blocks['blocks'])
        }

    def get_complaint_blocks(self):
        blocks = PageBlockLookup.get_complaints_blocks(self.short_name)
        return {
            'introduction': self.get_block_by_slug(blocks['introduction']),
            'first-block': self.get_block_by_slug(blocks['first-block']),
            'blocks': self.get_blocks_by_slugs(blocks['blocks'])
        }

    def get_assaults_blocks(self):
        blocks = PageBlockLookup.get_assaults_blocks(self.short_name)
        return {
            'introduction': self.get_block_by_slug(blocks['introduction']),
            'first-block': self.get_block_by_slug(blocks['first-block']),
            'blocks': self.get_blocks_by_slugs(blocks['blocks'])
        }

    def get_complaint_schema_blocks(self):
        blocks = PageBlockLookup.get_complaint_schema_blocks(self.short_name)
        return {
            'introduction': self.get_block_by_slug(blocks['introduction']),
            'footer': self.get_block_by_slug(blocks['footer']),
            'disclaimer': self.get_block_by_slug(blocks['disclaimer']),
            'blocks': self.get_blocks_by_slug_startswith(blocks['blocks'])
        }

    def get_uof_schema_blocks(self):
        blocks = PageBlockLookup.get_uof_schema_blocks(self.short_name)
        return {
            'introduction': self.get_block_by_slug(blocks['introduction']),
            'footer': self.get_block_by_slug(blocks['footer']),
            'disclaimer': self.get_block_by_slug(blocks['disclaimer']),
            'blocks': self.get_blocks_by_slug_startswith(blocks['blocks'])
        }

    def get_ois_schema_blocks(self):
        blocks = PageBlockLookup.get_ois_schema_blocks(self.short_name)
        return {
            'introduction': self.get_block_by_slug(blocks['introduction']),
            'footer': self.get_block_by_slug(blocks['footer']),
            'disclaimer': self.get_block_by_slug(blocks['disclaimer']),
            'blocks': self.get_blocks_by_slug_startswith(blocks['blocks'])
        }

    def get_assaults_schema_blocks(self):
        blocks = PageBlockLookup.get_assaults_schema_blocks(self.short_name)
        return {
            'introduction': self.get_block_by_slug(blocks['introduction']),
            'footer': self.get_block_by_slug(blocks['footer']),
            'disclaimer': self.get_block_by_slug(blocks['disclaimer']),
            'blocks': self.get_blocks_by_slug_startswith(blocks['blocks'])
        }

    def get_introduction_blocks(self):
        return dict([(block.slug, block) for block in self.chart_blocks if block.dataset in ["introduction"]])

    def get_raw_department_demographics(self):
        return [v for v in self.demographic_values if v.department_value]

    def get_raw_city_demographics(self):
        return [v for v in self.demographic_values if not v.department_value]

    def get_city_demographics(self):
        result = []
        demographic_values = [
            v for v in self.demographic_values if not v.department_value]

        total = 0

        for value in demographic_values:
            total += value.count

        for value in demographic_values:
            result.append({
                "gender": value.gender,
                "race": value.race,
                "count": value.count,
                "percent": "{0:.0f}%".format(value.count / total * 100)
            })
        return result

    def serialize_demographics(self):
        results = []
        for v in self.demographic_values:
            results.append({
                'race': v.race,
                'count': v.count,
                'entity': 'department' if v.department_value else 'city'
            })
        return json.dumps(results)

    def get_extractor(self):
        extractors = list(filter(lambda u: u.type == "extractors", self.users))
        return extractors[0] if extractors else None

    def get_block_by_slug(self, slug):
        next_block = None
        try:
            next_block = next(b for b in self.chart_blocks if b.slug == slug)
        except StopIteration:
            # no matching chart block was found
            return None

        return next_block

    def get_blocks_by_slugs(self, slugs, sort_by_order=False):
        ''' Get chart blocks matching the passed list of slugs
        '''
        arr = []
        if sort_by_order:
            arr = [b for b in self.chart_blocks if b.slug in slugs]
            try:
                arr.sort(key=lambda k: k.order)
            except TypeError:
                pass

        # return the blocks in the order the slugs were passed
        else:
            for b in slugs:
                block = ChartBlock.query.filter_by(department_id=self.id, slug=b).first()
                if block:
                    arr.append(block)

        return arr

    def get_blocks_by_slug_startswith(self, partial_slug):
        arr = [b for b in self.chart_blocks if b.slug.startswith(partial_slug)]
        try:
            arr.sort(key=lambda k: k.order)
        except TypeError:
            pass
        return arr

    def __repr__(self):
        return '<Department({name})>'.format(name=self.name)

    def get_first_dataset_path(self):
        ''' Return a string representing the path to the first existing dataset page for this department.
            For use in url_for calls.
        '''
        datasets = ["complaints", "uof", "ois", "assaults"]
        for check in datasets:
            lookup = self.get_dataset_lookup(check)
            # if there's a class for this dataset, return its path
            try:
                getattr(importlib.import_module("comport.data.models"), "{}{}".format(lookup["class_prefix"], self.short_name))
            except AttributeError:
                continue
            else:
                return lookup["path"]

        # no dataset classes were found
        return None

    def get_uof_csv(self):
        output = io.StringIO()

        writer = csv.writer(output, quoting=csv.QUOTE_NONNUMERIC)

        uof_class = getattr(importlib.import_module("comport.data.models"), "UseOfForceIncident{}".format(self.short_name))

        csv_schema = uof_class.get_csv_schema()
        csv_headers = [col[0] for col in csv_schema]
        csv_vars = [col[1] for col in csv_schema]

        writer.writerow(csv_headers)

        use_of_force_incidents = uof_class.query.all()

        for incident in use_of_force_incidents:
            values = []
            for incident_var in csv_vars:
                incident_value = getattr(incident, incident_var)
                if incident_var == "occured_date":
                    incident_value = coalesce_date(incident_value)
                values.append(incident_value)

            writer.writerow(values)

        return output.getvalue()

    def get_ois_csv(self):
        output = io.StringIO()

        writer = csv.writer(output, quoting=csv.QUOTE_NONNUMERIC)

        ois_class = getattr(importlib.import_module("comport.data.models"), "OfficerInvolvedShooting{}".format(self.short_name))

        csv_schema = ois_class.get_csv_schema()
        csv_headers = [col[0] for col in csv_schema]
        csv_vars = [col[1] for col in csv_schema]

        writer.writerow(csv_headers)

        officer_involved_shootings = ois_class.query.all()

        for incident in officer_involved_shootings:
            values = []
            for incident_var in csv_vars:
                incident_value = getattr(incident, incident_var)
                if incident_var == "occured_date":
                    incident_value = coalesce_date(incident_value)
                values.append(incident_value)

            writer.writerow(values)

        return output.getvalue()

    def get_complaint_csv(self):
        output = io.StringIO()

        writer = csv.writer(output, quoting=csv.QUOTE_NONNUMERIC)

        complaint_class = getattr(importlib.import_module("comport.data.models"), "CitizenComplaint{}".format(self.short_name))

        csv_schema = complaint_class.get_csv_schema()
        csv_headers = [col[0] for col in csv_schema]
        csv_vars = [col[1] for col in csv_schema]

        writer.writerow(csv_headers)

        complaints = complaint_class.query.all()

        for complaint in complaints:
            values = []
            for incident_var in csv_vars:
                incident_value = getattr(complaint, incident_var)
                if incident_var == "occured_date":
                    incident_value = coalesce_date(incident_value)
                values.append(incident_value)

            writer.writerow(values)

        return output.getvalue()

    def get_assaults_csv(self):
        output = io.StringIO()

        writer = csv.writer(output, quoting=csv.QUOTE_NONNUMERIC)

        assaults_class = getattr(importlib.import_module("comport.data.models"), "AssaultOnOfficer{}".format(self.short_name))

        csv_schema = assaults_class.get_csv_schema()
        csv_headers = [col[0] for col in csv_schema]
        csv_vars = [col[1] for col in csv_schema]

        writer.writerow(csv_headers)

        incidents = assaults_class.query.all()

        for incident in incidents:
            values = []
            for incident_var in csv_vars:
                incident_value = getattr(incident, incident_var)
                if incident_var == "occured_date":
                    incident_value = coalesce_date(incident_value)
                values.append(incident_value)

            writer.writerow(values)

        return output.getvalue()

    def get_demographic_csv(self):
        output = io.StringIO()

        writer = csv.writer(output, quoting=csv.QUOTE_NONNUMERIC)

        writer.writerow(["race", "count", "cityOrDepartment"])

        values = sorted(self.demographic_values,
                        key=lambda x: (x.department_value, x.race))

        for value in values:
            cityOrDepartment = "department" if value.department_value else "city"
            row = [
                value.race,
                value.count,
                cityOrDepartment
            ]
            writer.writerow(row)

        return output.getvalue()

    def get_denominator_csv(self):
        output = io.StringIO()

        writer = csv.writer(output, quoting=csv.QUOTE_NONNUMERIC)

        writer.writerow(["year", "month", "officers out on service"])

        values = sorted(self.denominator_values,
                        key=lambda x: (x.year, x.month))

        for value in values:
            row = [
                value.year,
                value.month,
                value.officers_out_on_service
            ]
            writer.writerow(row)

        return output.getvalue()


class Extractor(User):
    __tablename__ = 'extractors'
    id = Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    next_month = Column(db.Integer)
    next_year = Column(db.Integer)
    last_contact = Column(db.DateTime)

    __mapper_args__ = {
        'polymorphic_identity': 'extractors',
        'inherit_condition': (id == User.id)
    }

    def generate_envs(self, password):
        return """
            COMPORT_USERNAME="%s"
            COMPORT_PASSWORD="%s"
        """ % (self.username, password,)

    def from_department_and_password(department, password):
        extractor = Extractor.create(username='%s-extractor' % department.name.replace(
            " ", "_"), email='extractor@example.com', password=password)
        extractor.departments.append(department)
        extractor.roles.append(Role.create(name="extractor"))
        extractor.save()

        envs = extractor.generate_envs(password)

        return (extractor, envs)
