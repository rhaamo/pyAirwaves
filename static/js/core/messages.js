"use strict";// overcome current Chrome and Firefox issues with ECMA6 stuff like classes
/***********************************************************
 * Airsuck JS Socket Message Handler
 * v. 0.1
 *
 * Licensed under GPL V3
 * https://github.com/ThreeSixes/airSuck
 *
 * Handles socket.io messages for vehicle data coming from node
 *
 * Deps: jQuery, vehicles.js, leaflet maps initialized
 **********************************************************/

/***************************************************
 * SOCKET MESSAGE HANDLER
 **************************************************/

function handleMessage(msgJSON) {
    if (!mapLoaded) {
        // Return early - the map isn't loaded yet
        if (debug) {
            console.log("Maps not loaded. Discarding aircraft data.");
        }
        return;
    }
    if (!sidebarLoaded) {
        // Return early - the map isn't loaded yet
        if (debug) {
            console.log("Sidebar not loaded. Discarding aircraft data.");
        }
        return;
    }
    // Dump the JSON string to the message box.
    if (debug) {
        $('#' + messageBx).attr('value', JSON.stringify(msgJSON, null, 10));
    }

    // JSONify the JSON string.
    //let msgJSON = JSON.parse();

    // Return early - don't continue processing the keepalive.
    if ('keepalive' in msgJSON) {
        return;
    }

    // Store the vehicle name for reference in the function
    let vehName = "veh" + msgJSON.addr.toString();

    // See if we have a vehicle in our vehicle data.
    if (vehName in vehicles && vehicles[vehName] != null) {
        // existing vehicle, call the update function
        vehicles[vehName].update(msgJSON);
    } else {
        // new vehicle, call the constructor, create marker and set listeners
        let index;// we need an index to manually traverse the vehicleTypes associative array
        let length = vehicleTypes.length;
        for (index = 0; index < length; ++index) {

            console.log('msgJson: ');
            console.log(msgJSON);
            console.log('msgJson END');
            if (msgJSON.type === vehicleTypes[index].protocol) {
                if (debug) {
                    console.log('New vehicle found, type registered: ' + msgJSON.type);
                }
                // add the new vehicle (constructor should call registered update functions)
                vehicles[vehName] = vehicleTypes[index].constructor(msgJSON);
                console.log('vehicles vehName: ');
                console.log(vehicles[vehName]);
                console.log('vehicles vehName END');

                // Add marker and listeners only if we have a Latitude and Longitude
                // Cannot create a marker without geoposition datas
                if (vehicles[vehName].lat && vehicles[vehName].lon) {
                    console.log("we have a lat lon for: " + vehicles[vehName].addr);

                    // create a marker icon for the vehicle (may move to the constructor)
                    vehicles[vehName].setMarker();

                    // Add listeners to marker - must be here to access the vehicles array
                    vehicles[vehName].marker.on('click', function () {
                        vehicleMarkerClickListener(vehName);
                    });
                    vehicles[vehName].marker.on('contextmenu', function () {
                        vehicleMarkerRightClickListener(vehName);
                        return false; // cancel browser context menu popup
                    });
                } else {
                    //debugger;
                    if (debug) {
                        console.log('handleMessage: No Lat/Lon available for: ' + vehicles[vehName].addr);
                    }
                }
                break;
            } else if (index === length) {
                // vehicle type not registered, drop data
                if (debug) {
                    console.log('New vehicle found, type not registered: ' + msgJSON.type + ' Dropping data.')
                }
            }
        }
    }
}

// Register the message handler
socket.on('message', handleMessage);