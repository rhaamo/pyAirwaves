<template>

  <div style="height: 500px; width: 100%">
    <l-map
      :zoom="zoom"
      :center="center"
      :options="mapOptions"
      @update:center="centerUpdate"
      @update:zoom="zoomUpdate"
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
      mapOptions: {
        zoomSnap: 0.5
      },
      purgeVehiclesPoller: null
    }
  },
  computed: {
    markers () {
      return this.$store.state.vehicles.markers
    }
  },
  created () {
    console.log('setting up the purge vehicules poller')
    this.purgeVehiclesPoller = setInterval(() => {
      this.purgeVehicles()
    }, 1000)
  },
  beforeDestroy () {
    clearInterval(this.purgeVehiclesPoller)
  },
  methods: {
    purgeVehicles () {
      console.log('purgeVehicles running')
      for (const [address, vehicle] of Object.entries(this.$store.state.vehicles.aisVehicles)) {
        // Compute the time delta
        const vehDelta = Date.now() - vehicle.lastUpdate
        if (vehDelta >= 1000) {
          console.log(`Vehicle ${vehicle.addr} Expired`)
          // remove from markers
          for (const markerIndex in this.$store.state.vehicles.markers) {
            const marker = this.$store.state.vehicles.markers[markerIndex]
            if (String(marker.addr) === address) {
              console.log(`we have to delete marker index ${markerIndex}`)
              this.$store.state.vehicles.markers.splice(markerIndex, 1)
            }
          }
          // remove from vehicles
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
    innerClick () {
      alert('Click!')
    }
  }
}
</script>
