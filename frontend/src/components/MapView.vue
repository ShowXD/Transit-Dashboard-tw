<script setup lang="ts">
import L from 'leaflet'
import { onMounted, onUnmounted, watch } from 'vue'
import type { ParkingLot, RoadSection } from '../api'

const props = defineProps<{
  lots: ParkingLot[]
  sections: RoadSection[]
}>()

// Taichung city center
const DEFAULT_LAT = 24.147
const DEFAULT_LON = 120.674

let map: L.Map | null = null
const lotLayer = L.layerGroup()
const sectionLayer = L.layerGroup()

function availabilityColor(available: number | null, total: number | null): string {
  if (available === null || total === null || total === 0) return '#9ca3af' // gray
  const ratio = available / total
  if (ratio >= 0.5) return '#22c55e'  // green
  if (ratio >= 0.2) return '#f59e0b'  // amber
  return '#ef4444'                     // red
}

function renderLots() {
  lotLayer.clearLayers()
  for (const lot of props.lots) {
    if (lot.lat === null || lot.lon === null) continue
    const color = availabilityColor(lot.available_spaces, lot.total_spaces)
    L.circleMarker([lot.lat, lot.lon], {
      radius: 10,
      color,
      fillColor: color,
      fillOpacity: 0.85,
      weight: 2,
    })
      .bindPopup(
        `<b>${lot.name}</b><br>` +
        `可用：${lot.available_spaces ?? '—'} / ${lot.total_spaces ?? '—'}<br>` +
        `${lot.address ?? ''}<br>` +
        `<small>${lot.charge_description ?? ''}</small>`,
      )
      .addTo(lotLayer)
  }
}

function renderSections() {
  sectionLayer.clearLayers()
  for (const s of props.sections) {
    if (s.lat === null || s.lon === null) continue
    const color = availabilityColor(s.available_spaces, s.total_spaces)
    L.circleMarker([s.lat, s.lon], {
      radius: 7,
      color,
      fillColor: color,
      fillOpacity: 0.75,
      weight: 2,
    })
      .bindPopup(
        `<b>${s.road_name}${s.section_name ? ' ' + s.section_name : ''}</b><br>` +
        `可用：${s.available_spaces ?? '—'} / ${s.total_spaces ?? '—'}`,
      )
      .addTo(sectionLayer)
  }
}

onMounted(() => {
  map = L.map('map').setView([DEFAULT_LAT, DEFAULT_LON], 14)
  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '© OpenStreetMap contributors',
    maxZoom: 19,
  }).addTo(map)
  lotLayer.addTo(map)
  sectionLayer.addTo(map)
  renderLots()
  renderSections()
})

onUnmounted(() => map?.remove())

watch(() => props.lots, renderLots)
watch(() => props.sections, renderSections)
</script>

<template>
  <div id="map" style="width: 100%; height: 100%" />
</template>
