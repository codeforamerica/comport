# -*- coding: utf-8 -*-
"""Public section, including homepage and signup."""
from flask import (Blueprint, request, render_template, flash, url_for, abort, redirect)
from flask.ext.login import login_user, login_required, logout_user

from comport.extensions import login_manager
from comport.user.models import User, Invite_Code
from comport.department.models import Department
from comport.public.forms import LoginForm
from comport.user.forms import RegisterForm, PasswordResetForm
from comport.utils import flash_errors

blueprint = Blueprint('public', __name__, static_folder="../static")


@login_manager.user_loader
def load_user(id):
    return User.get_by_id(int(id))


@blueprint.route("/", methods=["GET"])
def home():
    return render_template("public/home.html", published=True)


@blueprint.route("/login/", methods=["GET", "POST"])
def login():
    form = LoginForm(request.form)
    # Handle logging in
    if request.method == 'POST':
        if form.validate_on_submit():
            login_user(form.user)
            flash("You are logged in.", 'success')
            if form.user.is_admin():
                redirect_url = request.args.get("next") or url_for("admin.admin_dashboard")
                return redirect(redirect_url)
            else:
                if request.args.get("next"):
                    return redirect(request.args.get("next"))
                if form.user.first_department():
                    return redirect(url_for("department.department_dashboard", department_id=form.user.first_department().id))
                else:
                    flash("You are not registered in any department. Please contact support.", 'alert alert-danger')
                    return render_template("public/login.html", form=form, published=True)
        else:
            flash_errors(form)
    return render_template("public/login.html", form=form, published=True)


@blueprint.route('/logout/')
@login_required
def logout():
    logout_user()
    flash('You are logged out.', 'info')
    return redirect(url_for('public.home'))


@blueprint.route("/register/", methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form, csrf_enabled=False)
    if form.validate_on_submit():
        invite_code = Invite_Code.query.filter_by(code=form.invite_code.data).first()
        invite_code.used = True
        invite_code.save()

        new_user = User.create(
            username=form.username.data,
            email=form.email.data,
            password=form.password.data,
            active=True
        )

        new_user.departments.append(Department.get_by_id(invite_code.department_id))

        flash("Thank you for registering. You can now log in.", 'success')
        return redirect(url_for('public.home'))
    else:
        flash_errors(form)
    return render_template('public/register.html', form=form)

@blueprint.route("/passwordReset/<password_reset_uuid>", methods=['GET', 'POST'])
def password_reset(password_reset_uuid):

    user = User.query.filter_by(password_reset_uuid=password_reset_uuid).first()

    if not user:
        abort(404)

    form = PasswordResetForm(request.form, csrf_enabled=False)
    if form.validate_on_submit():
        user.password_reset_uuid = None
        user.set_password(form.password.data)
        user.save()
        flash("Thank you for resetting your password. You can now log in.", 'success')
        return redirect(url_for('public.login'))
    else:
        flash_errors(form)

    return render_template('public/passwordReset.html', form=form)


@blueprint.route("/about/")
def about():
    form = LoginForm(request.form)
    return render_template("public/about.html", form=form)
