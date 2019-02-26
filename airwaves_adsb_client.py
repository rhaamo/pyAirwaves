#!/usr/bin/env python
"""
blah
"""

import traceback
import config
import socket
import time
import datetime
from flask_socketio import SocketIO
import config as cfg
from libPyAirwaves.adsb import is_valid_adsb_message
from libPyAirwaves.structs import AdsbType
from models import db, Aircrafts, AircraftModes, AircraftOwner, AircraftRegistration
from app import create_app

count_failed_connection = 0
max_failed_connection = 10

app = create_app()
app.app_context().push()

if __name__ == "__main__":
    socketio = SocketIO(message_queue=cfg.SOCKETIO_MESSAGE_QUEUE)

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
                        sock.connect(("fenouil", 30003))
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
                        adsb_message.populate_from_list(line)
                        # Emit Socket.IO message only if altitude, latitude and longitude are set
                        # AKA a "MSG,3" message and perhaps a "MSG,2" (Surface position)
                        if adsb_message.has_location():
                            adsb_message.entryPoint = "airwaves_adsb_client"
                            adsb_message.src = config.PYAW_HOSTNAME
                            adsb_message.clientName = config.ADSB_SOURCE["name"]
                            adsb_message.dataOrigin = "dump1090"

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
                                .filter(AircraftModes.mode_s == adsb_message.addr)
                                .join(Aircrafts, Aircrafts.icao == AircraftModes.icao_type_code)
                                .join(AircraftOwner, AircraftOwner.registration == AircraftModes.registration)
                                .join(AircraftRegistration, AircraftRegistration.country == AircraftModes.mode_s_country)
                                .first()
                            )

                            adsb_message.icaoAACC = sqlcraft.prefix
                            adsb_message.category = sqlcraft.aircraft_description

                            print(adsb_message.to_dict())
                            socketio.emit("message", adsb_message.to_dict())
                    # It's valid, reset stream message
                    data_str = ""
                else:
                    # stream message still too short
                    data_str = d
                    continue

    except KeyboardInterrupt:
        print("Closing socket connection")
        sock.close()
