#!/usr/bin/env python
"""
blah
"""

import traceback
import config
import socket
import time
import datetime
from libPyAirwaves.adsb import is_valid_adsb_message
from libPyAirwaves.structs import AdsbType
from models import Session, Aircrafts, AircraftModes, AircraftOwner, AircraftRegistration
import redis
import json

count_failed_connection = 0
max_failed_connection = 10

redis = redis.from_url(config.REDIS_URL)
pubsub = redis.pubsub()
pubsub.subscribe("room:vehicles")
session = Session()

if __name__ == "__main__":
    while count_failed_connection < max_failed_connection:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((config.ADSB_SOURCE["host"], config.ADSB_SOURCE["port"]))
            count_failed_connection = 1
            print("Connected to dump1090")
            break
        except socket.error:
            count_failed_connection += 1
            print(
                f"Cannot connect to dump1090 main {count_failed_connection}/{max_failed_connection}: {traceback.format_exc()}"
            )
            time.sleep(5)
    else:
        quit()

    data_str = ""
    start_time = datetime.datetime.utcnow()
    last_time = start_time

    try:
        while True:
            cur_time = datetime.datetime.utcnow()
            ds = cur_time.isoformat()
            ts = cur_time.strftime("%H:%M:%S")

            try:
                message = sock.recv(512)
                data_str += message.decode().strip("\n")
            except socket.error:
                pass

            if len(message) == 0:
                print(ts, "No broadcast received. Attempting to reconnect")
                time.sleep(5)
                sock.close()

                while count_failed_connection < max_failed_connection:
                    try:
                        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        sock.connect((config.ADSB_SOURCE["host"], config.ADSB_SOURCE["port"]))
                        count_failed_connection = 1
                        print("Connected to dump1090")
                        break
                    except socket.error:
                        count_failed_connection += 1
                        print(
                            f"Cannot connect to dump1090 while {count_failed_connection}/{max_failed_connection}: {traceback.format_exc()}"
                        )
                        time.sleep(5)
                else:
                    quit()

                continue

            # split if multiple messages have been received
            data = data_str.split("\n")

            for d in data:
                d = d.strip()
                line = d.split(",")
                # we need 22 items to be a valid looking message
                if len(line) == 22:
                    if is_valid_adsb_message(line):
                        adsb_message = AdsbType()
                        adsb_message.populate_from_sbs(line)
                        # print(adsb_message.to_dict())
                        # Emit Socket.IO message only if altitude, latitude and longitude are set
                        # AKA a "MSG,3" message and perhaps a "MSG,2" (Surface position)
                        if adsb_message.has_location():
                            adsb_message.entryPoint = "airwaves_adsb_client"
                            adsb_message.ourName = config.PYAW_HOSTNAME
                            adsb_message.srcName = config.ADSB_SOURCE["name"]
                            adsb_message.srcLat = config.ADSB_SOURCE["lat"]
                            adsb_message.srcLon = config.ADSB_SOURCE["lon"]
                            adsb_message.srcPosMode = config.ADSB_SOURCE["posMode"]
                            adsb_message.dataOrigin = "dump1090"

                            # Get more datas from SQL
                            sqlcraft = (
                                session.query(
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
                                .filter(AircraftModes.mode_s == adsb_message.hexIdent)
                                .join(Aircrafts, Aircrafts.icao == AircraftModes.icao_type_code)
                                .join(AircraftOwner, AircraftOwner.registration == AircraftModes.registration)
                                .first()
                            )

                            try:
                                # does not work for some reasons
                                adsb_message.icaoAACC = sqlcraft.mode_s_country
                            except AttributeError:
                                None

                            try:
                                adsb_message.category = sqlcraft.aircraft_description
                            except AttributeError:
                                None

                            print(adsb_message.to_dict())
                            redis.publish("room:vehicles", json.dumps(adsb_message.to_dict()))
                    # It's valid, reset stream message
                    data_str = ""
                else:
                    # stream message still too short
                    data_str = d
                    continue

    except KeyboardInterrupt:
        print("Closing socket connection")
        sock.close()
