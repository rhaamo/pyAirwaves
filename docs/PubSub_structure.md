# PubSub (redis) JSON structure definition

## Common
|name|type|used by frontend|required|description|
|----|----|----------------|--------|-----------|
|srcPosMode|integer enum-like|no|no|How the source position is determined.|
|srcLat|float|no|no|Latitude of the source|
|srcLon|float|no|no|Longitude of the source|
|srcName|string|yes|required|Name for the source giving out datas|
|ourName|string|yes|required|Name for the server gathering the clients datas|
|entryPoint|string|no|yes|Name of the script/tool used to push datas to the redis pubsub (ie airwaves_ais_client)|
|dataOrigin|string|no|yes|how is the data gathered ? (ie rtl-ais,...)|
## ADSB

## AIS

## Integers enum-like
- srcPosMode
    - 0 unknown
    - 1 manual
    - 2 gps_manual
    - 3 gps_auto
