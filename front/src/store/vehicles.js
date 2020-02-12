import L from 'leaflet'

export default {
  state: {
    aisVehicles: {},
    countAisVehicles: 0,
    markers: []
  },
  mutations: {
    'saveVehicle' (state, data) {
      if (data.type === 'airAIS') {
        let createMarker = false
        if (!state.aisVehicles[data.addr] && data.lat && data.lon) {
          createMarker = true
        }
        // beware, data.addr is a string in the dict
        state.aisVehicles[data.addr] = data
        state.aisVehicles[data.addr].lastUpdate = Date.now()
        state.countAisVehicles = Object.keys(state.aisVehicles).length
        if (createMarker) {
          state.markers.push({ addr: data.addr, latlng: L.latLng([data.lat, data.lon]) })
        }
      } else if (data.type === 'airSSR') {
        console.error('airSSR not handled')
      } else {
        console.error(`message type ${data.type} is not handled`)
      }
    }
  },
  actions: {
    'SOCKET_message' ({ dispatch, commit }, payload) {
      commit('saveVehicle', payload)
    },
    'SOCKET_oops' (state, server) {
      console.log('oops', server)
    },
    'SOCKET_success' (state, server) {
      console.log('success', server)
    },
    'SOCKET_info' (state, server) {
      console.log('info', server)
    }
  }
}
