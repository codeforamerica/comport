# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, url_for, redirect, flash, request
from flask.ext.login import login_required
from flask_login import current_user
from comport.public.forms import LoginForm

blueprint = Blueprint("user", __name__, url_prefix='/users',
                      static_folder="../static")


@blueprint.route("/")
@login_required
def home():
    form = LoginForm(request.form)
    if current_user.is_admin():
        redirect_url = url_for("admin.admin_dashboard")
        return redirect(redirect_url)
    else:
        if current_user.first_department():
            return redirect(url_for("department.department_dashboard", department_id=current_user.first_department().id))
        else:
            flash("You are not registered in any department. Please contact support.", 'alert alert-danger')
            return render_template("public/login.html", form=form, published=True)
