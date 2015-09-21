# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, request, redirect, url_for, flash, send_file, Response
from comport.utils import flash_errors
from .models import Department, Extractor
from .forms import IndexContentForm
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

#<<<<<<<< SITE ENDPOINTS >>>>>>>>>>
@blueprint.route("/<int:department_id>/site/useofforce")
@login_required
@admin_or_department_required()
def use_of_force(department_id):
    department = Department.get_by_id(department_id)
    if not department:
        abort(404)
    return render_template("department/useofforce.html", department=department, chart_blocks=department.get_uof_blocks())

@blueprint.route("/<int:department_id>/site/index",methods=["GET","POST"])
@login_required
@admin_or_department_required()
def index(department_id):
    department = Department.get_by_id(department_id)
    if not department:
        abort(404)
    form = IndexContentForm(request.form)

    if form.validate_on_submit():
        department.why_we_are_doing_this = form.why_we_are_doing_this.data
        department.what_this_is = form.what_this_is.data
        department.contact_us = form.contact_us.data
        department.how_you_can_use_this_data = form.how_you_can_use_this_data.data
        department.save()
        flash("Saved.", 'success')
        return redirect(url_for(
            'department.index', department_id=department_id
        ))
    else:
        flash_errors(form)



    form.why_we_are_doing_this.data = department.why_we_are_doing_this
    form.what_this_is.data = department.what_this_is
    form.contact_us.data = department.contact_us
    form.how_you_can_use_this_data.data = department.how_you_can_use_this_data

    return render_template("department/index.html", form=form, department=department)


#<<<<<<<< DATA ENDPOINTS >>>>>>>>>>
@blueprint.route('/<int:department_id>/uof.csv')
@login_required
@admin_or_department_required()
def use_of_force_csv(department_id):
    department = Department.get_by_id(department_id)
    if not department:
        abort(404)
    return Response(department.get_uof_csv(), mimetype="text/csv")

@blueprint.route('/<int:department_id>/denominator.csv')
@login_required
@admin_or_department_required()
def denominator_csv(department_id):
    department = Department.get_by_id(department_id)
    if not department:
        abort(404)
    return Response(department.get_denominator_csv(), mimetype="text/csv")
