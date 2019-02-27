from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_searchable import make_searchable
import datetime

db = SQLAlchemy()
make_searchable(db.metadata)


class Translation(db.Model):
    """Translation table for ACARSD"""

    __tablename__ = "translation"

    id = db.Column(db.Integer, primary_key=True)
    reg = db.Column(db.String(20))
    reg_correct = db.Column(db.String(20))
    operator = db.Column(db.String(20))
    operator_correct = db.Column(db.String(20))
    source = db.Column(db.String(255))
    date_added = db.Column(db.DateTime(timezone=False), default=datetime.datetime.utcnow)
    date_modified = db.Column(
        db.DateTime(timezone=False), default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow
    )


class Aircrafts(db.Model):
    __tablename__ = "aircraft"

    id = db.Column(db.Integer, primary_key=True)
    icao = db.Column(db.String(10), nullable=False, unique=True)
    type = db.Column(db.String(255), nullable=False)
    manufacturer = db.Column(db.String(255), nullable=False)
    official_page = db.Column(db.String(255), nullable=False)
    aircraft_shadow = db.Column(db.String(255), default=None)
    aircraft_description = db.Column(db.String(255), default=None)
    engine_type = db.Column(db.String(255), default=None)
    engine_count = db.Column(db.Integer, default=None)
    wake_category = db.Column(db.String(10), default=None)
    mfr = db.Column(db.String(255), default=None)


class AircraftModes(db.Model):
    __tablename__ = "aircraft_modes"

    id = db.Column(db.Integer, primary_key=True)
    first_created = db.Column(db.DateTime(timezone=False), default=datetime.datetime.utcnow)
    last_modified = db.Column(db.DateTime(timezone=False))
    mode_s = db.Column(db.String(6), nullable=False)
    mode_s_country = db.Column(db.String(40))  # originally 24 chars
    registration = db.Column(db.String(20))
    icao_type_code = db.Column(db.String(4))
    type_flight = db.Column(db.String(50))
    source = db.Column(db.String(255))
    source_type = db.Column(db.String(255), default="modes")


class AircraftOwner(db.Model):
    __tablename__ = "aircraft_owner"

    id = db.Column(db.Integer, primary_key=True)
    registration = db.Column(db.String(255), nullable=False)
    base = db.Column(db.String(255), default=None)
    owner = db.Column(db.String(255))
    date_first_reg = db.Column(db.DateTime(timezone=False), default=None)
    source = db.Column(db.String(255), nullable=False)
    is_private = db.Column(db.Boolean, default=False)


class AircraftRegistration(db.Model):
    __tablename__ = "aircraft_registration"

    id = db.Column(db.Integer, primary_key=True)
    country = db.Column(db.String(255), nullable=False)
    prefix = db.Column(db.String(10), nullable=False)


class ArchiveAdsbMessage(db.Model):
    __tablename__ = "archive_adsb_message"

    id = db.Column(db.Integer, primary_key=True)

    # Common part of ADS-B message
    message_type = db.Column(db.String("5"), nullable=False)
    transmission_type = db.Column(db.Integer, nullable=False)
    session_id = db.Column(db.String(20))
    aircraft_id = db.Column(db.String(20))
    hex_ident = db.Column(db.String(20))  # ModeS ident
    flight_id = db.Column(db.String(20))
    date_msg_gen = db.Column(db.String(20))
    time_msg_gen = db.Column(db.String(20))
    msg_gen = db.Column(db.DateTime(timezone=False))
    date_msg_log = db.Column(db.String(20))
    time_msg_log = db.Column(db.String(20))
    msg_log = db.Column(db.DateTime(timezone=False))

    # Other part
    callsign = db.Column(db.String(20))
    altitude = db.Column(db.Integer)
    ground_speed = db.Column(db.Integer)
    track = db.Column(db.String(20))
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    vertical_rate = db.Column(db.Integer)
    squawk = db.Column(db.Integer)
    alert = db.Column(db.String(20))
    emergency = db.Column(db.String(20))
    spi_ident = db.Column(db.String(20))
    is_on_ground = db.Column(db.Boolean, default=False)

    # More things not included in a RAW ADS-B SBS BaseStation message
    src = db.Column(db.String(255))
    client_name = db.Column(db.String(255))
    data_origin = db.Column(db.String(255))
    entry_point = db.Column(db.String(255))

    def raw(self):
        return ",".join(
            [
                self.message_type,
                self.transmission_type,
                self.session_id,
                self.aircraft_id,
                self.hex_ident,
                self.flight_id,
                self.date_msg_gen,
                self.time_msg_gen,
                self.date_msg_log,
                self.time_msg_log,
                self.callsign,
                self.altitude,
                self.ground_speed,
                self.track,
                self.latitude,
                self.longitude,
                self.vertical_rate,
                self.squawk,
                self.alert,
                self.emergency,
                self.spi_ident,
                self.is_on_ground,
            ]
        )

    def vert_stat(self):
        return "air" if self.is_on_ground else "gnd"
