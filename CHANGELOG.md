# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

## [Unreleased]
### Added
- AIS Support
- A bunch of missing indexes
- Help in top left header

### Changed
- **Breaking:** Services files now uses gunicorn for production, please update according to `installation/pyairwaves-*.service` and `installation/nginx.conf`
- Javascript libraries updated
- Maps changed from B&W OSM to only OSM ones plus ESRI World View
- Cleanup some unused python libs
- airSSR & airAIS, headings etc. are now fixed to two decimals
- Resized down the boat icon
- Plane icon is now on coordinates instead of aside
- Markers trail is now hiden by default
- Canvas bounding box of Plane and Boat have been reduced to bigger-length of extremities of the icon plus a small margin

### Fixed
- Debug/console.log cleanups
- lastClientName and lastSrc report properly
- shipTypeMeta now reported