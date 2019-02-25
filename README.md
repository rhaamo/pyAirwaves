# pyAirwaves, realtime planes and boats display on map with rtl-sdr

<a href="https://dronegh.sigpipe.me/rhaamo/pyAirwaves"><img src="https://dronegh.sigpipe.me/api/badges/rhaamo/pyAirwaves/status.svg" alt="Build Status"/></a>
<a href="https://github.com/rhaamo/pyAirwaves/blob/master/LICENSE"><img src="https://img.shields.io/badge/license-AGPL3-green.svg"/></a>
<img src="https://img.shields.io/badge/python-%3E%3D3.6-blue.svg"/> [![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)

## Licensing

This project is licensed under AGPL v3, except a few files in `js` and `css` which are GPL v3 from AirSuck project.
See `LICENSE.other` file.

## What is it

This project use the [AirSuck](https://github.com/ThreeSixes/airSuck) frontend with new features, improvements and uses Leaflets maps.

The entire backend haven't been kept and then entirely write from scratch.

pyAirwaves will use `dump1090` and `rtl-ais` daemons to send real-time display of airplanes and boards to a maps for display.

Some more features will be available like airplane picture, company, and statistics.

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