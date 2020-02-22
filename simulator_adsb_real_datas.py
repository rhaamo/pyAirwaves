#!/usr/bin/env python

from real_datas_test import REAL_DATA_ADSB
from libPyAirwaves.structs import AdsbType
import time
import config as cfg
from models import db, Aircrafts, AircraftModes, AircraftOwner, AircraftRegistration
import redis
import json

DELAY_MESSAGES = 0.5  # second

redis = redis.from_url(cfg.REDIS_URL)
pubsub = redis.pubsub()
pubsub.subscribe("room:vehicles")

print("Sending messages...")

try:
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
                AircraftRegistration.prefix,
            )
            .filter(AircraftModes.mode_s == adsb_msg.addr)
            .join(Aircrafts, Aircrafts.icao == AircraftModes.icao_type_code)
            .join(AircraftOwner, AircraftOwner.registration == AircraftModes.registration)
            .join(AircraftRegistration, AircraftRegistration.country == AircraftModes.mode_s_country)
            .first()
        )

        try:
            adsb_msg.icaoAACC = sqlcraft.country
        except AttributeError:
            None

        try:
            adsb_msg.category = sqlcraft.aircraft_description
        except AttributeError:
            None

        redis.publish("room:vehicles", json.dumps(adsb_msg.to_dict()))
        time.sleep(DELAY_MESSAGES)

except KeyboardInterrupt:
    print("Stopping.")
