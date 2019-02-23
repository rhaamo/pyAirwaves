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
import config as cfg
from structs import AdsbType

count_failed_connection = 0
max_failed_connection = 10


# Do some basic checks on the ADS-B received message
# http://woodair.net/sbs/article/barebones42_socket_data.htm
def is_valid_adsb_message(fields):
    is_valid = False

    if len(fields) == 22:
        is_valid = True

    if fields[0].upper() in ['MSG', 'STA', 'ID', 'AIR', 'SEL', 'CLK']:
        is_valid = True
    else:
        logging.error(f"Field 1 invalid : '{fields[0]}'")
        logging.error(f"Invalid ADSB Message: '{fields}'")

    if int(fields[1]) in [1, 2, 3, 4, 5, 6, 7, 8]:
        is_valid = True
    else:
        logging.error(f"Field 2 invalid: '{fields[1]}'")
        logging.error(f"Invalid ADSB Message: '{fields}'")

    if not is_valid:
        logging.error(f"Invalid ADSB Message: '{fields}'")

    return is_valid


def get_adsb_message(fields):
    # Remember that fields start at 1 but python array at 0, so field 3 (session ID) is at position 2
    msg = AdsbType()
    msg.addr = fields[4]  # int(fields[4], 16)
    msg.idInfo = fields[3]
    msg.aSquawk = fields[17]
    msg.alt = int(fields[11]) if fields[11] else None
    msg.lon = float(fields[15]) if fields[15] else None
    msg.lat = float(fields[14]) if fields[14] else None
    msg.entryPoint = 'airwaves_client'
    msg.dts = str(datetime.datetime.utcnow())
    msg.src = 'patate'  # TODO from cfg
    msg.lastSrc = msg.src
    msg.data = ",".join(fields)
    msg.srcPos = False  # TODO add position support
    msg.vertState = fields[21]
    msg.vertRate = int(fields[16]) if fields[16] else None
    msg.category = None
    msg.icaoAACC = None
    msg.velo = None
    msg.heading = None
    msg.supersonic = None
    msg.clientName = "dump1090_adsb"  # todo from cfg
    msg.lastClientName = msg.clientName
    return msg


if __name__ == "__main__":
    socketio = SocketIO(message_queue=cfg.SOCKETIO_MESSAGE_QUEUE)

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
                        print(f"Cannot connect to dump1090 while {count_failed_connection}/{max_failed_connection}: {traceback.format_exc()}")
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
                        adsb_message = get_adsb_message(line)
                        # Emit Socket.IO message only if altitude, latitude and longitude are set
                        # AKA a "MSG,3" message and perhaps a "MSG,2" (Surface position)
                        if adsb_message.has_location():
                            print(adsb_message.to_dict())
                            socketio.emit('message', adsb_message.to_dict())
                    # It's valid, reset stream message
                    data_str = ""
                else:
                    # stream message still too short
                    data_str = d
                    continue

    except KeyboardInterrupt:
        print("Closing socket connection")
        sock.close()
