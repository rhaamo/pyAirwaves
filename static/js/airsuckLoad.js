"use strict";// overcome current Chrome and Firefox issues with ECMA6 stuff like classes
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


/***************************************************
 * GLOBALS
 **************************************************/
var sidebarLoaded = false;

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

// Load Socket.IO
$.getScript("static/js/socket.io.js", function () {
    window.socket = io();
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

            // load font-awesome for icons
            $('<link/>', {
                rel: 'stylesheet',
                type: 'text/css',
                href: 'static/css/font-awesome/css/font-awesome.min.css'
            }).appendTo('head');

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