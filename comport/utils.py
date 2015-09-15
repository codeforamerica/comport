# -*- coding: utf-8 -*-
"""Helper utilities and decorators."""
from flask import flash
import string
from random import randint
from datetime import datetime, timedelta


def flash_errors(form, category="warning"):
    """Flash all errors for a form."""
    for field, errors in form.errors.items():
        for error in errors:
            flash("{0} - {1}"
                  .format(getattr(form, field).label.text, error), category)

def random_string(N):
    return ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(N))

def parse_date(date):
    return None if date == 'NULL' else datetime.strptime(date, '%Y-%m-%d %H:%M:%S')

def random_date(start, end):
    return start + timedelta(
        seconds=randint(0, int((end - start).total_seconds())))
