import Vue from 'vue'
import L from 'leaflet'

import BoatIcon from '../markers/boat'
import PlaneIcon from '../markers/plane'
import Ship from '../structs/airAIS'
import Aircraft from '../structs/airSSR'

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
          Vue.set(state.vehicles, vehName, newShip) // reactive insert
          if (state.vehicles[vehName].lat && state.vehicles[vehName].lon) {
            // We have latitude and longitude, show marker
            state.vehicles[vehName].marker = true
            state.vehicles[vehName].latlng = L.latLng([data.lat, data.lon])
            if (state.vehicles[vehName].courseOverGnd) {
              state.vehicles[vehName].icon = new BoatIcon({
                color: '#f4ff01',
                idleCircle: false,
                course: data.courseOverGnd
              })
              state.vehicles[vehName].icon.setHeading(data.courseOverGnd)
            } else {
              state.vehicles[vehName].icon = new BoatIcon({
                color: '#f4ff01',
                idleCircle: false
              })
            }
          } else {
            state.vehicles[vehName].marker = false
          }
        }
      } else if (data.type === 'airSSR') {
        const vehName = 'veh' + String(data.addr)
        if (vehName in state.vehicles && state.vehicles[vehName] != null) {
          console.log(vehName, 'already exists')
          // existing vehicle, call update function
          state.vehicles[vehName].update(data)
        } else {
          console.log(vehName, 'does not exists')
          // new vehicle, call the constructor
          const newAircraft = new Aircraft(data)
          Vue.set(state.vehicles, vehName, newAircraft) // reactive insert
          if (state.vehicles[vehName].lat && state.vehicles[vehName].lon) {
            // We have latitude and longitude, show marker
            state.vehicles[vehName].marker = true
            state.vehicles[vehName].latlng = L.latLng([data.lat, data.lon])
            state.vehicles[vehName].icon = new PlaneIcon({
              color: '#f4ff01',
              idleCircle: false,
              course: data.heading
            })
            state.vehicles[vehName].icon.setHeading(data.heading)
          } else {
            state.vehicles[vehName].marker = false
          }
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
