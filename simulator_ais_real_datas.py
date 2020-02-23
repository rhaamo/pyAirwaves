#!/usr/bin/env python

from real_datas_test import REAL_DATA_AIS
from libPyAirwaves.structs import AisType
import time
import config as cfg
import redis
import json


DELAY_MESSAGES = 0.5  # second

redis = redis.from_url(cfg.REDIS_URL)
pubsub = redis.pubsub()
pubsub.subscribe("room:vehicles")

print("Sending messages...")

try:
    for msg in REAL_DATA_AIS[0:20]:
        print(msg)
        ais_msg = AisType()
        if not ais_msg.populate_from_string(msg):
            print("invalid message")
            continue
        ais_msg.entryPoint = "simulator"
        ais_msg.ourName = cfg.PYAW_HOSTNAME
        ais_msg.srcName = cfg.AIS_SOURCE["name"]
        ais_msg.srcLat = cfg.AIS_SOURCE["lat"]
        ais_msg.srcLon = cfg.AIS_SOURCE["lon"]
        ais_msg.srcPosMode = cfg.AIS_SOURCE["posMode"]
        ais_msg.dataOrigin = "rtl-ais"

        redis.publish("room:vehicles", json.dumps(ais_msg.to_dict()))
        time.sleep(DELAY_MESSAGES)

except KeyboardInterrupt:
    print("Stopping.")
