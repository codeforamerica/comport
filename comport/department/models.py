# -*- coding: utf-8 -*-
from comport.database import (Column, db, Model, relationship, SurrogatePK)
from comport.content.defaults import ChartBlockDefaults

from comport.utils import coalesce_date
from comport.user.models import User, Role
import csv
import io
import json
import copy

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
    invite_codes = relationship("Invite_Code", backref="department")
    users = relationship("User", secondary=user_department_relationship_table, backref="departments")
    use_of_force_incidents = relationship(
        "UseOfForceIncident", backref="department")
    citizen_complaints = relationship("CitizenComplaint", backref="department")
    officer_involved_shootings = relationship(
        "OfficerInvolvedShooting", backref="department")
    chart_blocks = relationship("ChartBlock", backref="department")
    denominator_values = relationship("DenominatorValue", backref="department")
    demographic_values = relationship("DemographicValue", backref="department")

    def __init__(self, name, load_defaults=True, **kwargs):
        db.Model.__init__(self, name=name, **kwargs)
        if load_defaults:
            for default_chart_block in ChartBlockDefaults.defaults:
                self.chart_blocks.append(copy.deepcopy(default_chart_block))
            self.save()

    def get_uof_blocks(self):
        return {
            'introduction': self.get_block_by_slug('uof-introduction'),
            'first-block': self.get_block_by_slug('uof-force-type'),
            'blocks': self.get_blocks_by_slugs([
                'uof-by-inc-district',
                'officer-demographics',
                'uof-race'
            ])
        }

    def get_ois_blocks(self):
        return {
            'introduction': self.get_block_by_slug('ois-introduction'),
            'first-block': self.get_block_by_slug('ois-by-inc-district'),
            'blocks': self.get_blocks_by_slugs([
                'ois-weapon-type',
                'officer-demographics',
                'ois-race',
            ])
        }

    def get_complaint_blocks(self):
        return {
            'introduction': self.get_block_by_slug('complaints-introduction'),
            'first-block': self.get_block_by_slug('complaints-by-month'),
            'blocks': self.get_blocks_by_slugs([
                'complaints-by-allegation',
                'complaints-by-allegation-type',
                'complaints-by-disposition',
                'complaints-by-precinct',
                'officer-demographics',
                'complaints-by-demographic',
                'complaints-by-officer',
            ])
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
        return next(b for b in self.chart_blocks if b.slug == slug)

    def get_blocks_by_slugs(self, slugs):
        return [b for b in self.chart_blocks if b.slug in slugs]

    def __repr__(self):
        return '<Department({name})>'.format(name=self.name)

    def get_uof_csv(self):
        output = io.StringIO()

        writer = csv.writer(output, quoting=csv.QUOTE_NONNUMERIC)

        writer.writerow(["id", "occurredDate", "division", "district", "shift", "beat",
                         "useOfForceReason", "officerForceType", "disposition",
                         "serviceType", "arrestMade", "arrestCharges", "residentInjured",
                         "residentHospitalized", "residentCondition", "officerInjured",
                         "officerHospitalized", "officerCondition", "residentRace",
                         "residentSex", "residentAge", "officerRace", "officerSex",
                         "officerAge", "officerYearsOfService", "officerIdentifier"])

        use_of_force_incidents = self.use_of_force_incidents

        for incident in use_of_force_incidents:
            occured_date = coalesce_date(incident.occured_date)
            values = [
                incident.opaque_id,
                occured_date,
                incident.division,
                incident.precinct,
                incident.shift,
                incident.beat,
                incident.use_of_force_reason,
                incident.officer_force_type,
                incident.disposition,
                incident.service_type,
                incident.arrest_made,
                incident.arrest_charges,
                incident.resident_injured,
                incident.resident_hospitalized,
                incident.resident_condition,
                incident.officer_injured,
                incident.officer_hospitalized,
                incident.officer_condition,
                incident.resident_race,
                incident.resident_sex,
                incident.resident_age,
                incident.officer_race,
                incident.officer_sex,
                incident.officer_age,
                incident.officer_years_of_service,
                incident.officer_identifier
            ]
            writer.writerow(values)

        return output.getvalue()

    def get_ois_csv(self):
        output = io.StringIO()

        writer = csv.writer(output, quoting=csv.QUOTE_NONNUMERIC)

        writer.writerow(["id", "occurredDate", "division", "district", "shift", "beat",
                         "disposition", "residentWeaponUsed", "officerWeaponUsed",
                         "serviceType", "residentCondition", "officerCondition",
                         "residentRace", "residentSex", "residentAge", "officerRace",
                         "officerSex", "officerAge", "officerYearsOfService",
                         "officerIdentifier"])

        officer_involved_shootings = self.officer_involved_shootings
        for incident in officer_involved_shootings:
            occured_date = coalesce_date(incident.occured_date)
            values = [
                incident.opaque_id,
                occured_date,
                incident.division,
                incident.precinct,
                incident.shift,
                incident.beat,
                incident.disposition,
                incident.resident_weapon_used,
                incident.officer_weapon_used,
                incident.service_type,
                incident.resident_condition,
                incident.officer_condition,
                incident.resident_race,
                incident.resident_sex,
                incident.resident_age,
                incident.officer_race,
                incident.officer_sex,
                incident.officer_age,
                incident.officer_years_of_service,
                incident.officer_identifier
            ]
            writer.writerow(values)

        return output.getvalue()

    def get_complaint_csv(self):
        output = io.StringIO()

        writer = csv.writer(output, quoting=csv.QUOTE_NONNUMERIC)

        writer.writerow(["id", "occurredDate", "division", "district", "shift",
                         "beat", "serviceType", "source", "allegationType",
                         "allegation", "finding", "residentRace", "residentSex",
                         "residentAge", "officerRace", "officerSex", "officerAge",
                         "officerYearsOfService", "officerIdentifier"])

        complaints = self.citizen_complaints

        for complaint in complaints:
            occured_date = coalesce_date(complaint.occured_date)
            values = [
                complaint.opaque_id,
                occured_date,
                complaint.division,
                complaint.precinct,
                complaint.shift,
                complaint.beat,
                complaint.service_type,
                complaint.source,
                complaint.allegation_type,
                complaint.allegation,
                complaint.disposition,
                complaint.resident_race,
                complaint.resident_sex,
                complaint.resident_age,
                complaint.officer_race,
                complaint.officer_sex,
                complaint.officer_age,
                complaint.officer_years_of_service,
                complaint.officer_identifier
            ]
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
