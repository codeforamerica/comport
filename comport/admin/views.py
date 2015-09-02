# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, request, redirect, url_for, flash
from comport.utils import flash_errors
from flask.ext.login import login_required
from .forms import NewDepartmentForm, NewInviteForm
from comport.department.models import Department
from comport.user.models import Invite_Code
from comport.decorators import requires_roles
import uuid

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
    if request.method == 'POST':
        if form.validate_on_submit():
            Department.create(name=form.department_name.data)
            flash('Department %s created.' % form.department_name.data, 'info')
            return redirect(url_for('admin.admin_dashboard'))
        else:
            flash_errors(form)
    return render_template("admin/newDepartment.html", form=form)

@blueprint.route("/invite/new", methods=["GET", "POST"] )
@login_required
@requires_roles(["admin"])
def new_invite_code():
    form = NewInviteForm(request.form)
    form.department_id.choices =  [(d.id, d.name) for d in Department.query.order_by('name')]
    if request.method == 'POST':
        if form.validate_on_submit():
            invite = Invite_Code.create(department_id=form.department_id.data, code=str(uuid.uuid4()), used=False)
            flash('Invite Code for {0}: {1} created.'.format(invite.department.name, invite.code), 'info')
            return redirect(url_for('admin.view_active_invites'))
        else:
            flash_errors(form)
    return render_template("admin/newInvite.html", form=form)


@blueprint.route("/invite/", methods=["GET"] )
@login_required
@requires_roles(["admin"])
def view_active_invites():
    return render_template("admin/showInvites.html", invites=Invite_Code.query.filter_by(used=False))
