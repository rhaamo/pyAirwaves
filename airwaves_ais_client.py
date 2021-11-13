#!/usr/bin/env python
"""
blah
"""

import config
from libPyAirwaves.structs import AisType
import pyais
import redis
import json
import time


count_failed_connection = 0
max_failed_connection = 10

redis = redis.from_url(config.REDIS_URL)
pubsub = redis.pubsub()
pubsub.subscribe("room:vehicles")


def broadcast(msg: pyais.messages.NMEAMessage):
    is_fragmented = msg.count > 1
    # if is_fragmented:
    #     print("Fragmented packet:", msg)
    # else:
    #     print("Single packet:", msg)

    ais_message = AisType()
    ais_message.entryPoint = "airwaves_ais_client"
    ais_message.ourName = config.PYAW_HOSTNAME
    ais_message.srcName = config.AIS_SOURCE["name"]
    ais_message.srcLat = config.AIS_SOURCE["lat"]
    ais_message.srcLon = config.AIS_SOURCE["lon"]
    ais_message.srcPosMode = config.AIS_SOURCE["posMode"]
    ais_message.dataOrigin = "rtl-ais"
    ais_message.raw = msg.raw.decode("utf-8")
    ais_message.payload = msg.data.decode("utf-8")

    ais_parsed = msg.decode()

    if is_fragmented:
        ais_message.isAssembled = True

    # Populate the structure from parsed VDM
    ais_message.populateFromParsedVdm(ais_parsed)

    # Valid message and emit if lat/lon are present
    # if ais_message.lat and ais_message.lon:
    # print(ais_message.to_dict())
    redis.publish("room:vehicles", json.dumps(ais_message.to_dict()))


if __name__ == "__main__":
    while True:
        try:
            for msg in pyais.TCPStream(config.AIS_SOURCE["host"], port=config.AIS_SOURCE["port"]):
                decoded_message = msg.decode()
                broadcast(msg)
        except Exception as e:
            print("Got an exception, reconnecting...", e)
            time.sleep(config.AIS_SOURCE["reconnect_delay"])
            pass
