# -*- coding: utf-8 -*-
"""Helper utilities and decorators."""
from flask import flash, current_app
import requests
import json
import string
from random import randint, choice
from datetime import datetime, timedelta

def slack_escape(str):
    ''' Escape a string to be sent to Slack, as per https://api.slack.com/docs/formatting#how_to_escape_characters
    '''
    return str.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')

def send_slack_message(title='', body_lines=None):
    ''' Send a slack webhook with the passed message. Body can be a string or a list of strings; each string in the list will be shown on its own line.
    '''
    # Only send if a Slack webhook URL has been set
    webhook_url = current_app.config.get('SLACK_WEBHOOK_URL')
    if webhook_url:
        # format the title
        title_text = 'New Message from Comport!'
        if title:
            title_text = '*{}*'.format(title)

        body_text = ''
        fallback_text = ''
        if body_lines:
            if type(body_lines) is list:
                body_lines = [slack_escape(line) for line in body_lines if line]
            else:
                body_lines = [slack_escape(body_lines)]
            fallback_text = ', '.join(body_lines)
            body_text = '\n'.join(body_lines)

        attachment_values = dict(text=body_text, fallback=fallback_text, color="#0071bc")
        payload_values = dict(text=title_text)
        payload_values['attachments'] = [attachment_values]
        payload = json.dumps(payload_values)
        headers = {'Content-type': 'application/json'}
        requests.post(webhook_url, data=payload, headers=headers)

def flash_errors(form, category="warning"):
    """Flash all errors for a form."""
    for field, errors in form.errors.items():
        for error in errors:
            flash("{0} - {1}"
                  .format(getattr(form, field).label.text, error), category)

def random_string(N):
    return ''.join(choice(string.ascii_uppercase + string.digits + '     ') for _ in range(N))

def parse_date(date):
    parsed = None
    # try it with time
    try:
        parsed = datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
    except (ValueError, TypeError):
        pass

    # try it without time
    try:
        parsed = datetime.strptime(date, '%Y-%m-%d')
    except (ValueError, TypeError):
        pass

    return parsed

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
