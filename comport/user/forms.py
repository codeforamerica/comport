# -*- coding: utf-8 -*-
from flask_wtf import Form
from wtforms import TextField, PasswordField
from wtforms.validators import DataRequired, Email, EqualTo, Length

from .models import User, Invite_Code


class PasswordResetForm(Form):
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6, max=40)])
    confirm = PasswordField('Verify password', [DataRequired(), EqualTo('password', message='Passwords must match')])

    def __init__(self, *args, **kwargs):
        super(PasswordResetForm, self).__init__(*args, **kwargs)

    def validate(self):
        initial_validation = super(PasswordResetForm, self).validate()
        if not initial_validation:
            return False
        return True


class RegisterForm(Form):
    username = TextField('Username', validators=[DataRequired(), Length(min=3, max=25)])
    email = TextField('Email', validators=[DataRequired(), Email(), Length(min=6, max=40)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6, max=40)])
    confirm = PasswordField('Verify password', [DataRequired(), EqualTo('password', message='Passwords must match')])

    invite_code = TextField('Invite Code', validators=[DataRequired()])

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        self.user = None

    def validate(self):
        initial_validation = super(RegisterForm, self).validate()
        if not initial_validation:
            return False
        user = User.query.filter_by(username=self.username.data).first()
        if user:
            self.username.errors.append("Username already registered")
            return False
        user = User.query.filter_by(email=self.email.data).first()
        if user:
            self.email.errors.append("Email already registered")
            return False
        found_invite_code = Invite_Code.query.filter_by(code=self.invite_code.data).first()
        if not found_invite_code:
            self.invite_code.errors.append("Invite Code not recognized.")
            return False
        if found_invite_code.used:
            self.invite_code.errors.append("Invite Code has already been used.")
            return False
        return True
