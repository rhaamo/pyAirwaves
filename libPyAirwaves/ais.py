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
        struct = msg_9(decoded)
    elif t == 12:
        struct = msg_12(decoded)
    elif t == 14:
        struct = msg_14(decoded)
    elif t == 18:
        struct = msg_18(decoded)
    elif t == 21:
        struct = msg_21(decoded)
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
    Message type 1, 2, 3 - Class A AIS Position Report

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
    Message type 4 - AIS Base Station Report

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
    Message type 5 - AIS Class A Ship Static And Voyage Related Data

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


def msg_9(decoded: pyais.messages.AISMessage):
    """
    Message type 9 - AIS Standard Search And Rescue Aircraft Position Report

    {'type': 9, 'repeat': 0, 'mmsi': 111232506, 'alt': 583, 'speed': 122, 'accuracy': False, 'lon': -2.14309, 'lat': 50.685065,
    'course': 117.7, 'second': 1, 'dte': True, 'assigned': False, 'raim': False, 'radio': 49549}
    """
    return {
        "altitude": decoded["alt"],
        "altitude_sensor": None,  # not handled ?
        "assigned_mode_flag": 1 if decoded["assigned"] else 0,
        "cog": decoded["course"],
        "communication_state": decoded["radio"],
        "communication_state_selector_flag": None,  # not handled ?
        "latitude": decoded["lat"],
        "longitude": decoded["lon"],
        "position_accuracy": 1 if decoded["accuracy"] else 0,
        "raim_flag": 1 if decoded["raim"] else 0,
        "repeat_indicator": decoded["repeat"],
        "sog": decoded["speed"],
        "spare1": None,
        "spare2": None,
        "time_stamp": decoded["second"],
        "user_id": decoded["mmsi"],
        "dte": decoded["dte"],
    }


def msg_12(decoded: pyais.messages.AISMessage):
    """
    Message type 12 - AIS Addressed Safety Related Message

    {'type': 12, 'repeat': 0, 'mmsi': 271002099, 'seqno': 0, 'dest_mmsi': 271002111, 'retransmit': True, 'text': 'MSG FROM 271002099'}
    """
    return {
        "destination_id": decoded["dest_mmsi"],
        "repeat_indicator": decoded["repeat"],
        "retransmit_flag": 1 if decoded["retransmit"] else 0,
        "safety_related_text": decoded["text"],
        "sequence_number": decoded["seqno"],
        "source_id": decoded["mmsi"],
        "spare": None,
    }


def msg_14(decoded: pyais.messages.AISMessage):
    """
    Message type 14 - AIS Safety Related Broadcast Message

    {'type': 14, 'repeat': 0, 'mmsi': 351809000, 'text': 'RCVD YR TEST MSG'}
    """
    return {
        "repeat_indicator": decoded["repeat"],
        "safety_related_text": decoded["text"],
        "source_id": decoded["mmsi"],
        "spare": None,
    }


def msg_18(decoded: pyais.messages.AISMessage):
    """
    Message type 18 - AIS Standard Class B Equipment Position Report

    {'type': 18, 'repeat': 0, 'mmsi': 227006810, 'speed': 10.5, 'accuracy': False, 'lon': 0.08755666666666667, 'lat': 49.477621666666664,
    'course': 126.7, 'heading': 511, 'second': 5, 'regional': 0, 'cs': True, 'display': False, 'dsc': True, 'band': True, 'msg22': True,
    'assigned': False, 'raim': True, 'radio': 917510}
    """
    return {
        "class_b_band_flag": 1 if decoded["band"] else 0,
        "class_b_display_flag": 1 if decoded["display"] else 0,
        "class_b_dsc_flag": 1 if decoded["dsc"] else 0,
        "class_b_message_22_flag": 1 if decoded["msg22"] else 0,
        "class_b_unit_flag": 1 if decoded["regional"] else 0,
        "cog": decoded["course"],
        "communication_state": decoded["radio"],
        "communication_state_selector_flag": 1 if decoded["cs"] else 0,
        "latitude": decoded["lat"],
        "longitude": decoded["lon"],
        "mode_flag": 1 if decoded["assigned"] else 0,
        "position_accuracy": 1 if decoded["accuracy"] else 0,
        "raim_flag": 1 if decoded["raim"] else 0,
        "repeat_indicator": decoded["repeat"],
        "sog": decoded["speed"],
        "spare1": None,
        "spare2": None,
        "time_stamp": decoded["second"],
        "true_heading": decoded["heading"],
        "user_id": decoded["mmsi"],
    }


def msg_21(decoded: pyais.messages.AISMessage):
    """
    Message type 21 - AIS Aids To Navigation (ATON) ReportAIS Aids To Navigation (ATON) Report

    {'type': 21, 'repeat': 0, 'mmsi': 992276203, 'aid_type': <NavAid.ISOLATED_DANGER: 28>, 'name': 'EPAVE ANTARES', 'accuracy': False,
    'lon': 0.0315, 'lat': 49.536165, 'to_bow': 5, 'to_stern': 6, 'to_port': 7, 'to_starboard': 7, 'epfd': <EpfdType.Undefined: 0>,
    'second': 60, 'off_position': False, 'regional': 0, 'raim': False, 'virtual_aid': False, 'assigned': False, 'name_extension': ''}
    """
    return {
        "assigned_mode_flag": 1 if decoded["assigned"] else 0,
        "aton_status": 00000000,  # doesn't seems handled ?
        "dimension_a": decoded["to_bow"],
        "dimension_b": decoded["to_stern"],
        "dimension_c": decoded["to_port"],
        "dimension_d": decoded["to_starboard"],
        "latitude": decoded["lat"],
        "longitude": decoded["lon"],
        "name_of_aids_to_navigation": decoded["name"],
        "name_extension": decoded["name_extension"],
        "assembled_name": decoded["name"] + decoded["name_extension"],  # TODO validate
        "off_position_indicator": 1 if decoded["off_position"] else 0,
        "position_accuracy": 1 if decoded["accuracy"] else 0,
        "raim_flag": 1 if decoded["raim"] else 0,
        "repeat_indicator": decoded["repeat"],
        "spare": None,
        "time_stamp": decoded["second"],
        "type_of_aids_to_navigation": int(decoded["aid_type"]),
        "type_of_electronic_position_fixing_device": int(decoded["epfd"]),
        "virtual_aton_flag": 1 if decoded["virtual_aid"] else 0,
    }
