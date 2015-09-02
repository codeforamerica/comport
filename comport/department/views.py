# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, request, redirect, url_for, flash
from comport.utils import flash_errors
from .models import Department
from flask.ext.login import login_required
from comport.decorators import admin_or_department_required


blueprint = Blueprint("department", __name__, url_prefix='/department',
                      static_folder="../static")


@blueprint.route("/<int:department_id>")
@login_required
@admin_or_department_required()
def department_dashboard(department_id):
    department = Department.get_by_id(department_id)
    return render_template("department/dashboard.html", department=department)
