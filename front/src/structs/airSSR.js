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

import Vehicle from './vehicle'
import Vue from 'vue'
import utils from './utils'

const spinnerAnim = ['+', '&#45;', '&#92;', '&#124;', '&#47;', '&#42;']

/***************************************************
 * SSR OBJECT DECLARATION
 **************************************************/
export default class Aircraft extends Vehicle {
  constructor (msg) {
    // create the generic vehicle object
    super(msg, 'SSR')
    // extend with SSR specific data
    Vue.util.extend(this, msg)
    // add additional parameters
    this.lastAltitudes = [] // Will contains the five last altitudes reported
    this.domName = 'SSR'
    this.maxAge = 10 * 1000 // 2 * (60 * 1000); // How long to retain an aircraft after losing contact (miliseconds)
    // Icon variables
    this.dirIcoPath = 'm 0,0 -20,50 20,-20 20,20 -20,-50' // Path we want to use for ADS-B targets we have direction data for.
    this.dirIcoScale = 0.15 // Scale of the path.
    this.dirIcoDefaultScale = 0.15 // Default scale of the path
    this.ndIcoPath = 'm 15,15 a 15,15 0 1 1 -30,0 15,15 0 1 1 30,0 z' // Path we want to sue for ADS-B targets we don't have direction data for.
    this.ndIcoSacle = 0.24 // Scale of the path.
    this.ndIcoDefaultScale = 0.24 // Default scale of the path.
    this.vehColorActive = '#ff0000' // Color of active aircraft icons (hex)
    this.vehColorInactive = '#660000' // Color of nonresponsive aircraft icons (hex)
    this.vehColorSelected = '#00ffff' // Color of the vehicle icon when selected
    this.stkColor = '#FFFFFF' // Color of the path
    // set the name string
    this.name = this.parseName()
  }
}

/* Add altitude to array and remove old ones */
Aircraft.prototype.addLastAlt = function (alt) {
  if (this.lastAltitudes.length >= 5) {
    this.lastAltitudes.shift()
  }
  this.lastAltitudes.push(alt)
}

/***************************************************
 * FUNCTION DETERMINES VEHICLE NAME
 * OVERRIDES DEFAULT TO USE COLOR RAMP
 **************************************************/
Aircraft.prototype.update = function (msg) {
  // Set old lat and lon
  this.lastLat = this.lat
  this.lastLon = this.lon
  // Also insert altitude in array
  this.addLastAlt(this.alt)

  // then update data in the object
  Vue.util.extend(this, msg)

  // if not set to active, reactivate
  if (this.active === false) {
    this.active = true
    // Reset so the counter bounces up to 1.
    this.spinState = 0
  }

  // Handle the animation. If the state is lower than the length.
  if (this.spinState < (spinnerAnim.length - 2)) {
    // Increment the animation counter.
    this.spinState++
  } else if (this.spinState === (spinnerAnim.length - 2)) {
    // Reset counter at 1. We do this to make sure we have > 1 frame from the target.
    this.spinState = 1
  }

  // set the path color if we have an altitude
  // if (this.alt !== 'undefined' && this.alt != null) {
  //   this.stkColor = '#' + polyRamp.colourAt(this.alt / 1000) // Color of the path
  // }

  // Modify the icon to have the correct rotation, and to indicate there is bearing data.
  this.heading = utils.bearingFromTwoCoordinates(this.lastLat, this.lastLon, this.lat, this.lon)

  // update the last update parameter
  this.lastUpdate = Date.now()
  // update the vehicle entry in its' table
  this.updateTableEntry()
  // move the maps position
  this.movePosition()
}

/***************************************************
 * FUNCTION DETERMINES VEHICLE NAME
 **************************************************/
Aircraft.prototype.parseName = function () {
  let idStr = ''
  // If we have a plane/flight ID
  if (this.idInfo) {
    // If we have 'default' or 'blank' idInfo field
    if (this.idInfo !== '@@@@@@@@') {
      // Just blank the field.
      idStr += this.idInfo + ' '
    }
  }
  // And if we have a squawk code...
  if (this.aSquawk) {
    idStr += '(' + this.aSquawk + ') '
  }
  // We should always have an ICAO address.
  idStr += '[' + this.addr.toUpperCase() + ']'
  return idStr
}

/***************************************************
 * FUNCTION ADDS VEHICLE TO THE INFO TABLE
 * TO DO: separate the table info population function
 * so we don't duplicate with the update function
 **************************************************/
Aircraft.prototype.createTableEntry = function () {
  console.log('Creating new table entry for aircraft: ' + this.addr + ' in table: #table-' + this.domName)

  // Handle mode A stuff out-of-band.
  if (this.aSquawkMeta != null) {
  }

  // Handle registration stuff out of band.
  if (this.regData === 'True') {
    this.regMetaStr = ''
  }
}

/***************************************************
 * FUNCTION UPDATES VEHICLE IN THE INFO TABLE
 **************************************************/
Aircraft.prototype.updateTableEntry = function () {
  console.log('Updating table entry for aircraft: ' + this.addr + ' in table: #table-' + this.domName)
  // update the summary
}
