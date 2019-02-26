import logging
from typing import List
from libPyAirwaves.structs import AdsbType
import datetime

# List Of String type
list_of_strings = List[str]


# Do some basic checks on the ADS-B received message
# http://woodair.net/sbs/article/barebones42_socket_data.htm
def is_valid_adsb_message(fields: list_of_strings):
    """
    Check if the ADS-B message is valid:
    - contains 22 fields
    - At least a valid message type field
    - At least a valid transmission type field
    :param fields: List of strings containing the ADS-B message, splitted on ','
    :return: True or False
    """
    is_valid = False

    if len(fields) == 22:
        is_valid = True

    if fields[0].upper() in ["MSG", "STA", "ID", "AIR", "SEL", "CLK"]:
        is_valid = True
    else:
        logging.error(f"Field 1 invalid : '{fields[0]}'")
        logging.error(f"Invalid ADSB Message: '{fields}'")

    if int(fields[1]) in [1, 2, 3, 4, 5, 6, 7, 8]:
        is_valid = True
    else:
        logging.error(f"Field 2 invalid: '{fields[1]}'")
        logging.error(f"Invalid ADSB Message: '{fields}'")

    if not is_valid:
        logging.error(f"Invalid ADSB Message: '{fields}'")

    return is_valid


def get_adsb_message(fields: list_of_strings):
    """
    Use the splitted ADS-B message and returns an AdsbType structure containing it
    :param fields: List of strings containing the ADS-B message, splitted on ','
    :return: an AdsbType structure
    """
    # Remember that fields start at 1 but python array at 0, so field 3 (session ID) is at position 2
    msg = AdsbType()
    msg.addr = fields[4]  # int(fields[4], 16)
    msg.idInfo = fields[3]
    msg.aSquawk = fields[17]
    msg.alt = int(fields[11]) if fields[11] else None
    msg.lon = float(fields[15]) if fields[15] else None
    msg.lat = float(fields[14]) if fields[14] else None
    msg.dts = str(datetime.datetime.utcnow())
    msg.lastSrc = msg.src
    msg.data = ",".join(fields)
    msg.srcPos = False  # TODO add position support
    if fields[21] == 0 or fields[21] == "0":
        msg.vertStat = "air"
    else:
        msg.vertStat = "gnd"
    msg.vertRate = int(fields[16]) if fields[16] else None
    msg.category = None
    msg.icaoAACC = None
    msg.velo = None
    msg.heading = None
    msg.supersonic = None
    msg.lastClientName = msg.clientName
    return msg
