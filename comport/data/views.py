# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, request, redirect, url_for, flash
from comport.utils import flash_errors
from flask.ext.login import login_required
from comport.decorators import extractor_auth_required
from comport.department.models import Extractor
from comport.data.models import UseOfForceIncident, CitizenComplaint
from comport.utils import parse_date
import json

blueprint = Blueprint("data", __name__, url_prefix='/data',
                      static_folder="../static")

@blueprint.route("/heartbeat", methods=['POST'])
@extractor_auth_required()
def heartbeat():
    username = request.authorization.username
    extractor = Extractor.query.filter_by(username=username).first()

    if extractor.next_month and extractor.next_year:
        return json.dumps({"received":request.json, "nextMonth":extractor.next_month, "nextYear":extractor.next_year})

    return json.dumps({"received":request.json})

@blueprint.route("/UOF", methods=['POST'])
@extractor_auth_required()
def use_of_force():
    username = request.authorization.username
    extractor = Extractor.query.filter_by(username=username).first()
    j = request.json
    added_rows = 0
    updated_rows = 0

    for incident in j['data']:
        print(incident)
        found_incident = UseOfForceIncident.query.filter_by(opaque_id=incident["opaqueId"]).first()

        occured_date = parse_date(incident["occuredDate"])

        if not found_incident:
            found_incident = UseOfForceIncident.create(
                    department_id = extractor.department_id,
                    opaque_id = incident["opaqueId"],
                    occured_date = occured_date,
                    division = incident["division"],
                    precinct =incident["precinct"],
                    shift = incident["shift"],
                    beat =incident["beat"],
                    disposition =incident["disposition"],
                    census_tract = None,
                    officer_force_type =incident["officerForceType"],
                    resident_resist_type =incident["residentResistType"],
                    officer_weapon_used =incident["officerWeaponUsed"],
                    resident_weapon_used =incident["residentWeaponUsed"],
                    service_type =incident["serviceType"],
                    arrest_made =incident["arrestMade"],
                    arrest_charges =incident["arrestCharges"],
                    resident_injured =incident["residentInjured"],
                    resident_hospitalized =incident["residentHospitalized"],
                    officer_injured =incident["officerInjured"],
                    officer_hospitalized =incident["officerHospitalized"],
                    use_of_force_reason =incident["useOfForceReason"],
                    resident_race =incident["residentRace"],
                    officer_race =incident["officerRace"],
                    officer_identifier =incident["officerIdentifier"],
                    officer_years_of_service =incident["officerYearsOfService"])
            added_rows += 1
            continue

        found_incident.department_id = extractor.department_id
        found_incident.opaque_id = incident["opaqueId"],
        found_incident.occured_date = occured_date,
        found_incident.division = incident["division"],
        found_incident.precinct =incident["precinct"],
        found_incident.shift = incident["shift"],
        found_incident.beat =incident["beat"],
        found_incident.disposition =incident["disposition"],
        found_incident.census_tract = None,
        found_incident.officer_force_type =incident["officerForceType"],
        found_incident.resident_resist_type =incident["residentResistType"],
        found_incident.officer_weapon_used =incident["officerWeaponUsed"],
        found_incident.resident_weapon_used =incident["residentWeaponUsed"],
        found_incident.service_type =incident["serviceType"],
        found_incident.arrest_made =incident["arrestMade"],
        found_incident.arrest_charges =incident["arrestCharges"],
        found_incident.resident_injured =incident["residentInjured"],
        found_incident.resident_hospitalized =incident["residentHospitalized"],
        found_incident.officer_injured =incident["officerInjured"],
        found_incident.officer_hospitalized =incident["officerHospitalized"],
        found_incident.use_of_force_reason =incident["useOfForceReason"],
        found_incident.resident_race =incident["residentRace"],
        found_incident.officer_race =incident["officerRace"],
        found_incident.officer_identifier =incident["officerIdentifier"],
        found_incident.officer_years_of_service =incident["officerYearsOfService"]
        found_incident.save()
        updated_rows += 1

    extractor.next_month = None
    extractor.next_year = None
    extractor.save()
    return json.dumps({"added": added_rows, "updated": updated_rows})

@blueprint.route("/complaints", methods=['POST'])
@extractor_auth_required()
def complaints():
    username = request.authorization.username
    extractor = Extractor.query.filter_by(username=username).first()
    j = request.json
    added_rows = 0
    updated_rows = 0

    for incident in j['data']:
        print(incident)
        found_incident = CitizenComplaint.query.filter_by(opaque_id=incident["opaqueId"]).first()

        occured_date = parse_date(incident["occuredDate"])

        if not found_incident:
            found_incident = CitizenComplaint.create(
                    department_id = extractor.department_id,
                    opaque_id = incident["opaqueId"],
                    occured_date = occured_date,
                    division = incident["division"],
                    precinct =incident["precinct"],
                    shift = incident["shift"],
                    beat =incident["beat"],
                    disposition =incident["disposition"],
                    category = None,
                    census_tract = None,
                    resident_race =incident["residentRace"],
                    officer_race =incident["officerRace"],
                    resident_sex =incident["residentSex"],
                    officer_sex =incident["officerSex"],
                    officer_identifier =incident["officerIdentifier"],
                    officer_years_of_service =incident["officerYearsOfService"])
            added_rows += 1
            continue

        found_incident = department_id = extractor.department_id,
        found_incident = opaque_id = incident["opaqueId"],
        found_incident = occured_date = occured_date,
        found_incident = division = incident["division"],
        found_incident = precinct =incident["precinct"],
        found_incident = shift = incident["shift"],
        found_incident = beat =incident["beat"],
        found_incident = disposition =incident["disposition"],
        found_incident = category = None,
        found_incident = census_tract = None,
        found_incident = resident_race =incident["residentRace"],
        found_incident = officer_race =incident["officerRace"],
        found_incident = resident_sex =incident["residentSex"],
        found_incident = officer_sex =incident["officerSex"],
        found_incident = officer_identifier =incident["officerIdentifier"],
        found_incident = officer_years_of_service =incident["officerYearsOfService"]
        found_incident.save()
        updated_rows += 1

    extractor.next_month = None
    extractor.next_year = None
    extractor.save()
    return json.dumps({"added": added_rows, "updated": updated_rows})
