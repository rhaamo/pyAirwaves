import L from 'leaflet'
import Vue from 'vue'

import BoatIcon from '../markers/boat'
import Ship from '../structs/airAIS'

export default {
  state: {
    countSsrVehicles: 0,
    ssrVehicles: [],
    vehicles: []
  },
  mutations: {
    'saveVehicle' (state, data) {
      if (data.type === 'airAIS' && data.addr) {
        const vehName = 'veh' + String(data.addr)
        if (vehName in state.vehicles && state.vehicles[vehName] != null) {
          console.log(vehName, 'already exists')
          // existing vehicle, call update function
          state.vehicles[vehName].update(data)
        } else {
          console.log(vehName, 'does not exists')
          // new vehicle, call the constructor
          const newShip = new Ship(data)
          console.log('new ship', newShip)
          Vue.set(state.vehicles, vehName, newShip) // reactive insert
          if (state.vehicles[vehName].lat && state.vehicles[vehName].lon) {
            // We have latitude and longitude, show marker
            state.vehicles[vehName].marker = true
            state.vehicles[vehName].latlng = L.latLng([data.lat, data.lon])
            state.vehicles[vehName].icon = new BoatIcon({
              color: '#f4ff01',
              idleCircle: false,
              course: data.courseOverGnd
            })
            state.vehicles[vehName].icon.setHeading(data.courseOverGnd)
          } else {
            state.vehicles[vehName].marker = false
          }
        }
      } else if (data.type === 'airSSR') {
        const vehName = 'veh' + data.addr
        let createMarker = false
        if (!state.ssrVehicles[vehName] && !!data.lat && !!data.lon) {
          createMarker = true
        }
        // We can't uses object[index] = thing or Vue won't be able to detect the change
        Vue.set(state.ssrVehicles, vehName, data)
        state.ssrVehicles[vehName].lastUpdate = Date.now()
        state.ssrVehicles[vehName].showMarker = (!!data.lat && !!data.lon)
        state.countSsrVehicles = Object.keys(state.ssrVehicles).length
        if (createMarker) {
          state.ssrVehicles[vehName].latlng = L.latLng([data.lat, data.lon])
        }
      } else {
        console.error(`message type ${data.type} is not handled`)
      }
    }
  },
  getters: {
    mapMarkers: state => {
      return Object.values(state.vehicles).filter(x => x.marker)
    },
    ssrMarkers: state => {
      return Object.values(state.ssrVehicles).filter(x => x.showMarker)
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
