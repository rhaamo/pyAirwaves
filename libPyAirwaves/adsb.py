from typing import List

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
        print(f"Field 1 invalid : '{fields[0]}'")
        print(f"Invalid ADSB Message: '{fields}'")

    if int(fields[1]) in [1, 2, 3, 4, 5, 6, 7, 8]:
        is_valid = True
    else:
        print(f"Field 2 invalid: '{fields[1]}'")
        print(f"Invalid ADSB Message: '{fields}'")

    if not is_valid:
        print(f"Invalid ADSB Message: '{fields}'")

    return is_valid
