<template>

  <div style="height: 500px; width: 100%">
    <l-map
      :zoom="zoom"
      :center="center"
      :options="mapOptions"
      @update:center="centerUpdate"
      @update:zoom="zoomUpdate"
      @update:bounds="boundsUpdated"
      id="map"
    >
      <l-tile-layer
        :url="url"
        :attribution="attribution"
      />
      <l-marker v-for="marker in markers" :lat-lng="marker.latlng" :key="marker.addr" :icon="marker.icon">
        <l-popup>{{marker.addr}}</l-popup>
      </l-marker>
      <l-marker v-for="marker in ssrMarkers" :lat-lng="marker.latlng" :key="marker.addr">
        <l-popup>{{marker.addr}}</l-popup>
      </l-marker>
    </l-map>
  </div>
</template>

<script>
import logger from '@/logging'

import { latLng } from 'leaflet'

export default {
  name: 'Home',
  components: {
  },
  data () {
    return {
      zoom: 10,
      center: latLng(49.432413, 0.164795),
      url: 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
      attribution:
        '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors',
      currentZoom: 10,
      currentCenter: latLng(49.432413, 0.164795),
      bounds: null,
      mapOptions: {
        zoomSnap: 0.5
      },
      purgeVehiclesPoller: null
    }
  },
  computed: {
    markers () {
      return this.$store.getters.mapMarkers
    },
    ssrMarkers () {
      return this.$store.getters.ssrMarkers
    }
  },
  created () {
    logger.default.info('Setting up the vehicle purge poller')
    // this.purgeVehiclesPoller = setInterval(() => {
    //   this.purgeVehicles()
    // }, 10000) // 5s
  },
  beforeDestroy () {
    clearInterval(this.purgeVehiclesPoller)
    logger.default.info('Vehicle purge poller deactivated')
  },
  methods: {
    purgeVehicles () {
      for (var key in this.$store.state.vehicles) {
        if (this.$store.state.vehicles[key] != null) {
          switch (this.$store.state.vehicles[key].checkExpiration()) {
            case 'HalfLife':
              console.log('half life for object id', key)
              this.$store.state.vehicles[key].setHalfLife()
              break
            case 'Expired':
              console.log('expired vehicle id', key)
              this.$store.state.vehicles.aisVehicles.splice(key, 1)
              break
            default:
              break
          }
        }
      }
    },
    zoomUpdate (zoom) {
      this.currentZoom = zoom
    },
    centerUpdate (center) {
      this.currentCenter = center
    },
    boundsUpdated (bounds) {
      this.bounds = bounds
    }
  }
}
</script>
