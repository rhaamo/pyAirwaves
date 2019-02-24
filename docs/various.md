# Various notes

From ADSB you get a Mode S identifier, like "0A008A", you can then get infos from:
- table aircraft_modes where mode_s="0A008A"
- table aircraft where icao=icao from aircraft_modes
- table aircraft_owner where registration=registration from aircraft_modes