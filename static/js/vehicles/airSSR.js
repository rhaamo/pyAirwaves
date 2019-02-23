"use strict";// overcome current Chrome and Firefox issues with ECMA6 stuff like classes
/***********************************************************
 * Airsuck JS custom vehicle for Aircraft
 * v. 0.1
 *
 * Licensed under GPL V3
 * https://github.com/ThreeSixes/airSuck
 *
 * Vehicle creator, manipulation, and destruction functions
 *
 * Deps: jQuery
 **********************************************************/
// Register vehicle type
if (debug) {
    console.log('Registering vehicle type: SSR');
}
registerVehicleType('airSSR', 'SSR', 'fa-plane', function (msgJSON) {
    return new Aircraft(msgJSON);
}, function (container) {
    $(container).append('<tr><th>ID</th><th>Cat.</th><th>Flag</th><th>Altitude</th><th>Velocity</th><th>Heading</th><th>Pos</th><th>Sig</th></tr>');
});

/***************************************************
 * SSR OBJECT DECLARATION
 **************************************************/
class Aircraft extends Vehicle {
    constructor(msgJSON) {
        // create the generic vehicle object
        super(msgJSON, 'SSR');
        // extend with SSR specific data
        $.extend(true, this, msgJSON);
        // add additional parameters
        this.domName = 'SSR';
        this.maxAge = 2 * (60 * 1000); // How long to retain an aircraft after losing contact (miliseconds)
        // Icon variables
        this.dirIcoPath = "m 0,0 -20,50 20,-20 20,20 -20,-50"; // Path we want to use for ADS-B targets we have direction data for.
        this.dirIcoScale = 0.15; // Scale of the path.
        this.dirIcoDefaultScale = 0.15; // Default scale of the path
        this.ndIcoPath = "m 15,15 a 15,15 0 1 1 -30,0 15,15 0 1 1 30,0 z"; // Path we want to sue for ADS-B targets we don't have direction data for.
        this.ndIcoSacle = 0.24; // Scale of the path.
        this.ndIcoDefaultScale = 0.24; // Default scale of the path.
        this.vehColorActive = "#ff0000"; // Color of active aircraft icons (hex)
        this.vehColorInactive = "#660000"; // Color of nonresponsive aircraft icons (hex)
        this.vehColorSelected = "#00ffff"; // Color of the vehicle icon when selected
        this.stkColor = "#FFFFFF"; // Color of the path
        // set the name string
        this.name = this.parseName();
        // create the table entry
        this.createTableEntry();
    }
}

/***************************************************
 * FUNCTION DETERMINES VEHICLE NAME
 * OVERRIDES DEFAULT TO USE COLOR RAMP
 **************************************************/
Aircraft.prototype.update = function (msgJSON) {
    // update data in the object **do this first**
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

    // set the path color if we have an altitude
    if (this.alt !== 'undefined' && this.alt != null) {
        this.stkColor = "#" + polyRamp.colourAt(this.alt / 1000); // Color of the path
    }
    // update the last update parameter
    this.lastUpdate = Date.now();
    // update the vehicle entry in its' table
    this.updateTableEntry();
    // move the maps position
    this.movePosition();
};

/***************************************************
 * FUNCTION DETERMINES VEHICLE NAME
 **************************************************/
Aircraft.prototype.parseName = function () {
    let idStr = '';
    // If we have a plane/flight ID
    if (this.idInfo) {
        // If we have 'default' or 'blank' idInfo field
        if (this.idInfo !== "@@@@@@@@") {
            // Just blank the field.
            idStr += this.idInfo + " ";
        }

    }
    // And if we have a squawk code...
    if (this.aSquawk) {
        idStr += "(" + this.aSquawk + ") ";
    }
    // We should always have an ICAO address.
    idStr += "[" + this.addr.toUpperCase() + "]";
    return idStr;
};

/***************************************************
 * FUNCTION ADDS VEHICLE TO THE INFO TABLE
 * TO DO: separate the table info population function
 * so we don't duplicate with the update function
 **************************************************/
Aircraft.prototype.createTableEntry = function () {
    if (debug) {
        console.log('Creating new table entry for aircraft: ' + this.addr + ' in table: #table-' + this.domName);
    }
    let hasPos;
    let colLength = $('#table-' + this.domName).find('th').length;//number of columns to span for the detail row
    if (this.lat) {
        hasPos = true;
    } else {
        hasPos = false;
    }

    // Handle mode A stuff out-of-band.
    if (this.aSquawkMeta != null) {
        var aSquawkMetaStr = '<tr>\
          <td class="tblHeader">Squawk meta</td>\
          <td class="tblCell" colspan=3>' + this.aSquawkMeta + '</td>\
        </tr>';
    }

    // Handle registration stuff out of band.
    if (this.regData == "True") {
        this.regMetaStr = '<tr>\
          <td class="tblHeader">Reg. tail number</td>\
          <td class="tblCell" colspan="3">' + this.regTail + ' (' + this.regAuthority + ')</td>\
          </tr>\
          <tr>\
          <td class="tblHeader">Reg. name</td>\
          <td class="tblCell" colspan=3>' + this.regName + '</td>\
          </tr>\
          <tr>\
          <td class="tblHeader">Reg. aircraft</td>\
          <td class="tblCell" colspan=3>' + this.regAircraft + '</td>\
          </tr>';
    }

    $('#table-' + this.domName).append('\
    <tr id="' + this.addr + '-row-summary" class="vehicle-table-entry">\
      <td>' + this.name + '</td>\
      <td>' + ((this.category == null) ? '--' : this.category) + '</td>\
      <td>' + ((this.icaoAACC == null) ? '--' : this.icaoAACC) + '</td>\
      <td>' + ((this.alt == null) ? '--' : this.alt + ' ft') + '</td>\
      <td>' + ((this.velo == null) ? '--' : this.velo + ' kt') + '</td>\
      <td>' + ((this.heading == null) ? '--' : degreeToCardinal(this.heading)) + '</td>\
      <td>' + ((hasPos) ? '*' : '--') + '</td>\
      <td>' + spinnerAnim[this.spinState] + '</td>\
    </tr>\
    <tr id="' + this.addr + '-row-detail" class="vehicle-table-detail">\
      <td colspan="' + colLength + '">\
        <table class="infoTable"><tbody>\
           <tr>\
        <td class="tblHeader">Air/Gnd</td>\
        <td class="tblCell">' + ((this.vertStat == null) ? '--' : this.vertStat) + '</td>\
        <td class="tblHeader">Flight status</td>\
        <td class="tblCell">' + ((this.fs == null) ? '--' : this.fs) + '</td>\
      </tr>\
      <tr>\
        <td class="tblHeader">Supersonic</td>\
        <td class="tblCell">' + ((typeof this.supersonic === "undefined") ? '--' : ((this.supersonic === true) ? 'Yes' : 'No')) + '</td>\
        <td class="tblHeader">Heading</td>\
        <td class="tblCell">' + ((this.heading == null) ? '--' : this.heading + ' deg') + '</td>\
      </tr>\
      <tr>\
        <td class="tblHeader">Climb rate</td>\
        <td class="tblCell">' + ((this.vertRate == null) ? '--' : (this.vertRate > 0) ? '+' + this.vertRate + ' ft/min' : this.vertRate + ' ft/min') + '</td>\
        <td class="tblHeader"></td>\
        <td class="tblCell"></td>\
      </tr>\
      <tr>\
        <td class="tblHeader">Position</td>\
        <td colspan=3 class="tblCell">' + ((this.lat == null) ? '--' : this.lat.toFixed(7) + ', ' + this.lon.toFixed(7)) + '</td>\
      </tr>\
      <tr>\
        <td class="tblHeader">Data src.</td>\
        <td class="tblCell" colspan=3>' + this.lastClientName + ' -&gt; ' + this.lastSrc + '</td>\
      </tr>\
      ' + ((aSquawkMetaStr == null) ? '' : aSquawkMetaStr) + '\
      ' + ((this.regMetaStr == null) ? '' : this.regMetaStr) + '\
        </tbody></table>\
      </td>\
    </tr>'
    );

    // set the row click function to display the row detail and highlight the plane
    $('#' + this.addr + '-row-summary').click(function () {
        // get vehicle name from the row ID
        let vehName = this.id.substring(0, this.id.length - 12);//ID is parsed correctly

        if ($(this).next().css('display') == 'none') {
            // details aren't shown, change the plane's icon color & size
            // select the icon
            vehicles['veh' + vehName].setMarkerSelected();
            // display the info table
            $(this).next().css('display', 'table-row');
        } else {
            // details are shown, return the plane's icon color & size to normal
            // unselect the icon
            vehicles['veh' + vehName].setMarkerUnselected();
            // close the info table
            $(this).next().css('display', 'none');
        }
    });

    // set the row hover function to highlight the airplane
    $('#' + this.addr + '-row-summary').mouseenter(function () {
        // mouse in function, highlight the icon
        // check to see if the info table is already shown, if so do nothing
        if ($(this).next().css('display') == 'none') {
            // table isn't shown, adjust the icon
            // get vehicle name from the row ID and set the marker selected
            let vehName = this.id.substring(0, this.id.length - 12);
            vehicles['veh' + vehName].setMarkerHover();
        }
        // table is shown, do nothing
        return;
    }).mouseleave(function () {
        // mouse out function, unhighlight the icon
        // check to see if the info table is already shown, if so do nothing
        if ($(this).next().css('display') == 'none') {
            // table isn't shown, unhighlight the icon
            // get vehicle name from the row ID and set the marker unselected
            let vehName = this.id.substring(0, this.id.length - 12);
            vehicles['veh' + vehName].setMarkerUnselected();
        }
        // table is shown, do nothing
        return;
    });


};

/***************************************************
 * FUNCTION UPDATES VEHICLE IN THE INFO TABLE
 **************************************************/
Aircraft.prototype.updateTableEntry = function () {
    if (debug) {
        console.log('Updating table entry for aircraft: ' + this.addr + ' in table: #table-' + this.domName);
    }
    let hasPos;
    hasPos = !!this.lat;

    // update the summary
    $('#' + this.addr + '-row-summary').html('\
    <td>' + this.parseName() + '</td>\
    <td>' + ((this.category == null) ? '--' : this.category) + '</td>\
    <td>' + ((this.icaoAACC == null) ? '--' : this.icaoAACC) + '</td>\
    <td>' + ((this.alt == null) ? '--' : this.alt + ' ft') + '</td>\
    <td>' + ((this.velo == null) ? '--' : this.velo + ' kt') + '</td>\
    <td>' + ((this.heading == null) ? '--' : degreeToCardinal(this.heading)) + '</td>\
    <td>' + ((hasPos) ? '*' : '--') + '</td>\
    <td>' + spinnerAnim[this.spinState] + '</td>');

    // Handle mode A stuff out-of-band.
    if (this.aSquawkMeta != null) {
        var aSquawkMetaStr = '<tr>\
          <td class="tblHeader">Squawk meta</td>\
          <td class="tblCell" colspan=3>' + this.aSquawkMeta + '</td>\
        </tr>';
    }

    // update the detail table
    $('#' + this.addr + '-row-detail').find('.infoTable').html('\
      <tr>\
        <td class="tblHeader">Air/Gnd</td>\
        <td class="tblCell">' + ((this.vertStat == null) ? '--' : this.vertStat) + '</td>\
        <td class="tblHeader">Flight status</td>\
        <td class="tblCell">' + ((this.fs == null) ? '--' : this.fs) + '</td>\
      </tr>\
      <tr>\
        <td class="tblHeader">Supersonic</td>\
        <td class="tblCell">' + ((typeof this.supersonic === "undefined") ? '--' : ((this.supersonic === true) ? 'Yes' : 'No')) + '</td>\
        <td class="tblHeader">Heading</td>\
        <td class="tblCell">' + ((this.heading == null) ? '--' : this.heading + ' deg') + '</td>\
      </tr>\
      <tr>\
        <td class="tblHeader">Climb rate</td>\
        <td class="tblCell">' + ((this.vertRate == null) ? '--' : (this.vertRate > 0) ? '+' + this.vertRate + ' ft/min' : this.vertRate + ' ft/min') + '</td>\
        <td class="tblHeader"></td>\
        <td class="tblCell"></td>\
      </tr>\
      <tr>\
        <td class="tblHeader">Position</td>\
        <td colspan=3 class="tblCell">' + ((this.lat == null) ? '--' : this.lat.toFixed(7) + ', ' + this.lon.toFixed(7)) + '</td>\
      </tr>\
      <tr>\
        <td class="tblHeader">Data src.</td>\
        <td class="tblCell" colspan=3>' + this.lastClientName + ' -&gt; ' + this.lastSrc + '</td>\
      </tr>\
      ' + ((aSquawkMetaStr == null) ? '' : aSquawkMetaStr) + '\
      ' + ((this.regMetaStr == null) ? '' : this.regMetaStr));
};
