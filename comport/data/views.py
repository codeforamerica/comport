# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, request, redirect, url_for, flash
from comport.utils import flash_errors
from flask.ext.login import login_required
from comport.decorators import extractor_auth_required
from comport.department.models import Extractor
from comport.data.models import UseOfForceIncident
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

        found_incident = UseOfForceIncident.query.filter_by(opaque_id=incident["opaqueId"]).first()

        occured_date = parse_date(incident["occuredDate"])
        received_date = parse_date(incident["receivedDate"])

        if not found_incident:

            found_incident = UseOfForceIncident.create(
                opaque_id=incident["opaqueId"],
                service_type=incident["serviceType"],
                occured_date = occured_date,
                received_date = received_date,
                use_of_force_reason = incident["useOfForceReason"],
                citizen_weapon = incident["citizenWeapon"],
                census_tract = incident["censusTract"],
                department_id=extractor.department_id)
            added_rows += 1
            continue

        found_incident.service_type = incident["serviceType"]
        found_incident.occured_date = occured_date
        found_incident.received_date = received_date
        found_incident.use_of_force_reason = incident["useOfForceReason"]
        found_incident.citizen_weapon = incident["citizenWeapon"]
        found_incident.census_tract = incident["censusTract"]
        found_incident.save()
        updated_rows += 1

    extractor.next_month = None
    extractor.next_year = None
    extractor.save()
    return json.dumps({"added": added_rows, "updated": updated_rows})
