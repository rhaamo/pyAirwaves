"use strict"; // overcome current Chrome and Firefox issues with ECMA6 stuff like classes
/***********************************************************
 * Airsuck Maps system setup
 * v. 0.1
 *
 * Licensed under GPL V3
 * https://github.com/ThreeSixes/airSuck
 *
 * Deps: jQuery, Leaflet JS API loaded
 **********************************************************/

/* global defaultLat, defaultLng, defaultZoom, map, layers */

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
        if ("geolocation" in navigator) {
            // We can use it
            navigator.geolocation.getCurrentPosition(function (position) {
                window.defautLng = position.coords.longitude;
                window.defaultLat = position.coords.latitude;
                console.log("GeoLocation authorized, coords used.");
            }, function (error) {
                if (error.code === error.PERMISSION_DENIED) {
                    console.log("GeoLocation denied, defaulting to server's one.");
                }
            });
        } else {
            console.log("GeoLocation deactivated, defaulting to server's one.");
        }
    }

    // Setup layers
    let baseLayers = {
        "OpenStreetMap": L.tileLayer.provider('OpenStreetMap.Mapnik'),
        "Esri World Imagery": L.tileLayer.provider('Esri.WorldImagery'),
        "OpenTopo": L.tileLayer.provider('OpenTopoMap'),
        "Stamen Terrain": L.tileLayer.provider('Stamen.Terrain'),
        "Esri Ocean Basemap": L.tileLayer.provider('Esri.OceanBasemap')
    };

    let overlaysLayers = {
        "OpenSeaMap": L.tileLayer.provider('OpenSeaMap')
    };

    window.layers = Object.assign({}, baseLayers, overlaysLayers);

    // Set up the map object.
    window.map = new L.Map(document.getElementById('map')).setView([defaultLat, defaultLng], defaultZoom);
    map.addLayer(layers["OpenStreetMap"]);
    map.addLayer(layers["OpenSeaMap"]);

    // Add layers control
    L.control.layers(baseLayers, overlaysLayers).addTo(map);

    // The map loaded.
    window.mapLoaded = true;
}