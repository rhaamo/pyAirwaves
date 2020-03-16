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
    ais_message["source_metadatas"] = {
        "entry_point": "airwaves_ais_client",
        "our_name": config.PYAW_HOSTNAME,
        "src_name": config.AIS_SOURCE["name"],
        "src_lat": config.AIS_SOURCE["lat"],
        "src_lon": config.AIS_SOURCE["lon"],
        "src_pos_mode": config.AIS_SOURCE["posMode"],
        "data_origin": "rtl-ais",
        "type": "airAIS",
    }

    # print(ais_message)
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
