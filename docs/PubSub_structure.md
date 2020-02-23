# PubSub (redis) JSON structure definition

## Common
|name|type|used by frontend|required|description|
|----|----|----------------|--------|-----------|
|srcPosMode|integer enum-like|no|no|How the source position is determined.|

## ADSB

## AIS

## Integers enum-like
- srcPosMode
    - 0 unknown
    - 1 manual
    - 2 gps_manual
    - 3 gps_auto
