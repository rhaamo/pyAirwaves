import datetime
import pyais
from libPyAirwaves import datas_ais


class DefaultType:
    """
    Default type for messages structures
    """

    def __init__(self):
        # Incoming data type – airAIS or airADSB
        self.type: str = None


class AdsbType(DefaultType):
    """
    Type for ADS-B messages
    """

    def __init__(self):
        DefaultType.__init__(self)
        self.type: str = "airADSB"

        # Connector component the data arrived in the stack from
        self.entryPoint: str = None

        # Data origin describes the software source of the data (dump1090/aisConn)
        self.dataOrigin: str = None

        # Date/time stamp data hits system or is generated
        self.dts: datetime = None

        # Raw data frame.
        self.data: str = None

        # Name for the source giving out datas
        self.srcName: str = None

        # Name for the server gathering the clients datas
        self.ourName: str = None

        # Data source latitude
        self.srcLat: float = None

        # Data source longitude
        self.srcLon: float = None

        # Mode on how the source position is determined.
        self.srcPosMode: str = None

        # ADS-B Data "source" between "SBS" and "RAW MODE-S"
        self.srcAdsb: str = None

        # ADSB Fields
        # 1 - (MSG, STA, ID, AIR, SEL or CLK)
        self.msgType: str = None

        # 2 - MSG sub types 1 to 8. Not used by other message types.
        self.transmissionType: int = None

        # 3 - Database Session record number
        self.sessionId: str = None

        # 4 - Database Aircraft record number
        self.aircraftId: str = None

        # 5 - Aircraft Mode S hexadecimal code
        self.hexIdent: str = None

        # 6 - Database Flight record number
        self.flightId: str = None

        # 7 - Date message generated
        self.generated_date: str = None

        # 8 - Time message generated
        self.generated_time: str = None

        # 9 - Date message logged
        self.logged_date: str = None

        # 10 - Time message logged
        self.logged_time: str = None

        # End of standard fields
        # Now aircraft specific

        # 11 - An eight digit flight ID - can be flight number or registration (or even nothing).
        self.callsign: str = "@@@@@@@@"

        # 12 - Mode C altitude. Height relative to 1013.2mb (Flight Level). Not height AMSL
        self.altitude: int = None

        # 13 - Speed over ground (not indicated airspeed)
        self.ground_speed: int = None

        # 14 - Track of aircraft (not heading). Derived from the velocity E/W and velocity N/S
        # FYI in dump1090 this is the aircraft heading
        self.track: int = None

        # 15 - North and East positive. South and West negative
        self.lat: float = None

        # 16 - North and East positive. South and West negative
        self.lon: float = None

        # 17 - 64ft resolution
        self.vertical_rate: int = None

        # 18 - Assigned Mode A squawk code
        self.squawk: str = None

        # 19 - Flag to indicate squawk has changed
        self.alert: bool = None

        # 20 - Flag to indicate emergency code has been set
        self.emergency: bool = None

        # 21 - Flag to indicate transponder Ident has been activated
        self.spi_ident: bool = None

        # 22 - Flag to indicate ground squat switch is active
        self.is_on_ground: bool = None

        # EOA

        # Aircraft ID string
        self.idInfo: str = None

        # Vertical status of vehicle (air/gnd)
        self.vertStat: str = None

        # Category
        # Filled by SQL
        self.category: str = None

        # Country code of the block the ICAO AA is in. (Might also be “ICAO” reserved)
        # Filled by SQL
        self.icaoAACC: str = None

        # Veocity in knots
        self.velo: float = None

        # Heading data, not available from SBS, needs to be calculated
        self.heading: float = None

        # True if aircraft is moving at supersonic speeds
        self.supersonic: bool = None

    # A SBS flag is -1 for True, 0 for False...
    def flag(self, f):
        return False if f in ["0", 0] else True

    def populate_from_raw(self, msg: dict):
        print(msg)
        self.srcAdsb = "RAW MODE-S"

        if "rawLat" in msg:
            print(type(msg["rawLat"]))

    # Populate class with datas
    # TODO: add remaining fields of the ADS-B transmission message
    # http://woodair.net/sbs/article/barebones42_socket_data.htm
    # Python arrays starts at 0, ADSB doc at 1, we pad the first entry to avoid messing with our brain
    def populate_from_sbs(self, fields):
        # pad first entry because lazyness
        fields = ["pad"] + fields
        print(fields)

        self.data = ",".join(fields[1:])  # exclude the padding
        self.srcAdsb = "SBS"

        self.msgType = fields[1]
        self.transmissionType = int(fields[2])
        self.sessionId = fields[3]
        self.aircraftId = fields[4]
        self.hexIdent = fields[5]  # Aircraft MODE S Address
        self.flightId = fields[6]
        self.generated_date = fields[7]
        self.generated_time = fields[8]
        self.logged_date = fields[9]
        self.logged_time = fields[10]

        self.callsign = fields[11] if fields[11] else "@@@@@@@@"
        self.altitude = int(fields[12]) if fields[12] else None
        self.ground_speed = int(fields[13]) if fields[13] else None
        self.track = int(fields[14]) if fields[14] else None
        self.lat = float(fields[15]) if fields[15] else None
        self.lon = float(fields[16]) if fields[16] else None
        self.vertical_rate = int(fields[17]) if fields[17] else None
        self.squawk = fields[18] if fields[18] else None
        self.alert = self.flag(fields[19]) if fields[19] else None
        self.emergency = self.flag(fields[20]) if fields[20] else None
        self.spi_ident = self.flag(fields[21]) if fields[21] else None
        self.is_on_ground = self.flag(fields[22]) if fields[22] else None

        # custom
        self.vertStat = "gnd" if self.is_on_ground else "air"
        self.supersonic = None  # unknown in SBS
        self.heading = None
        self.velo = None
        self.icaoAACC = None
        self.category = None

    # Various functions

    def to_dict(self):
        """
        :return: All variables except `__thoses__` ones, and transform `_things` into `things`
        """
        return {
            k.replace("_", ""): v for k, v in self.__dict__.items() if not (k.startswith("__") and k.endswith("__"))
        }

    def has_location(self):
        if self.lat and self.lon and self.altitude:
            return True
        else:
            return False


class AisType(DefaultType):
    """
    Type for AIS messages
    https://www.navcen.uscg.gov/?pageName=AISMessages
    """

    def __init__(self):
        DefaultType.__init__(self)
        self.type: str = "airAIS"

        # Connector component the data arrived in the stack from
        self.entryPoint: str = None

        # Data origin describes the software source of the data (dump1090/aisConn)
        self.dataOrigin: str = None

        # Date/time stamp data hits system or is generated
        self.dts: datetime = None

        # Name for the source giving out datas
        self.srcName: str = None

        # Name for the server gathering the clients datas
        self.ourName: str = None

        # vdm[vdm] Raw data frame.
        self.data: str = None

        # Is this an assembled packet from multiple fragments ?
        self.isAssembled: bool = False

        # Data source latitude
        self.srcLat: float = None

        # Data source longitude
        self.srcLon: float = None

        # Mode on how the source position is determined.
        self.srcPosMode: str = None

        # Decoded longitude
        self.lon: float = None

        # Decoded latitude
        self.lat: float = None

        # Heading data
        self.heading: float = None

        # Course Over Ground whatev
        self.courseOverGnd: float = None

        # Rate of Turn
        self.turnRt: float = None

        # Vehicle address – will be a ICAO aircraft address or MMSI
        self.addr: str = None

        # Maritime Mobile Service Identity ID
        self.mmsi: int = None

        # Position Accuracy. true = high <10m; false low >10m; default=false
        self.posAcc: bool = None

        # FIXME (libAirSuck/aisParse.py:616)
        self.maneuver: int = None

        # Receiver autonomous integrity monitoring; false=not in use; true=in use; default=true
        self.raim: bool = None

        # Radio status
        self.radioStatus: int = None

        # Ship type
        self.mmsiType: str = None

        # Ship Country
        self.mmsiCC: str = None

        # Ship destination
        self.destination: str = None

        # Ship callsign
        self.callsign: str = None

        # Ship EPFD Type (positioning device)
        self.epfdMeta: str = None

        # Ship Navigation Status
        self.navStatMeta: str = None

        # Ship dimensions
        self.dimToBow: int = None
        self.dimToStern: int = None
        self.dimToPort: int = None
        self.dimToStarboard: int = None

        # Distance between "water line" and water
        self.draught: float = None

        # Ship ETA
        self.etaStr: str = None

        # Ship type
        self.shipTypeMeta: str = None

    def to_dict(self):
        """
        :return: All variables except `__thoses__` ones or "" or None, and transform `_things` into `things`
        """
        return {
            k.replace("_", ""): v
            for k, v in self.__dict__.items()
            if not ((k.startswith("__") and k.endswith("__")) or v == "" or v is None)
        }

    def populateFromParsedVdm(self, message: pyais.messages.AISMessage):
        # Populate fields from VDM

        # Raw VDM looks like
        # {'ais_id': 1, 'raw': '!AIVDM,1,1,,B,13HOI<PP0000kQ6LCo574OwN0D1e,0*59', 'talker': 'AI', 'msg_type': 'VDM',
        # 'count': 1, 'index': 1, 'seq_id': '', 'channel': 'B', 'data': '13HOI<PP0000kQ6LCo574OwN0D1e',
        # 'checksum': 89, 'bit_array': 'xxx'}
        # Raw AIS single packet
        # {'type': 1, 'repeat': 0, 'mmsi': 227006770, 'status': <NavigationStatus.UnderWayUsingEngine: 0>,
        # 'turn': -128, 'speed': 0.0, 'accuracy': False, 'lon': 0.175845, 'lat': 49.47587333333333, 'course': 180.9,
        # 'heading': 511, 'second': 47, 'maneuver': <ManeuverIndicator.NotAvailable: 0>, 'raim': False, 'radio': 82029}
        # Raw fragmented
        # {'type': 4, 'repeat': 0, 'mmsi': 2276010, 'year': 2020, 'month': 2, 'day': 11, 'hour': 17, 'minute': 39,
        # 'second': 50, 'accuracy': True, 'lon': 0.23283333333333334, 'lat': 49.42783333333333,
        # 'epfd': <EpfdType.Surveyed: 7>, 'raim': False, 'radio': 34683}
        # {'type': 5, 'repeat': 0, 'mmsi': 228022900, 'ais_version': 0, 'imo': 9420423, 'callsign': 'FIDP',
        # 'shipname': 'ETRETAT', 'shiptype': <ShipType.Passenger_NoAdditionalInformation: 69>, 'to_bow': 24,
        # 'to_stern': 163, 'to_port': 8, 'to_starboard': 18, 'epfd': <EpfdType.GPS: 1>, 'month': 2, 'day': 13,
        # 'hour': 17, 'minute': 30, 'draught': 6.0, 'destination': 'SANTANDER', 'dte': False}
        print("chomp chomp AIS VDM")

        self.dts = str(datetime.datetime.utcnow())

        self.lon = message["lon"]
        self.lat = message["lat"]
        if message["heading"]:
            self.heading = round(message["heading"], 3)
        if message["course"]:
            self.courseOverGnd = round(message["course"], 3)
        self.turnRt = message["turn"]
        self.mmsi = message["mmsi"]
        self.addr = self.mmsi
        self.posAcc = message["accuracy"]
        if message["maneuver"]:
            self.maneuver = message["maneuver"].numerator
        self.raim = message["raim"]
        self.radioStatus = message["radio"]

        # Extract MMSI Datas
        mmsiMeta = self.__getMMSIMeta()
        self.mmsiCC = mmsiMeta.get("mmsiCC", "")
        self.mmsiType = mmsiMeta.get("mmsiType", "")
        # Extract Ship Type
        if message["shiptype"]:
            self.shipTypeMeta = self.__getAISShipType(message["shiptype"])
        self.name = message["shipname"]

        self.destination = message["destination"]
        self.callsign = message["callsign"]

        if message["epfd"]:
            self.epfdMeta = self.__getEPFDMeta(message["epfd"])
        if message["status"]:
            self.navStatMeta = self.__getAISNavStat(message["status"])
        self.dimToBow = message["to_bow"]
        self.dimToStern = message["to_stern"]
        self.dimToPort = message["to_port"]
        self.dimToStarboard = message["to_starboard"]
        self.draught = message["draught"]

    def isoCCtoCountry(self, isoCC):
        """
        Convert a given ISO country code string to a country name
        :param isoCC:
        :return: Country name as dict
        """
        retVal = {}

        try:
            retVal = datas_ais.isoCC2country[isoCC]
        except KeyError:
            pass

        return retVal

    def __getAISNavStat(self, navstat):
        """
        Accepts a 4-bit number representing navigation status
        :param navstat: 4-bit navigation status
        :return: navigation status text
        """
        retVal = "Invalid"
        if (navstat >= 0) or (navstat <= 15):
            statArray = [
                "Underway using engine",
                "Anchored",
                "Not under command",
                "Restricted maneuverability",
                "Constrained by draught",
                "Moored",
                "Aground",
                "Fishing",
                "Underway sailing",
                "Reserved (HSC)",
                "Reserved (WIG)",
                "Reserved",
                "Reserved",
                "Reserved",
                "AIS-SART (lifeboat)",
                "Not defined",
            ]
            retVal = statArray[navstat]
        return retVal

    def __getEPFDMeta(self, epfd):
        """
        Get EPFD metadata given an EPFD value.
        :param epfd: EPFD value
        :return: string
        """
        retVal = ""
        epfdDesc = [
            "Undefined",
            "GPS",
            "GLONASS",
            "GPS + GLONASS",
            "Loran-C",
            "Chayka",
            "Integrated nav system",
            "Surveyed",
            "Galileo",
        ]
        if epfd <= 8:
            retVal = epfdDesc[epfd]
        else:
            retVal = "Unknown"

        return retVal

    def __getMMSIMeta(self, cc2Country=False):
        """
        Get metatdata from a given MMSI address. This is based on the following table:
        http://www.vtexplorer.com/vessel-tracking-mmsi-mid-codes.html

        :param cc2Country: True to only return the country name
        :return: A dict with MMSI Metadatas
        """

        retVal = {}

        # The character at which our MID starts
        midCursor = 0

        # Type of MMSI address. Defaults to ship.
        mmsiType = "Ship"

        if not self.mmsi:
            return {"mmsiType": mmsiType}

        # Figure out if we have certain types of MMSI address.
        if (self.mmsi >= 800000000) and (self.mmsi <= 899999999):
            mmsiType = "Diver's radio"

            # Where does the MID start?
            midCursor = 1

        if (self.mmsi >= 10000000) and (self.mmsi <= 99999999):
            mmsiType = "Group of ships"

            # Where does the MID start?
            midCursor = 0

        if (self.mmsi >= 1000000) and (self.mmsi <= 9999999):
            mmsiType = "Coastal station"

            # Where does the MID start?
            midCursor = 0

        if (self.mmsi >= 111000000) and (self.mmsi <= 111999999):
            mmsiType = "SAR aircraft"

            # Where does the MID start?
            midCursor = 3

        if (self.mmsi >= 990000000) and (self.mmsi <= 999999999):
            mmsiType = "Aid to Navigation"

            # Where does the MID start?
            midCursor = 2

        if (self.mmsi >= 980000000) and (self.mmsi <= 989999999):
            mmsiType = "Craft w/ parent ship"

            # Where does the MID start?
            midCursor = 2

        if (self.mmsi >= 970000000) and (self.mmsi <= 970999999):
            mmsiType = "SART (Search and Rescue Xmitter)"

            # Where does the MID start?
            midCursor = 3

        if (self.mmsi >= 972000000) and (self.mmsi <= 972999999):
            mmsiType = "MOB (Man Overboard) device"

            # Where does the MID start?
            midCursor = 3

        if (self.mmsi >= 974000000) and (self.mmsi <= 974999999):
            mmsiType = "EPIRB"

            # Where does the MID start?
            midCursor = 3

        # Set the mmsiType.
        retVal.update({"mmsiType": mmsiType})

        try:
            # Get the MID portion of the MMSI.
            midStr = str(self.mmsi)[midCursor : (midCursor + 3)]
            midCtry = datas_ais.mid2isoCC[midStr]

            # Set the country data.
            retVal.update({"mmsiCC": midCtry["isoCC"]})

            # If we explicitly want the country name...
            if cc2Country:
                retVal.update({"mmsiCountry": self.isoCCtoCountry(midCtry["isoCC"])})

        except KeyError:
            # Do nothing because sometimes there's a bad value.
            pass

        except Exception as e:
            # Pass the exception back up the stack.
            raise e

            # Send the data back along.
        return retVal

    def __getAISShipType(self, shipType):
        """
        Get the text description of a given AIS ship type
        :param shipType: int, ship type
        :return: str, ship type name
        """

        retVal = ""
        print("ship type")
        try:
            retVal = datas_ais.shipTypes[shipType]
        except (IndexError, TypeError):
            print("???")
            pass
        except Exception as e:
            print(e)
            raise e

        return retVal

    def has_location(self):
        if self.lat and self.lon:
            return True
        else:
            return False
