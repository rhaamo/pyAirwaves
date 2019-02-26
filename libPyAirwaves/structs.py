import datetime


class DefaultType:
    """
    Default type for messages structures
    """

    def __init__(self):
        # Incoming data type – airAIS or airSSR
        self.type: str = None


class AdsbType(DefaultType):
    """
    Type for ADS-B messages
    """

    def __init__(self):
        DefaultType.__init__(self)
        self.type: str = "airSSR"

        # Vehicle address – will be a ICAO aircraft address or MMSI
        self.addr: str = None

        # Aircraft ID string
        self.idInfo: str = None

        # Mode A squawk code. 4 character string representing four octal numbers.
        self.aSquawk: str = None

        # Altitude data in feet
        self.alt: int = None

        # Decoded longitude
        self.lon: float = None

        # Decoded latitude
        self.lat: float = None

        # Connector component the data arrived in the stack from
        self.entryPoint: str = None

        # Data origin describes the software source of the data (dump1090/aisConn)
        self.dataOrigin: str = None

        # Date/time stamp data hits system or is generated
        self.dts: datetime = None

        # Name of source host.
        self._src: str = None
        # Equals to src
        self.lastSrc: str = None

        # Raw data frame.
        self.data: str = None

        # I don't know, probably unused
        self._clientName: str = None
        # Equals to clientName
        self.lastClientName: str = None

        # Is srcPos available
        self.srcPos: bool = False

        # Data source latitude
        self.srcLat: float = None

        # Data source longitude
        self.srcLon: float = None

        # Metadata about how srcLat and srcLon are derived.
        self.srcPosMeta: str = None

        # Vertical status of vehicle (air/gnd)
        self.vertStat: str = None

        # Aircraft climb or decline rate in feet/min.
        self.vertRate: int = None

        # Category
        self.category: str = None

        # Country code of the block the ICAO AA is in. (Might also be “ICAO” reserved)
        self.icaoAACC: str = None

        # Veocity in knots
        self.velo: float = None

        # Heading data, not available from SBS, needs to be calculated
        self.heading: float = None

        # True if aircraft is moving at supersonic speeds
        self.supersonic: bool = None

    # Populate class with datas

    # Remember that fields start at 1 but python array at 0, so field 3 (session ID) is at position 2
    def populate_from_list(self, fields):
        self.addr = fields[4]  # int(fields[4], 16)
        self.idInfo = fields[3]
        self.aSquawk = fields[17]
        self.alt = int(fields[11]) if fields[11] else None
        self.lon = float(fields[15]) if fields[15] else None
        self.lat = float(fields[14]) if fields[14] else None
        self.dts = str(datetime.datetime.utcnow())
        self.data = ",".join(fields)
        self.srcPos = False  # TODO add position support
        if fields[21] == 0 or fields[21] == "0":
            self.vertStat = "air"
        else:
            self.vertStat = "gnd"
        self.vertRate = int(fields[16]) if fields[16] else None
        self.category = None
        self.icaoAACC = None
        self.velo = None
        self.heading = None
        self.supersonic = None

    def populate_from_string(self, msg):
        self.populate_from_list(msg.split(","))

    # Various functions

    def to_dict(self):
        """
        :return: All variables except `__thoses__` ones, and transform `_things` into `things`
        """
        return {
            k.replace("_", ""): v for k, v in self.__dict__.items() if not (k.startswith("__") and k.endswith("__"))
        }

    def has_location(self):
        if self.lat and self.lon and self.alt:
            return True
        else:
            return False

    # Setters and Getters

    def set_src(self, value):
        self._src = value
        self.lastSrc = value

    def get_src(self):
        return self._src

    def set_client_name(self, value):
        self._clientName = value
        self.lastClientName = value

    def get_client_name(self):
        return self._clientName

    src = property(get_src, set_src)
    clientName = property(get_client_name, set_client_name)
