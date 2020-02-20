"use strict"; // overcome current Chrome and Firefox issues with ECMA6 stuff like classes
/***********************************************************
 * Airsuck JS initiator
 * v. 0.1
 *
 * Licensed under GPL V3
 * https://github.com/ThreeSixes/airSuck
 *
 * Load required and optional JS files,
 * init JS main functions
 *
 * Deps: jquery
 **********************************************************/

/* exported vehicleTypes, vehicles */
/* global debug, socket, mapLoaded, vehExpireCheckInterval, expireVehicles */

/***************************************************
 * GLOBALS
 **************************************************/
var sidebarLoaded = false;
var vehicleTypes = []; // Array for registering vehicle types (AIS, ADSB)
var vehicles = []; // Main array holding vehicles - replacing vehData array with vehicle objects

/***************************************************
 * LOAD CONFIG OPTIONS AND HELPER SCRIPTS
 **************************************************/
$.getScript("/js/config.js")
    .done(function () {
        if (debug) {
            $('.msgBx').removeClass('dbgInactive').addClass('dbgActive');
        }
        // set the html object ID for sending on-screen debug and messages
        window.messageBx = 'message';

        // Initialize the logger
        Logger.useDefaults()
        if (debug) {
            Logger.setLevel(Logger.trace)
        } else {
            Logger.setLevel(Logger.error)
        }
        Logger.info('Configuration loaded.')
    })
    .fail(function (jqxhr, settings, exception) {
        console.log("ERROR: Cannot load configuration file", exception)
    });


// Initiate the WebSocket
window.socket = new Phoenix.Socket("/ws", {params: {}});
socket.connect();
window.vehiclesChannel = socket.channel("room:vehicles")

/***************************************************
 * SETUP AND LOAD VEHICLES
 **************************************************/
// load Vehicles early as the types are prerequisite to other files
// load the Vehicle class first
$.getScript("/js/vehicles/vehicle.js", function () {
    // Start the vehcile expiration routine which should be executed at the specified interval.
    window.setInterval(function () {
        // If our map has been loaded then we can start "expiring" vehicles.
        if (mapLoaded) {
            expireVehicles();
        }
    }, vehExpireCheckInterval);
    // Load any custom vehicles
    let index;
    for (index = 0; index < loadCustomVehicles.length; index++) {
        Logger.info('Loading custom vehicle: ' + loadCustomVehicles[index]);
        $.getScript("/js/vehicles/" + loadCustomVehicles[index]);
    }

    // Initialize the sidebar
    window.sidebar = L.control.sidebar('sidebar', {position: 'right'}).addTo(map);

    // Load the message handler
    $.getScript("/js/core/messages.js");
});

/***************************************************
 * SETUP AND LOAD MAPS
 **************************************************/
$(document).ready(function () {
    // Load RainbowVis to color vehicle paths by height
    $.getScript("/js/plugins/rainbowvis.js", function () {
        // Instanciate RainbowVis and set global color ramp by plane height
        window.polyRamp = new Rainbow();
        polyRamp.setNumberRange(minimumAltitude, maximumAltitude);
        polyRamp.setSpectrum(spectrum[0], spectrum[1], spectrum[2], spectrum[3]);
    });
    // Globals
    window.map = null;
    window.layers = null;
    window.mapLoaded = false;
    window.vehData = {}; // Create a generic array to hold our vehicle data
    $.getScript("/js/core/map_init.js", function () {
        initMap();
        Logger.info("Map initialized.")
    });
});