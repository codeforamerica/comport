# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, request, redirect, url_for, flash, Response, abort
from .models import Department, Extractor
from comport.data.models import DemographicValue, DenominatorValue
from flask.ext.login import login_required

from comport.decorators import admin_or_department_required, authorized_access_only
import uuid
import datetime

blueprint = Blueprint("department", __name__, url_prefix='/department',
                      static_folder="../static")

# <<<<<<<< ADMIN ENDPOINTS >>>>>>>>>>
@blueprint.route("/<int:department_id>")
@login_required
@admin_or_department_required()
def department_dashboard(department_id):
    department = Department.get_by_id(department_id)
    if not department:
        abort(404)
    current_date = datetime.datetime.now()
    return render_template("department/dashboard.html", department=department, current_month=current_date.month, current_year=current_date.year)


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

@blueprint.route("/<int:department_id>/start", methods=['POST'])
@login_required
@admin_or_department_required()
def start_extractor(department_id):
    department = Department.get_by_id(department_id)
    if not department:
        abort(404)
    if request.method == 'POST':
        if request.form['submit'] == 'Set':
            extractor = department.get_extractor()
            extractor.next_year = request.form["year"]
            extractor.next_month = request.form["month"]
            extractor.save()
            flash("Extractor start date set to {}/{}".format(extractor.next_month, extractor.next_year), "info")
            return redirect(url_for('department.department_dashboard', department_id=department.id))

# <<<<<<<< EDIT ENDPOINTS >>>>>>>>>>
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

@blueprint.route("/<int:department_id>/edit/assaultsonofficers")
@login_required
@admin_or_department_required()
def edit_assaultsonofficers(department_id):
    department = Department.get_by_id(department_id)
    if not department:
        abort(404)
    return render_template("department/site/assaults.html", department=department, chart_blocks=department.get_assaults_blocks(), editing=True)

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
        department_values=department.get_raw_department_demographics(),
        city_values=department.get_raw_city_demographics())

@blueprint.route("/<int:department_id>/demographicValue/create", methods=["POST"])
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
        department_value=request.form["department_or_city"] == "department")

    return redirect(url_for(
        'department.edit_demographics', department_id=department_id
    ))

@blueprint.route("/<int:department_id>/demographicValue/<int:value_id>/delete", methods=["POST"])
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
        denominator_values=department.denominator_values
    )

@blueprint.route("/<int:department_id>/denominatorValue/create", methods=["POST"])
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

@blueprint.route("/<int:department_id>/denominatorValue/<int:value_id>/delete", methods=["POST"])
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

@blueprint.route("/<int:department_id>/edit/index", methods=["GET", "POST"])
@login_required
@admin_or_department_required()
def edit_index(department_id):
    department = Department.get_by_id(department_id)
    if not department:
        abort(404)

    return render_template("department/site/index.html", department=department, chart_blocks=department.get_introduction_blocks(), editing=True)

# <<<<<<<< PREVIEW ENDPOINTS >>>>>>>>>>
@blueprint.route("/<int:department_id>/preview/ois")
@login_required
@admin_or_department_required()
def preview_ois(department_id):
    department = Department.get_by_id(department_id)
    if not department:
        abort(404)
    return render_template("department/site/ois.html", department=department, chart_blocks=department.get_ois_blocks(), editing=False, preview_mode=True, endpoint_name="ois")

@blueprint.route("/<int:department_id>/preview/useofforce")
@login_required
@admin_or_department_required()
def preview_use_of_force(department_id):
    department = Department.get_by_id(department_id)
    if not department:
        abort(404)
    return render_template("department/site/useofforce.html", department=department, chart_blocks=department.get_uof_blocks(), editing=False, preview_mode=True, endpoint_name="useofforce")

@blueprint.route("/<int:department_id>/preview/complaints")
@login_required
@admin_or_department_required()
def preview_complaints(department_id):
    department = Department.get_by_id(department_id)
    if not department:
        abort(404)
    return render_template("department/site/complaints.html", department=department, chart_blocks=department.get_complaint_blocks(), editing=False, preview_mode=True, endpoint_name="complaints")

@blueprint.route("/<int:department_id>/preview/assaultsonofficers")
@login_required
@admin_or_department_required()
def preview_assaults(department_id):
    department = Department.get_by_id(department_id)
    if not department:
        abort(404)
    return render_template("department/site/assaults.html", department=department, chart_blocks=department.get_assaults_blocks(), editing=False, preview_mode=True, endpoint_name="assaultsonofficers")

@blueprint.route("/<int:department_id>/preview/index")
@login_required
@admin_or_department_required()
def preview_index(department_id):
    department = Department.get_by_id(department_id)
    if not department:
        abort(404)
    return render_template("department/site/index.html", chart_blocks=department.get_introduction_blocks(), department=department, editing=False, preview_mode=True, endpoint_name="index")


# <<<<<<<< SCHEMA ENDPOINTS >>>>>>>>>>
@blueprint.route('/<int:department_id>/preview/schema/complaints')
@login_required
@admin_or_department_required()
def complaints_schema_preview(department_id):
    department = Department.get_by_id(department_id)
    if not department:
        abort(404)
    return render_template("department/site/schema/complaints.html", department=department, chart_blocks=department.get_complaint_schema_blocks(), editing=False, preview_mode=True, endpoint_name="complaints")

@blueprint.route('/<int:department_id>/edit/schema/complaints')
@login_required
@admin_or_department_required()
def complaints_schema_edit(department_id):
    department = Department.get_by_id(department_id)
    if not department:
        abort(404)
    return render_template("department/site/schema/complaints.html", department=department, chart_blocks=department.get_complaint_schema_blocks(), editing=True,)

@blueprint.route('/<int:department_id>/preview/schema/useofforce')
@login_required
@admin_or_department_required()
def useofforce_schema_preview(department_id):
    department = Department.get_by_id(department_id)
    if not department:
        abort(404)
    return render_template("department/site/schema/useofforce.html", department=department, chart_blocks=department.get_uof_schema_blocks(), editing=False, preview_mode=True, endpoint_name="useofforce")

@blueprint.route('/<int:department_id>/edit/schema/useofforce')
@login_required
@admin_or_department_required()
def useofforce_schema_edit(department_id):
    department = Department.get_by_id(department_id)
    if not department:
        abort(404)
    return render_template("department/site/schema/useofforce.html", department=department, chart_blocks=department.get_uof_schema_blocks(), editing=True)

@blueprint.route('/<int:department_id>/edit/schema/ois')
@login_required
@admin_or_department_required()
def ois_schema_edit(department_id):
    department = Department.get_by_id(department_id)
    if not department:
        abort(404)
    return render_template("department/site/schema/ois.html", department=department, chart_blocks=department.get_ois_schema_blocks(), editing=True)

@blueprint.route('/<int:department_id>/preview/schema/ois')
@login_required
@admin_or_department_required()
def ois_schema_preview(department_id):
    department = Department.get_by_id(department_id)
    if not department:
        abort(404)
    return render_template("department/site/schema/ois.html", department=department, chart_blocks=department.get_ois_schema_blocks(), editing=False,preview_mode=True, endpoint_name="ois")


@blueprint.route('/<int:department_id>/preview/schema/assaultsonofficers')
@login_required
@admin_or_department_required()
def assaults_schema_preview(department_id):
    department = Department.get_by_id(department_id)
    if not department:
        abort(404)
    return render_template("department/site/schema/assaults.html", department=department, chart_blocks=department.get_assaults_schema_blocks(), editing=False, preview_mode=True, endpoint_name="assaultsonofficers")


@blueprint.route('/<int:department_id>/edit/schema/assaultsonofficers')
@login_required
@admin_or_department_required()
def assaults_schema_edit(department_id):
    department = Department.get_by_id(department_id)
    if not department:
        abort(404)
    return render_template("department/site/schema/assaults.html", department=department, chart_blocks=department.get_assaults_schema_blocks(), editing=True)

# <<<<<<<< DATA ENDPOINTS >>>>>>>>>>
@blueprint.route('/<int:department_id>/uof.csv')
@authorized_access_only(dataset="use_of_force_incidents")
def use_of_force_csv(department_id):
    department = Department.get_by_id(department_id)
    if not department:
        abort(404)
    return Response(department.get_uof_csv(), mimetype="text/csv")

@blueprint.route('/<int:department_id>/complaints.csv')
@authorized_access_only(dataset="citizen_complaints")
def complaints_csv(department_id):
    department = Department.get_by_id(department_id)
    if not department:
        abort(404)
    return Response(department.get_complaint_csv(), mimetype="text/csv")

@blueprint.route('/<int:department_id>/assaultsonofficers.csv')
@authorized_access_only(dataset="assaults_on_officers")
def assaults_csv(department_id):
    department = Department.get_by_id(department_id)
    if not department:
        abort(404)
    return Response(department.get_assaults_csv(), mimetype="text/csv")

@blueprint.route('/<int:department_id>/ois.csv')
@authorized_access_only(dataset="officer_involved_shootings")
def ois_csv(department_id):
    department = Department.get_by_id(department_id)
    if not department:
        abort(404)
    return Response(department.get_ois_csv(), mimetype="text/csv")

@blueprint.route('/<int:department_id>/officerCalls.csv')
@authorized_access_only()
def denominator_csv(department_id):
    department = Department.get_by_id(department_id)
    if not department:
        abort(404)
    return Response(department.get_denominator_csv(), mimetype="text/csv")

@blueprint.route('/<int:department_id>/demographics.csv')
@authorized_access_only()
def demographics_csv(department_id):
    department = Department.get_by_id(department_id)
    if not department:
        abort(404)
    return Response(department.get_demographic_csv(), mimetype="text/csv")


# <<<<<<<< PUBLIC ENDPOINTS >>>>>>>>>>
@blueprint.route("/<short_name>/")
@authorized_access_only()
def public_intro(short_name):
    department = Department.query.filter_by(short_name=short_name.upper()).first()
    if not department:
        abort(404)
    return render_template("department/site/index.html", chart_blocks=department.get_introduction_blocks(), department=department, editing=False, published=True)

@blueprint.route("/<short_name>/complaints/")
@authorized_access_only(dataset="citizen_complaints")
def public_complaints(short_name):
    department = Department.query.filter_by(short_name=short_name.upper()).first()
    if not department:
        abort(404)
    return render_template("department/site/complaints.html", department=department, chart_blocks=department.get_complaint_blocks(), editing=False, published=True)

@blueprint.route('/<short_name>/schema/complaints/')
@authorized_access_only(dataset="citizen_complaints")
def public_complaints_schema(short_name):
    department = Department.query.filter_by(short_name=short_name.upper()).first()
    if not department:
        abort(404)
    return render_template("department/site/schema/complaints.html", department=department, chart_blocks=department.get_complaint_schema_blocks(), published=True)

@blueprint.route("/<short_name>/assaultsonofficers/")
@authorized_access_only(dataset="assaults_on_officers")
def public_assaults(short_name):
    department = Department.query.filter_by(short_name=short_name.upper()).first()
    if not department:
        abort(404)
    return render_template("department/site/assaults.html", department=department, chart_blocks=department.get_assaults_blocks(), editing=False, published=True)

@blueprint.route('/<short_name>/schema/assaultsonofficers/')
@authorized_access_only(dataset="assaults_on_officers")
def public_assaults_schema(short_name):
    department = Department.query.filter_by(short_name=short_name.upper()).first()
    if not department:
        abort(404)
    return render_template("department/site/schema/assaults.html", department=department, chart_blocks=department.get_assaults_schema_blocks(), editing=False, published=True)

@blueprint.route("/<short_name>/useofforce/")
@authorized_access_only(dataset="use_of_force_incidents")
def public_uof(short_name):
    department = Department.query.filter_by(short_name=short_name.upper()).first()
    if not department:
        abort(404)
    return render_template("department/site/useofforce.html", department=department, chart_blocks=department.get_uof_blocks(), editing=False, published=True)

@blueprint.route("/<short_name>/officerinvolvedshootings/")
@authorized_access_only(dataset="officer_involved_shootings")
def public_ois(short_name):
    department = Department.query.filter_by(short_name=short_name.upper()).first()
    if not department:
        abort(404)
    return render_template("department/site/ois.html", department=department, chart_blocks=department.get_ois_blocks(), editing=False, published=True)

@blueprint.route('/<short_name>/schema/useofforce/')
@authorized_access_only(dataset="use_of_force_incidents")
def public_uof_schema(short_name):
    department = Department.query.filter_by(short_name=short_name.upper()).first()
    if not department:
        abort(404)
    return render_template("department/site/schema/useofforce.html", department=department, chart_blocks=department.get_uof_schema_blocks(), editing=False, published=True)

@blueprint.route('/<short_name>/schema/officerinvolvedshootings/')
@authorized_access_only(dataset="officer_involved_shootings")
def public_ois_schema(short_name):
    department = Department.query.filter_by(short_name=short_name.upper()).first()
    if not department:
        abort(404)
    return render_template("department/site/schema/ois.html", department=department, chart_blocks=department.get_ois_schema_blocks(), editing=False, published=True)
