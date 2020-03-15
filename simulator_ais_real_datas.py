#!/usr/bin/env python

from real_datas_test import REAL_DATA_AIS
from libPyAirwaves.ais import restructure_ais
import time
import config as cfg
import redis
import json
import pyais


DELAY_MESSAGES = 0.5  # second

redis = redis.from_url(cfg.REDIS_URL)
pubsub = redis.pubsub()
pubsub.subscribe("room:vehicles")

print("Sending messages...")

try:
    for msg in REAL_DATA_AIS[0:20]:
        nmea = pyais.NMEAMessage.from_string(msg)
        ais_message = restructure_ais(nmea)
        ais_message["entryPoint"] = "simulator"
        ais_message["ourName"] = cfg.PYAW_HOSTNAME
        ais_message["srcName"] = "simulator_ais_real_datas"
        ais_message["srcLat"] = 0
        ais_message["srcLon"] = 0
        ais_message["srcPosMode"] = 0
        ais_message["dataOrigin"] = "real_datas"

        redis.publish("room:vehicles", json.dumps(ais_message))
        time.sleep(DELAY_MESSAGES)

except KeyboardInterrupt:
    print("Stopping.")
