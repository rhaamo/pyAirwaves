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
    Logger.info("Initializing maps...");

    // Attempt to detect user location if turned on
    if (useLocation) {
        if ("geolocation" in navigator) {
            // We can use it
            navigator.geolocation.getCurrentPosition(function (position) {
                window.defautLng = position.coords.longitude;
                window.defaultLat = position.coords.latitude;
                Logger.info("GeoLocation authorized, coords used.");
            }, function (error) {
                if (error.code === error.PERMISSION_DENIED) {
                    Logger.error("GeoLocation denied, defaulting to server's one.");
                }
            });
        } else {
            Logger.info("GeoLocation deactivated, defaulting to server's one.");
        }
    }

    // Setup layers
    if (mapUsesLocalCache === false) {
        Logger.info('Using RRZE tile server directly.');
        var rrzeUrl = 'https://osm.rrze.fau.de/osmhd';
    } else {
        Logger.info('Using RRZE tile server through local cache.');
        var rrzeUrl = '/cache/tiles/rrze/osmhd';
    }
    let layerRrze = L.tileLayer(rrzeUrl + '/{z}/{x}/{y}.png', {
        attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors and <a href="https://osm.rrze.fau.de/">RRZE Tile Server</a'
    })
    let baseLayers = {
        "OpenStreetMap": layerRrze,
        "Esri World Imagery": L.tileLayer.provider('Esri.WorldImagery'),
        "OpenTopo (non-hd)": L.tileLayer.provider('OpenTopoMap'),
        "Stamen Terrain": L.tileLayer.provider('Stamen.Terrain'),
        "Esri Ocean Basemap (non-hd)": L.tileLayer.provider('Esri.OceanBasemap')
    };

    let overlaysLayers = {
        "OpenSeaMap": L.tileLayer.provider('OpenSeaMap')
    };

    window.layers = Object.assign({}, baseLayers, overlaysLayers);

    // Set up the map object.
    window.map = new L.Map(document.getElementById('map'), {zoomControl: false}).setView([defaultLat, defaultLng], defaultZoom);
    map.addLayer(layers["OpenStreetMap"]);
    map.addLayer(layers["OpenSeaMap"]);

    // Add layers control
    L.control.layers(baseLayers, overlaysLayers).addTo(map);

    // Add a scale on bottom left
    L.control.scale().addTo(map);

    // Handle a dynamic hash in URL for hotlinking
    window.hash = new L.Hash(map);

    // Location Controller
    window.positioncontrol = L.control.locate({
		position: 'topleft',
		showCompass: true,
		strings: {title: "Show my location"},
		icon: 'fa fa-map-marker',
        locateOptions: {enableHighAccuracy: true},
        keepCurrentZoomLevel: true,
        returnToPrevBounds: true,
	}).addTo(map);

    var htmlObject = positioncontrol.getContainer();
	var a = document.getElementById('LocateMe')
	function setParent(el, newParent){
		newParent.appendChild(el);
	}
    setParent(htmlObject, a);
    $('div.leaflet-control-locate').removeClass('leaflet-bar');


    // L.Terminator (greyline)
    var t = L.terminator();
    setInterval(function(){updateTerminator(t)}, 1000);

    function updateTerminator(t) {
        var check = $('input#toggleGreyline').is(':checked');
        if (!check) {
            return;
        }
        var t2 = L.terminator();
        t.setLatLngs(t2.getLatLngs());
        t.redraw();
    }

    $('input#toggleGreyline').change(function() {
        var checked = this.checked;
        if (checked) {
            t.addTo(map);
            Logger.info("Added greyline");
        } else {
            map.removeLayer(t);
            Logger.info("Removed greyline");
        }
    })

    // The map loaded.
    window.mapLoaded = true;
}

function zoomIn() {
    map.zoomIn(1)
}

function zoomOut() {
    map.zoomOut(1)
}