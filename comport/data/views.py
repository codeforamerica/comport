# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, request, redirect, url_for, flash
from comport.utils import flash_errors
from flask.ext.login import login_required
from comport.decorators import extractor_auth_required
from comport.department.models import Extractor
from comport.data.models import Month
import json

blueprint = Blueprint("data", __name__, url_prefix='/data',
                      static_folder="../static")

@blueprint.route("/heartbeat", methods=['POST'])
@extractor_auth_required()
def heartbeat():
    return json.dumps({"received":request.json})

@blueprint.route("/serviceType", methods=['POST'])
@extractor_auth_required()
def service_type():
    username = request.authorization.username
    extractor = Extractor.query.filter_by(username=username).first()
    j = request.json
    month = Month.create(month=int(j["month"]), year=int(j["year"]), department_id=extractor.department_id)
    return json.dumps(month.to_json())
