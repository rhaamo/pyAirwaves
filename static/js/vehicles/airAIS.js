"use strict"; // overcome current Chrome and Firefox issues with ECMA6 stuff like classes
/***********************************************************
 * Airsuck JS custom vehicle for Ships
 * v. 0.1
 *
 * Licensed under GPL V3
 * https://github.com/ThreeSixes/airSuck
 *
 * Ship class extends the default Vehicle class
 *
 * Deps: jQuery, vehicles.js
 **********************************************************/

/* jshint multistr: true */

// Register vehicle type
if (debug) {
  console.log('Registering vehicle type: AIS');
}
registerVehicleType('airAIS', 'AIS', 'fa-ship', function (msgJSON) {
  return new Ship(msgJSON);
}, function (container) {
  $(container).append('<tr><th>ID</th><th>Flag</th><th>Velocity</th><th>Course</th><th>Destination</th><th>Pos</th><th>Sig</th></tr>');
});

/***************************************************
 * AIS OBJECT DECLARATION
 **************************************************/
class Ship extends Vehicle {
  constructor(msgJSON) {
    // create the generic vehicle object
    super(msgJSON, 'AIS');
    // extend with AIS specific data
    $.extend(true, this, msgJSON);
    // add additional parameters
    this.domName = 'AIS';
    this.maxAge = 5 * (60 * 1000); // How long to retain a ship after losing contact (miliseconds)
    // gMap icon stuff
    this.dirIcoPath = "m 0,0 -20,50 40,0 -20,-50"; // Path we want to use for AIS targets that we have direction data for.
    this.dirIcoScale = 0.15; // Current scale of the icon.
    this.dirIcoDefaultScale = 0.15; // Default scale of the icon.
    this.ndIcoPath = "m 0,0 -20,20 20,20 20,-20 -20,-20"; // Path we want to use for AIS targets that we don't have direction data for.
    this.ndIcoScale = 0.21; // Current scale of the icon.
    this.ndIcoDefaultScale = 0.21; // Default scale of the icon.
    this.vehColorActive = "#0000ff"; // Color of active ship icons (hex)
    this.vehColorInactive = "#000066"; // Color of nonresponsive ship icons (hex)
    this.vehColorSelected = "#00ffff"; // Color of selected ship icons (hex)
    this.stkColor = "#00ffff"; // Color of the path
    // set the name string
    this.name = this.parseName();
    // create the table entry
    this.createTableEntry();
  }
}

/***************************************************
 * FUNCTION DETERMINES VEHICLE NAME
 **************************************************/
Ship.prototype.parseName = function () {
  let idStr = '';
  // If we have a vessel name
  if (this.vesselName) {
    if (this.vesselName !== undefined) {
      idStr += this.vesselName + " ";
    }
  }
  // If we have a valid IMO
  if (this.imo) {
    if (this.imo > 0) {
      idStr += "(" + this.imo + ((this.imoCheck === false) ? "*" : "") + ") ";
    }
  }
  // We should always have an MMSI address.
  idStr += "[" + this.addr.toString() + "]";
  return idStr;
};

/***************************************************
 * FUNCTION ADDS VEHICLE TO THE INFO TABLE
 **************************************************/
Ship.prototype.createTableEntry = function () {
  if (debug) {
    console.log('Creating new table entry for ship: ' + this.addr + ' in table: #table-' + this.domName);
  }
  let hasPos;
  let etaStr = "--";
  let colLength = $('#table-' + this.domName).find('th').length; //number of columns to span for the detail row
  //console.log('AIS table columns determined for: '+this.addr+' as this many columns: '+colLength);

  // Work out our ETA info.
  if (this.etaMonth != null || this.etaDay != null || this.etaHour != null || this.etaMinute != null) {
    // Build date and time string with -- indicating something that's intentionally not specified.
    ((this.etaMonth != null && this.etaMonth > 0) ? etaStr = this.zerofill(this.etaMonth, 2) + "/" : etaStr = "--/");
    ((this.etaDay != null && this.etaDay > 0) ? etaStr = etaStr + this.zerofill(this.etaDay, 2) + " " : etaStr = etaStr + "-- ");
    ((this.etaHour != null && this.etaHour < 24) ? etaStr = etaStr + this.zerofill(this.etaHour, 2) + ":" : etaStr = etaStr + "--:");
    ((this.etaMintue != null && this.etaMinute < 60) ? etaStr = etaStr + this.zerofill(this.etaMinute, 2) : etaStr = etaStr + "--");
  }

  if (this.lat) {
    hasPos = true;
  } else {
    hasPos = false;
  }
  $('#table-' + this.domName).append('\
    <tr id="' + this.addr + '-row-summary" class="vehicle-table-entry">\
      <td>' + ((this.name == null) ? '--' : this.name) + '</td>\
      <td>' + ((this.mmsiCC == null) ? '--' : this.mmsiCC) + '</td>\
      <td>' + ((this.velo == null) ? '--' : this.velo + ' kt') + '</td>\
      <td>' + ((this.courseOverGnd == null) ? '--' : degreeToCardinal(this.courseOverGnd)) + '</td>\
      <td>' + ((this.destination == null) ? '--' : this.destination) + '</td>\
      <td>' + ((hasPos) ? '*' : '--') + '</td>\
      <td>' + spinnerAnim[this.spinState] + '</td>\
    </tr>\
    <tr id="' + this.addr + '-row-detail" class="vehicle-table-detail">\
      <td colspan="' + colLength + '">\
        <table class="infoTable"><tbody>\
          <tr>\
            <td class="tblHeader">MMSI Type</td>\
            <td class="tblCell">' + ((this.mmsiType == null) ? '--' : this.mmsiType) + '</td>\
            <td class="tblHeader">Dim.</td>\
            <td class="tblCell">' + ((this.dimToBow > 0 && this.dimToStern > 0 && this.dimToPort > 0 && this.dimToStarboard > 0) ? (this.dimToPort + this.dimToStarboard) + 'x' + (this.dimToBow + this.dimToStern) + ' m' : '--') + '</td>\
          </tr>\
          <tr>\
            <td class="tblHeader">COG / Hdg</td>\
            <td class="tblCell">' + ((this.courseOverGnd == null) ? '--' : this.courseOverGnd) + ' / ' + ((this.heading == null || this.heading == 511) ? '--' : this.heading + ' deg') + '</td>\
            <td class="tblHeader">Turn rate</td>\
            <td class="tblCell">' + '--' + '</td>\
          </tr>\
          <tr>\
            <td class="tblHeader">Callsign</td>\
            <td class="tblCell">' + ((this.callsign == null) ? '--' : this.callsign) + '</td>\
            <td class="tblHeader">Draught</td>\
            <td class="tblCell">' + ((this.draught == null) ? '--' : ((this.draught > 0) ? this.draught.toString() + ' m' : '--')) + '</td>\
          </tr>\
          <tr>\
            <td class="tblHeader">Pos. type</td>\
            <td class="tblCell">' + ((this.epfdMeta == null) ? '--' : this.epfdMeta) + '</td>\
            <td class="tblHeader">ETA</td>\
            <td class="tblCell">' + ((this.etaStr == null) ? '--' : this.etaStr) + '</td>\
          </tr>\
          <tr>\
            <td class="tblHeader">Ship type</td>\
            <td class="tblCell" colspan=3>' + ((this.shipTypeMeta == null) ? '--' : this.shipTypeMeta) + '</td>\
          </tr>\
          <tr>\
            <td class="tblHeader">Position</td>\
            <td colspan=3 class="tblCell">' + ((this.lat == null) ? '--' : this.lat.toFixed(4) + ', ' + this.lon.toFixed(4)) + '</td>\
          </tr>\
          <tr>\
            <td class="tblHeader">Nav. Stat.</td>\
            <td class="tblCell" colspan=3>' + ((this.navStatMeta == null) ? '--' : this.navStatMeta) + '</td>\
          </tr>\
          <tr>\
            <td class="tblHeader">Data src.</td>\
            <td class="tblCell" colspan=3>' + this.lastClientName + ' -&gt; ' + this.lastSrc + '</td>\
          </tr>\
        </tbody></table>\
      </td>\
    </tr>\
  ');

  // set the row click function to display the row detail and highlight the plane
  $('#' + this.addr + '-row-summary').click(function () {
    // get vehicle name from the row ID
    let vehName = this.id.substring(0, this.id.length - 12); //ID is parsed correctly

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
Ship.prototype.updateTableEntry = function () {
  if (debug) {
    console.log('Updating table entry for ship: ' + this.addr + ' in table: #table-' + this.domName);
  }
  let hasPos;
  let etaStr = "--";
  let colLength = $('#table-' + this.domName).find('th').length; //number of columns to span for the detail row

  // Work out our ETA info.
  if (this.etaMonth != null || this.etaDay != null || this.etaHour != null || this.etaMinute != null) {
    // Build date and time string with -- indicating something that's intentionally not specified.
    ((this.etaMonth != null && this.etaMonth > 0) ? etaStr = this.zerofill(this.etaMonth, 2) + "/" : etaStr = "--/");
    ((this.etaDay != null && this.etaDay > 0) ? etaStr = etaStr + this.zerofill(this.etaDay, 2) + " " : etaStr = etaStr + "-- ");
    ((this.etaHour != null && this.etaHour < 24) ? etaStr = etaStr + this.zerofill(this.etaHour, 2) + ":" : etaStr = etaStr + "--:");
    ((this.etaMintue != null && this.etaMinute < 60) ? etaStr = etaStr + this.zerofill(this.etaMinute, 2) : etaStr = etaStr + "--");
  }

  if (this.lat) {
    hasPos = true;
  } else {
    hasPos = false;
  }
  $('#' + this.addr + '-row-summary').html('\
    <td>' + this.name + '</td>\
    <td>' + ((this.mmsiCC == null) ? '--' : this.mmsiCC) + '</td>\
    <td>' + ((this.velo == null) ? '--' : this.velo + ' kt') + '</td>\
    <td>' + ((this.courseOverGnd == null) ? '--' : degreeToCardinal(this.courseOverGnd)) + '</td>\
    <td>' + ((this.destination == null) ? '--' : this.destination) + '</td>\
    <td>' + ((hasPos) ? '*' : '--') + '</td>\
    <td>' + spinnerAnim[this.spinState] + '</td>');
  $('#' + this.addr + '-row-detail').html('\
    <td colspan="' + colLength + '">\
      <table class="infoTable"><tbody>\
        <tr>\
          <td class="tblHeader">MMSI Type</td>\
          <td class="tblCell">' + ((this.mmsiType == null) ? '--' : this.mmsiType) + '</td>\
          <td class="tblHeader">Dim.</td>\
          <td class="tblCell">' + ((this.dimToBow > 0 && this.dimToStern > 0 && this.dimToPort > 0 && this.dimToStarboard > 0) ? (this.dimToPort + this.dimToStarboard) + 'x' + (this.dimToBow + this.dimToStern) + ' m' : '--') + '</td>\
        </tr>\
        <tr>\
          <td class="tblHeader">COG / Hdg</td>\
          <td class="tblCell">' + ((this.courseOverGnd == null) ? '--' : this.courseOverGnd) + ' / ' + ((this.heading == null || this.heading == 511) ? '--' : this.heading + ' deg') + '</td>\
          <td class="tblHeader">Turn rate</td>\
          <td class="tblCell">' + '--' + '</td>\
        </tr>\
        <tr>\
          <td class="tblHeader">Callsign</td>\
          <td class="tblCell">' + ((this.callsign == null) ? '--' : this.callsign) + '</td>\
          <td class="tblHeader">Draught</td>\
          <td class="tblCell">' + ((this.draught == null) ? '--' : ((this.draught > 0) ? this.draught.toString() + ' m' : '--')) + '</td>\
        </tr>\
        <tr>\
          <td class="tblHeader">Pos. type</td>\
          <td class="tblCell">' + ((this.epfdMeta == null) ? '--' : this.epfdMeta) + '</td>\
          <td class="tblHeader">ETA</td>\
          <td class="tblCell">' + etaStr + '</td>\
        </tr>\
        <tr>\
            <td class="tblHeader">Ship type</td>\
            <td class="tblCell" colspan=3>' + ((this.shipTypeMeta == null) ? '--' : this.shipTypeMeta) + '</td>\
          </tr>\
        <tr>\
          <td class="tblHeader">Position</td>\
          <td colspan=3 class="tblCell">' + ((this.lat == null) ? '--' : this.lat.toFixed(4) + ', ' + this.lon.toFixed(4)) + '</td>\
        </tr>\
        <tr>\
          <td class="tblHeader">Nav. Stat.</td>\
          <td class="tblCell" colspan=3>' + ((this.navStatMeta == null) ? '--' : this.navStatMeta) + '</td>\
        </tr>\
        <tr>\
          <td class="tblHeader">Data src.</td>\
          <td class="tblCell" colspan=3>' + this.lastClientName + ' -&gt; ' + this.lastSrc + '</td>\
        </tr>\
      </tbody></table>\
    </td>\
  ');
};

/***************************************************
 * FUNCTION SETS THE VEHICLE ICON
 * OVERRIDES DEFAULT TO USE courseOverGnd
 **************************************************/
Ship.prototype.createIcon = function () {
  var newIcon;
  // If we have heading data for the vehicle
  if (this.courseOverGnd) {
    // Create our icon for a vehicle with heading data.
    newIcon = new L.BoatIcon({
      color: '#f4ff01',
      idleCircle: false,
      course: this.courseOverGnd
    });
    newIcon.setHeading(this.courseOverGnd);
  } else {
    // Create our icon for a vehicle without heading data.
    newIcon = new L.BoatIcon({
      color: '#f4ff01',
      idleCircle: false
    });
  }

  return newIcon;
};