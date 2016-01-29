# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, request, redirect, url_for, flash, abort
from comport.utils import flash_errors
from flask.ext.login import login_required
from .forms import NewDepartmentForm, NewInviteForm, EditUserForm, EditExtractorForm
from comport.department.models import Department, Extractor
from comport.user.models import Invite_Code, User
from comport.interest.models import Interested
from comport.decorators import requires_roles
import uuid

blueprint = Blueprint("admin", __name__, url_prefix='/admin',
                      static_folder="../static")


@blueprint.route("/")
@login_required
@requires_roles(["admin"])
def admin_dashboard():
    interesteds=Interested.query.all()
    invites=Invite_Code.query.filter_by(used=False)
    users=User.query.filter_by(active=True)
    extractors = Extractor.query.all()
    return render_template("admin/dashboard.html", interesteds=interesteds, invites=invites, users=users, extractors=extractors)

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

@blueprint.route("/user/<int:user_id>/edit", methods=["GET", "POST"] )
@login_required
@requires_roles(["admin"])
def edit_user(user_id):
    user = User.get_by_id(user_id)
    if not user:
        abort(404)

    form = EditUserForm(request.form, departments=[d.id for d in user.departments])
    form.departments.choices =  [(d.id, d.name) for d in Department.query.order_by('name')]

    if request.method == 'POST':
        user.departments = [Department.get_by_id(int(d)) for d in form.departments.data ]
        user.save()
        flash('User updated.', 'info')
        return redirect(url_for('admin.admin_dashboard'))


    return render_template("admin/editUser.html", form=form, user=user)

@blueprint.route("/user/<int:user_id>/passwordReset", methods=["GET", "POST"] )
@login_required
@requires_roles(["admin"])
def start_password_reset(user_id):
    user = User.get_by_id(user_id)
    if not user:
        abort(404)

    if request.method == 'POST':
        user.password_reset_uuid = str(uuid.uuid4())
        user.save()
        flash('User password reset engaged.', 'info')
        return redirect(url_for('admin.edit_user',user_id=user_id))


    return redirect(url_for('admin.edit_user',user_id=user_id))


@blueprint.route("/extractor/<int:extractor_id>/edit", methods=["GET", "POST"] )
@login_required
@requires_roles(["admin"])
def edit_extractor(extractor_id):
    extractor = Extractor.get_by_id(extractor_id)
    if not extractor:
        abort(404)

    form = EditExtractorForm(request.form, departments=[d.id for d in extractor.departments])
    form.departments.choices =  [(d.id, d.name) for d in Department.query.order_by('name')]

    if request.method == 'POST':
        extractor.departments = [Department.get_by_id(int(d)) for d in form.departments.data ]
        extractor.save()
        flash('Extractor updated.', 'info')
        return redirect(url_for('admin.admin_dashboard'))


    return render_template("admin/editExtractor.html", form=form, extractor=extractor)
