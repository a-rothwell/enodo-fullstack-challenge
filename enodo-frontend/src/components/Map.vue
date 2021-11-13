<template>
  <div style="height: 100%; width: 100%">
    <l-map style="height: 100%; width: 100%" :zoom="zoom" :center="center" @update:zoom="zoomUpdated"
      @update:center="centerUpdated" @update:bounds="boundsUpdated">
      <l-tile-layer :url="url" :attribution="attribution"></l-tile-layer>
      <template>
        <l-marker v-for="(marker, index) in markers" :lat-lng="marker['lat-long']" :key="index">
          <l-popup>{{marker['property']}}</l-popup>
        </l-marker>
      </template>
    </l-map>
  </div>
</template>

<script>
  export default {
    name: 'Map',
    data() {
      return {
        url: 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
        attribution: '&copy; <a target="_blank" href="http://osm.org/copyright">OpenStreetMap</a> contributors',
        zoom: 12,
        center: [41.8781, -87.6298],
        bounds: null,
        markers: [],
      };
    },
    methods: {
      zoomUpdated(zoom) {
        this.zoom = zoom;
      },
      centerUpdated(center) {
        this.center = center;
      },
      boundsUpdated(bounds) {
        this.bounds = bounds;
      }
    },
    mounted() {
      this.$root.$on('add_marker', data => {
        this.markers.push(data)
      });
      this.$root.$on('remove_marker', data => {
        this.markers = this.markers.filter(marker => marker["lat-long"][0] != data["lat"] && marker["lat-long"][
          1] != data["long"])
      });
    }
  }
</script>