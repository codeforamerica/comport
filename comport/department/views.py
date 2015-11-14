# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, request, redirect, url_for, flash, send_file, Response,abort
from comport.utils import flash_errors
from .models import Department, Extractor
from comport.data.models import DemographicValue, DenominatorValue
from flask.ext.login import login_required

from comport.decorators import admin_or_department_required, extractor_auth_required
import uuid
import datetime
import json
import io

blueprint = Blueprint("department", __name__, url_prefix='/department',
                      static_folder="../static")

#<<<<<<<< ADMIN ENDPOINTS >>>>>>>>>>
@blueprint.route("/<int:department_id>")
@login_required
@admin_or_department_required()
def department_dashboard(department_id):
    department = Department.get_by_id(department_id)
    return render_template("department/dashboard.html", department=department, current_year=datetime.datetime.now().year)


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

@blueprint.route("/<int:department_id>/start", methods=['POST'])
@login_required
@admin_or_department_required()
def start_extractor(department_id):
    department = Department.get_by_id(department_id)
    if not department:
        abort(404)
    if request.method == 'POST':
        if request.form['submit'] == 'Start':
            extractor = department.get_extractor()
            extractor.next_year = request.form["year"]
            extractor.next_month = request.form["month"]
            extractor.save()
            flash("Extractor started", "info")
            return redirect(url_for('department.department_dashboard',department_id=department.id))

#<<<<<<<< EDIT ENDPOINTS >>>>>>>>>>
@blueprint.route("/<int:department_id>/edit/ois")
@login_required
@admin_or_department_required()
def edit_ois(department_id):
    department = Department.get_by_id(department_id)
    if not department:
        abort(404)
    return render_template("department/site/ois.html", department=department, chart_blocks=department.get_ois_blocks(), editing=True)

@blueprint.route("/<int:department_id>/edit/useofforce")
@login_required
@admin_or_department_required()
def edit_use_of_force(department_id):
    department = Department.get_by_id(department_id)
    if not department:
        abort(404)
    return render_template("department/site/useofforce.html", department=department, chart_blocks=department.get_uof_blocks(), editing=True)

@blueprint.route("/<int:department_id>/edit/complaints")
@login_required
@admin_or_department_required()
def edit_complaints(department_id):
    department = Department.get_by_id(department_id)
    if not department:
        abort(404)
    return render_template("department/site/complaints.html", department=department, chart_blocks=department.get_complaint_blocks(), editing=True)

@blueprint.route("/<int:department_id>/edit/demographics")
@login_required
@admin_or_department_required()
def edit_demographics(department_id):
    department = Department.get_by_id(department_id)
    if not department:
        abort(404)
    return render_template(
        "department/demographics.html",
        department=department,
        department_values= department.get_raw_department_demographics(),
        city_values= department.get_raw_city_demographics())

@blueprint.route("/<int:department_id>/demographicValue/create",methods=["POST"])
@login_required
@admin_or_department_required()
def new_demographic_row(department_id):
    department = Department.get_by_id(department_id)
    if not department:
        abort(404)

    DemographicValue.create(
        department_id=department_id,
        race=request.form["race"],
        count=int(request.form["count"]),
        department_value=request.form["department_or_city"]=="department")

    return redirect(url_for(
        'department.edit_demographics', department_id=department_id
    ))

@blueprint.route("/<int:department_id>/demographicValue/<int:value_id>/delete",methods=["POST"])
@login_required
@admin_or_department_required()
def delete_demographic_row(department_id, value_id):
    department = Department.get_by_id(department_id)
    value = DemographicValue.get_by_id(value_id)

    if not department or not value:
        abort(404)

    value.delete()

    return redirect(url_for(
        'department.edit_demographics', department_id=department_id
    ))

@blueprint.route("/<int:department_id>/edit/denominators")
@login_required
@admin_or_department_required()
def edit_denominators(department_id):
    department = Department.get_by_id(department_id)
    if not department:
        abort(404)
    return render_template(
        "department/denominators.html",
        department=department,
        denominator_values= department.denominator_values
        )

@blueprint.route("/<int:department_id>/denominatorValue/create",methods=["POST"])
@login_required
@admin_or_department_required()
def new_denominator_row(department_id):
    department = Department.get_by_id(department_id)
    if not department:
        abort(404)

    DenominatorValue.create(
        department_id=department_id,
        month=int(request.form["month"]),
        year=int(request.form["year"]),
        officers_out_on_service=int(request.form["officersOutOnService"])
        )

    return redirect(url_for(
        'department.edit_denominators', department_id=department_id
    ))

@blueprint.route("/<int:department_id>/denominatorValue/<int:value_id>/delete",methods=["POST"])
@login_required
@admin_or_department_required()
def delete_denominator_row(department_id, value_id):
    department = Department.get_by_id(department_id)
    value = DenominatorValue.get_by_id(value_id)

    if not department or not value:
        abort(404)

    value.delete()

    return redirect(url_for(
        'department.edit_denominators', department_id=department_id
    ))

@blueprint.route("/<int:department_id>/edit/index",methods=["GET","POST"])
@login_required
@admin_or_department_required()
def edit_index(department_id):
    department = Department.get_by_id(department_id)
    if not department:
        abort(404)

    return render_template("department/site/index.html", department=department, chart_blocks=department.get_introduction_blocks(), editing=True)

#<<<<<<<< PREVIEW ENDPOINTS >>>>>>>>>>
@blueprint.route("/<int:department_id>/preview/ois")
@login_required
@admin_or_department_required()
def preview_ois(department_id):
    department = Department.get_by_id(department_id)
    if not department:
        abort(404)
    return render_template("department/site/ois.html", department=department, chart_blocks=department.get_ois_blocks(), editing=False)

@blueprint.route("/<int:department_id>/preview/useofforce")
@login_required
@admin_or_department_required()
def preview_use_of_force(department_id):
    department = Department.get_by_id(department_id)
    if not department:
        abort(404)
    return render_template("department/site/useofforce.html", department=department, chart_blocks=department.get_uof_blocks(), editing=False)

@blueprint.route("/<int:department_id>/preview/complaints")
@login_required
@admin_or_department_required()
def preview_complaints(department_id):
    department = Department.get_by_id(department_id)
    if not department:
        abort(404)
    return render_template("department/site/complaints.html", department=department, chart_blocks=department.get_complaint_blocks(), editing=False)

@blueprint.route("/<int:department_id>/preview/index")
@login_required
@admin_or_department_required()
def preview_index(department_id):
    department = Department.get_by_id(department_id)
    if not department:
        abort(404)
    return render_template("department/site/index.html", chart_blocks=department.get_introduction_blocks(), department=department, editing=False)


#<<<<<<<< SCHEMA ENDPOINTS >>>>>>>>>>
@blueprint.route('/<int:department_id>/schema/complaints')
@login_required
@admin_or_department_required()
def use_of_force_schema(department_id):
    department = Department.get_by_id(department_id)
    if not department:
        abort(404)
    return render_template("department/site/schema/complaints.html", department=department)


#<<<<<<<< DATA ENDPOINTS >>>>>>>>>>
@blueprint.route('/<int:department_id>/uof.csv')
def use_of_force_csv(department_id):
    department = Department.get_by_id(department_id)
    if not department:
        abort(404)
    return Response(department.get_uof_csv(), mimetype="text/csv")

@blueprint.route('/<int:department_id>/complaints.csv')
def complaints_csv(department_id):
    department = Department.get_by_id(department_id)
    if not department:
        abort(404)
    return Response(department.get_complaint_csv(), mimetype="text/csv")

@blueprint.route('/<int:department_id>/ois.csv')
def ois_csv(department_id):
    department = Department.get_by_id(department_id)
    if not department:
        abort(404)
    return Response(department.get_ois_csv(), mimetype="text/csv")

@blueprint.route('/<int:department_id>/officerCalls.csv')
def denominator_csv(department_id):
    department = Department.get_by_id(department_id)
    if not department:
        abort(404)
    return Response(department.get_denominator_csv(), mimetype="text/csv")

@blueprint.route('/<int:department_id>/demographics.csv')
def demographics_csv(department_id):
    department = Department.get_by_id(department_id)
    if not department:
        abort(404)
    return Response(department.get_demographic_csv(), mimetype="text/csv")


#<<<<<<<< PUBLIC ENDPOINTS >>>>>>>>>>
@blueprint.route("/IMPD")
def public_intro():
    department = Department.get_by_id(1)
    if not department:
        abort(404)
    return render_template("department/site/index.html", chart_blocks=department.get_introduction_blocks(), department=department, editing=False, published=True)

@blueprint.route("/IMPD/complaints")
def public_complaints():
    department = Department.get_by_id(1)
    if not department:
        abort(404)
    return render_template("department/site/complaints.html", department=department, chart_blocks=department.get_complaint_blocks(), editing=False, published=True)

@blueprint.route('/IMPD/schema/complaints')
def public_complaints_schema():
    department = Department.get_by_id(1)
    if not department:
        abort(404)
    return render_template("department/site/schema/complaints.html", department=department, published=True)

@blueprint.route("/IMPD/useofforce")
def public_uof():
    department = Department.get_by_id(1)
    if not department:
        abort(404)
    return render_template("department/site/useofforce.html", department=department, chart_blocks=department.get_uof_blocks(), editing=False, published=True)

@blueprint.route("/IMPD/officerinvolvedshootings")
def public_ois():
    department = Department.get_by_id(1)
    if not department:
        abort(404)
    return render_template("department/site/ois.html", department=department, chart_blocks=department.get_ois_blocks(), editing=False, published=True)

@blueprint.route('/IMPD/schema/useofforce')
def public_uof_schema():
    department = Department.get_by_id(1)
    if not department:
        abort(404)
    return render_template("department/site/schema/useofforce.html", department=department, published=True)

@blueprint.route('/IMPD/schema/officerinvolvedshootings')
def public_ois_schema():
    department = Department.get_by_id(1)
    if not department:
        abort(404)
    return render_template("department/site/schema/ois.html", department=department, published=True)
