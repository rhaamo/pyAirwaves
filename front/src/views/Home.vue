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
      <l-marker v-for="marker in markers" :lat-lng="marker.latlng" :key="marker.addr"></l-marker>
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
      // return this.$store.state.vehicles.markers
      return this.$store.getters.mapMarkers
    }
  },
  created () {
    logger.default.info('Setting up the vehicle purge poller')
    this.purgeVehiclesPoller = setInterval(() => {
      this.purgeVehicles()
    }, 5000) // 5s
  },
  beforeDestroy () {
    clearInterval(this.purgeVehiclesPoller)
    logger.default.info('Vehicle purge poller deactivated')
  },
  methods: {
    purgeVehicles () {
      for (const [address, vehicle] of Object.entries(this.$store.state.vehicles.aisVehicles)) {
        // Compute the time delta
        const vehDelta = Date.now() - vehicle.lastUpdate
        if (vehDelta >= 1000) {
          logger.default.info(`Vehicle ${address} Expired`)
          // remove vehicle
          delete this.$store.state.vehicles.aisVehicles[address]
        } else {
          return
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
