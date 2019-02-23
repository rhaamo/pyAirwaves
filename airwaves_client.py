#!/usr/bin/env python
"""
blah
"""

import logging
import traceback
import re
import socket
import time
import datetime
from flask_socketio import SocketIO

sources = [
    {'name': 'ADSB', 'host': 'patate', 'port': 30003, 'type': 'adsb'},
    {'name': 'AIS', 'host': 'patate', 'port': 0, 'type': 'dummy'}
]

count_failed_connection = 0
max_failed_connection = 10

if __name__ == "__main__":
    socketio = SocketIO(message_queue='redis://127.0.0.1:6379/3')

    while count_failed_connection < max_failed_connection:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect(("patate", 30003))
            count_failed_connection = 1
            print("Connected to dump1090")
            break
        except socket.error:
            count_failed_connection += 1
            print(f"Cannot connect to dump1090 main {count_failed_connection}/{max_failed_connection}: {traceback.format_exc()}")
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
                message = sock.recv(128)
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
                        print(f"Cannot connect to dump1090 while {count_failed_connection}/{max_failed_connection}: {traceback.format_exc()}")
                        time.sleep(5)
                else:
                    quit()

                continue

            data = data_str.split("\n")

            # http://woodair.net/sbs/article/barebones42_socket_data.htm

            for d in data:
                line = d.split(",")

                if len(line) == 22:
                    print(f"VALID DATA: {len(line)}: {d}")
                    socketio.emit('adsb-new', {'message': d})
                    data_str = ""
                else:
                    #print(f"INVALID DATA: {len(line)}: {d}")
                    data_str = d
                    continue

    except KeyboardInterrupt:
        print("Closing socket connection")
        sock.close()
