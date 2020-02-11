# SocketIO JSON Protocol

This is a work in progress, reverse ingeneered from AirSuck.

## ADS-B (dump1090 SBS Base Station format, port 30003)

SBS Reference: http://woodair.net/sbs/article/barebones42_socket_data.htm

| Field name | Description | Type | SBS Field | Example,value |
| ---------- | ----------- | ---- | --------- | ------------- |
|   required   |
|type|Incoming data type – airAIS or airSSR|string| |airAIS,airSSR
|addr|Vehicle address – will be a ICAO aircraft address or MMSI|string|field 5|3C6426
|idInfo|Aircraft ID string|string|field 4|1
|aSquawk|Mode A squawk code. 4 character string representing four octal numbers.|string|field 18|
|alt|Altitude data in feet|int|field 12|29000
|lon|Decoded longitude|float|field 16|
|lat|Decoded latitude|float|field 15|
|entryPoint|Connector component the data arrived in the stack from|string| |airwaves_client
|dts|Date/time stamp data hits system or is generated|str(datetime.utcnow())| |2019-02-23 15:34:49.495070
|src|Name of source host.|string| |some_server
|data|Raw data frame.|string| |MSG,3,1,1,407...
|srcPos|Is srcPos available|boolean|
|srcLat|Data source latitude|float| |
|srcLon|Data source longitude|float| |
|srcPosMeta|Metadata about how srcLat and srcLon are derived.|string| |
|  optional  |
|vertStat|Vertical status of vehicle (air/gnd)|string|field 22, |gnd,air
|vertRate|Aircraft climb or decline rate in feet/min.|int|field 17|
|category|Category|string| |
|icaoAACC|Country code of the block the ICAO AA is in. (Might also be “ICAO” reserved)|string| |
|velo|Veocity in knots|float| |
|heading|Heading data|float| |
|supersonic|True if aircraft is moving at supersonic speeds|bool| |
|clientName|Data source name|string| |dump1090_ant_b|
|fs|Flight status bit|int|
|regTail|Registration number|string| |
|regAuthority|Country registration|string| |
|regName|Registration owner|string| |
|regAircraft|Manufacturer year, model, name|string| |

|UI Text|Json Field|Type|Description|
|-------|----------|----|-----------|
|     table list    ||||
|ID|
|Cat.|
|Flag|
|Altitude|
|Velocity|
|Heading|
|Pos|
|Sig|
|     details     ||||
|Air / Gnd|
|Supersonic|
|Climb rate|
|Position|
|Data src.|
|Flight status|
|Heading|

## AIS (rtl-ais)

This is currently untested.

| Field name | Description | Type |
| ---------- | ----------- | ---- |
|entryPoint|Connector component the data arrived in the stack from|string|
|dataOrigin|Data origin describes the software source of the data (dump1090/aisConn)|string|
|type|Incoming data type – airAIS or airSSR|string|
|dts|Date/time stamp data hits system or is generated|str(datetime.utcnow())||
|src|Name of source host.|string|
|data|Raw data frame.|string|
|isFrag|unknown ?|bool|
|isAssembled|unknown ?|bool|
|srcLat|Data source latitude|float|
|srcLon|Data source longitude|float|
|srcPosMeta|Metadata about how srcLat and srcLon are derived.|string|
|fragCount|fragment count|int|
|fragNumber|fragment number|int|
|messageID|message ID number|int|
|channel|Channel 1 or 2 (A or B)|string|
|payload|payload string|string|
|padBits|number of padding bits included in the sentence (related to len==2==CRC)|int|


|UI Text|Json Field|Type|Description|
|-------|----------|----|-----------|
|     table list    ||||
|ID|name|   |Name of the boat|
|Flag|mmsiCC|   |MMSI Country|
|Velocity|velo|    |Velocity|
|Course|courseOverGnd|    |Course|
|Destination|destination|    |Destination|
|     details     ||||
|MMSI Type|mmsiType|    |    |
|COG / Hdg|courseOverGnd & heading|    |    |
|Callsign|callsign|    |    |
|Pos. type|epfdMeta|    |    |
|Ship type|shipTypeMeta|string|Ship type description|
|Position|lat & lon|foat & float|Latitude and Longitude|
|Nav. Stat.|navStatMeta|string|Navigation status|
|Data src.|lastClientName & lastSrc|    |    |
|Dim.|dimToBow & dimToStern & dimToPort & dimToStarboard|all int|    |
|Turn rate|unused ?|    |    |
|Draught|draught|    |    |
|ETA|etaStr|    |    |
