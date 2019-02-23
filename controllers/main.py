from flask import Blueprint, render_template
from flask_babelex import gettext

bp_main = Blueprint("bp_main", __name__)


# Show public logbooks
@bp_main.route("/")
def home():
    pcfg = {"title": gettext("Home")}

    return render_template("home.jinja2", pcfg=pcfg)


@bp_main.route("/about")
def about():
    return render_template("about.jinja2")
