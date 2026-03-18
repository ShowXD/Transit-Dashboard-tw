import { onUnmounted, ref } from 'vue'
import { fetchLots, fetchRoadSections, type ParkingLot, type RoadSection } from '../api'

const POLL_INTERVAL_MS = 30_000

export function useParkingData(lat?: number, lon?: number) {
  const lots = ref<ParkingLot[]>([])
  const sections = ref<RoadSection[]>([])
  const loading = ref(false)
  const error = ref<string | null>(null)

  async function refresh() {
    loading.value = true
    error.value = null
    try {
      const [lotsRes, sectionsRes] = await Promise.all([
        fetchLots(lat, lon),
        fetchRoadSections(lat, lon),
      ])
      lots.value = lotsRes.data
      sections.value = sectionsRes.data
    } catch (e) {
      error.value = e instanceof Error ? e.message : 'Unknown error'
    } finally {
      loading.value = false
    }
  }

  refresh()
  const timer = setInterval(refresh, POLL_INTERVAL_MS)
  onUnmounted(() => clearInterval(timer))

  return { lots, sections, loading, error, refresh }
}
