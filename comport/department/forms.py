# -*- coding: utf-8 -*-
from flask_wtf import Form
from wtforms import TextAreaField

from wtforms.validators import DataRequired

class IndexContentForm(Form):
    why_we_are_doing_this = TextAreaField('Why We Are Doing This')

    def __init__(self, *args, **kwargs):
        super(IndexContentForm, self).__init__(*args, **kwargs)
