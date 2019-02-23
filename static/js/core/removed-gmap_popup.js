/***********************************************************
 * Airsuck Google Maps popup factory
 * v. 0.1
 *
 * Licensed under GPL V3
 * https://github.com/ThreeSixes/airSuck
 *
 * Deps: jQuery, GoogleMaps JS API loaded
 **********************************************************/

/***************************************************
 * VEHICLE POPUP ON LEFT CLICK
 **************************************************/
// Create info windows for vehicles.
function infoFactory(vehName) {
  var retVal = null;
  
  // Which position type do we have?
  // ADS-B/SSR
  if (vehData[vehName].type == "airSSR") {
    // Build an aircraft identity string.
    var idStr = "";
    var catStr = "--";
    var fsStr = "-";
    var altStr = "--";
    var vertRateStr = "--";
    var vrSign = "";
    var veloStr = "--";
    var headingStr = "--";
    var vertStatStr = "--";
    var posStr = "";
    var supersonicStr = "--";
    
    // If we have a plane/flight ID
    if ("idInfo" in vehData[vehName]) {
      idStr += vehData[vehName].idInfo + " ";
    }
    
    // And if we have a squawk code...
    if ("aSquawk" in vehData[vehName]) {
      idStr += "(" + vehData[vehName].aSquawk + ") ";
    }
    
    // We should always have an ICAO address.
    idStr += "[" + vehData[vehName].addr.toUpperCase() + "]";
    
    // If we have flight status data...
    if ("fs" in vehData[vehName]) {
      fsStr = vehData[vehName].fs;
    }
    
    // If we have category data...
    if ("category" in vehData[vehName]) {
      catStr = vehData[vehName].category;
    }
    
    // If we have altitude data...
    if ("alt" in vehData[vehName]) {
      altStr = vehData[vehName].alt;
    }
    
    // If we have vertical rate data...
    if ("vertRate" in vehData[vehName]) {
      if (vehData[vehName].vertRate > 0) {
        vrSign = "+";
      }
      vertRateStr = vrSign + vehData[vehName].vertRate;
    }
    
    // If we have velocity data...
    if ("velo" in vehData[vehName]) {
      veloStr = vehData[vehName].velo;
    }
    
    // If we have vertical status data...
    if ("vertStat" in vehData[vehName]) {
      vertStatStr = vehData[vehName].vertStat;
    }
    
    // If we have heading data...
    if ("heading" in vehData[vehName]) {
      headingStr = vehData[vehName].heading;
    }
    
    // If we have position data...
    if ("lat" in vehData[vehName]) {
      posStr = vehData[vehName].lat.toFixed(7) + ", " + vehData[vehName].lon.toFixed(7);
    }
    
    // If we have supersonic data...
    if ("supersonic" in vehData[vehName]) {
      if (vehData[vehName].supersonic == 0) {
        supersonicStr = "No";
      } else if (vehData[vehName].supersonic == 1) {
        supersonicStr = "Yes";
      }
    }
    
    // Build our table.
    retVal = "<table class=\"infoTable\">";
    retVal += "<tr><td colspan=4 class=\"vehInfoHeader\">" + idStr + "</td></td></tr>";
    retVal += "<tr><td class=\"tblHeader\">Category</td><td class=\"tblCell\">" + catStr + "</td><td class=\"tblHeader\">Flight status</td><td class=\"tblCell\">" + fsStr + "</td></tr>";
    retVal += "<tr><td class=\"tblHeader\">Velocity</td><td class=\"tblCell\">" + veloStr + " kt</td><td class=\"tblHeader\">Heading</td><td class=\"tblCell\">" + headingStr + " deg</td></tr>";
    retVal += "<tr><td class=\"tblHeader\">Altitude</td><td class=\"tblCell\">" + altStr + " ft</td><td class=\"tblHeader\">Climb rate</td><td class=\"tblCell\">" + vertRateStr + " ft/min</td></tr>";
    retVal += "<tr><td class=\"tblHeader\">Position</td><td colspan=3 class=\"tblCell\">" + posStr + "</td></tr>";
    retVal += "<tr><td class=\"tblHeader\">Air/Gnd</td><td class=\"tblCell\">" + vertStatStr + "</td><td class=\"tblHeader\">Supersonic</td><td class=\"tblCell\">" + supersonicStr + "</td></tr>";
    
    // If we have some sort of emergency...
    if ('emergency' in vehData[vehName]) {
      if ((vehData[vehName].emergency == true) && ("emergencyData" in vehData[vehName])) {
        retVal += "<tr><td class=\"tblEmerg\" colspan=4>** EMERGENCY **</td></tr>";
        retVal += "<td class=\"tblEmerg\" colspan=4>Description - " + vehData[vehName].emergencyData + "</td></tr>";
      }
    }
    
    // If we have Mode A metadata...
    if ("aSquawkMeta" in vehData[vehName]) {
      retVal += "<tr><td class=\"tblHeader\" colspan=4>Metadata</td></tr>";
      retVal += "<td class=\"tblCell\" colspan=4>Mode A - " + vehData[vehName].aSquawkMeta + "</td></tr>";
    }
    
    retVal += "</table>";
  }
  
  // AIS
  else if (vehData[vehName].type == "airAIS") {
    // Build a ship identity string.
    var idStr = "";
    var veloStr = "--";
    var headingStr = "--";
    var courseOverGndStr = "--";
    var navStatStr = "--";
    var callsignStr = "--";
    var draughtStr = "--";
    var etaStr = "--";
    var shipTypeStr = "--";
    var epfdMetaStr = "--";
    var dimStr = "--";
    var turnRtStr = "--";
    var posStr = "--";
    var flagStr = "--";
    var imoFlagStr = "";
    
    // If we have the vessel name...
    if ("vesselName" in vehData[vehName]) {
      idStr += vehData[vehName].vesselName + " ";
    }
    
    // If we an IMO that doesn't check out...
    if ("imoCheck" in vehData[vehName]) {
      if (vehData[vehName].imoCheck == false) {
        imoFlagStr = "*";
      }
    }
    
    // If we have a non-zero IMO...
    if ("imo" in vehData[vehName]) {
      if (vehData[vehName].imo > 0) {
        idStr += "(" + vehData[vehName].imo + imoFlagStr + ") ";
      }
    }
    
    // We should always have an MMSI address.
    idStr += "[" + vehData[vehName].addr.toString() + "]";
    
    // If we have velocity data...
    if ("velo" in vehData[vehName]) {
      veloStr = vehData[vehName].velo;
    }
    
    // If we have heading data...
    if ("heading" in vehData[vehName]) {
      if (vehData[vehName].heading != 511) {
        headingStr = vehData[vehName].heading;
      }
    }
    
    // If we have course over ground data...
    if ("courseOverGnd" in vehData[vehName]) {
      cogStr = vehData[vehName].courseOverGnd;
    }
    
    // If we have navigation status data...
    if ("navStat" in vehData[vehName]) {
      if (vehData[vehName].navStat < 15) {
        navStatStr = vehData[vehName].navStat;
        
        // If we have navigation stuatus metadata...
        if ("navStatMeta" in vehData[vehName]) {
          navStatStr = vehData[vehName].navStatMeta + " (" + navStatStr + ")";
        }
      }
    }
    
    // If we have navigation status data...
    if ("callsign" in vehData[vehName]) {
      if (vehData[vehName].callsign != "") {
        callsignStr = vehData[vehName].callsign;
      }
    }
    
    // If we have draught data.
    if ("draught" in vehData[vehName]) {
      // If we have good draught data...
      if (vehData[vehName].draught > 0) {
        // Set the draught string.
        draughtStr = vehData[vehName].draught.toString()
      }
    }
    
    // If we have EPFD metadata...
    if ("epfdMeta" in vehData[vehName]) {
      epfdMetaStr = vehData[vehName].epfdMeta;
    }
    
    // If we have position data...
    if ("lat" in vehData[vehName]) {
      posStr = vehData[vehName].lat + ", " + vehData[vehName].lon;
    }
    
    // If we have country code data...
    if ("mmsiCC" in vehData[vehName]) {
      flagStr = vehData[vehName].mmsiCC;
    }
    
    // Figure out our dimensions.
    if ("dimToBow" in vehData[vehName]) {
      // 
      dimBow = vehData[vehName].dimToBow;
      dimStern = vehData[vehName].dimToStern;
      dimPort = vehData[vehName].dimToPort;
      dimStarboard = vehData[vehName].dimToStarboard;
      
      // See if we have good data for our dimensions.
      if (dimBow > 0 && dimStern > 0 && dimPort > 0 && dimStarboard > 0) {
        // Create our dimension string.
        shipLen = dimBow + dimStern;
        shipWidth = dimPort + dimStarboard;
        dimStr = shipWidth.toString() + "x" + shipLen.toString();
      }
    }
    
    // Build our table.
    retVal = "<table class=\"infoTable\">";
    retVal += "<tr><td colspan=4 class=\"vehInfoHeader\">" + idStr + "</td></td></tr>";
    retVal += "<tr><td class=\"tblHeader\">Velocity</td><td class=\"tblCell\">" + veloStr + " kt</td><td class=\"tblHeader\">Flag</td><td class=\"tblCell\">" + flagStr + "</td></tr>";
    retVal += "<tr><td class=\"tblHeader\">COG / Hdg</td><td class=\"tblCell\">" + cogStr + " / " + headingStr + " deg</td><td class=\"tblHeader\">Pos. type</td><td class=\"tblCell\">" + epfdMetaStr + "</td></tr>";
    retVal += "<tr><td class=\"tblHeader\">Callsign</td><td class=\"tblCell\">" + callsignStr + "</td><td class=\"tblHeader\">Draught</td><td class=\"tblCell\">" + draughtStr + " m</td></tr>";
    retVal += "<tr><td class=\"tblHeader\">Turn rate</td><td class=\"tblCell\">" + turnRtStr + " deg</td><td class=\"tblHeader\">Dim.</td><td class=\"tblCell\">" + dimStr + " m</td></tr>";
    
    if (posStr != "--") {
      retVal += "<tr><td class=\"tblHeader\">Position</td><td colspan=3 class=\"tblCell\">" + posStr + "</td></tr>";
    }
    
    
    if (navStatStr != "--") {
      retVal += "<td class=\"tblHeader\">NavStat</td><td colspan=3 class=\"tblCell\">" + navStatStr + "</td></tr>";
    }
    
    // If we have ship type data...
    if ('shipTypeMeta' in vehData[vehName]) {
      if (vehData[vehName].shipTypeMeta != "") {
        retVal += "<td class=\"tblHeader\">Ship type</td><td colspan=3 class=\"tblCell\">" + vehData[vehName].shipTypeMeta + "</td></tr>";
      }
    }
    
    // If we have destination data...
    if ('destination' in vehData[vehName]) {
      if (vehData[vehName].destination != "") {
        retVal += "<td class=\"tblHeader\">Dest.</td><td colspan=3 class=\"tblCell\">" + vehData[vehName].destination + "</td></tr>";
      }
    }
    
    // If we have ETA data...
    if (etaStr != "--") {
      retVal += "<td class=\"tblHeader\">ETA</td><td colspan=3 class=\"tblCell\">" + etaStr + "</td></tr>";
    }
    
    // If we have MMSI type data...
    if ('mmsiType' in vehData[vehName]) {
      retVal += "<td class=\"tblHeader\">MMSI type</td><td colspan=3 class=\"tblCell\">" + vehData[vehName].mmsiType + "</td></tr>";
    }
    
    // If we have some sort of emergency...
    if ('emergency' in vehData[vehName]) {
      if ((vehData[vehName].emergency == true) && ("emergencyData" in vehData[vehName])) {
        retVal += "<tr><td class=\"tblEmerg\" colspan=4>** EMERGENCY **</td></tr>";
        retVal += "<td class=\"tblEmerg\" colspan=4>Description - " + vehData[vehName].emergencyData + "</td></tr>";
      }
    }
    
    retVal += "</table>";
  }
  
  // Return information to be included in the infoWindow's contents.
  return retVal;
}