# -*- coding: utf-8 -*-
"""Public section, including homepage and signup."""
from flask import (Blueprint, request, render_template, flash, url_for, redirect)

from comport.interest.models import Interested
from comport.interest.forms import InterestForm
from comport.utils import flash_errors

blueprint = Blueprint('interest', __name__, url_prefix='/interest', static_folder="../static")

@blueprint.route("/", methods=["GET", "POST"])
def home():
    form = InterestForm(request.form, csrf_enabled=False)
    if request.method == 'POST':
        if form.validate_on_submit():
            Interested.create(
                name=form.name.data,
                agency=form.agency.data,
                location=form.location.data,
                phone=form.phone.data,
                email=form.email.data,
                comments=form.comments.data)
            flash("Thank you. We will be in contact shortly.", 'success')
            return redirect(url_for('public.home'))
        else:
            flash_errors(form)
    return render_template("public/interest_form.html", interest_form=form)
