import L from 'leaflet'
import Vue from 'vue'

export default {
  state: {
    aisVehicles: [],
    countAisVehicles: 0
  },
  mutations: {
    'saveVehicle' (state, data) {
      if (data.type === 'airAIS' && data.addr) {
        const vehName = 'veh' + data.addr
        let createMarker = false
        if (!state.aisVehicles[vehName] && !!data.lat && !!data.lon) {
          createMarker = true
        }
        // We can't uses object[index] = thing or Vue won't be able to detect the change
        Vue.set(state.aisVehicles, vehName, data)
        state.aisVehicles[vehName].lastUpdate = Date.now()
        state.aisVehicles[vehName].showMarker = (!!data.lat && !!data.lon)
        state.countAisVehicles = Object.keys(state.aisVehicles).length
        if (createMarker) {
          state.aisVehicles[vehName].latlng = L.latLng([data.lat, data.lon])
        }
      } else if (data.type === 'airSSR') {
        console.error('airSSR not handled')
      } else {
        console.error(`message type ${data.type} is not handled`)
      }
    }
  },
  getters: {
    mapMarkers: state => {
      return Object.values(state.aisVehicles).filter(x => x.showMarker)
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
