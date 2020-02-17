from flask import Blueprint, render_template

bp_main = Blueprint("bp_main", __name__)


# Show map
@bp_main.route("/")
def home():
    pcfg = {"title": "Map"}

    return render_template("home.jinja2", pcfg=pcfg)


@bp_main.route("/about")
def about():
    pcfg = {"title": "About"}

    return render_template("about.jinja2", pcfg=pcfg)
