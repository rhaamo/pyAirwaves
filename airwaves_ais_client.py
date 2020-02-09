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
from libPyAirwaves.structs import AisType
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
            sock.connect((config.AIS_SOURCE["host"], config.AIS_SOURCE["port"]))
            count_failed_connection = 1
            print("Connected to rtl-ais")
            break
        except socket.error:
            count_failed_connection += 1
            print(
                f"Cannot connect to rtl-ais main {count_failed_connection}/{max_failed_connection}: {traceback.format_exc()}"
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
                        sock.connect((config.AIS_SOURCE["host"], config.AIS_SOURCE["port"]))
                        count_failed_connection = 1
                        print("Connected to rtl-ais")
                        break
                    except socket.error:
                        count_failed_connection += 1
                        print(
                            f"Cannot connect to rtl-ais while {count_failed_connection}/{max_failed_connection}: {traceback.format_exc()}"
                        )
                        time.sleep(5)
                else:
                    quit()

                continue

            # split if multiple messages have been received
            data = data_str.split("\n")

            for line in data:
                line = line.strip()
                if line.startswith("!"):
                    ais_message = AisType()
                    if ais_message.populate_from_string(line):
                        ais_message.entryPoint = "airwaves_ais_client"
                        ais_message.src = config.PYAW_HOSTNAME
                        ais_message.clientName = config.AIS_SOURCE["name"]
                        ais_message.dataOrigin = "rtl-ais"

                        # Valid message
                        print(ais_message.to_dict())
                        socketio.emit("message", ais_message.to_dict())
                    # It's valid, reset stream message
                    data_str = ""

    except KeyboardInterrupt:
        print("Closing socket connection")
        sock.close()
