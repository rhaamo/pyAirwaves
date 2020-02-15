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
var vehicleTypes = []; // Array for registering vehicle types (AIS, SSR)
var vehicles = []; // Main array holding vehicles - replacing vehData array with vehicle objects

/***************************************************
 * LOAD CONFIG OPTIONS AND HELPER SCRIPTS
 **************************************************/
$.getScript("static/js/config.js", function () {
    if (debug) {
        $('.msgBx').addClass('dbgActive');
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
});


// Initiate Socket.IO, it will connect back to the server automatically
window.socket = io();

function socketOk(msg) {
    $("#websocket-status").removeClass().addClass(["badge badge-pill", "badge-success"]).prop('title', msg);
    $("#websocket-status i").removeClass().addClass(["fa", "fa-check icon-socket-ok"]);
    Logger.info("SocketIO OK: " + msg);
}

function socketNok(msg) {
    $("#websocket-status").removeClass().addClass(["badge badge-pill", "badge-success"]).prop('title', msg);
    $("#websocket-status i").removeClass().addClass(["fa", "fa-close icon-socket-nok"]);
    Logger.info("SocketIO Err: " + msg);

}

// Error handling
// https://socket.io/docs/client-api/#Event-%E2%80%98connect%E2%80%99
socket.on('connect', function () {
    socketOk("Websocket is connected");
});
socket.on('connect_error', function (error) {
    socketNok("Websocket error", error);
});

/***************************************************
 * SETUP AND LOAD VEHICLES
 **************************************************/
// load Vehicles early as the types are prerequisite to other files
// load the Vehicle class first
$.getScript("static/js/vehicles/vehicle.js", function () {
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
        $.getScript("static/js/vehicles/" + loadCustomVehicles[index]);
    }

    // Initialize the sidebar
    window.sidebar = L.control.sidebar('sidebar', {position: 'right'}).addTo(map);

    // Load the message handler
    $.getScript("static/js/core/messages.js");
});

/***************************************************
 * SETUP AND LOAD MAPS
 **************************************************/
$(document).ready(function () {
    // Load RainbowVis to color vehicle paths by height
    $.getScript("static/js/plugins/rainbowvis.js", function () {
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
    $.getScript("static/js/core/map_init.js", function () {
        initMap();
    });
});