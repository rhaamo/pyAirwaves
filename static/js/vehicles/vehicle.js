"use strict"; // overcome current Chrome and Firefox issues with ECMA6 stuff like classes
/***********************************************************
 * Airsuck JS vehicle-specific functions
 * v. 0.1
 *
 * Licensed under GPL V3
 * https://github.com/ThreeSixes/airSuck
 *
 * Vehicle class prototype definition and functions, some
 * to be replaced by custom vehicle types
 *
 * Deps: jQuery
 **********************************************************/

/***************************************************
 * VEHICLE EXPIRATION LOOP
 **************************************************/
// Expire vehicles.
function expireVehicles() {
    if (debug) {
        console.log("Expiration check running");
    }
    let key;
    for (key in vehicles) {
        // Get the state of the vehicle and take appropriate action
        // Don't run the check on nulled objects because JS ECMAScript 6 doesn't allow delete...
        if (vehicles[key] != null) {
            switch (vehicles[key].checkExpiration()) {
                case 'Halflife':
                    if (debug) {
                        console.log('Halflife determined for vehicle: ' + vehicles[key].parseName());
                    }
                    // Set halflife mode.
                    vehicles[key].setHalflife();
                    break;
                case 'Expired':
                    if (debug) {
                        console.log('Expiration determined for vehicle: ' + vehicles[key].parseName());
                    }
                    // Vehicle expired, cleanup the vehicles things...
                    vehicles[key].destroy();
                    // Nullify the entry since ECMAScript 6 doesn't let us use destroy
                    vehicles[key] = null;
                    break;
                default:
                    // Do nothing on active or other
                    break;
            }
        }
    }
}

/***************************************************
 * CLICK LISTENERS
 **************************************************/

function vehicleMarkerRightClickListener(vehName) {
    // Listener called from messages.js for access to vehicles array
    // Check to see if the path is visible and reverse the visiblity
    if (map.hasLayer(vehicles[vehName].pathPoly) === true) {
        map.removeLayer(vehicles[vehName].pathPoly);
    } else {
        map.addLayer(vehicles[vehName].pathPoly);
    }
}

function vehicleMarkerClickListener(vehName) {
    // Listener called from messages.js for access to vehicles array

    // Info window functions, check if open and toggle
    if (vehicles[vehName].info.shown) {
        // Close it.
        vehicles[vehName].info.setContent("");
        map.removeLayer(vehicles[vehName].info);
        vehicles[vehName].info.shown = false;
        // Hide the sidebar details
        $('#' + vehicles[vehName].addr + '-row-detail').toggle();
    } else {
        // Set data in case we don't have it, open it, and flag it as open.
        vehicles[vehName].info.setContent(vehicles[vehName].setInfoWindow());
        vehicles[vehName].info.addTo(map);
        vehicles[vehName].info.shown = true;
        // Show the sidebar details
        $('#' + vehicles[vehName].addr + '-row-detail').toggle();
    }
}

function vehicleTableRowClickListener(vehName) {
    // check the string for validity
    if (vehName === 'undefined') {
        if (debug) {
            console.log('Error: ID passed to vehicleTableRowClickListener is invalid.');
        }
        return false;
    } else if (vehName.substring(0, 2) !== 'veh') {
        vehName = 'veh' + vehName; //missing veh at the beginning, add
    }
    if (debug) {
        console.log('Changing marker for: ' + vehName);
    }
    vehicles[vehName].setMarkerSelected();
}

/***************************************************
 * MISC HELPERS
 **************************************************/

// Converts a heading from degrees to a cardinal direction, 16 settings
function degreeToCardinal(degree) {
    let bearing;
    //determing the relevant bearing
    bearing = Math.round(degree / (360 / 16));
    // return the relevant cardinal bearing
    switch (bearing) {
        case 0:
            return 'N';
        case 1:
            return 'NNE';
        case 2:
            return 'NE';
        case 3:
            return 'ENE';
        case 4:
            return 'E';
        case 5:
            return 'ESE';
        case 6:
            return 'SE';
        case 7:
            return 'SSE';
        case 8:
            return 'S';
        case 9:
            return 'SSW';
        case 10:
            return 'SW';
        case 11:
            return 'WSW';
        case 12:
            return 'W';
        case 13:
            return 'WNW';
        case 14:
            return 'NW';
        case 15:
            return 'NNW';
        case 16:
            return 'N';
        default:
            if (debug) {
                console.log('degreeToBearing: error in calculating bearing');
            }
            return null;
    }
}

/***************************************************
 * VEHICLE PROTOTYPE
 **************************************************/

class Vehicle {
    constructor(msgJSON, protocol) {
        if (debug) {
            console.log('Vehicle constructor executed for vehicle: ' + msgJSON.addr + ', Using protocol: ' + protocol);
        }
        this.spinState = 0; // This is just for tracking the spinner animation state.
        this.addr = msgJSON.addr;
        this.protocol = protocol; // communications protocol used (AIS,SSR)
        this.lastPos = "none";
        this.lastUpdate = new Date().getTime();
        this.active = true; // set true if the vehicle is currently active
        this.selected = false; // records whether the vehicle has been selected in the sidebar or by clicking the icon
        this.maxAge = 1000; // default vehicle expiration time in milliseconds since last contact
        // gMap icon stuff
        this.dirIcoPath = "m 0,0 -20,50 20,-20 20,20 -20,-50"; // Path we want to use for ADS-B targets we have direction data for.
        this.dirIcoScale = 0.15; // Current scale of the path
        this.dirIcoDefaultScale = 0.15; // Default scale of the path
        this.ndIcoPath = "m 15,15 a 15,15 0 1 1 -30,0 15,15 0 1 1 30,0 z"; // Path we want to sue for ADS-B targets we don't have direction data for.
        this.ndIcoScale = 0.24; // Current scale of the path.
        this.ndIcoDefaultScale = 0.24; // Default scale of the path.
        this.vehColorActive = "#ff0000"; // Color of active vehicle icons (hex)
        this.vehColorInactive = "#660000"; // Color of nonresponsive vehicle icons (hex)
        this.vehColorSelected = "#ff00ff"; // Color of the vehicle icon when selected
        this.marker = null; // Placeholder for the map marker
        this.info = null; // Placeholder for the map info popup
        this.pathPoly = new L.polyline([]).addTo(map);
    }
}

/***************************************************
 * DEFAULT FUNCTION DETERMINES VEHICLE NAME
 * TO BE OVERRIDEN BY CUSTOM VEHICLES
 **************************************************/
Vehicle.prototype.parseName = function () {
    // default vehicle name function, to be customized per vehicle type
    return this.addr.toUpperCase();
};

/*
 * Vehicle 'PLANE' icon definition
 */
Vehicle.prototype.drawPlane = function (icon, type) {
    if (type === 'icon') {
        let ctx = icon.getContext('2d');
        ctx.beginPath();
        ctx.moveTo(109.375000, 307.375000);
        ctx.lineTo(109.375000, 279.375000);
        ctx.lineTo(139.375000, 255.375000);
        ctx.lineTo(139.375000, 183.375000);
        ctx.lineTo(6.375000, 227.375000);
        ctx.lineTo(6.375000, 192.375000);
        ctx.lineTo(138.375000, 112.375000);
        ctx.lineTo(138.375000, 14.375000);
        ctx.bezierCurveTo(138.375000, -6.625000, 172.375000, -6.625000, 172.375000, 14.375000);
        ctx.lineTo(172.375000, 112.375000);
        ctx.lineTo(306.375000, 192.375000);
        ctx.lineTo(306.375000, 227.375000);
        ctx.lineTo(173.375000, 184.375000);
        ctx.lineTo(173.375000, 255.375000);
        ctx.lineTo(203.375000, 279.375000);
        ctx.lineTo(203.375000, 307.375000);
        ctx.lineTo(156.375000, 292.375000);
    }

};

/***************************************************
 * FUNCTION CREATES VEHICLE ICONS FOR GMAPS
 * OVERRIDE IF USING A DIFFERENT HEADING
 **************************************************/
Vehicle.prototype.createIcon = function () {
    var newIcon;
    // If we have heading data for the vehicle
    if (this.heading) {
        // Create our icon for a vehicle with heading data.
        //newIcon = new google.maps.Marker({
        //  path: this.dirIcoPath,
        //  scale: this.dirIcoScale,
        //  strokeWeight: 1.5,
        //  strokeColor: (this.selected == true) ? this.vehColorSelected : ((this.active == true) ? this.vehColorActive : this.vehColorInactive),
        //  rotation: this.heading
        //});
        console.log("TODO: heading");
        newIcon = new L.PlaneIcon({
            color: '#f4ff01',
            idleCircle: false,
            course: this.heading
        });
        newIcon.setHeading(this.heading);
    } else {
        // Create our icon for a vehicle without heading data.
        //newIcon = new google.maps.Marker({
        //  path: this.ndIcoPath,
        //  scale: this.ndIcoScale,
        //  strokeWeight: 1.5,
        //  strokeColor: (this.selected == true) ? this.vehColorSelected : ((this.active == true) ? this.vehColorActive : this.vehColorInactive)
        //});
        console.log("TODO: no heading");
        newIcon = new L.PlaneIcon({
            color: '#f4ff01',
            idleCircle: false
        });
    }
    // And return it.
    return newIcon;
};

/***************************************************
 * FUNCTION ADDS A GMAPS MARKER TO THE VEHICLE
 **************************************************/
Vehicle.prototype.setMarker = function () {
    // Create our marker.
    console.log("Asked creating a marker for: " + this.addr);
    console.log("TODO4 also set icon: .setIcon()");
    this.marker = new L.marker(new L.LatLng(this.lat, this.lon), {
        vehName: this.addr,
        icon: this.createIcon()
    }).addTo(map);

    // Create our info window
    this.setInfoWindow();

    // Can't set the listeners here, scoping doesn't allow
    // access to the vehicles array.
};

/***************************************************
 * FUNCTION CREATES VEHICLE ICONS FOR GMAPS
 * SPECIFICALLY ENLARGES THE ICON WHEN SELECTED
 **************************************************/
Vehicle.prototype.setMarkerSelected = function () {
    // set the selected flag
    this.selected = true;
    // enlarge the icon
    this.dirIcoScale = this.dirIcoScale * 1.5;
    this.ndIcoScale = this.ndIcoScale * 1.5;

    // use the move function to update the icon
    this.movePosition();
};
Vehicle.prototype.setMarkerHover = function () {
    // set the selected flag
    this.selected = true;
    // use the move function to update the icon
    this.movePosition();
};
Vehicle.prototype.setMarkerUnselected = function () {
    // set the selected flag
    this.selected = false;
    // shrink the icon
    this.dirIcoScale = this.dirIcoDefaultScale;
    this.ndIcoScale = this.ndIcoDefaultScale;

    // use the move function to update the icon
    this.movePosition();
};

/***************************************************
 * FUNCTION MOVES THE VEHICLE MARKER AND INFO POSITIONS
 **************************************************/
Vehicle.prototype.movePosition = function () {
    console.log(this);

    // We can do this only if we have a non-null non-undefined lat and lon
    if (this.lat && this.lon) {
        console.log(this);
        // Figure out where we are in 2D space
        let thisPos = this.lat + "," + this.lon;
        // Update the path object with the new position
        // copy the path object
        let pathObject = this.pathPoly.getLatLngs();
        // update with the new path
        pathObject.push(new L.LatLng(this.lat, this.lon));
        // push back to the polyline
        this.pathPoly.setLatLngs(pathObject);
        // set the polyline color
        this.pathPoly.setStyle({
            color: this.stkColor
        });

        // Update the marker
        // Modify the icon to have the correct rotation, and to indicate there is bearing data.
        console.log("TODO FIXME set icon w/ bearing rotation");
        console.log(this.marker);
        console.log(this);
        this.marker.setIcon(this.createIcon());
        // Move the marker.
        this.marker.setLatLng(new L.LatLng(this.lat, this.lon));

        // also update popup info if opened
        if (this.info.shown === true) {
            this.info.setLatLng(new L.LatLng(this.lat, this.lon));
            this.info.update();
        }

        // Record the new position for testing on next update
        this.lastPos = thisPos;
    } else {
        if (debug) {
            console.log("movePosition: Cannot move marker without lat/lon for: " + this.addr);
        }
    }
};

/***************************************************
 * FUNCTION ADDS A MAPS INFO WINDOW TO THE VEHICLE
 **************************************************/
Vehicle.prototype.setInfoWindow = function () {
    // Create our info window.
    this.info = new L.popup({
        shown: false,
        offset: new L.point(0, -35) // Add little offset to be on top of the marker icon
    }).setLatLng(new L.LatLng(this.lat, this.lon)).setContent(this.parseName());
};

/***************************************************
 * FUNCTIONS UPDATE THE VEHICLE INFO AND TABLE ENTRY
 * updateTableEntry function to be overridden by
 * custom vehicle types
 **************************************************/
Vehicle.prototype.updateTableEntry = function () {
    if (debug) {
        console.log('Error: Function updateTableEntry not set for protocol: ' + this.protocol);
    }
};

Vehicle.prototype.update = function (msgJSON) {
    // update data in the object
    $.extend(true, this, msgJSON);
    // if not set to active, reactivate
    if (this.active === false) {
        this.active = true;
        // Reset so the counter bounces up to 1.
        this.spinState = 0;
    }

    // Handle the animation. If the state is lower than the length.
    if (this.spinState < (spinnerAnim.length - 2)) {
        // Increment the animation counter.
        this.spinState++;
    } else if (this.spinState === (spinnerAnim.length - 2)) {
        // Reset counter at 1. We do this to make sure we have > 1 frame from the target.
        this.spinState = 1;
    }

    // update the last update parameter
    this.lastUpdate = Date.now();
    // update the vehicle entry in its' table
    this.updateTableEntry();
    // move the maps position
    this.movePosition();
};

/***************************************************
 * SUPPORT ZERO-FILLING NUMBERS. THIS CAN OR SHOULD
 * BE MOVED EVENTUALLY TO A BETTER PLACE.
 **************************************************/
Vehicle.prototype.zerofill = function (number, numberOfDigits) {
    // Set return value.
    var retVal = number.toString();
    // Figure out the length of the number in digits.
    var numLen = retVal.length;

    // Figure out the minimum size of the number.
    if (numLen < numberOfDigits) {
        // Add zeros.
        for (var i = 0; i < (numberOfDigits - numLen); i++) {
            // Prepend a string zero.
            retVal = "0" + retVal;
        }
    }

    return retVal;
};

/***************************************************
 * VEHICLE DESTRUCTOR
 **************************************************/
Vehicle.prototype.destroy = function () {
    if (debug) {
        console.log('Destroying vehicle: ' + this.parseName());
    }

    // Remove table entries
    $('#' + this.addr + '-row-summary').remove();
    $('#' + this.addr + '-row-detail').remove();

    // Default destructor processes
    if (this.info !== null) {
        map.removeLayer(this.info);
    }

    if (map.hasLayer(this.pathPoly)) {
        map.removeLayer(this.pathPoly);
    }

    if (map.hasLayer(this.marker)) {
        map.removeLayer(this.marker);
    }
    //vehicles[this.addr] = null;// invalidate this object, can't fully delete since its gone in ECMAScript 6...
};

/***************************************************
 * FUNCTION SETS THE ICON TO HALFLIFE, SETS INACTIVE
 **************************************************/
Vehicle.prototype.setHalflife = function () {
    // Deactivate vehicle and change the icon for it.
    this.active = false;
    // Set the icon.
    console.log("TODO FIXME set icon for idle / greyed");
    if (this.marker) {
        this.marker.setIcon(this.createIcon());
    }
};

/***************************************************
 * FUNCTION DETERMINES IF A VEHICLE SHOULD BE
 * SET TO HALFLIFE, EXPIRED, OR REMAIN ACTIVE
 **************************************************/
Vehicle.prototype.checkExpiration = function () {
    // Compute the time delta
    let vehDelta = Date.now() - this.lastUpdate;
    // Return Active, Halflife, or Expired
    if (vehDelta >= this.maxAge) {
        return ('Expired');
    } else if ((vehDelta >= (this.maxAge / 2)) && (this.active === true)) {
        // Set to inactive animation.
        this.spinState = spinnerAnim.length - 1;
        return ('Halflife');
    } else {
        return ('Active');
    }
};

/***************************************************
 * VEHICLE TYPE REGISTRATION
 * CUSTOM VEHICLES NEED TO REGISTER USING THIS FUNCTION
 **************************************************/
// Function to register new vehicle types
function registerVehicleType(newProtocol, newDomName, newFaIcon, newConstructor, newTableHeader) {
    // TO DO: validate input
    vehicleTypes.push({
        protocol: newProtocol, // the name to look for in the type field of incoming data
        domName: newDomName, // the name used for this vehicle type in the DOM
        faIcon: newFaIcon, // the icon used for this vehicle type in the sidebar and menus
        constructor: newConstructor, // constructor function for this vehicle type
        buildTable: newTableHeader // header row to use for this vehicle type in its' data table
    });
}