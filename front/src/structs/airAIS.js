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

import Vehicle from './vehicle'
import Vue from 'vue'

/***************************************************
 * AIS OBJECT DECLARATION
 **************************************************/
export default class Ship extends Vehicle {
  constructor (msg) {
    // create the generic vehicle object
    super(msg, 'AIS')
    // extend with AIS specific data
    // merge msg in this struct this.extend(true, this, msg)
    Vue.util.extend(this, msg)
    // add additional parameters
    this.domName = 'AIS'
    this.maxAge = 10 * 1000 // 5 * (60 * 1000) // How long to retain a ship after losing contact (miliseconds)
    // gMap icon stuff
    this.dirIcoPath = 'm 0,0 -20,50 40,0 -20,-50' // Path we want to use for AIS targets that we have direction data for.
    this.dirIcoScale = 0.15 // Current scale of the icon.
    this.dirIcoDefaultScale = 0.15 // Default scale of the icon.
    this.ndIcoPath = 'm 0,0 -20,20 20,20 20,-20 -20,-20' // Path we want to use for AIS targets that we don't have direction data for.
    this.ndIcoScale = 0.21 // Current scale of the icon.
    this.ndIcoDefaultScale = 0.21 // Default scale of the icon.
    this.vehColorActive = '#0000ff' // Color of active ship icons (hex)
    this.vehColorInactive = '#000066' // Color of nonresponsive ship icons (hex)
    this.vehColorSelected = '#00ffff' // Color of selected ship icons (hex)
    this.stkColor = '#00ffff' // Color of the path
    // set the name string
    this.name = this.parseName()
  }
}

/***************************************************
 * FUNCTION DETERMINES VEHICLE NAME
 **************************************************/
Ship.prototype.parseName = function () {
  let idStr = ''
  // If we have a vessel name
  if (this.vesselName) {
    if (this.vesselName !== undefined) {
      idStr += this.vesselName + ' '
    }
  }
  // If we have a valid IMO
  if (this.imo) {
    if (this.imo > 0) {
      idStr += '(' + this.imo + ((this.imoCheck === false) ? '*' : '') + ') '
    }
  }
  // We should always have an MMSI address.
  idStr += '[' + this.addr.toString() + ']'
  return idStr
}
