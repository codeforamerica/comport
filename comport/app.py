# -*- coding: utf-8 -*-
"""The app module, containing the app factory function."""
from flask import Flask, render_template

from comport.settings import ProdConfig
from comport.assets import assets
from comport.extensions import (
    bcrypt,
    cache,
    db,
    login_manager,
    migrate,
    debug_toolbar,
)
from comport import (public, user, admin, department, data, content, interest, template_globals)
from flask_sslify import SSLify
import logging
import sys
import os


def create_app(config_object=ProdConfig):
    """An application factory, as explained here:
        http://flask.pocoo.org/docs/patterns/appfactories/

    :param config_object: The configuration object to use.
    """
    app = Flask(__name__)
    sslify = SSLify(app)
    app.config.from_object(config_object)
    register_extensions(app)
    register_blueprints(app)
    register_errorhandlers(app)
    register_template_globals(app)

    @app.before_first_request
    def before_first_request():
        register_logging(app)

    return app


def register_extensions(app):
    assets.init_app(app)
    bcrypt.init_app(app)
    cache.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    debug_toolbar.init_app(app)
    migrate.init_app(app, db)
    return None

def register_blueprints(app):
    app.register_blueprint(public.views.blueprint)
    app.register_blueprint(user.views.blueprint)
    app.register_blueprint(admin.views.blueprint)
    app.register_blueprint(department.views.blueprint)
    app.register_blueprint(data.views.blueprint)
    app.register_blueprint(content.views.blueprint)
    app.register_blueprint(interest.views.blueprint)
    return None

def register_errorhandlers(app):
    def render_error(error):
        # If a HTTPException, pull the `code` attribute; default to 500
        error_code = getattr(error, 'code', 500)
        return render_template("{0}.html".format(error_code)), error_code
    for errcode in [401, 404, 500]:
        app.errorhandler(errcode)(render_error)
    return None

def register_template_globals(app):
    app.jinja_env.globals.update(markdown=template_globals.markdown)


def register_logging(app):
    if 'config.ProductionConfig' in os.environ.get('APP_SETTINGS', []):

        print("PROD LOGGING ENGAGED")

        # for heroku, just send everything to the console (instead of a file)
        # and it will forward automatically to the logging service

        # disable the existing flask handler, we are replacing it with our own
        app.logger.removeHandler(app.logger.handlers[0])

        app.logger.setLevel(logging.DEBUG)
        stdout = logging.StreamHandler(sys.stdout)
        stdout.setFormatter(logging.Formatter(
            '''--------------------------------------------------------------------------------
%(asctime)s | %(levelname)s in %(module)s [%(funcName)s] | %(user_id)s | [%(pathname)s:%(lineno)d] | %(message)s
--------------------------------------------------------------------------------'''
        ))
        app.logger.addHandler(stdout)

        # log to a file. this is commented out for heroku deploy, but kept
        # in case we need it later

        # file_handler = logging.handlers.RotatingFileHandler(log_file(app), 'a', 10000000, 10)
        # file_handler.setFormatter(logging.Formatter(
        #     '%(asctime)s | %(name)s | %(levelname)s in %(module)s [%(pathname)s:%(lineno)d]: %(message)s')
        # )
        # app.logger.addHandler(file_handler)
        # app.logger.setLevel(logging.DEBUG)

    else:
        # log to console for dev
        app.logger.setLevel(logging.DEBUG)

    return None
