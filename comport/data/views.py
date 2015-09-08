# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, request, redirect, url_for, flash
from comport.utils import flash_errors
from flask.ext.login import login_required
from comport.decorators import extractor_auth_required
from comport.department.models import Extractor
from comport.data.models import Month, ServiceType
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

@blueprint.route("/serviceType", methods=['POST'])
@extractor_auth_required()
def service_type():
    username = request.authorization.username
    extractor = Extractor.query.filter_by(username=username).first()
    j = request.json

    found_month = Month.query.filter_by(month=int(j["month"]), year=int(j["year"]), department_id=extractor.department_id).first()

    if not found_month:
        found_month = Month.create(month=int(j["month"]), year=int(j["year"]), department_id=extractor.department_id)

    found_month.service_types = []

    for json_service_type in j["data"]:
        service_type = ServiceType.create(service_type=json_service_type["serviceType"], count=json_service_type["count"], month_id=found_month.id)

    found_month.save()
    extractor.next_month = None
    extractor.next_year = None
    extractor.save()
    return json.dumps({"month": found_month.month, "year":found_month.year, "addedRows": len(found_month.service_types)})
