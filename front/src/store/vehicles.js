export default {
  state: {

  },
  actions: {
    'SOCKET_oops' (state, server) {
      console.log('oops', server)
    },
    'SOCKET_success' (state, server) {
      console.log('success', server)
    },
    'SOCKET_info' (state, server) {
      console.log('info', server)
    },
    'SOCKET_message' (state, server) {
      console.log('message received, pls handle')
    }
  }
}
