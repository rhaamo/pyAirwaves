# PubSub (redis) JSON structure definition

## Common, in a dict named "source_metadatas"
|name|type|used by frontend|required|description|
|----|----|----------------|--------|-----------|
|src_pos_mode|integer enum-like|no|no|How the source position is determined.|
|src_lat|float|no|no|Latitude of the source|
|src_lon|float|no|no|Longitude of the source|
|src_name|string|yes|required|Name for the source giving out datas|
|our_name|string|yes|required|Name for the server gathering the clients datas|
|entry_point|string|no|yes|Name of the script/tool used to push datas to the redis pubsub (ie airwaves_ais_client)|
|data_origin|string|no|yes|how is the data gathered ? (ie rtl-ais,...)|

## ADSB

## AIS
See the files 'backend/lib/pyairwaves/archive_ship_message/*.ex`.

Each message type has his own structure.

## Integers enum-like
- srcPosMode
    - 0 unknown
    - 1 manual
    - 2 gps_manual
    - 3 gps_auto
