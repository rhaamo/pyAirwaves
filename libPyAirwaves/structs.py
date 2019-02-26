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
        self.src: str = None
        # Equals to src
        self.lastSrc: str = None

        # Raw data frame.
        self.data: str = None

        # I don't know, probably unused
        self.clientName: str = None
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

    def to_dict(self):
        return {k: v for k, v in self.__dict__.items() if not (k.startswith("__") and k.endswith("__"))}

    def has_location(self):
        if self.lat and self.lon and self.alt:
            return True
        else:
            return False
