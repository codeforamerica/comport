# -*- coding: utf-8 -*-
from flask_wtf import Form
from wtforms import TextField, SelectField

from wtforms.validators import DataRequired

class EditLinkForm(Form):
    title = TextField("Title", validators=[DataRequired()])
    url  = TextField("Url", validators=[DataRequired()])
    type = SelectField('Type of Link', choices=[("policy","policy"),("training","training"),("outreach","outreach")])

    def validate(self):
        return super(EditLinkForm, self).validate()

    def __init__(self, *args, **kwargs):
        super(EditLinkForm, self).__init__(*args, **kwargs)
