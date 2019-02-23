import datetime
import hashlib
import os
import subprocess
from os.path import splitext
import csv
import zipfile
import pycurl

from flask import current_app
from flask_security import current_user

from models import db, FaaMfr


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


def ingest_faa_aircrafts(file: str):
    # clean previous entries
    # rmed = FaaMfr.query.delete()
    # print(f"Removed {rmed} entries")

    data_row = False
    rows = {}

    with open(file, "rt") as csvFile:
        for row in csv.reader(csvFile):
            # blank the row
            this_row = {}

            if data_row:
                # Type-correct our CSV data.
                try:
                    this_row.update({"mfgName": row[1].strip()})
                except:
                    None

                try:
                    this_row.update({"modelName": row[2].strip()})
                except:
                    None

                try:
                    this_row.update({"acType": int(row[3].strip())})
                except:
                    None

                try:
                    this_row.update({"engType": int(row[4].strip())})
                except:
                    None

                try:
                    this_row.update({"acCat": int(row[5].strip())})
                except:
                    None

                try:
                    this_row.update({"buldCert": int(row[6].strip())})
                except:
                    None

                try:
                    this_row.update({"engCt": int(row[7].strip())})
                except:
                    None

                try:
                    this_row.update({"seatCt": int(row[8].strip())})
                except:
                    None

                try:
                    this_row.update({"weight": int(row[9].replace("CLASS ", "").strip())})
                except:
                    None

                try:
                    this_row.update({"cruiseSpd": int(row[10].strip())})
                except:
                    None

                print(this_row)
                rows.update({row[0].strip(): this_row})

            else:
                dataRow = True

            # Then eat the datas
            # print(rows)


def utils_download_and_ingest_faa():
    print("Downloading and ingesting FAA infos")

    file_target = os.path.join(current_app.config["FAA_DL_TEMP_PATH"], "faa.zip")

    print("Downloading file...")

    try:
        try:
            os.makedirs(current_app.config["FAA_DL_TEMP_PATH"])
        except OSError:
            None
        except:
            raise

        with open(file_target, "wb") as zip_file:
            crl = pycurl.Curl()
            crl.setopt(crl.URL, current_app.config["FAA_ARCHIVE_URL"])
            crl.setopt(crl.WRITEDATA, zip_file)
            crl.perform()
            crl.close()
    except:
        raise

    print("Extracting files...")

    try:
        # Open and extract MASTER, AIRCRAFT and ENGINE
        zip = zipfile.ZipFile(file_target, "r")
        zip.extractall(current_app.config["FAA_DL_TEMP_PATH"], ["MASTER.txt", "ACFTREF.txt", "ENGINE.txt"])
    except:
        raise
    finally:
        zip.close()

    aircrafts_file = os.path.join(current_app.config["FAA_DL_TEMP_PATH"], "ACFTREF.txt")
    engines_file = os.path.join(current_app.config["FAA_DL_TEMP_PATH"], "ENGINE.txt")
    master_file = os.path.join(current_app.config["FAA_DL_TEMP_PATH"], "MASTER.txt")

    ingest_faa_aircrafts(aircrafts_file)
