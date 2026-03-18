<script setup lang="ts">
import InfoPanel from '../components/InfoPanel.vue'
import MapView from '../components/MapView.vue'
import { useParkingData } from '../composables/useParkingData'

const { lots, sections, loading, error } = useParkingData()
</script>

<template>
  <div class="dashboard">
    <InfoPanel
      :lots="lots"
      :sections="sections"
      :loading="loading"
      :error="error"
    />
    <MapView :lots="lots" :sections="sections" />
  </div>
</template>

<style scoped>
.dashboard {
  display: flex;
  height: 100vh;
  width: 100vw;
  overflow: hidden;
}
</style>
