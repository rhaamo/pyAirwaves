#!/usr/bin/env python

from real_datas_test import REAL_DATA_AIS
from libPyAirwaves.ais import restructure_ais
import time
import config
import redis
import json
import pyais


DELAY_MESSAGES = 0.5  # second

redis = redis.from_url(config.REDIS_URL)
pubsub = redis.pubsub()
pubsub.subscribe("room:vehicles")

print("Sending messages...")

try:
    for msg in REAL_DATA_AIS[0:20]:
        nmea = pyais.NMEAMessage.from_string(msg)
        ais_message = restructure_ais(nmea)
        ais_message["source_metadatas"] = {
            "entry_point": "simulator",
            "our_name": config.PYAW_HOSTNAME,
            "src_name": "simulator_ais_real_datas",
            "src_lat": 0,
            "src_lon": 0,
            "src_pos_mode": 0,
            "data_origin": "real_datas",
        }
        redis.publish("room:vehicles", json.dumps(ais_message))
        time.sleep(DELAY_MESSAGES)

except KeyboardInterrupt:
    print("Stopping.")
