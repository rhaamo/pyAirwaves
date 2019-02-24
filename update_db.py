from models import db, Translation, AircraftModes, AircraftOwner
from utils import download_and_extract_zip, download_and_gunzip
from sqlalchemy import or_, create_engine, and_
from flask import current_app
import os
import csv

URLS = {
    "translation": {"url": "http://www.acarsd.org/download/translation.php", "md5": None, "filename": "translation.zip"},
    "ModeS": {"url": "http://data.flightairmap.com/data/BaseStation.sqb.gz", "md5": None, "filename": "BaseStation.sqb.gz"}
}


def update_translation():
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
    # $query = "DELETE FROM aircraft_modes WHERE Source = :source AND ModeS IN (SELECT * FROM (SELECT ModeS FROM aircraft_modes WHERE Source = 'ACARS') _alias)";
    q = db.session.query(AircraftModes.mode_s).filter(AircraftModes.source == 'ACARS')
    db.session.query(AircraftModes).filter(and_(
        AircraftModes.source == fname,
        AircraftModes.mode_s.in_(q)
    )).delete(synchronize_session='fetch')

    print("Done.")


def update_all():
    # update_translation()  #  to be removed, or kept but we need more datas tables for it
    update_mode_s()
