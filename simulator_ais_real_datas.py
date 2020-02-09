#!/usr/bin/env python

from real_datas_test import REAL_DATA_AIS
from libPyAirwaves.structs import AisType
import time
from flask_socketio import SocketIO
import config as cfg
from app import create_app


DELAY_MESSAGES = 0.5  # second

app = create_app()
app.app_context().push()
socketio = SocketIO(message_queue=cfg.SOCKETIO_MESSAGE_QUEUE)

print("Sending messages...")

try:
    for msg in REAL_DATA_AIS[0:20]:
        print(msg)
        ais_msg = AisType()
        if not ais_msg.populate_from_string(msg):
            print("invalid message")
            continue
        ais_msg.entryPoint = "simulator"
        ais_msg.src = cfg.PYAW_HOSTNAME
        ais_msg.clientName = "sim_host"
        ais_msg.dataOrigin = "rtl-ais"

        socketio.emit("message", ais_msg.to_dict())
        time.sleep(DELAY_MESSAGES)

except KeyboardInterrupt:
    print("Stopping.")
