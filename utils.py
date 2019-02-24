import datetime
import hashlib
import os
from os.path import splitext
import csv
import zipfile
import pycurl
import gzip

from flask import current_app


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
                this_row.update({"mfgName": row[1].strip()})
                this_row.update({"modelName": row[2].strip()})
                this_row.update({"acType": int(row[3].strip())})
                this_row.update({"engType": int(row[4].strip())})
                this_row.update({"acCat": int(row[5].strip())})
                this_row.update({"buldCert": int(row[6].strip())})
                this_row.update({"engCt": int(row[7].strip())})
                this_row.update({"seatCt": int(row[8].strip())})
                this_row.update({"weight": int(row[9].replace("CLASS ", "").strip())})
                this_row.update({"cruiseSpd": int(row[10].strip())})

                print(this_row)
                rows.update({row[0].strip(): this_row})

            else:
                data_row = True

            # Then eat the datas
            # print(rows)

def utils_download_and_ingest_faa():
    print("Downloading and ingesting FAA infos")

    file_target = os.path.join(current_app.config["FAA_DL_TEMP_PATH"], "faa.zip")

    print("Downloading file...")

    try:
        os.makedirs(current_app.config["FAA_DL_TEMP_PATH"])
    except OSError:
        None

    with open(file_target, "wb") as zip_file:
        crl = pycurl.Curl()
        crl.setopt(crl.URL, current_app.config["FAA_ARCHIVE_URL"])
        crl.setopt(crl.WRITEDATA, zip_file)
        crl.perform()
        crl.close()

    print("Extracting files...")

    try:
        # Open and extract MASTER, AIRCRAFT and ENGINE
        zip = zipfile.ZipFile(file_target, "r")
        zip.extractall(current_app.config["FAA_DL_TEMP_PATH"], ["MASTER.txt", "ACFTREF.txt", "ENGINE.txt"])
    finally:
        zip.close()

    aircrafts_file = os.path.join(current_app.config["FAA_DL_TEMP_PATH"], "ACFTREF.txt")
    # engines_file = os.path.join(current_app.config["FAA_DL_TEMP_PATH"], "ENGINE.txt")
    # master_file = os.path.join(current_app.config["FAA_DL_TEMP_PATH"], "MASTER.txt")

    ingest_faa_aircrafts(aircrafts_file)


def download_file(url: str, filename: str):
    print(f"Downloading {url}...")
    file_target = os.path.join(current_app.config['UPDATE_DB_TEMP_PATH'], filename)

    try:
        os.makedirs(current_app.config['UPDATE_DB_TEMP_PATH'])
    except OSError:
        None

    with open(file_target, "wb") as zip_file:
        crl = pycurl.Curl()
        crl.setopt(crl.URL, url)
        crl.setopt(crl.WRITEDATA, zip_file)
        crl.setopt(crl.FOLLOWLOCATION, True)
        crl.perform()
        crl.close()

    try:
        if os.path.getsize(file_target) > 0:
            print(f"Downloaded file to {file_target}")
            return True
        else:
            return False
    except OSError:
        return False


def gunzip(source_filepath, dest_filepath, block_size=65536):
    with gzip.open(source_filepath, 'rb') as s_file, open(dest_filepath, 'wb') as d_file:
        while True:
            block = s_file.read(block_size)
            if not block:
                break
            else:
                d_file.write(block)
        d_file.write(block)

    return True


def download_and_gunzip(url: str, f_source: str, f_target: str):
    # Download file
    downloaded = download_file(url, f_source)
    if not downloaded:
        return False

    print(f"gunzip-ing file {f_source}...")
    file_source = os.path.join(current_app.config['UPDATE_DB_TEMP_PATH'], f_source)
    file_target = os.path.join(current_app.config['UPDATE_DB_TEMP_PATH'], f_target)

    ret = gunzip(file_source, file_target)
    if not ret:
        return False

    if os.path.exists(file_source):
        os.remove(file_source)

    try:
        if os.path.getsize(file_target) > 0:
            print(f"File extracted to {file_target}")
            return True
        else:
            return False
    except OSError:
        return False


def download_and_extract_zip(url: str, archive_name: str, filename: str):
    # Download the file first
    downloaded = download_file(url, archive_name)
    if not downloaded:
        return False

    file_target = os.path.join(current_app.config['UPDATE_DB_TEMP_PATH'], filename)

    print(f"Extracting {filename}...")

    try:
        zip_file = zipfile.ZipFile(file_target, "r")
        zip_file.extract(filename, current_app.config['UPDATE_DB_TEMP_PATH'])
    except zipfile.BadZipFile as e:
        print(f"Error opening zip archive: {e}")
        return False
    except KeyError as e:
        print(f"Error extracting file: {e}")
        return False
    finally:
        zip_file.close()

    if os.path.exists(file_target):
        os.remove(file_target)

    filename_final = os.path.join(current_app.config['UPDATE_DB_TEMP_PATH'], filename)
    try:
        if os.path.getsize(filename_final) > 0:
            print(f"File extracted to {filename_final}")
            return True
        else:
            return False
    except OSError:
        return False
