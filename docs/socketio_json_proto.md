# SocketIO JSON Protocol

This is a work in progress, reverse ingeneered from AirSuck.

## ADS-B (dump1090 SBS Base Station format, port 30003)

SBS Reference: http://woodair.net/sbs/article/barebones42_socket_data.htm

| Field name | Description | Type | SBS Field |
| ---------- | ----------- | ---- | --------- |
|type|Incoming data type – airAIS or airSSR|string||
|addr|Vehicle address – will be a ICAO aircraft address or MMSI|string|field 5|
|idInfo|Aircraft ID string|string|field 4|
|aSquawk|Mode A squawk code. 4 character string representing four octal numbers.|string|field 18|
|alt|Altitude data in feet|int|field 12|
|lon|Decoded longitude|float|field 16|
|lat|Decoded latitude|float|field 15|
|entryPoint|Connector component the data arrived in the stack from|string||
|dataOrigin|Data origin describes the software source of the data (dump1090/aisConn)|string||
|dts|Date/time stamp data hits system or is generated|str(datetime.utcnow())||
|src|Name of source host.|string||
|data|Raw data frame.|string||
|srcPos|Is srcPos available|boolean|
|srcLat|Data source latitude|float||
|srcLon|Data source longitude|float||
|srcPosMeta|Metadata about how srcLat and srcLon are derived.|string||

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
