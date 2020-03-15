import pyais


def restructure_ais(msg: pyais.messages.NMEAMessage):
    decoded = msg.decode()
    t = decoded["type"]
    struct = {}
    if t in [1, 2, 3]:
        struct = msg_123(decoded)
    elif t == 4:
        struct = msg_4(decoded)
    elif t == 5:
        struct = msg_5(decoded)
    elif t == 9:
        pass
    elif t == 12:
        pass
    elif t == 14:
        pass
    elif t == 18:
        pass
    elif t == 21:
        pass
    else:
        return {}

    # Add specific stuff from the NMEA message itself
    struct["channel"] = (str(msg.channel),)
    struct["checksum"] = hex(msg.checksum)[2:]
    struct["current"] = str(msg.index)
    struct["formatter"] = msg.msg_type
    struct["message_id"] = msg.ais_id
    struct["padding"] = str(str(msg.raw).split("*")[0].split(",")[-1])
    struct["payload"] = str(msg.data)
    struct["talker"] = msg.talker
    struct["total"] = str(msg.count)
    struct["sequential"] = str(msg.seq_id)

    return struct


def msg_123(decoded: pyais.messages.AISMessage):
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
    }


def msg_4(decoded: pyais.messages.AISMessage):
    """
    Message type 4

    {'type': 4, 'repeat': 0, 'mmsi': 2288218, 'year': 2020, 'month': 3, 'day': 15, 'hour': 19, 'minute': 16, 'second': 23, 'accuracy': False,
    'lon': 0.07107166666666667, 'lat': 49.50914, 'epfd': <EpfdType.GPS: 1>, 'raim': False, 'radio': 49251}
    """
    return {
        "communication_state": decoded["radio"],
        "latitude": decoded["lat"],
        "longitude": decoded["lon"],
        "position_accuracy": 1 if decoded["accuracy"] else 0,
        "raim_flag": 1 if decoded["raim"] else 0,
        "repeat_indicator": decoded["repeat"],
        "spare": None,
        "transmission_control_for_long_range_broadcast_message": None,  # idk
        "type_of_electronic_position_fixing_device": int(decoded["epfd"]),
        "user_id": decoded["mmsi"],
        "utc_day": decoded["day"],
        "utc_hour": decoded["hour"],
        "utc_minute": decoded["minute"],
        "utc_second": decoded["second"],
        "utc_year": decoded["year"],
    }


def msg_5(decoded: pyais.messages.AISMessage):
    """
    Message type 5

    {'type': 5, 'repeat': 0, 'mmsi': 228179700, 'ais_version': 1, 'imo': 9293040, 'callsign': 'FVFB', 'shipname': 'VB BARFLEUR (18)',
    'shiptype': <ShipType.Trug: 52>, 'to_bow': 10, 'to_stern': 20, 'to_port': 5, 'to_starboard': 5, 'epfd': <EpfdType.GPS: 1>,
    'month': 0, 'day': 0, 'hour': 24, 'minute': 60, 'draught': 5.0, 'destination': '', 'dte': False}
    """
    return {
        "ais_version_indicator": decoded["ais_version"],
        "call_sign": decoded["callsign"],
        "destination": decoded["destination"],
        "dimension_a": decoded["to_bow"],
        "dimension_b": decoded["to_stern"],
        "dimension_c": decoded["to_port"],
        "dimension_d": decoded["to_starboard"],
        "dte": 1 if decoded["dte"] else 0,
        "eta": {"day": decoded["day"], "hour": decoded["hour"], "minute": decoded["minute"], "month": decoded["month"]},
        "imo_number": decoded["imo"],
        "maximum_present_static_draught": decoded["draught"],
        "name": decoded["shipname"],
        "repeat_indicator": decoded["repeat"],
        "spare": None,
        "type_of_electronic_position_fixing_device": int(decoded["epfd"]),
        "type_of_ship_and_cargo_type": int(decoded["shiptype"]),
        "user_id": decoded["mmsi"],
    }
