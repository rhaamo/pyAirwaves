import Vue from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import { LMap, LTileLayer, LMarker } from 'vue2-leaflet'
import 'leaflet/dist/leaflet.css'
import VueSocketIO from 'vue-socket.io'

Vue.config.productionTip = false

Vue.component('l-map', LMap)
Vue.component('l-tile-layer', LTileLayer)
Vue.component('l-marker', LMarker)

Vue.use(new VueSocketIO({
  debug: false,
  connection: 'http://192.168.10.167:5000/',
  vuex: {
    store,
    actionPrefix: 'SOCKET_'
  },
  options: {}
}))

new Vue({
  router,
  store,
  render: h => h(App),
  sockets: {
    connect: function () {
      console.log('webchaussette connected')
    },
    disconnect: function () {
      console.log('webchaussette disconnected')
    },
    message: function (data) {
      // console.log('message can be handled from there too...')
    }
  }
}).$mount('#app')
