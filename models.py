import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from config import SQLALCHEMY_DATABASE_URI, SQLALCHEMY_RECORD_QUERIES

Base = declarative_base()
engine = create_engine(SQLALCHEMY_DATABASE_URI, echo=SQLALCHEMY_RECORD_QUERIES)
Session = sessionmaker(bind=engine)


class Translation(Base):
    """Translation table for ACARSD"""

    __tablename__ = "translation"

    id = Column(Integer, primary_key=True)
    reg = Column(String(20))
    reg_correct = Column(String(20))
    operator = Column(String(20))
    operator_correct = Column(String(20))
    source = Column(String(255))
    date_added = Column(DateTime(timezone=False), default=datetime.datetime.utcnow)
    date_modified = Column(
        DateTime(timezone=False), default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow
    )


class Aircrafts(Base):
    __tablename__ = "aircraft"

    id = Column(Integer, primary_key=True)
    icao = Column(String(10), nullable=False, unique=True)
    type = Column(String(255), nullable=False)
    manufacturer = Column(String(255), nullable=False)
    official_page = Column(String(255), nullable=False)
    aircraft_shadow = Column(String(255), default=None)
    aircraft_description = Column(String(255), default=None)
    engine_type = Column(String(255), default=None)
    engine_count = Column(Integer, default=None)
    wake_category = Column(String(10), default=None)
    mfr = Column(String(255), default=None)


class AircraftModes(Base):
    __tablename__ = "aircraft_mode"

    id = Column(Integer, primary_key=True)
    first_created = Column(DateTime(timezone=False), default=datetime.datetime.utcnow)
    last_modified = Column(DateTime(timezone=False))
    mode_s = Column(String(6), nullable=False, index=True)
    mode_s_country = Column(String(40), index=True)  # originally 24 chars
    registration = Column(String(20), index=True)
    icao_type_code = Column(String(4), index=True)
    type_flight = Column(String(50))
    source = Column(String(255))
    source_type = Column(String(255), default="modes")


class AircraftOwner(Base):
    __tablename__ = "aircraft_owner"

    id = Column(Integer, primary_key=True)
    registration = Column(String(255), nullable=False, index=True)
    base = Column(String(255), default=None)
    owner = Column(String(255))
    date_first_reg = Column(DateTime(timezone=False), default=None)
    source = Column(String(255), nullable=False)
    is_private = Column(Boolean, default=False)


class AircraftRegistration(Base):
    __tablename__ = "aircraft_registration"

    id = Column(Integer, primary_key=True)
    country = Column(String(255), nullable=False, index=True)
    prefix = Column(String(10), nullable=False)
