# -*- coding: utf-8 -*-
"""Helper utilities and decorators."""
from flask import flash
import string
from random import randint, choice
from datetime import datetime, timedelta
from factory.fuzzy import _random


def flash_errors(form, category="warning"):
    """Flash all errors for a form."""
    for field, errors in form.errors.items():
        for error in errors:
            flash("{0} - {1}"
                  .format(getattr(form, field).label.text, error), category)

def random_string(N):
    return ''.join(choice(string.ascii_uppercase + string.digits + '     ') for _ in range(N))

def factory_random_string(N):
    return ''.join(_random.choice(string.ascii_uppercase + string.digits) for _ in range(N))

def parse_date(date):
    return None if not date else datetime.strptime(date, '%Y-%m-%d %H:%M:%S')

def parse_csv_date(date):
    try:
        return None if date == 'NULL' else datetime.strptime(date, '%m/%d/%y')
    except ValueError:
        print("Can't parse the following date: " + date)

def parse_int(data):
    if data == "":
        return None
    return int(data)

def random_date(start, end):
    return start + timedelta(
        seconds=randint(0, int((end - start).total_seconds())))

def diff_month(d1, d2):
    return (d1.year - d2.year) * 12 + d1.month - d2.month

def coalesce_date(date):
    return "" if date is None else datetime.strftime(date, '%Y-%m-%d %H:%M:%S')
