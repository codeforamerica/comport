# -*- coding: utf-8 -*-
from comport.database import (Column, db, Model, SurrogatePK)
from .cleaners import Cleaners
from comport.utils import parse_date, parse_int

class DenominatorValue(SurrogatePK, Model):
    __tablename__ = "denominator_values"
    department_id = Column(db.Integer, db.ForeignKey('departments.id'), nullable=False)
    month = Column(db.Integer, unique=False, nullable=False)
    year = Column(db.Integer, unique=False, nullable=False)
    officers_out_on_service = Column(db.Integer, unique=False, nullable=True)

    def __init__(self, **kwargs):
        db.Model.__init__(self, **kwargs)

class DemographicValue(SurrogatePK, Model):
    __tablename__ = "demographic_values"
    department_id = Column(db.Integer, db.ForeignKey('departments.id'), nullable=False)
    race = Column(db.String(255), unique=False, nullable=True)
    count = Column(db.Integer, unique=False, nullable=True)
    department_value = Column(db.Boolean, nullable=True)

    def __init__(self, **kwargs):
        db.Model.__init__(self, **kwargs)

#
# INDIANAPOLIS METRO POLICE DEPARTMENT
#

class UseOfForceIncidentIMPD(SurrogatePK, Model):
    __tablename__ = 'use_of_force_incidents_impd'
    department_id = Column(db.Integer, db.ForeignKey('departments.id'), nullable=False)
    opaque_id = Column(db.String(255), unique=False, nullable=False)
    occured_date = Column(db.DateTime, nullable=True)
    division = Column(db.String(255), unique=False, nullable=True)
    precinct = Column(db.String(255), unique=False, nullable=True)
    shift = Column(db.String(255), unique=False, nullable=True)
    beat = Column(db.String(255), unique=False, nullable=True)
    disposition = Column(db.String(255), unique=False, nullable=True)
    census_tract = Column(db.String(255), unique=False, nullable=True)
    officer_force_type = Column(db.String(255), unique=False, nullable=True)
    resident_resist_type = Column(db.String(255), unique=False, nullable=True)
    officer_weapon_used = Column(db.String(255), unique=False, nullable=True)
    resident_weapon_used = Column(db.String(255), unique=False, nullable=True)
    service_type = Column(db.String(255), unique=False, nullable=True)
    arrest_made = Column(db.Boolean, nullable=True)
    arrest_charges = Column(db.String(255), unique=False, nullable=True)
    resident_injured = Column(db.Boolean, nullable=True)
    resident_hospitalized = Column(db.Boolean, nullable=True)
    officer_injured = Column(db.Boolean, nullable=True)
    officer_hospitalized = Column(db.Boolean, nullable=True)
    use_of_force_reason = Column(db.String(255), unique=False, nullable=True)
    resident_race = Column(db.String(255), unique=False, nullable=True)
    officer_race = Column(db.String(255), unique=False, nullable=True)
    resident_sex = Column(db.String(255), unique=False, nullable=True)
    officer_sex = Column(db.String(255), unique=False, nullable=True)
    officer_identifier = Column(db.String(255), unique=False, nullable=True)
    officer_years_of_service = Column(db.String(255), unique=False, nullable=True)
    officer_age = Column(db.String(255), unique=False, nullable=True)
    resident_age = Column(db.String(255), unique=False, nullable=True)
    officer_condition = Column(db.String(255), unique=False, nullable=True)
    resident_condition = Column(db.String(255), unique=False, nullable=True)

    def __init__(self, **kwargs):
        db.Model.__init__(self, **kwargs)

    @classmethod
    def get_csv_schema(cls):
        ''' Get the CSV column headers and variable names.
        '''
        return [("id", "opaque_id"), ("occurredDate", "occured_date"), ("division", "division"), ("district", "precinct"), ("shift", "shift"), ("beat", "beat"), ("useOfForceReason", "use_of_force_reason"), ("officerForceType", "officer_force_type"), ("disposition", "disposition"), ("serviceType", "service_type"), ("arrestMade", "arrest_made"), ("arrestCharges", "arrest_charges"), ("residentInjured", "resident_injured"), ("residentHospitalized", "resident_hospitalized"), ("residentCondition", "resident_condition"), ("officerInjured", "officer_injured"), ("officerHospitalized", "officer_hospitalized"), ("officerCondition", "officer_condition"), ("residentRace", "resident_race"), ("residentSex", "resident_sex"), ("residentAge", "resident_age"), ("officerRace", "officer_race"), ("officerSex", "officer_sex"), ("officerAge", "officer_age"), ("officerYearsOfService", "officer_years_of_service"), ("officerIdentifier", "officer_identifier")]

    @classmethod
    def add_or_update_incident(cls, department, incident):
        ''' Add a new UOF incident or update an existing one
        '''
        row_added = False
        # get a cleaner instance
        cleaner = Cleaners()
        # capitalize the location
        incident["division"] = cleaner.capitalize(incident["division"])
        incident["precinct"] = cleaner.capitalize(incident["precinct"])
        incident["shift"] = cleaner.capitalize(incident["shift"])
        incident["beat"] = cleaner.capitalize(incident["beat"])
        # clean force type, race, gender
        incident["officerForceType"] = cleaner.officer_force_type(incident["officerForceType"])
        incident["residentRace"] = cleaner.race(incident["residentRace"])
        incident["residentSex"] = cleaner.sex(incident["residentSex"])
        incident["officerRace"] = cleaner.race(incident["officerRace"])
        incident["officerSex"] = cleaner.sex(incident["officerSex"])
        # make sure values that might've been sent as integers are strings
        incident["residentAge"] = cleaner.number_to_string(incident["residentAge"])
        incident["officerAge"] = cleaner.number_to_string(incident["officerAge"])
        incident["officerYearsOfService"] = cleaner.number_to_string(incident["officerYearsOfService"])

        found_incident = cls.query.filter_by(
            opaque_id=incident["opaqueId"],
            department_id=department.id,
            officer_identifier=incident["officerIdentifier"],
            officer_force_type=incident["officerForceType"]
        ).first()

        if not found_incident:
            found_incident = cls.create(
                department_id=department.id,
                opaque_id=incident["opaqueId"])
            row_added = True

        found_incident.department_id = department.id
        found_incident.opaque_id = incident["opaqueId"]
        found_incident.occured_date = parse_date(incident["occuredDate"])
        found_incident.division = incident["division"]
        found_incident.precinct = incident["precinct"]
        found_incident.shift = incident["shift"]
        found_incident.beat = incident["beat"]
        found_incident.disposition = incident["disposition"]
        found_incident.census_tract = None
        found_incident.officer_force_type = incident["officerForceType"]
        found_incident.use_of_force_reason = incident["useOfForceReason"]
        found_incident.service_type = incident["serviceType"]
        found_incident.arrest_made = incident["arrestMade"]
        found_incident.arrest_charges = incident["arrestCharges"]
        found_incident.resident_weapon_used = incident["residentWeaponUsed"]
        found_incident.resident_injured = incident["residentInjured"]
        found_incident.resident_hospitalized = incident["residentHospitalized"]
        found_incident.officer_injured = incident["officerInjured"]
        found_incident.officer_hospitalized = incident["officerHospitalized"]
        found_incident.resident_race = incident["residentRace"]
        found_incident.resident_sex = incident["residentSex"]
        found_incident.resident_age = incident["residentAge"]
        found_incident.resident_condition = incident["residentCondition"]
        found_incident.officer_identifier = incident["officerIdentifier"]
        found_incident.officer_race = incident["officerRace"]
        found_incident.officer_sex = incident["officerSex"]
        found_incident.officer_age = incident["officerAge"]
        found_incident.officer_years_of_service = incident["officerYearsOfService"]
        found_incident.officer_condition = incident["officerCondition"]
        found_incident.save()

        return row_added

class AssaultOnOfficerIMPD(SurrogatePK, Model):
    __tablename__ = 'assaults_on_officers_impd'
    department_id = Column(db.Integer, db.ForeignKey('departments.id'), nullable=False)
    opaque_id = Column(db.String(255), unique=False, nullable=False)
    officer_identifier = Column(db.String(255), unique=False, nullable=True)
    service_type = Column(db.String(255), unique=False, nullable=True)
    force_type = Column(db.String(255), unique=False, nullable=True)
    assignment = Column(db.String(255), unique=False, nullable=True)
    arrest_made = Column(db.Boolean, nullable=True)
    officer_injured = Column(db.Boolean, nullable=True)
    officer_killed = Column(db.Boolean, nullable=True)
    report_filed = Column(db.Boolean, nullable=True)

    def __init__(self, **kwargs):
        db.Model.__init__(self, **kwargs)

    @classmethod
    def get_csv_schema(cls):
        ''' Get the CSV column headers and variable names.
        '''
        return [("id", "opaque_id"), ("officerIdentifier", "officer_identifier"), ("serviceType", "service_type"), ("forceType", "force_type"), ("assignment", "assignment"), ("arrestMade", "arrest_made"), ("officerInjured", "officer_injured"), ("officerKilled", "officer_killed"), ("reportFiled", "report_filed")]

    @classmethod
    def add_or_update_incident(cls, department, incident):
        ''' Add a new Assaults on Officers incident or update an existing one
        '''
        row_added = False
        # get a cleaner instance
        cleaner = Cleaners()
        # capitalize all the fields in the incident
        incident = cleaner.capitalize_incident(incident)

        found_incident = cls.query.filter_by(
            department_id=department.id,
            opaque_id=incident["opaqueId"],
            officer_identifier=incident["officerIdentifier"]
        ).first()

        if not found_incident:

            found_incident = cls.create(
                department_id=department.id,
                opaque_id=incident["opaqueId"]
            )

            row_added = True

        found_incident.department_id = department.id
        found_incident.opaque_id = incident["opaqueId"]
        found_incident.officer_identifier = incident["officerIdentifier"]
        found_incident.service_type = incident["serviceType"]
        found_incident.force_type = incident["forceType"]
        found_incident.force_type = incident["forceType"]
        found_incident.assignment = incident["assignment"]
        found_incident.arrest_made = incident["arrestMade"]
        found_incident.officer_injured = incident["officerInjured"]
        found_incident.officer_killed = incident["officerKilled"]
        found_incident.report_filed = incident["reportFiled"]
        found_incident.save()

        return row_added

class CitizenComplaintIMPD(SurrogatePK, Model):
    __tablename__ = 'citizen_complaints_impd'
    department_id = Column(db.Integer, db.ForeignKey('departments.id'), nullable=False)
    opaque_id = Column(db.String(255), unique=False, nullable=False)
    occured_date = Column(db.DateTime, nullable=True)
    service_type = Column(db.String(255), unique=False, nullable=True)
    source = Column(db.String(255), unique=False, nullable=True)
    division = Column(db.String(255), unique=False, nullable=True)
    precinct = Column(db.String(255), unique=False, nullable=True)
    shift = Column(db.String(255), unique=False, nullable=True)
    beat = Column(db.String(255), unique=False, nullable=True)
    disposition = Column(db.String(255), unique=False, nullable=True)
    allegation_type = Column(db.String(255), unique=False, nullable=True)
    allegation = Column(db.String(255), unique=False, nullable=True)
    census_tract = Column(db.String(255), unique=False, nullable=True)
    resident_race = Column(db.String(255), unique=False, nullable=True)
    officer_race = Column(db.String(255), unique=False, nullable=True)
    resident_sex = Column(db.String(255), unique=False, nullable=True)
    officer_sex = Column(db.String(255), unique=False, nullable=True)
    officer_identifier = Column(db.String(255), unique=False, nullable=True)
    officer_years_of_service = Column(db.String(255), unique=False, nullable=True)
    officer_age = Column(db.String(255), unique=False, nullable=True)
    resident_age = Column(db.String(255), unique=False, nullable=True)

    def __init__(self, **kwargs):
        db.Model.__init__(self, **kwargs)

    @classmethod
    def get_csv_schema(cls):
        ''' Get the CSV column headers and variable names.
        '''
        return [("id", "opaque_id"), ("occurredDate", "occured_date"), ("division", "division"), ("district", "precinct"), ("shift", "shift"), ("beat", "beat"), ("serviceType", "service_type"), ("source", "source"), ("allegationType", "allegation_type"), ("allegation", "allegation"), ("finding", "disposition"), ("residentRace", "resident_race"), ("residentSex", "resident_sex"), ("residentAge", "resident_age"), ("officerRace", "officer_race"), ("officerSex", "officer_sex"), ("officerAge", "officer_age"), ("officerYearsOfService", "officer_years_of_service"), ("officerIdentifier", "officer_identifier")]

    @classmethod
    def add_or_update_incident(cls, department, incident):
        ''' Add a new Citizen Complaints incident or update an existing one
        '''
        row_added = False
        # get a cleaner instance
        cleaner = Cleaners()
        # make sure values that might've been sent as integers are strings
        incident["residentAge"] = cleaner.number_to_string(incident["residentAge"])
        incident["officerAge"] = cleaner.number_to_string(incident["officerAge"])
        incident["officerYearsOfService"] = cleaner.number_to_string(incident["officerYearsOfService"])
        # capitalize all the fields in the incident
        incident = cleaner.capitalize_incident(incident)
        # clean sex & race
        incident["residentSex"] = cleaner.sex(incident["residentSex"])
        incident["residentRace"] = cleaner.race(incident["residentRace"])
        incident["officerSex"] = cleaner.sex(incident["officerSex"])
        incident["officerRace"] = cleaner.race(incident["officerRace"])

        found_incident = cls.query.filter_by(
            opaque_id=incident["opaqueId"],
            allegation_type=incident["allegationType"],
            allegation=incident["allegation"],
            officer_identifier=incident["officerIdentifier"],
            department_id=department.id,
            resident_race=incident["residentRace"],
            resident_sex=incident["residentSex"],
            resident_age=incident["residentAge"]
        ).first()

        if not found_incident:

            # check for multiple complainants
            # :TODO: validate this practice!
            multiple_complaintant_check = cls.query.filter_by(
                opaque_id=incident["opaqueId"],
                allegation_type=incident["allegationType"],
                allegation=incident["allegation"],
                officer_identifier=incident["officerIdentifier"],
                department_id=department.id
            ).first()

            if multiple_complaintant_check:
                return None

            found_incident = cls.create(
                department_id=department.id,
                opaque_id=incident["opaqueId"]
            )
            row_added = True

        found_incident.department_id = department.id
        found_incident.opaque_id = incident["opaqueId"]
        found_incident.service_type = incident["serviceType"]
        found_incident.source = incident["source"]
        found_incident.occured_date = parse_date(incident["occuredDate"])
        found_incident.division = incident["division"]
        found_incident.precinct = incident["precinct"]
        found_incident.shift = incident["shift"]
        found_incident.beat = incident["beat"]
        found_incident.allegation_type = incident["allegationType"]
        found_incident.allegation = incident["allegation"]
        found_incident.disposition = incident["disposition"]
        found_incident.resident_race = incident["residentRace"]
        found_incident.resident_sex = incident["residentSex"]
        found_incident.resident_age = incident["residentAge"]
        found_incident.officer_identifier = incident["officerIdentifier"]
        found_incident.officer_race = incident["officerRace"]
        found_incident.officer_sex = incident["officerSex"]
        found_incident.officer_age = incident["officerAge"]
        found_incident.officer_years_of_service = incident["officerYearsOfService"]
        found_incident.census_tract = None
        found_incident.save()

        return row_added

class OfficerInvolvedShootingIMPD(SurrogatePK, Model):
    __tablename__ = 'officer_involved_shootings_impd'
    department_id = Column(db.Integer, db.ForeignKey('departments.id'), nullable=False)
    opaque_id = Column(db.String(255), unique=False, nullable=False)
    occured_date = Column(db.DateTime, nullable=True)
    division = Column(db.String(255), unique=False, nullable=True)
    precinct = Column(db.String(255), unique=False, nullable=True)
    shift = Column(db.String(255), unique=False, nullable=True)
    beat = Column(db.String(255), unique=False, nullable=True)
    disposition = Column(db.String(255), unique=False, nullable=True)
    census_tract = Column(db.String(255), unique=False, nullable=True)
    officer_weapon_used = Column(db.String(255), unique=False, nullable=True)
    resident_weapon_used = Column(db.String(255), unique=False, nullable=True)
    service_type = Column(db.String(255), unique=False, nullable=True)
    resident_race = Column(db.String(255), unique=False, nullable=True)
    officer_race = Column(db.String(255), unique=False, nullable=True)
    resident_sex = Column(db.String(255), unique=False, nullable=True)
    officer_sex = Column(db.String(255), unique=False, nullable=True)
    officer_identifier = Column(db.String(255), unique=False, nullable=True)
    officer_years_of_service = Column(db.Integer, unique=False, nullable=True)
    officer_age = Column(db.String(255), unique=False, nullable=True)
    resident_age = Column(db.String(255), unique=False, nullable=True)
    officer_condition = Column(db.String(255), unique=False, nullable=True)
    resident_condition = Column(db.String(255), unique=False, nullable=True)

    def __init__(self, **kwargs):
        db.Model.__init__(self, **kwargs)

    @classmethod
    def get_csv_schema(cls):
        ''' Get the CSV column headers and variable names.
        '''
        return [("id", "opaque_id"), ("occurredDate", "occured_date"), ("division", "division"), ("district", "precinct"), ("shift", "shift"), ("beat", "beat"), ("disposition", "disposition"), ("residentWeaponUsed", "resident_weapon_used"), ("officerWeaponUsed", "officer_weapon_used"), ("serviceType", "service_type"), ("residentCondition", "resident_condition"), ("officerCondition", "officer_condition"), ("residentRace", "resident_race"), ("residentSex", "resident_sex"), ("residentAge", "resident_age"), ("officerRace", "officer_race"), ("officerSex", "officer_sex"), ("officerAge", "officer_age"), ("officerYearsOfService", "officer_years_of_service"), ("officerIdentifier", "officer_identifier")]

    @classmethod
    def add_or_update_incident(cls, department, incident):
        ''' Add a new OIS incident or update an existing one
        '''
        row_added = False
        # get a cleaner instance
        cleaner = Cleaners()
        # capitalize the location
        incident["division"] = cleaner.capitalize(incident["division"])
        incident["precinct"] = cleaner.capitalize(incident["precinct"])
        incident["shift"] = cleaner.capitalize(incident["shift"])
        incident["beat"] = cleaner.capitalize(incident["beat"])
        # clean weapon, race, gender
        incident["residentWeaponUsed"] = cleaner.resident_weapon_used(incident["residentWeaponUsed"])
        incident["residentSex"] = cleaner.sex(incident["residentSex"])
        incident["residentRace"] = cleaner.race(incident["residentRace"])
        incident["officerSex"] = cleaner.sex(incident["officerSex"])
        incident["officerRace"] = cleaner.race(incident["officerRace"])
        # make sure values that might've been sent as integers are strings
        incident["residentAge"] = cleaner.number_to_string(incident["residentAge"])
        incident["officerAge"] = cleaner.number_to_string(incident["officerAge"])
        # and values that might've been sent as strings are integers
        incident["officerYearsOfService"] = cleaner.string_to_integer(incident["officerYearsOfService"])

        found_incident = cls.query.filter_by(
            opaque_id=incident["opaqueId"],
            department_id=department.id,
            officer_identifier=incident["officerIdentifier"]
        ).first()

        if not found_incident:
            found_incident = cls.create(
                department_id=department.id,
                opaque_id=incident["opaqueId"]
            )
            row_added = True

        found_incident.department_id = department.id
        found_incident.opaque_id = incident["opaqueId"]
        found_incident.service_type = incident["serviceType"]
        found_incident.occured_date = parse_date(incident["occuredDate"])
        found_incident.division = incident["division"]
        found_incident.precinct = incident["precinct"]
        found_incident.shift = incident["shift"]
        found_incident.beat = incident["beat"]
        found_incident.disposition = incident["disposition"]
        found_incident.resident_race = incident["residentRace"]
        found_incident.resident_sex = incident["residentSex"]
        found_incident.resident_age = incident["residentAge"]
        found_incident.resident_weapon_used = incident["residentWeaponUsed"]
        found_incident.resident_condition = incident["residentCondition"]
        found_incident.officer_identifier = incident["officerIdentifier"]
        found_incident.officer_weapon_used = incident["officerForceType"]
        found_incident.officer_race = incident["officerRace"]
        found_incident.officer_sex = incident["officerSex"]
        found_incident.officer_age = incident["officerAge"]
        found_incident.officer_years_of_service = parse_int(incident["officerYearsOfService"])
        found_incident.officer_condition = incident["officerCondition"]
        found_incident.census_tract = None
        found_incident.save()

        return row_added

#
# BALTIMORE POLICE DEPARTMENT
#

class UseOfForceIncidentBPD(SurrogatePK, Model):
    __tablename__ = 'use_of_force_incidents_bpd'
    department_id = Column(db.Integer, db.ForeignKey('departments.id'), nullable=False)
    opaque_id = Column(db.String(255), unique=False, nullable=False)
    occured_date = Column(db.DateTime, nullable=True)
    bureau = Column(db.String(255), unique=False, nullable=True)
    division = Column(db.String(255), unique=False, nullable=True)
    assignment = Column(db.String(255), unique=False, nullable=True)
    use_of_force_reason = Column(db.String(255), unique=False, nullable=True)
    officer_force_type = Column(db.String(255), unique=False, nullable=True)
    service_type = Column(db.String(255), unique=False, nullable=True)
    arrest_made = Column(db.Boolean, nullable=True)
    arrest_charges = Column(db.String(255), unique=False, nullable=True)
    resident_injured = Column(db.Boolean, nullable=True)
    resident_hospitalized = Column(db.Boolean, nullable=True)
    resident_condition = Column(db.String(255), unique=False, nullable=True)
    officer_injured = Column(db.Boolean, nullable=True)
    officer_hospitalized = Column(db.Boolean, nullable=True)
    officer_condition = Column(db.String(255), unique=False, nullable=True)
    resident_identifier = Column(db.String(255), unique=False, nullable=True)
    resident_weapon_used = Column(db.String(255), unique=False, nullable=True)
    resident_race = Column(db.String(255), unique=False, nullable=True)
    resident_sex = Column(db.String(255), unique=False, nullable=True)
    resident_age = Column(db.String(255), unique=False, nullable=True)
    officer_race = Column(db.String(255), unique=False, nullable=True)
    officer_sex = Column(db.String(255), unique=False, nullable=True)
    officer_age = Column(db.String(255), unique=False, nullable=True)
    officer_years_of_service = Column(db.String(255), unique=False, nullable=True)
    officer_identifier = Column(db.String(255), unique=False, nullable=True)

    def __init__(self, **kwargs):
        db.Model.__init__(self, **kwargs)

    @classmethod
    def get_csv_schema(cls):
        ''' Get the CSV column headers and variable names.
        '''
        return [("id", "opaque_id"), ("occurredDate", "occured_date"), ("bureau", "bureau"), ("division", "division"), ("assignment", "assignment"), ("useOfForceReason", "use_of_force_reason"), ("officerForceType", "officer_force_type"), ("serviceType", "service_type"), ("arrestMade", "arrest_made"), ("arrestCharges", "arrest_charges"), ("residentInjured", "resident_injured"), ("residentHospitalized", "resident_hospitalized"), ("residentCondition", "resident_condition"), ("officerInjured", "officer_injured"), ("officerHospitalized", "officer_hospitalized"), ("officerCondition", "officer_condition"), ("residentIdentifier", "resident_identifier"), ("residentWeaponUsed", "resident_weapon_used"), ("residentRace", "resident_race"), ("residentSex", "resident_sex"), ("residentAge", "resident_age"), ("officerRace", "officer_race"), ("officerSex", "officer_sex"), ("officerAge", "officer_age"), ("officerYearsOfService", "officer_years_of_service"), ("officerIdentifier", "officer_identifier")]

    @classmethod
    def add_or_update_incident(cls, department, incident):
        ''' Add a new UOF incident or update an existing one
        '''
        row_added = False
        # get a cleaner instance
        cleaner = Cleaners()
        # capitalize the location
        incident["bureau"] = cleaner.capitalize(incident["bureau"])
        incident["division"] = cleaner.capitalize(incident["division"])
        incident["assignment"] = cleaner.capitalize(incident["assignment"])
        # clean force type, race, gender
        incident["officerForceType"] = cleaner.officer_force_type(incident["officerForceType"])
        incident["residentRace"] = cleaner.race(incident["residentRace"])
        incident["residentSex"] = cleaner.sex(incident["residentSex"])
        incident["officerRace"] = cleaner.race(incident["officerRace"])
        incident["officerSex"] = cleaner.sex(incident["officerSex"])
        # make sure values that might've been sent as integers are strings
        incident["residentAge"] = cleaner.number_to_string(incident["residentAge"])
        incident["officerAge"] = cleaner.number_to_string(incident["officerAge"])
        incident["officerYearsOfService"] = cleaner.number_to_string(incident["officerYearsOfService"])

        found_incident = False
        # found_incident = cls.query.filter_by(
        #     opaque_id=incident["opaqueId"],
        #     department_id=department.id,
        #     officer_identifier=incident["officerIdentifier"],
        #     resident_identifier=incident["residentIdentifier"],
        #     officer_force_type=incident["officerForceType"]
        # ).first()

        if not found_incident:
            found_incident = cls.create(
                department_id=department.id,
                opaque_id=incident["opaqueId"])
            row_added = True

        found_incident.department_id = department.id
        found_incident.opaque_id = incident["opaqueId"]
        found_incident.occured_date = parse_date(incident["occuredDate"])
        found_incident.bureau = incident["bureau"]
        found_incident.division = incident["division"]
        found_incident.assignment = incident["assignment"]
        found_incident.use_of_force_reason = incident["useOfForceReason"]
        found_incident.officer_force_type = incident["officerForceType"]
        found_incident.service_type = incident["serviceType"]
        found_incident.arrest_made = incident["arrestMade"]
        found_incident.arrest_charges = incident["arrestCharges"]
        found_incident.resident_injured = incident["residentInjured"]
        found_incident.resident_hospitalized = incident["residentHospitalized"]
        found_incident.resident_condition = incident["residentCondition"]
        found_incident.officer_injured = incident["officerInjured"]
        found_incident.officer_hospitalized = incident["officerHospitalized"]
        found_incident.officer_condition = incident["officerCondition"]
        found_incident.resident_identifier = incident["residentIdentifier"]
        found_incident.resident_weapon_used = incident["residentWeaponUsed"]
        found_incident.resident_race = incident["residentRace"]
        found_incident.resident_sex = incident["residentSex"]
        found_incident.resident_age = incident["residentAge"]
        found_incident.officer_race = incident["officerRace"]
        found_incident.officer_sex = incident["officerSex"]
        found_incident.officer_age = incident["officerAge"]
        found_incident.officer_years_of_service = incident["officerYearsOfService"]
        found_incident.officer_identifier = incident["officerIdentifier"]

        found_incident.save()

        return row_added

class CitizenComplaintBPD(SurrogatePK, Model):
    __tablename__ = 'citizen_complaints_bpd'
    department_id = Column(db.Integer, db.ForeignKey('departments.id'), nullable=False)
    opaque_id = Column(db.String(255), unique=False, nullable=False)
    occured_date = Column(db.DateTime, nullable=True)
    bureau = Column(db.String(255), unique=False, nullable=True)
    division = Column(db.String(255), unique=False, nullable=True)
    assignment = Column(db.String(255), unique=False, nullable=True)
    service_type = Column(db.String(255), unique=False, nullable=True)
    source = Column(db.String(255), unique=False, nullable=True)
    allegation = Column(db.String(255), unique=False, nullable=True)
    disposition = Column(db.String(255), unique=False, nullable=True)
    resident_identifier = Column(db.String(255), unique=False, nullable=True)
    resident_race = Column(db.String(255), unique=False, nullable=True)
    resident_sex = Column(db.String(255), unique=False, nullable=True)
    resident_age = Column(db.String(255), unique=False, nullable=True)
    officer_identifier = Column(db.String(255), unique=False, nullable=True)
    officer_race = Column(db.String(255), unique=False, nullable=True)
    officer_sex = Column(db.String(255), unique=False, nullable=True)
    officer_age = Column(db.String(255), unique=False, nullable=True)
    officer_years_of_service = Column(db.String(255), unique=False, nullable=True)

    def __init__(self, **kwargs):
        db.Model.__init__(self, **kwargs)

    @classmethod
    def get_csv_schema(cls):
        ''' Get the CSV column headers and variable names.
        '''
        return [("id", "opaque_id"), ("occurredDate", "occured_date"), ("bureau", "bureau"), ("division", "division"), ("assignment", "assignment"), ("serviceType", "service_type"), ("source", "source"), ("allegation", "allegation"), ("disposition", "disposition"), ("residentIdentifier", "resident_identifier"), ("residentRace", "resident_race"), ("residentSex", "resident_sex"), ("residentAge", "resident_age"), ("officerIdentifier", "officer_identifier"), ("officerRace", "officer_race"), ("officerSex", "officer_sex"), ("officerAge", "officer_age"), ("officerYearsOfService", "officer_years_of_service")]

    @classmethod
    def add_or_update_incident(cls, department, incident):
        ''' Add a new Citizen Complaints incident or update an existing one
        '''
        row_added = False
        # get a cleaner instance
        cleaner = Cleaners()
        # make sure values that might've been sent as integers are strings
        incident["residentAge"] = cleaner.number_to_string(incident["residentAge"])
        incident["officerAge"] = cleaner.number_to_string(incident["officerAge"])
        incident["officerYearsOfService"] = cleaner.number_to_string(incident["officerYearsOfService"])
        # capitalize all the fields in the incident
        incident = cleaner.capitalize_incident(incident)
        # clean sex & race
        incident["residentSex"] = cleaner.sex(incident["residentSex"])
        incident["residentRace"] = cleaner.race(incident["residentRace"])
        incident["officerSex"] = cleaner.sex(incident["officerSex"])
        incident["officerRace"] = cleaner.race(incident["officerRace"])

        found_incident = False
        # found_incident = cls.query.filter_by(
        #     opaque_id=incident["opaqueId"],
        #     allegation=incident["allegation"],
        #     officer_identifier=incident["officerIdentifier"],
        #     department_id=department.id,
        #     resident_race=incident["residentRace"],
        #     resident_sex=incident["residentSex"],
        #     resident_age=incident["residentAge"]
        # ).first()

        if not found_incident:

            # check for multiple complainants
            # :TODO: validate this practice!
            # multiple_complaintant_check = cls.query.filter_by(
            #     opaque_id=incident["opaqueId"],
            #     allegation=incident["allegation"],
            #     officer_identifier=incident["officerIdentifier"],
            #     department_id=department.id
            # ).first()

            # if multiple_complaintant_check:
            #     return None

            found_incident = cls.create(
                department_id=department.id,
                opaque_id=incident["opaqueId"]
            )
            row_added = True

        found_incident.department_id = department.id
        found_incident.opaque_id = incident["opaqueId"]
        found_incident.occured_date = parse_date(incident["occuredDate"])
        found_incident.bureau = incident["bureau"]
        found_incident.division = incident["division"]
        found_incident.assignment = incident["assignment"]
        found_incident.service_type = incident["serviceType"]
        found_incident.source = incident["source"]
        found_incident.allegation = incident["allegation"]
        found_incident.disposition = incident["disposition"]
        found_incident.resident_identifier = incident["residentIdentifier"]
        found_incident.resident_race = incident["residentRace"]
        found_incident.resident_sex = incident["residentSex"]
        found_incident.resident_age = incident["residentAge"]
        found_incident.officer_identifier = incident["officerIdentifier"]
        found_incident.officer_race = incident["officerRace"]
        found_incident.officer_sex = incident["officerSex"]
        found_incident.officer_age = incident["officerAge"]
        found_incident.officer_years_of_service = incident["officerYearsOfService"]
        found_incident.save()

        return row_added

class OfficerInvolvedShootingBPD(SurrogatePK, Model):
    __tablename__ = 'officer_involved_shootings_bpd'
    department_id = Column(db.Integer, db.ForeignKey('departments.id'), nullable=False)
    opaque_id = Column(db.String(255), unique=False, nullable=False)
    occured_date = Column(db.DateTime, nullable=True)
    bureau = Column(db.String(255), unique=False, nullable=True)
    division = Column(db.String(255), unique=False, nullable=True)
    assignment = Column(db.String(255), unique=False, nullable=True)
    disposition = Column(db.String(255), unique=False, nullable=True)
    resident_weapon_used = Column(db.String(255), unique=False, nullable=True)
    officer_weapon_used = Column(db.String(255), unique=False, nullable=True)
    service_type = Column(db.String(255), unique=False, nullable=True)
    resident_condition = Column(db.String(255), unique=False, nullable=True)
    officer_condition = Column(db.String(255), unique=False, nullable=True)
    resident_identifier = Column(db.String(255), unique=False, nullable=True)
    resident_race = Column(db.String(255), unique=False, nullable=True)
    resident_sex = Column(db.String(255), unique=False, nullable=True)
    resident_age = Column(db.String(255), unique=False, nullable=True)
    officer_race = Column(db.String(255), unique=False, nullable=True)
    officer_sex = Column(db.String(255), unique=False, nullable=True)
    officer_age = Column(db.String(255), unique=False, nullable=True)
    officer_years_of_service = Column(db.Integer, unique=False, nullable=True)
    officer_identifier = Column(db.String(255), unique=False, nullable=True)

    def __init__(self, **kwargs):
        db.Model.__init__(self, **kwargs)

    @classmethod
    def get_csv_schema(cls):
        ''' Get the CSV column headers and variable names.
        '''
        return [("id", "opaque_id"), ("occurredDate", "occured_date"), ("bureau", "bureau"), ("division", "division"), ("assignment", "assignment"), ("disposition", "disposition"), ("residentWeaponUsed", "resident_weapon_used"), ("officerWeaponUsed", "officer_weapon_used"), ("serviceType", "service_type"), ("residentCondition", "resident_condition"), ("officerCondition", "officer_condition"), ("residentIdentifier", "resident_identifier"), ("residentRace", "resident_race"), ("residentSex", "resident_sex"), ("residentAge", "resident_age"), ("officerRace", "officer_race"), ("officerSex", "officer_sex"), ("officerAge", "officer_age"), ("officerYearsOfService", "officer_years_of_service"), ("officerIdentifier", "officer_identifier")]

    @classmethod
    def add_or_update_incident(cls, department, incident):
        ''' Add a new OIS incident or update an existing one
        '''
        row_added = False
        # get a cleaner instance
        cleaner = Cleaners()
        # capitalize the location
        incident["bureau"] = cleaner.capitalize(incident["bureau"])
        incident["division"] = cleaner.capitalize(incident["division"])
        incident["assignment"] = cleaner.capitalize(incident["assignment"])
        # clean weapon, race, gender
        incident["residentWeaponUsed"] = cleaner.resident_weapon_used(incident["residentWeaponUsed"])
        incident["residentSex"] = cleaner.sex(incident["residentSex"])
        incident["residentRace"] = cleaner.race(incident["residentRace"])
        incident["officerSex"] = cleaner.sex(incident["officerSex"])
        incident["officerRace"] = cleaner.race(incident["officerRace"])
        # make sure values that might've been sent as integers are strings
        incident["residentAge"] = cleaner.number_to_string(incident["residentAge"])
        incident["officerAge"] = cleaner.number_to_string(incident["officerAge"])
        # and values that might've been sent as strings are integers
        incident["officerYearsOfService"] = cleaner.string_to_integer(incident["officerYearsOfService"])

        found_incident = False
        # found_incident = cls.query.filter_by(
        #     opaque_id=incident["opaqueId"],
        #     department_id=department.id,
        #     officer_identifier=incident["officerIdentifier"]
        # ).first()

        if not found_incident:
            found_incident = cls.create(
                department_id=department.id,
                opaque_id=incident["opaqueId"]
            )
            row_added = True

        found_incident.department_id = department.id
        found_incident.opaque_id = incident["opaqueId"]
        found_incident.occured_date = parse_date(incident["occuredDate"])
        found_incident.bureau = incident["bureau"]
        found_incident.division = incident["division"]
        found_incident.assignment = incident["assignment"]
        found_incident.disposition = incident["disposition"]
        found_incident.resident_weapon_used = incident["residentWeaponUsed"]
        found_incident.officer_weapon_used = incident["officerWeaponUsed"]
        found_incident.service_type = incident["serviceType"]
        found_incident.resident_condition = incident["residentCondition"]
        found_incident.officer_condition = incident["officerCondition"]
        found_incident.resident_identifier = incident["residentIdentifier"]
        found_incident.resident_race = incident["residentRace"]
        found_incident.resident_sex = incident["residentSex"]
        found_incident.resident_age = incident["residentAge"]
        found_incident.officer_race = incident["officerRace"]
        found_incident.officer_sex = incident["officerSex"]
        found_incident.officer_age = incident["officerAge"]
        found_incident.officer_years_of_service = parse_int(incident["officerYearsOfService"])
        found_incident.officer_identifier = incident["officerIdentifier"]
        found_incident.save()

        return row_added
