# encoding: utf-8
import logging
import os
import subprocess
from logging.handlers import RotatingFileHandler
from flask_babelex import gettext, Babel
from flask import Flask, render_template, g, jsonify, request
from flask_mail import Mail
from flask_migrate import Migrate
from flask_socketio import SocketIO
from models import db

import texttable
from flask_debugtoolbar import DebugToolbarExtension

from utils import InvalidUsage, utils_download_and_ingest_faa

from pprint import pprint as pp
import click

from version import VERSION

__VERSION__ = VERSION

try:
    from raven.contrib.flask import Sentry
    import raven

    print(" * Sentry support loaded")
    HAS_SENTRY = True
except ImportError:
    print(" * No Sentry support")
    HAS_SENTRY = False

mail = Mail()
socketio = SocketIO()


def create_app(config_filename="config.py", app_name=None, register_blueprints=True):
    # App configuration
    app = Flask(app_name or __name__)
    app.config.from_pyfile(config_filename)

    socketio.init_app(app, message_queue=app.config['SOCKETIO_MESSAGE_QUEUE'])

    app.jinja_env.add_extension("jinja2.ext.with_")
    app.jinja_env.add_extension("jinja2.ext.do")

    if HAS_SENTRY:
        app.config["SENTRY_RELEASE"] = raven.fetch_git_sha(os.path.dirname(__file__))
        sentry = Sentry(app, dsn=app.config["SENTRY_DSN"])  # noqa: F841
        print(" * Sentry support activated")
        print(" * Sentry DSN: %s" % app.config["SENTRY_DSN"])

    if app.config["DEBUG"] is True:
        app.jinja_env.auto_reload = True
        app.logger.setLevel(logging.DEBUG)

    # Logging
    if not app.debug:
        formatter = logging.Formatter("%(asctime)s %(levelname)s: %(message)s " "[in %(pathname)s:%(lineno)d]")
        file_handler = RotatingFileHandler("%s/errors_app.log" % os.getcwd(), "a", 1000000, 1)
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)
        app.logger.addHandler(file_handler)

    mail.init_app(app)
    migrate = Migrate(app, db)  # noqa: F841
    babel = Babel(app)  # noqa: F841
    toolbar = DebugToolbarExtension(app)  # noqa: F841

    db.init_app(app)

    git_version = ""
    gitpath = os.path.join(os.getcwd(), ".git")
    if os.path.isdir(gitpath):
        git_version = subprocess.check_output(["git", "rev-parse", "--short", "HEAD"])
        if git_version:
            git_version = git_version.strip().decode("UTF-8")

    @babel.localeselector
    def get_locale():
        # if a user is logged in, use the locale from the user settings
        identity = getattr(g, "identity", None)
        if identity is not None and identity.id:
            return identity.user.locale
        # otherwise try to guess the language from the user accept
        # header the browser transmits.  We support fr/en in this
        # example.  The best match wins.
        return request.accept_languages.best_match(["fr", "en"])

    @babel.timezoneselector
    def get_timezone():
        identity = getattr(g, "identity", None)
        if identity is not None and identity.id:
            return identity.user.timezone

    @app.before_request
    def before_request():
        cfg = {
            "PYAIRWAVES_VERSION_VER": VERSION,
            "PYAIRWAVES_VERSION_GIT": git_version,
            "PYAIRWAVES_VERSION": "{0} ({1})".format(VERSION, git_version),
        }
        g.cfg = cfg

    @app.errorhandler(InvalidUsage)
    def handle_invalid_usage(error):
        response = jsonify(error.to_dict())
        response.status_code = error.status_code
        return response

    if register_blueprints:
        from controllers.main import bp_main

        app.register_blueprint(bp_main)

    @app.errorhandler(404)
    def page_not_found(msg):
        pcfg = {
            "title": gettext("Whoops, something failed."),
            "error": 404,
            "message": gettext("Page not found"),
            "e": msg,
        }
        return render_template("error_page.jinja2", pcfg=pcfg), 404

    @app.errorhandler(403)
    def err_forbidden(msg):
        pcfg = {
            "title": gettext("Whoops, something failed."),
            "error": 403,
            "message": gettext("Access forbidden"),
            "e": msg,
        }
        return render_template("error_page.jinja2", pcfg=pcfg), 403

    @app.errorhandler(410)
    def err_gone(msg):
        pcfg = {"title": gettext("Whoops, something failed."), "error": 410, "message": gettext("Gone"), "e": msg}
        return render_template("error_page.jinja2", pcfg=pcfg), 410

    if not app.debug:

        @app.errorhandler(500)
        def err_failed(msg):
            pcfg = {
                "title": gettext("Whoops, something failed."),
                "error": 500,
                "message": gettext("Something is broken"),
                "e": msg,
            }
            return render_template("error_page.jinja2", pcfg=pcfg), 500

    @app.after_request
    def set_x_powered_by(response):
        response.headers["X-Powered-By"] = "pyAirwaves"
        return response

    # Other commands
    @app.cli.command()
    def routes():
        """Dump all routes of defined app"""
        table = texttable.Texttable()
        table.set_deco(texttable.Texttable().HEADER)
        table.set_cols_dtype(["t", "t", "t"])
        table.set_cols_align(["l", "l", "l"])
        table.set_cols_width([50, 30, 80])

        table.add_rows([["Prefix", "Verb", "URI Pattern"]])

        for rule in sorted(app.url_map.iter_rules(), key=lambda x: str(x)):
            methods = ",".join(rule.methods)
            table.add_row([rule.endpoint, methods, rule])

        print(table.draw())

    @app.cli.command()
    def config():
        """Dump config"""
        pp(app.config)

    @app.cli.command()
    def seed():
        """Seed database with default content"""
        #make_db_seed(db)
        pass

    @app.cli.command()
    def download_and_ingest_faa():
        """Downloads and ingest FAA datas"""
        utils_download_and_ingest_faa()

    return app


if __name__ == '__main__':
    import eventlet
    eventlet.monkey_patch()
    socketio.run(create_app())
