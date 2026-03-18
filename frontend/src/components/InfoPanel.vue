<script setup lang="ts">
import type { ParkingLot, RoadSection } from '../api'

defineProps<{
  lots: ParkingLot[]
  sections: RoadSection[]
  loading: boolean
  error: string | null
}>()
</script>

<template>
  <aside class="info-panel">
    <h2>台中停車場即時資訊</h2>

    <div v-if="loading" class="status">載入中…</div>
    <div v-else-if="error" class="status error">{{ error }}</div>
    <div v-else class="summary">
      <div class="stat">
        <span class="label">路外停車場</span>
        <span class="value">{{ lots.length }}</span>
      </div>
      <div class="stat">
        <span class="label">路邊停車路段</span>
        <span class="value">{{ sections.length }}</span>
      </div>
    </div>

    <div class="legend">
      <div class="legend-item">
        <span class="dot green" /> 充裕（≥50%）
      </div>
      <div class="legend-item">
        <span class="dot amber" /> 緊張（20–50%）
      </div>
      <div class="legend-item">
        <span class="dot red" /> 接近滿位（&lt;20%）
      </div>
      <div class="legend-item">
        <span class="dot gray" /> 無資料
      </div>
    </div>

    <p class="hint">每 30 秒自動更新</p>
  </aside>
</template>

<style scoped>
.info-panel {
  width: 220px;
  padding: 16px;
  background: #1e293b;
  color: #e2e8f0;
  display: flex;
  flex-direction: column;
  gap: 16px;
  font-size: 14px;
}
h2 { font-size: 15px; font-weight: 600; margin: 0; }
.status { color: #94a3b8; }
.status.error { color: #f87171; }
.summary { display: flex; flex-direction: column; gap: 8px; }
.stat { display: flex; justify-content: space-between; }
.label { color: #94a3b8; }
.value { font-weight: 600; }
.legend { display: flex; flex-direction: column; gap: 6px; }
.legend-item { display: flex; align-items: center; gap: 8px; }
.dot {
  width: 12px; height: 12px; border-radius: 50%; flex-shrink: 0;
}
.dot.green  { background: #22c55e; }
.dot.amber  { background: #f59e0b; }
.dot.red    { background: #ef4444; }
.dot.gray   { background: #9ca3af; }
.hint { color: #64748b; font-size: 12px; margin: 0; }
</style>
