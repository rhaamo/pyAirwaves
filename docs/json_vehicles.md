# JSON Vehicles structure

The best way to see what's supported in the structure is to look at `libPyairwaves/structs.py`.

A table with relation between what the frontend uses vs the structure will be added later.

## Examples

### AIS
First packet is a "small" normal one, basically position report, the second one is a reassembled fragmented one with more data (ship name, destination, etc.)

```json
{
    'type' : 'airAIS',
    'entryPoint' : 'airwaves_ais_client',
    'dataOrigin' : 'rtl-ais',
    'dts' : '2020-02-22 07:15:43.874604',
    'src' : 'potato',
    'lastSrc' : 'potato',
    'isAssembled' : False,
    'lon' : 0.11315333333333333,
    'lat' : 49.48415,
    'heading' : 511,
    'turnRt' : -128,
    'addr' : 227485930,
    'mmsi' : 227485930,
    'posAcc' : False,
    'raim' : False,
    'radioStatus' : 49212,
    'mmsiType' : 'Ship',
    'mmsiCC' : 'FR',
    'clientName' : 'xxx',
    'lastClientName' : 'xxx',
    'raw' : '!AIVDM,1,1,,B,13Ht`rPP0000Q9`LD:NP0?wF0<0t,0*5B',
    'payload' : '13Ht`rPP0000Q9`LD:NP0?wF0<0t',
    'srcPos' : False
}

{
    'type' : 'airAIS',
    'entryPoint' : 'airwaves_ais_client',
    'dataOrigin' : 'rtl-ais',
    'dts' : '2020-02-22 07:15:43.365528',
    'src' : 'potato',
    'lastSrc' : 'potato',
    'isAssembled' : True,
    'addr' : 538004456,
    'mmsi' : 538004456,
    'mmsiType' : 'Ship',
    'mmsiCC' : 'MH',
    'destination' : 'RUEN FRANCE',
    'callsign' : 'V7XD9',
    'epfdMeta' : 'GPS',
    'dimToBow' : 152,
    'dimToStern' : 29,
    'dimToPort' : 10,
    'dimToStarboard' : 20,
    'draught' : 6.0,
    'shipTypeMeta' : 'Cargo',
    'clientName' : 'xxx',
    'lastClientName' : 'xxx',
    'raw' : '!AIVDM,2,1,0,A,5815;r02@h3qKMPCV21<4TqB0@TlUA8Tu>222216C0M:D4bB0?4UAC`1TPCP,0*10!AIVDM,2,2,0,A,iH888888880,2*05',
    'payload' : '5815;r02@h3qKMPCV21<4TqB0@TlUA8Tu>222216C0M:D4bB0?4UAC`1TPCPiH888888880',
    'srcPos' : False,
    'name' : 'SAINT DIMITRIOS'
}```

### ADSB
ADSB broadcasts only one kind of packet, but the structure contains more data, fetched from the database.
```json
{
    type': 'airADSB',
    'addr': 'AB6851', 
    'idInfo': '@@@@@@@@', 
    'aSquawk': None, 
    'alt': 35000, 
    'lon': 1.86366, 
    'lat': 49.22859, 
    'entryPoint': 
    'airwaves_adsb_client', 
    'dataOrigin': 'dump1090', 
    'dts': '2020-02-22 07:14:11.104637', 
    'src': 'potato', 
    'lastSrc': 'potato', 
    'data': 'MSG,3,1,1,AB6851,1,2020/02/22,08:14:11.069,2020/02/22,08:14:11.104,,35000,,,49.22859,1.86366,,,0,,0,0', 
    'clientName': 'patate', 
    'lastClientName': 'patate', 
    'srcPos': False, 
    'srcLat': None, 
    'srcLon': None, 
    'srcPosMeta': None, 
    'vertStat': 'air', 
    'vertRate': None, 
    'category': None, 
    'icaoAACC': None, 
    'velo': None, 
    'heading': None, 
    'supersonic': None
    }
```