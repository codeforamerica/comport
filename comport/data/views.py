# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, request, redirect, url_for, flash
from comport.utils import flash_errors
from flask.ext.login import login_required
from comport.decorators import admin_or_department_required
import uuid

blueprint = Blueprint("data", __name__, url_prefix='/data',
                      static_folder="../static")
