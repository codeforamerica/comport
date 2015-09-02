# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, request, redirect, url_for, flash
from comport.utils import flash_errors
from flask.ext.login import login_required
from .forms import NewDepartmentForm
from comport.department.models import Department
from comport.decorators import requires_roles

blueprint = Blueprint("admin", __name__, url_prefix='/admin',
                      static_folder="../static")


@blueprint.route("/")
@login_required
@requires_roles(["admin"])
def admin_dashboard():
    return render_template("admin/dashboard.html")

@blueprint.route("/department/new", methods=["GET", "POST"] )
@login_required
@requires_roles(["admin"])
def add_department():
    form = NewDepartmentForm(request.form)
    # Handle logging in
    if request.method == 'POST':
        if form.validate_on_submit():
            Department.create(name=form.department_name.data)
            flash('Department %s created.' % form.department_name.data, 'info')
            return redirect(url_for('admin.admin_dashboard'))
        else:
            flash_errors(form)
    return render_template("admin/newDepartment.html", form=form)
