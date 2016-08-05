# -*- coding: utf-8 -*-
from flask import Blueprint, request
from comport.decorators import extractor_auth_required
from comport.department.models import Extractor
from comport.data.models import UseOfForceIncidentIMPD, CitizenComplaintIMPD, OfficerInvolvedShootingIMPD, AssaultOnOfficerIMPD
from comport.utils import parse_date, parse_int, send_slack_message

from .cleaners import Cleaners

import json
import importlib
from datetime import datetime


blueprint = Blueprint("data", __name__, url_prefix='/data',
                      static_folder="../static")


@blueprint.route("/heartbeat", methods=['POST'])
@extractor_auth_required()
def heartbeat():
    username = request.authorization.username
    extractor = Extractor.query.filter_by(username=username).first()

    extractor.last_contact = datetime.now()
    extractor.save()

    heartbeat_response = json.dumps({"received": request.json})
    slack_body_lines = []
    extractor_department = extractor.first_department()
    if extractor_department:
        slack_body_lines.append('For: {}'.format(extractor_department.name))
    else:
        slack_body_lines.append('Username: {}'.format(username))

    slack_date_line = 'No extraction start date in reply.'

    now = datetime.now()
    next_month = extractor.next_month if extractor.next_month else now.month
    next_year = extractor.next_year if extractor.next_year else now.year

    heartbeat_response = json.dumps({"received": request.json, "nextMonth": next_month, "nextYear": next_year})
    slack_date_line = 'Replied with extraction start date: {}/{}'.format(next_month, next_year)

    slack_body_lines.append(slack_date_line)
    send_slack_message('Comport Pinged by Extractor!', slack_body_lines)

    return heartbeat_response


@blueprint.route("/UOF", methods=['POST'])
@extractor_auth_required()
def use_of_force():
    username = request.authorization.username
    extractor = Extractor.query.filter_by(username=username).first()
    department = extractor.first_department()
    request_json = request.json
    added_rows = 0
    updated_rows = 0

    uof_class = getattr(importlib.import_module("comport.data.models"), "UseOfForceIncident{}".format(department.short_name))

    for incident in request_json['data']:
        added = uof_class.add_or_update_incident(department, incident)
        if added is True:
            added_rows += 1
        elif added is False:
            updated_rows += 1

    extractor.next_month = None
    extractor.next_year = None
    extractor.save()
    return json.dumps({"added": added_rows, "updated": updated_rows})


@blueprint.route("/OIS", methods=['POST'])
@extractor_auth_required()
def officer_involved_shooting():
    username = request.authorization.username
    extractor = Extractor.query.filter_by(username=username).first()
    department = extractor.first_department()
    request_json = request.json
    added_rows = 0
    updated_rows = 0

    ois_class = getattr(importlib.import_module("comport.data.models"), "OfficerInvolvedShooting{}".format(department.short_name))

    for incident in request_json['data']:
        added = ois_class.add_or_update_incident(department, incident)
        if added is True:
            added_rows += 1
        elif added is False:
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
    department = extractor.first_department()
    request_json = request.json
    added_rows = 0
    updated_rows = 0

    complaint_class = getattr(importlib.import_module("comport.data.models"), "CitizenComplaint{}".format(department.short_name))

    for incident in request_json['data']:
        added = complaint_class.add_or_update_incident(department, incident)
        if added is True:
            added_rows += 1
        elif added is False:
            updated_rows += 1

    extractor.next_month = None
    extractor.next_year = None
    extractor.save()
    return json.dumps({"added": added_rows, "updated": updated_rows})

@blueprint.route("/assaults", methods=['POST'])
@extractor_auth_required()
def assaults():
    username = request.authorization.username
    extractor = Extractor.query.filter_by(username=username).first()
    department = extractor.first_department()
    request_json = request.json
    added_rows = 0
    updated_rows = 0

    assaults_class = getattr(importlib.import_module("comport.data.models"), "AssaultOnOfficer{}".format(department.short_name))

    for incident in request_json['data']:
        added = assaults_class.add_or_update_incident(department, incident)
        if added is True:
            added_rows += 1
        elif added is False:
            updated_rows += 1

    extractor.next_month = None
    extractor.next_year = None
    extractor.save()
    return json.dumps({"added": added_rows, "updated": updated_rows})
