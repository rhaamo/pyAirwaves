import pyais


def restructure_ais(msg: pyais.messages.NMEAMessage):
    decoded = msg.decode()
    if decoded["type"] in [1, 2, 3]:
        return msg_123(msg, decoded)
    else:
        return {}


def msg_123(msg: pyais.messages.NMEAMessage, decoded: pyais.messages.AISMessage):
    """
    Message type 1, 2, 3

    {'type': 1, 'repeat': 0, 'mmsi': 227729770, 'status': <NavigationStatus.UnderWayUsingEngine: 0>, 'turn': 0, 'speed': 5.6, 'accuracy': False,
    'lon': 0.11224333333333333, 'lat': 49.484318333333334, 'course': 272.0, 'heading': 316, 'second': 6, 'maneuver': <ManeuverIndicator.NotAvailable: 0>,
    'raim': False, 'radio': 2303}
    """
    return {
        "cog": decoded["course"],
        "communication_state": decoded["radio"],
        "latitude": decoded["lat"],
        "longitude": decoded["lon"],
        "navigational_status": int(decoded["status"]),
        "position_accuracy": 1 if decoded["accuracy"] else 0,
        "raim_flag": 1 if decoded["raim"] else 0,
        "rate_of_turn": decoded["turn"],
        "repeat_indicator": decoded["repeat"],
        "sog": decoded["speed"],
        "spare": None,
        "special_maneuvre_indicator": int(decoded["maneuver"]),
        "time_stamp": decoded["second"],
        "true_heading": decoded["heading"],
        "user_id": decoded["mmsi"],
        # Specific to the NMEA message
        "channel": str(msg.channel),
        "checksum": hex(msg.checksum)[2:],
        "current": str(msg.index),
        "formatter": msg.msg_type,
        "message_id": msg.ais_id,
        "padding": str(str(msg.raw).split("*")[0].split(",")[-1]),
        "payload": str(msg.data),
        "talker": msg.talker,
        "total": str(msg.count),
        "sequential": str(msg.seq_id),
    }
