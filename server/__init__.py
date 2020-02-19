import quart.flask_patch  # noqa: F401
from quart import Quart, websocket, render_template, g
import aioredis
import asyncio
import json
import os
import subprocess


VERSION = "0.0.1"
__VERSION__ = VERSION


def create_app():
    app = Quart(__name__)
    app.config.from_pyfile("config.py")

    if app.config["DEBUG"] is True:
        app.jinja_env.auto_reload = True

    git_version = ""
    gitpath = os.path.join(os.getcwd(), ".git")
    if os.path.isdir(gitpath):
        git_version = subprocess.check_output(["git", "rev-parse", "--short", "HEAD"])
        if git_version:
            git_version = git_version.strip().decode("UTF-8")

    @app.before_request
    async def before_request():
        cfg = {
            "PYAIRWAVES_VERSION_VER": VERSION,
            "PYAIRWAVES_VERSION_GIT": git_version,
            "PYAIRWAVES_VERSION": "{0} ({1})".format(VERSION, git_version),
        }
        g.cfg = cfg

    @app.route("/", methods=["GET"])
    async def home():
        return await render_template("home.jinja2")

    @app.websocket("/ws")
    async def ws():
        sub = await aioredis.create_redis("redis://localhost/4")

        res = await sub.subscribe("chan:1")
        ch1 = res[0]
        while True:
            await asyncio.sleep(2)
            while await ch1.wait_message():
                msg = await ch1.get_json()
                await websocket.send(json.dumps(msg))

    return app
