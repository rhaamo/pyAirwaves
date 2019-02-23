import datetime
import hashlib
import os
import subprocess
from os.path import splitext

from flask import current_app
from flask_security import current_user


class InvalidUsage(Exception):
    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv["message"] = self.message
        rv["status"] = "error"
        rv["code"] = self.status_code
        return rv


def duration_elapsed_human(seconds):
    print(seconds)
    seconds = round(seconds)
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    years, days = divmod(days, 365.242199)

    minutes = int(minutes)
    hours = int(hours)
    days = int(days)
    years = int(years)

    if years > 0:
        return "%d y" % years
    elif days > 0:
        return "%d d" % days
    elif hours > 0:
        return "%d h" % hours + "s" * (hours != 1)
    elif minutes > 0:
        return "%d mn" % minutes + "s" * (minutes != 1)
    else:
        return "right now"


def duration_song_human(seconds):
    if seconds is None:
        return "error"
    seconds = float(seconds)
    seconds = seconds
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    years, days = divmod(days, 365.242199)

    minutes = int(minutes)
    hours = int(hours)
    days = int(days)
    years = int(years)

    if years > 0:
        return "%d year" % years + "s" * (years != 1)
    elif days > 0:
        return "%d day" % days + "s" * (days != 1)
    elif hours > 0:
        return "%d hour" % hours + "s" * (hours != 1)
    elif minutes > 0:
        return "%d mn" % minutes + "s" * (minutes != 1)
    else:
        return "%.2f sec" % seconds + "s" * (seconds != 1)


def get_hashed_filename(filename):
    f_n, f_e = splitext(filename)

    fs_fname = hashlib.sha256()
    hashed_format = "%s-%s" % (f_n, datetime.datetime.now())
    fs_fname.update(hashed_format.encode("utf-8"))
    fs_fname = fs_fname.hexdigest()

    return fs_fname + f_e
