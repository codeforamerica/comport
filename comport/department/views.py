# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, request, redirect, url_for, flash
from comport.utils import flash_errors
from .models import Department, Extractor
from flask.ext.login import login_required
from comport.decorators import admin_or_department_required, extractor_auth_required
import uuid
import json

blueprint = Blueprint("department", __name__, url_prefix='/department',
                      static_folder="../static")


@blueprint.route("/<int:department_id>")
@login_required
@admin_or_department_required()
def department_dashboard(department_id):
    department = Department.get_by_id(department_id)
    return render_template("department/dashboard.html", department=department)


@blueprint.route("/<int:department_id>/activate", methods=['POST'])
@login_required
@admin_or_department_required()
def activate_extractor(department_id):
    department = Department.get_by_id(department_id)
    if not department:
        abort(404)
    if request.method == 'POST':
        if request.form['submit'] == 'Activate':
            password = str(uuid.uuid4())
            extractor, envs = Extractor.from_department_and_password(department=department, password=password)
            return render_template("department/extractorEnvs.html", department=department, envs=envs)
        elif request.form['submit'] == 'Regenerate':
            extractor = department.get_extractor()
            password = str(uuid.uuid4())
            extractor.set_password(password)
            extractor.save()

            envs = extractor.generate_envs(password=password)

            return render_template("department/extractorEnvs.html", department=department, envs=envs)
