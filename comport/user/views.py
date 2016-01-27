# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, url_for, redirect
from flask.ext.login import login_required
from flask_login import current_user

blueprint = Blueprint("user", __name__, url_prefix='/users',
                      static_folder="../static")


@blueprint.route("/")
@login_required
def home():
    if current_user.is_admin():
        redirect_url = url_for("admin.admin_dashboard")
        return redirect(redirect_url)
    else:
        redirect_url = url_for("department.department_dashboard", department_id=current_user.department_id)
        return redirect(redirect_url)
