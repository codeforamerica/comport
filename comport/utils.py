# -*- coding: utf-8 -*-
"""Helper utilities and decorators."""
from flask import flash
import string
import random


def flash_errors(form, category="warning"):
    """Flash all errors for a form."""
    for field, errors in form.errors.items():
        for error in errors:
            flash("{0} - {1}"
                  .format(getattr(form, field).label.text, error), category)

def random_string(N):
    return ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(N))
