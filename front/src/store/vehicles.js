export default {
  state: {
    aisVehicles: {},
    countAisVehicles: 0
  },
  mutations: {
    'saveVehicle' (state, data) {
      if (data.type === 'airAIS') {
        state.aisVehicles[data.addr] = data
        state.countAisVehicles = Object.keys(state.aisVehicles).length
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
      dispatch('/Home/addMarker', payload)
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
