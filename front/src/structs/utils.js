
function toRadians (deg) {
  return deg * Math.PI / 180
}
function toDeg (rad) {
  return rad * 180 / Math.PI
}

function bearingFromTwoCoordinates (lat1, lon1, lat2, lon2) {
  console.log('Bearing from ' + lat1 + ',' + lon1 + ' to ' + lat2 + ',' + lon2)

  const startLat = toRadians(lat1)
  const startLon = toRadians(lon1)
  const destLat = toRadians(lat2)
  const destLon = toRadians(lon2)

  const y = Math.sin(destLon - startLon) * Math.cos(destLat)
  const x = Math.cos(startLat) * Math.sin(destLat) - Math.sin(startLat) * Math.cos(destLat) * Math.cos(destLon - startLon)
  let brng = Math.atan2(y, x)
  brng = toDeg(brng)
  return (brng + 360) % 360
}

const utils = {
  bearingFromTwoCoordinates
}

export default utils
