#!/usr/bin/env python
"""
blah
"""

import config
from libPyAirwaves.ais import restructure_ais
import pyais
import redis
import json
import traceback

count_failed_connection = 0
max_failed_connection = 10

redis = redis.from_url(config.REDIS_URL)
pubsub = redis.pubsub()
pubsub.subscribe("room:vehicles")


def broadcast(msg: pyais.messages.NMEAMessage):
    # Populate the structure from parsed VDM
    ais_message = restructure_ais(msg)
    ais_message["entryPoint"] = "airwaves_ais_client"
    ais_message["ourName"] = config.PYAW_HOSTNAME
    ais_message["srcName"] = config.AIS_SOURCE["name"]
    ais_message["srcLat"] = config.AIS_SOURCE["lat"]
    ais_message["srcLon"] = config.AIS_SOURCE["lon"]
    ais_message["srcPosMode"] = config.AIS_SOURCE["posMode"]
    ais_message["dataOrigin"] = "rtl-ais"

    # Valid message and emit if lat/lon are present
    # if ais_message.lat and ais_message.lon:
    # print(ais_message.to_dict())
    print(ais_message)
    redis.publish("room:vehicles", json.dumps(ais_message))


if __name__ == "__main__":
    while True:
        try:
            for msg in pyais.TCPStream(config.AIS_SOURCE["host"], port=config.AIS_SOURCE["port"]):
                decoded_message = msg.decode()
                broadcast(msg)
        except Exception as e:
            print("Got an exception, reconnecting...", e)
            traceback.print_exc()
            pass
