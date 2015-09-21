# -*- coding: utf-8 -*-
from flask_wtf import Form
from wtforms import TextAreaField

from wtforms.validators import DataRequired

class IndexContentForm(Form):
    why_we_are_doing_this = TextAreaField('Why We Are Doing This')
    what_this_is = TextAreaField('What Is This')
    how_you_can_use_this_data = TextAreaField('How You Can Use This')
    contact_us = TextAreaField('contact_us')


    def __init__(self, *args, **kwargs):
        super(IndexContentForm, self).__init__(*args, **kwargs)
