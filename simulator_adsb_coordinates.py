#!/usr/bin/env python


from real_datas_test import fake_planes
from libPyAirwaves.structs import AdsbType
import time
from flask_socketio import SocketIO
import config as cfg
from app import create_app

DELAY_MESSAGES = 2  # second

app = create_app()
app.app_context().push()
socketio = SocketIO(message_queue=cfg.SOCKETIO_MESSAGE_QUEUE)

print("Sending messages...")

try:
    sample = "MSG,3,1,1,field_4,1,2019/02/25,20:49:58.331,2019/02/25,20:49:58.361,,field_11,,,field_14,field_15,,field_17,0,,0,0"
    foo = sample.split(",")

    # "addr": "000000", "idInfo": "LOLK293", "alt": 23000, "aSquawk": "1337"
    for coords in fake_planes["planeA"]["path"]:
        msg = foo
        msg[4] = fake_planes["planeA"]["idInfo"]
        msg[11] = str(fake_planes["planeA"]["alt"])
        msg[14] = str(coords[1])
        msg[15] = str(coords[0])
        msg[17] = fake_planes["planeA"]["aSquawk"]
        adsb_msg = AdsbType()
        adsb_msg.populate_from_list(msg)
        adsb_msg.entryPoint = "simulator"
        adsb_msg.src = cfg.PYAW_HOSTNAME
        adsb_msg.clientName = "sim_host"
        adsb_msg.dataOrigin = "dump1090"
        print(f"sent planeA {adsb_msg.to_dict()}")
        socketio.emit("message", adsb_msg.to_dict())
        time.sleep(DELAY_MESSAGES)

    # "addr": "ffffff", "idInfo": "WEE2162", "alt": 45000, "aSquawk": "7007"
    for coords in fake_planes["planeB"]["path"]:
        msg = foo
        msg[4] = fake_planes["planeB"]["idInfo"]
        msg[11] = str(fake_planes["planeB"]["alt"])
        msg[14] = str(coords[1])
        msg[15] = str(coords[0])
        msg[17] = fake_planes["planeB"]["aSquawk"]
        adsb_msg = AdsbType()
        adsb_msg.populate_from_list(msg)
        adsb_msg.entryPoint = "simulator"
        adsb_msg.src = cfg.PYAW_HOSTNAME
        adsb_msg.clientName = "sim_host"
        adsb_msg.dataOrigin = "dump1090"
        print(f"sent planeB {adsb_msg.to_dict()}")
        socketio.emit("message", adsb_msg.to_dict())
        time.sleep(DELAY_MESSAGES)

    # "addr": "111111", "idInfo": "NOPE", "alt": 40000, "aSquawk": "0666"
    for coords in fake_planes["planeC"]["path"]:
        msg = foo
        msg[4] = fake_planes["planeC"]["idInfo"]
        msg[11] = str(fake_planes["planeC"]["alt"])
        msg[14] = str(coords[1])
        msg[15] = str(coords[0])
        msg[17] = fake_planes["planeC"]["aSquawk"]
        adsb_msg = AdsbType()
        adsb_msg.populate_from_list(msg)
        adsb_msg.entryPoint = "simulator"
        adsb_msg.src = cfg.PYAW_HOSTNAME
        adsb_msg.clientName = "sim_host"
        adsb_msg.dataOrigin = "dump1090"
        print(f"sent planeC {adsb_msg.to_dict()}")
        socketio.emit("message", adsb_msg.to_dict())
        time.sleep(DELAY_MESSAGES)


except KeyboardInterrupt:
    print("Stopping.")
