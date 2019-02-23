"use strict";// overcome current Chrome and Firefox issues with ECMA6 stuff like classes
/***********************************************************
 * Airsuck Maps system setup
 * v. 0.1
 *
 * Licensed under GPL V3
 * https://github.com/ThreeSixes/airSuck
 *
 * Deps: jQuery, Leaflet JS API loaded
 **********************************************************/

/***************************************************
 * INITIALIZE MAPS
 * Using Leaflet, no Google Map available
 **************************************************/
// Initialize the map.
function initMap() {
    if (debug) {
        console.log("Maps loading...");
    }

    // Attempt to detect user location if turned on
    if (useLocation) {
        $.ajax({
            url: 'https://freegeoip.live/json/', type: 'POST', dataType: 'jsonp',
            success: function (location) {
                // update the lat and lng if we can detect them
                defaultLng = location.longitude;
                defaultLat = location.latitude;
                if (debug) {
                    console.log("Got lat/lng: " + defaultLat + ", " + defaultLng);
                }
            }
        });
    }

    // Setup layers
    let baseLayers = {
        "Black and White": L.tileLayer.provider("OpenStreetMap.BlackAndWhite"),
        "OpenStreetMap": L.tileLayer.provider('OpenStreetMap.Mapnik'),
        "OpenTopo": L.tileLayer.provider('OpenTopoMap'),
        "Stamen Terrain": L.tileLayer.provider('Stamen.Terrain'),
        "Esri Ocean Basemap": L.tileLayer.provider('Esri.OceanBasemap')
    };

    let overlaysLayers = {
        "OpenSeaMap": L.tileLayer.provider('OpenSeaMap')
    };

    layers = Object.assign({}, baseLayers, overlaysLayers);

    // Set up the map object.
    map = new L.Map(document.getElementById('map')).setView([defaultLat, defaultLng], defaultZoom);
    map.addLayer(layers["Black and White"]);
    map.addLayer(layers["OpenSeaMap"]);

    // Add layers control
    L.control.layers(baseLayers, overlaysLayers).addTo(map);

    // The map loaded.
    mapLoaded = true;
}
