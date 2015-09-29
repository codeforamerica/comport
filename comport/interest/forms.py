# -*- coding: utf-8 -*-
from flask_wtf import Form
from wtforms import TextField
from wtforms.validators import DataRequired, Email

class InterestForm(Form):
    name = TextField('Full Name', validators=[DataRequired()])
    agency = TextField('Agency', validators=[DataRequired()])
    location = TextField('City, State', validators=[DataRequired()])
    phone = TextField('Phone', validators=[DataRequired()])
    email = TextField('Email', validators=[DataRequired(), Email()])
    comments = TextField('Questions/Comments (Optional)', validators=[])

    def __init__(self, *args, **kwargs):
        super(InterestForm, self).__init__(*args, **kwargs)

    def validate(self):
        initial_validation = super(InterestForm, self).validate()
        if not initial_validation:
            return False

        return True
