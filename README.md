# pyAirwaves

## Licensing

This project is licensed under AGPL v3, except a few files in `js` and `css` which are GPL v3 from AirSuck project.

## Infos

This project use the [AirSuck](https://github.com/ThreeSixes/airSuck) frontend for which I already did a conversion to Leaflets.

I rewrote my own backend because I feels the one from AirSuck is super messy.

## Requirements
- redis server
- postgresql >= 10 (should work with lower but you are on your own)
- python >= 3.6

## Setup

```
git clone https://github.com/rhaamo/pyAirwaves
cd pyAirwaves
pip install --user -r requirements.txt
cp config.py.sample config.py
$EDITOR config.py
$EDITOR static/js/config.js
createdb ...
flask db upgrade
flask import_aircrafts
flask update_db
```

Daemons/scripts:
- `python airwaves_adsb_client.py` will connect to dump1090 and rtl-ais
- `simulator.py` instead of connecting to a remote dump1090, it will replay 15minutes of ADS-B datas
- `python app.py` will start the Flask-SocketIO server

## Docs

Various docs can be found in the `docs/` folder.

## Contact

Dashie <dashie@sigpipe.me>