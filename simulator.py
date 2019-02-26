#!/usr/bin/env python

from real_datas_test import REAL_DATA_ADSB
from libPyAirwaves.structs import AdsbType
import time
from flask_socketio import SocketIO
import config as cfg
from app import create_app
from models import db, Aircrafts, AircraftModes, AircraftOwner, AircraftRegistration


DELAY_MESSAGES = 0.5  # second

app = create_app()
app.app_context().push()
socketio = SocketIO(message_queue=cfg.SOCKETIO_MESSAGE_QUEUE)

print("Sending messages...")

for msg in REAL_DATA_ADSB:
    adsb_msg = AdsbType()
    adsb_msg.populate_from_string(msg)
    adsb_msg.entryPoint = "simulator"
    adsb_msg.src = cfg.PYAW_HOSTNAME
    adsb_msg.clientName = "sim_host"
    adsb_msg.dataOrigin = "dump1090"

    # Get more datas from SQL
    sqlcraft = (
        db.session.query(
            AircraftModes.icao_type_code,
            Aircrafts.type,
            Aircrafts.manufacturer,
            Aircrafts.aircraft_description,
            Aircrafts.engine_type,
            Aircrafts.engine_count,
            AircraftOwner.registration,
            AircraftOwner.owner,
            AircraftRegistration.country,
            AircraftRegistration.prefix
        )
            .filter(AircraftModes.mode_s == adsb_msg.addr)
            .join(Aircrafts, Aircrafts.icao == AircraftModes.icao_type_code)
            .join(AircraftOwner, AircraftOwner.registration == AircraftModes.registration)
            .join(AircraftRegistration, AircraftRegistration.country == AircraftModes.mode_s_country)
            .first()
    )

    try:
        adsb_message.icaoAACC = sqlcraft.country
    except AttributeError:
        None

    try:
        adsb_message.category = sqlcraft.aircraft_description
    except AttributeError:
        None

    socketio.emit("message", adsb_msg.to_dict())
    time.sleep(DELAY_MESSAGES)
