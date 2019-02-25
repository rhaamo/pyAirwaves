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

/* exported sidebarLoaded, vehicleTypes, vehicles */
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
});

// Initiate Socket.IO, it will connect back to the server automatically
window.socket = io();

function socketOk(msg) {
    $("#socket_state").removeClass().addClass(["fa", "fa-check icon-socket-ok"]).prop('title', msg);
    console.log("SocketIO OK: " + msg);
}

function socketNok(msg) {
    $("#socket_state").removeClass().addClass(["fa", "fa-close icon-socket-nok"]).prop('title', msg);
    console.log("SocketIO Err: " + msg);

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
        if (debug) {
            console.log('Loading custom vehicle: ' + loadCustomVehicles[index]);
        }
        $.getScript("static/js/vehicles/" + loadCustomVehicles[index]);
    }

    // Prevent race condition where sidebar loads before vehicle types finish registration.
    setTimeout(function () {
        // Load the message handler
        $.getScript("static/js/core/messages.js");

        // load sidebar (here so it loads in the right order...)
        $.getScript("static/js/core/sidebar.js", function () {
            // setup the sidebar on successful load
            setupSidebar();

            // load sidebar CSS
            $('<link/>', {
                rel: 'stylesheet',
                type: 'text/css',
                href: 'static/css/sidebar.css'
            }).appendTo('head');
        });
    }, 0.1);

});

/***************************************************
 * SETUP AND LOAD MAPS
 **************************************************/
$(document).ready(function () {
    console.log("Document ready.");
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