from models import db, Translation, AircraftModes, AircraftOwner, Aircrafts
from utils import download_file, download_and_extract_zip, download_and_gunzip
from sqlalchemy import or_, create_engine, and_
from flask import current_app
import os
import csv
import datetime

URLS = {
    "translation": {"url": "http://www.acarsd.org/download/translation.php", "md5": None, "filename": "translation.zip"},
    "ModeS": {"url": "http://data.flightairmap.com/data/BaseStation.sqb.gz", "md5": None, "filename": "BaseStation.sqb.gz"},
    "ogn": {"url": "http://ddb.glidernet.org/download/", "md5": None, "filename": "ogn.csv"}
}


def update_aircrafts():
    print("Importing Aircrafts datas...")
    fname = "aircrafts.csv"  # don't change it !
    file_path = os.path.join(os.getcwd(), "datas", fname)
    if not os.path.isfile(file_path):
        print(f"Error: file at path {file_path} doesn't exist !")
        return False

    print("Cleaning old datas...")
    # Remove old datas
    db.session.query(Aircrafts).delete()

    # Eat the CSV file

    # File format:
    # icao, type, manufacturer, official_page, aircraft_shadow, aircraft_description, engine_type, engine_count, wake_category, mfr
    with open(file_path, "rt") as csv_file:
        for row in csv.reader(csv_file, delimiter=',', quotechar="'"):
            # Ignore comments in file
            if row[0].startswith('#'):
                continue
            ac = Aircrafts()
            ac.icao = row[0]
            ac.type = row[1]
            ac.manufacturer = row[2]
            ac.official_page = row[3]
            ac.aircraft_shadow = row[4]
            ac.aircraft_description = row[5]
            ac.engine_type = row[6]
            ac.engine_count = int(row[7]) if row[7] != '' else None
            ac.wake_category = row[8]
            ac.mfr = row[9]
            db.session.add(ac)
        db.session.commit()

    print("Done.")


def update_translation():
    print("Downloading ACARS translations...")
    dl_infos = URLS["translation"]
    downloaded = download_and_extract_zip(dl_infos["url"], dl_infos["filename"], "translation.csv")
    if not downloaded:
        print("An error occured while downloading ACARS translations")
        return False

    # Remove old datas
    db.session.query(Translation).filter(or_(Translation.source == '', Translation.source == 'translation.csv')).delete()
    db.session.commit()

    # Eat the CSV file
    csv_filename = os.path.join(current_app.config['UPDATE_DB_TEMP_PATH'], "translation.csv")

    with open(csv_filename, "rt") as csv_file:
        for row in csv.reader(csv_file, delimiter=';'):
            # Ignore comments in file
            if row[0].startswith('#'):
                continue


def update_mode_s():
    print("Downloading Aircraft Mode S datas...")
    dl_infos = URLS["ModeS"]
    fname = "BaseStation.sqb"  # don't change it !
    downloaded = download_and_gunzip(dl_infos['url'], dl_infos['filename'], fname)
    if not downloaded:
        print("An error occured while downloading ModeS datas")
        return False

    print("Cleaning old datas...")

    # Remove old datas
    db.session.query(AircraftModes).filter(or_(AircraftModes.source == fname,
                                               AircraftModes.source.is_(None),
                                               AircraftModes.source == '')).delete()
    db.session.query(AircraftOwner).filter(or_(AircraftOwner.source == fname,
                                               AircraftOwner.source.is_(None),
                                               AircraftOwner.source == '')).delete()
    db.session.commit()

    db_filename = os.path.join(current_app.config['UPDATE_DB_TEMP_PATH'], fname)

    print("Importing datas...")
    import_engine = create_engine(f'sqlite:///{db_filename}')
    with import_engine.connect() as con:
        rs = con.execute("select * from Aircraft")
        for row in rs:
            acm = AircraftModes()
            acm.last_modified = row['LastModified']
            acm.mode_s = row['ModeS']
            acm.mode_s_country = row['ModeSCountry']
            acm.registration = row['Registration']
            acm.icao_type_code = row['ICAOTypeCode']
            acm.source = fname
            acm.type_flight = 'military' if row['UserString4'] == 'M' else None
            db.session.add(acm)

            # Add Aircraft Owner only if not empty, and not Private individual
            if row['RegisteredOwners'] != '' and row['RegisteredOwners'] is not None and row['RegisteredOwners'] != 'Private':
                aco = AircraftOwner()
                aco.registration = row['Registration']
                aco.source = fname
                aco.owner = row['RegisteredOwners']
                aco.is_private = False  # may be useful one day
                db.session.add(aco)
    # Commit Aircraft Mode S and Owner datas
    db.session.commit()

    print("Cleaning again...")
    # Remove data already in db from ACARS
    q = db.session.query(AircraftModes.mode_s).filter(AircraftModes.source == 'ACARS')
    db.session.query(AircraftModes).filter(and_(
        AircraftModes.source == fname,
        AircraftModes.mode_s.in_(q)
    )).delete(synchronize_session='fetch')

    print("Done.")


def update_mode_s_ogn():
    print("Downloading Aircraft Mode S OGN datas...")
    dl_infos = URLS["ogn"]
    fname = "ogn.csv"  # don't change it !
    downloaded = download_file(dl_infos["url"], fname)
    if not downloaded:
        print("An error occured while downloading ModeS OGN datas")
        return False

    print("Cleaning old datas...")
    # Remove old datas
    db.session.query(AircraftModes).filter(or_(AircraftModes.source == fname,
                                               AircraftModes.source.is_(None),
                                               AircraftModes.source == '')).delete()

    # Eat the CSV file
    csv_filename = os.path.join(current_app.config['UPDATE_DB_TEMP_PATH'], fname)

    # File format:
    # DEVICE_TYPE,DEVICE_ID,AIRCRAFT_MODEL,REGISTRATION,CN,TRACKED,IDENTIFIED
    with open(csv_filename, "rt") as csv_file:
        for row in csv.reader(csv_file, delimiter=',', quotechar="'"):
            # Ignore comments in file
            if row[0].startswith('#'):
                continue
            acm = AircraftModes()
            acm.mode_s = row[1]
            acm.registration = row[3]
            aircraft_name = row[2]

            # Check if we can find ICAO, else set it to GLID
            aircraft_name_split = aircraft_name.split(" ")

            q = Aircrafts.query.filter(Aircrafts.type.like(aircraft_name))

            if len(aircraft_name_split) > 1 and len(aircraft_name_split[1]) > 3:
                q = Aircrafts.query.filter(and_(Aircrafts.type.like(aircraft_name),
                                                Aircrafts.type.like(aircraft_name_split[0])))

            aircraft = q.first()
            if aircraft:
                acm.icao_type_code = aircraft.icao

            if acm.registration != '' and acm.registration != '0000' and acm.icao_type_code != '':
                acm.last_modified = datetime.datetime.utcnow()
                db.session.add(acm)

    db.session.commit()

    print("Cleaning again...")
    # Remove data already in db from ACARS
    q = db.session.query(AircraftModes.mode_s).filter(AircraftModes.source == 'ACARS')
    db.session.query(AircraftModes).filter(and_(
        AircraftModes.source == fname,
        AircraftModes.mode_s.in_(q)
    )).delete(synchronize_session='fetch')


def update_all():
    # update_translation()  #  to be removed, or kept but we need more datas tables for it
    update_mode_s()
    update_mode_s_ogn()
