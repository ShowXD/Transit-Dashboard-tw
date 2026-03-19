<script setup lang="ts">
import { ref } from 'vue'
import InfoPanel from '../components/InfoPanel.vue'
import MapView from '../components/MapView.vue'
import Navbar from '../components/Navbar.vue'
import { useParkingData } from '../composables/useParkingData'

const { lots, sections, loading, error, refresh } = useParkingData()
const lastUpdated = ref<Date | null>(null)
const sidebarOpen = ref(true)

async function handleRefresh() {
  await refresh()
  lastUpdated.value = new Date()
}
</script>

<template>
  <div class="layout">
    <Navbar :loading="loading" :last-updated="lastUpdated" :sidebar-open="sidebarOpen" @refresh="handleRefresh" @toggle-sidebar="sidebarOpen = !sidebarOpen" />
    <div class="body">
      <InfoPanel :lots="lots" :sections="sections" :error="error" :collapsed="!sidebarOpen" />
      <MapView :lots="lots" :sections="sections" />
    </div>
  </div>
</template>

<style scoped>
.layout {
  display: flex;
  flex-direction: column;
  height: 100vh;
  width: 100vw;
  overflow: hidden;
}
.body {
  display: flex;
  flex: 1;
  overflow: hidden;
}
</style>
