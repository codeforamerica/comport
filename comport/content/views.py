# -*- coding: utf-8 -*-
from flask import Blueprint, redirect, url_for, request, abort
from flask_login import current_user
from flask.ext.login import login_required
from urllib.parse import urlparse
from .models import ChartBlock


blueprint = Blueprint("content", __name__, url_prefix='/content',
                      static_folder="../static")

@blueprint.route("/<string:chart_slug>/<int:department_id>", methods=["POST"])
@login_required
def edit_chart_block(department_id, chart_slug):
    block = ChartBlock.query.filter_by(department_id=department_id, slug=chart_slug).first()

    if not block:
        abort(404)

    if not current_user.has_department(department_id) and not current_user.is_admin():
        abort(401)

    block.title = request.form["chart_title"]
    block.content = request.form["chart_content"]
    block.order = request.form["chart_order"]

    block.save()

    if request.referrer and 'edit' in request.referrer:
        new_path = urlparse(request.referrer.replace('/edit/', '/preview/')).path
    else:
        new_path = url_for(
            'department.department_dashboard', department_id=department_id
        )

    return redirect(new_path)
