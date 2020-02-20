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
 * LOAD CONFIG OPTIONS AND HELPER SCRIPTS
 **************************************************/
if (debug) {
    $('.msgBx').removeClass('dbgInactive').addClass('dbgActive');
}
// set the html object ID for sending on-screen debug and messages
window.messageBx = 'message';

// Initialize the logger
require('js-logger').useDefaults()
if (debug) {
    logger.setLevel(logger.trace)
} else {
    logger.setLevel(logger.error)
}
logger.info('Configuration loaded.')

// Initiate the WebSocket
window.socket = new WebSocket('ws://' + document.domain + ':' + location.port + '/ws');

function socketOk(msg) {
    $("#websocket-status").removeClass().addClass(["badge badge-pill", "badge-success"]).prop('title', msg);
    $("#websocket-status i").removeClass().addClass(["fa", "fa-check icon-socket-ok"]);
    logger.info("SocketIO OK: " + msg);
}

function socketNok(msg) {
    $("#websocket-status").removeClass().addClass(["badge badge-pill", "badge-success"]).prop('title', msg);
    $("#websocket-status i").removeClass().addClass(["fa", "fa-close icon-socket-nok"]);
    logger.info("SocketIO Err: " + msg);

}

socket.onopen = function(event) {
    socketOk("Websocket is connected");
};

socket.onclose = function(event) {
    socketNok("Websocket error", event);
};

socket.onerror = function(event) {
    socketNok("Websocket error", event);
};

/***************************************************
 * SETUP AND LOAD VEHICLES
 **************************************************/
// load Vehicles early as the types are prerequisite to other files
// load the Vehicle class first
// Start the vehcile expiration routine which should be executed at the specified interval.
window.setInterval(function () {
    // If our map has been loaded then we can start "expiring" vehicles.
    if (mapLoaded) {
        expireVehicles();
    }
}, vehExpireCheckInterval);
// Load any custom vehicles

// Initialize the sidebar
window.sidebar = L.control.sidebar('sidebar', {position: 'right'}).addTo(map);


/***************************************************
 * SETUP AND LOAD MAPS
 **************************************************/
// Instanciate RainbowVis and set global color ramp by plane height
window.polyRamp = new Rainbow();
polyRamp.setNumberRange(minimumAltitude, maximumAltitude);
polyRamp.setSpectrum(spectrum[0], spectrum[1], spectrum[2], spectrum[3]);

// Globals
window.map = null;
window.layers = null;
window.mapLoaded = false;
window.vehData = {}; // Create a generic array to hold our vehicle data

initMap();
