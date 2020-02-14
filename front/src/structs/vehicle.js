import L from 'leaflet'
import utils from './utils'
import Vue from 'vue'

const spinnerAnim = ['+', '&#45;', '&#92;', '&#124;', '&#47;', '&#42;']

/***************************************************
 * VEHICLE PROTOTYPE
 **************************************************/

export default class Vehicle {
  constructor (msg, protocol) {
    console.log('Vehicle constructor executed for vehicle: ' + msg.addr + ', Using protocol: ' + protocol)
    this.spinState = 0 // This is just for tracking the spinner animation state.
    this.addr = msg.addr
    this.protocol = protocol // communications protocol used (AIS,SSR)
    this.lastPos = 'none'
    this.lastLat = null
    this.lastLon = null
    this.lastUpdate = new Date().getTime()
    this.active = true // set true if the vehicle is currently active
    this.selected = false // records whether the vehicle has been selected in the sidebar or by clicking the icon
    this.maxAge = 1000 // default vehicle expiration time in milliseconds since last contact
    // gMap icon stuff
    this.dirIcoPath = 'm 0,0 -20,50 20,-20 20,20 -20,-50' // Path we want to use for ADS-B targets we have direction data for.
    this.dirIcoScale = 0.15 // Current scale of the path
    this.dirIcoDefaultScale = 0.15 // Default scale of the path
    this.ndIcoPath = 'm 15,15 a 15,15 0 1 1 -30,0 15,15 0 1 1 30,0 z' // Path we want to sue for ADS-B targets we don't have direction data for.
    this.ndIcoScale = 0.24 // Current scale of the path.
    this.ndIcoDefaultScale = 0.24 // Default scale of the path.
    this.vehColorActive = '#ff0000' // Color of active vehicle icons (hex)
    this.vehColorInactive = '#660000' // Color of nonresponsive vehicle icons (hex)
    this.vehColorSelected = '#ff00ff' // Color of the vehicle icon when selected
    this.marker = null // Placeholder for the map marker
    this.info = null // Placeholder for the map info popup
    this.pathPoly = null // new L.polyline([]).addTo(map)
    this.icon = null
    this.latlng = null
  }
}

/***************************************************
 * DEFAULT FUNCTION DETERMINES VEHICLE NAME
 * TO BE OVERRIDEN BY CUSTOM VEHICLES
 **************************************************/
Vehicle.prototype.parseName = function () {
  // default vehicle name function, to be customized per vehicle type
  return this.addr.toUpperCase()
}

/*
 * Vehicle 'PLANE' icon definition
 */
Vehicle.prototype.drawPlane = function (icon, type) {
  if (type === 'icon') {
    const ctx = icon.getContext('2d')
    ctx.beginPath()
    ctx.moveTo(109.375000, 307.375000)
    ctx.lineTo(109.375000, 279.375000)
    ctx.lineTo(139.375000, 255.375000)
    ctx.lineTo(139.375000, 183.375000)
    ctx.lineTo(6.375000, 227.375000)
    ctx.lineTo(6.375000, 192.375000)
    ctx.lineTo(138.375000, 112.375000)
    ctx.lineTo(138.375000, 14.375000)
    ctx.bezierCurveTo(138.375000, -6.625000, 172.375000, -6.625000, 172.375000, 14.375000)
    ctx.lineTo(172.375000, 112.375000)
    ctx.lineTo(306.375000, 192.375000)
    ctx.lineTo(306.375000, 227.375000)
    ctx.lineTo(173.375000, 184.375000)
    ctx.lineTo(173.375000, 255.375000)
    ctx.lineTo(203.375000, 279.375000)
    ctx.lineTo(203.375000, 307.375000)
    ctx.lineTo(156.375000, 292.375000)
  }
}

/***************************************************
 * FUNCTION CREATES VEHICLE ICONS FOR GMAPS
 * OVERRIDE IF USING A DIFFERENT HEADING
 **************************************************/
Vehicle.prototype.createIcon = function () {
  var newIcon
  // If we have heading data for the vehicle
  if (this.heading) {
    // Create our icon for a vehicle with heading data.
    // newIcon = new google.maps.Marker({
    //  path: this.dirIcoPath,
    //  scale: this.dirIcoScale,
    //  strokeWeight: 1.5,
    //  strokeColor: (this.selected == true) ? this.vehColorSelected : ((this.active == true) ? this.vehColorActive : this.vehColorInactive),
    //  rotation: this.heading
    // });
    console.log('TODO: heading')
    newIcon = new L.PlaneIcon({
      color: '#f4ff01',
      idleCircle: false,
      course: this.heading
    })
    newIcon.setHeading(this.heading)
  } else {
    // Create our icon for a vehicle without heading data.
    // newIcon = new google.maps.Marker({
    //  path: this.ndIcoPath,
    //  scale: this.ndIcoScale,
    //  strokeWeight: 1.5,
    //  strokeColor: (this.selected == true) ? this.vehColorSelected : ((this.active == true) ? this.vehColorActive : this.vehColorInactive)
    // });
    console.log('TODO: no heading')
    newIcon = new L.PlaneIcon({
      color: '#f4ff01',
      idleCircle: false
    })
  }
  // And return it.
  return newIcon
}

/***************************************************
 * FUNCTION MOVES THE VEHICLE MARKER AND INFO POSITIONS
 **************************************************/
Vehicle.prototype.movePosition = function () {
  console.log(this)

  // We can do this only if we have a non-null non-undefined lat and lon
  if (this.lat && this.lon) {
    console.log(this)
    // Figure out where we are in 2D space
    const thisPos = this.lat + ',' + this.lon
    // Update the path object with the new position
    // copy the path object
    const pathObject = this.pathPoly.getLatLngs()
    // update with the new path
    pathObject.push(new L.LatLng(this.lat, this.lon))
    // push back to the polyline
    this.pathPoly.setLatLngs(pathObject)
    // set the polyline color
    this.pathPoly.setStyle({
      color: this.stkColor
    })

    // Update the marker
    this.marker.setIcon(this.createIcon())
    // Move the marker.
    this.marker.setLatLng(new L.LatLng(this.lat, this.lon))

    // also update popup info if opened
    if (this.info.shown === true) {
      this.info.setLatLng(new L.LatLng(this.lat, this.lon))
      this.info.update()
    }

    // Record the new position for testing on next update
    this.lastPos = thisPos
  } else {
    console.log('movePosition: Cannot move marker without lat/lon for: ' + this.addr)
  }
}

/***************************************************
 * FUNCTION ADDS A MAPS INFO WINDOW TO THE VEHICLE
 **************************************************/
Vehicle.prototype.setInfoWindow = function () {
  // Create our info window.
  this.info = new L.popup({
    shown: false,
    offset: new L.point(0, -35) // Add little offset to be on top of the marker icon
  }).setLatLng(new L.LatLng(this.lat, this.lon)).setContent(this.parseName())
}

/***************************************************
 * FUNCTIONS UPDATE THE VEHICLE INFO AND TABLE ENTRY
 * updateTableEntry function to be overridden by
 * custom vehicle types
 **************************************************/
Vehicle.prototype.updateTableEntry = function () {
  console.log('Error: Function updateTableEntry not set for protocol: ' + this.protocol)
}

Vehicle.prototype.update = function (msg) {
  // Set old lat and lon
  this.lastLat = this.lat
  this.lastLon = this.lon

  // update data in the object
  // ???? this.extend(true, this, msg)
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
 * SUPPORT ZERO-FILLING NUMBERS. THIS CAN OR SHOULD
 * BE MOVED EVENTUALLY TO A BETTER PLACE.
 **************************************************/
Vehicle.prototype.zerofill = function (number, numberOfDigits) {
  // Set return value.
  var retVal = number.toString()
  // Figure out the length of the number in digits.
  var numLen = retVal.length

  // Figure out the minimum size of the number.
  if (numLen < numberOfDigits) {
    // Add zeros.
    for (var i = 0; i < (numberOfDigits - numLen); i++) {
      // Prepend a string zero.
      retVal = '0' + retVal
    }
  }

  return retVal
}

/***************************************************
 * VEHICLE DESTRUCTOR
 **************************************************/
Vehicle.prototype.destroy = function () {
  console.log('Destroying vehicle: ' + this.parseName())

  // Remove table entries
  //  $('#' + this.addr + '-row-summary').remove()
  //  $('#' + this.addr + '-row-detail').remove()

  //   // Default destructor processes
  //   if (this.info !== null) {
  //     map.removeLayer(this.info)
  //   }

  //   if (map.hasLayer(this.pathPoly)) {
  //     map.removeLayer(this.pathPoly)
  //   }

//   if (map.hasLayer(this.marker)) {
//     map.removeLayer(this.marker)
//   }
}

/***************************************************
 * FUNCTION SETS THE ICON TO HALFLIFE, SETS INACTIVE
 **************************************************/
Vehicle.prototype.setHalflife = function () {
  // Deactivate vehicle and change the icon for it.
  this.active = false
  // Set the icon.
  console.log('TODO FIXME set icon for idle / greyed')
  if (this.marker) {
    this.marker.setIcon(this.createIcon())
  }
}

/***************************************************
 * FUNCTION DETERMINES IF A VEHICLE SHOULD BE
 * SET TO HALFLIFE, EXPIRED, OR REMAIN ACTIVE
 **************************************************/
Vehicle.prototype.checkExpiration = function () {
  // Compute the time delta
  const vehDelta = Date.now() - this.lastUpdate
  // Return Active, Halflife, or Expired
  if (vehDelta >= this.maxAge) {
    return ('Expired')
  } else if ((vehDelta >= (this.maxAge / 2)) && (this.active === true)) {
    // Set to inactive animation.
    this.spinState = spinnerAnim.length - 1
    return ('Halflife')
  } else {
    return ('Active')
  }
}
