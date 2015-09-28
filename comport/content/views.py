# -*- coding: utf-8 -*-
from flask import Blueprint, redirect, url_for, render_template, flash
from comport.utils import flash_errors
from flask_login import current_user
from flask.ext.login import login_required
from .forms import EditLinkForm

from .models import Link


blueprint = Blueprint("content", __name__, url_prefix='/content',
                      static_folder="../static")

@blueprint.route("/link/new", methods=["GET","POST"])
@login_required
def add_link():
    department_id = current_user.department_id
    form = EditLinkForm()
    if form.validate_on_submit():
        Link.create(title=form.title.data, url=form.url.data, department_id=department_id, type=form.type.data)
        flash("Created.", 'success')
        return redirect(url_for(
            'department.edit_index', department_id=department_id
        ))
    else:
        flash_errors(form)


    return render_template("content/edit_link.html", form=form)

@blueprint.route("/link/<int:link_id>", methods=["GET","POST"])
@login_required
def edit_link(link_id):
    department_id = current_user.department_id
    link = Link.get_by_id(link_id)
    if not link:
        abort(404)
    form = EditLinkForm(obj=link)

    if form.validate_on_submit():
        link.title = form.title.data
        link.url = form.url.data
        link.type = form.type.data
        link.save()

        flash("Updated.", 'success')
        return redirect(url_for(
            'department.edit_index', department_id=department_id
        ))
    else:
        flash_errors(form)


    return render_template("content/edit_link.html", form=form)
