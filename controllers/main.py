from flask import Blueprint, render_template, redirect

bp_main = Blueprint("bp_main", __name__)


# Show public logbooks
@bp_main.route("/")
def home():
    pcfg = {"title": "Home"}

    return render_template("home.jinja2", pcfg=pcfg)


@bp_main.route("/about")
def about():
    return redirect("https://github.com/rhaamo/pyAirwaves/")
