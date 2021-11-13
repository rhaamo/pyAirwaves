# pyAirwaves, realtime planes and boats display on map with rtl-sdr

<a href="https://dronegh.sigpipe.me/rhaamo/pyAirwaves"><img src="https://dronegh.sigpipe.me/api/badges/rhaamo/pyAirwaves/status.svg" alt="Build Status"/></a>
<a href="https://github.com/rhaamo/pyAirwaves/blob/master/LICENSE"><img src="https://img.shields.io/badge/license-AGPL3-green.svg"/></a>
<img src="https://img.shields.io/badge/python-%3E%3D3.6-blue.svg"/> <img src="https://img.shields.io/badge/elixir-1.5%2B-blue" />

## Screenshot
  <img src="https://raw.githubusercontent.com/rhaamo/pyAirwaves/master/screenshot.png" alt="screenshow" width="800px">

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
- elixir >= 1.5
- at least 5G of disk space on the server running nginx (tile caching)
- an ADSB source (dump1090)
- an AIS source (rtl-ais)


## Setup

See `docs/install.md`

Daemons/scripts:
- `airwaves_adsb_client.py` will connect to dump1090
- `airwaves_ais_client.py` will connect to rtl-ais
- `simulator_adsb_real_datas.py` instead of connecting to a remote dump1090, it will replay 15minutes of ADS-B datas
- `simulator_adsb_coordinates.py` instead of connecting to a remote dump1090, it will replay three planes looping somewhere in the USA
- `simulator_ais_real_datas.py` instead of connecting to a remote rtl-ais, it will replay a few minutes of AIS datas
- `installation/*.service` systemd services files for the daemons and production server

## Docs

Various docs can be found in the `docs/` folder.

## Contact

Dashie <dashie@sigpipe.me>