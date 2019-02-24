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
    date_modified = db.Column(db.DateTime(timezone=False),
                              default=datetime.datetime.utcnow,
                              onupdate=datetime.datetime.utcnow)


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
    source_type = db.Column(db.String(255), default='modes')


class AircraftOwner(db.Model):
    __tablename__ = "aircraft_owner"

    id = db.Column(db.Integer, primary_key=True)
    registration = db.Column(db.String(255), nullable=False)
    base = db.Column(db.String(255), default=None)
    owner = db.Column(db.String(255))
    date_first_reg = db.Column(db.DateTime(timezone=False), default=None)
    source = db.Column(db.String(255), nullable=False)
    is_private = db.Column(db.Boolean, default=False)
