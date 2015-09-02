# -*- coding: utf-8 -*-
from flask import Blueprint, render_template
from flask.ext.login import login_required
from comport.decorators import requires_roles

blueprint = Blueprint("admin", __name__, url_prefix='/admin',
                      static_folder="../static")


@blueprint.route("/")
@login_required
@requires_roles(["admin"])
def admin_dashboard():
    return render_template("admin/dashboard.html")
