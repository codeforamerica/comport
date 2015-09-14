# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, request, redirect, url_for, flash
from comport.utils import flash_errors
from flask.ext.login import login_required
from comport.decorators import extractor_auth_required
from comport.department.models import Extractor
from comport.data.models import UseOfForceIncident
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

        if not found_incident:
            found_incident = UseOfForceIncident.create(opaque_id=incident["opaqueId"], service_type=incident["serviceType"],department_id=extractor.department_id)
            added_rows += 1
            continue

        found_incident.service_type = incident["serviceType"]

        found_incident.save()
        updated_rows += 1

    extractor.next_month = None
    extractor.next_year = None
    extractor.save()
    return json.dumps({"added": added_rows, "updated": updated_rows})
