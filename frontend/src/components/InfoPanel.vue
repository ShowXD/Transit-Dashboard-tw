<script setup lang="ts">
import type { ParkingLot, RoadSection } from '../api'

const props = defineProps<{
  lots: ParkingLot[]
  sections: RoadSection[]
  error: string | null
  collapsed: boolean
}>()

function availRatio(available: number | null, total: number | null): number | null {
  if (available === null || total === null || total === 0) return null
  return available / total
}

function statusClass(lot: ParkingLot): string {
  const r = availRatio(lot.available_spaces, lot.total_spaces)
  if (r === null) return 'gray'
  if (r >= 0.5) return 'green'
  if (r >= 0.2) return 'amber'
  return 'red'
}
</script>

<template>
  <aside class="sidebar" :class="{ collapsed }">
    <div v-if="error" class="error-banner">{{ error }}</div>

    <!-- 統計卡片 -->
    <div class="stats-grid">
      <div class="stat-card">
        <div class="stat-value">{{ lots.length }}</div>
        <div class="stat-label">路外停車場</div>
      </div>
      <div class="stat-card">
        <div class="stat-value">{{ sections.length }}</div>
        <div class="stat-label">路邊路段</div>
      </div>
      <div class="stat-card">
        <div class="stat-value">{{ lots.reduce((s, l) => s + (l.available_spaces ?? 0), 0) }}</div>
        <div class="stat-label">可用車位</div>
      </div>
      <div class="stat-card">
        <div class="stat-value">{{ lots.reduce((s, l) => s + (l.total_spaces ?? 0), 0) }}</div>
        <div class="stat-label">總車位</div>
      </div>
    </div>

    <!-- 圖例 -->
    <div class="section-title">車位狀態</div>
    <div class="legend">
      <div class="legend-item"><span class="dot green" /> 充裕（≥ 50%）</div>
      <div class="legend-item"><span class="dot amber" /> 緊張（20–50%）</div>
      <div class="legend-item"><span class="dot red" /> 接近滿位（&lt; 20%）</div>
      <div class="legend-item"><span class="dot gray" /> 無資料</div>
    </div>

    <!-- 停車場列表 -->
    <div class="section-title">停車場列表</div>
    <div class="lot-list">
      <div v-for="lot in lots" :key="lot.id" class="lot-item">
        <div class="lot-header">
          <span :class="['status-dot', statusClass(lot)]" />
          <span class="lot-name">{{ lot.name }}</span>
        </div>
        <div class="lot-avail">
          {{ lot.available_spaces ?? '—' }} / {{ lot.total_spaces ?? '—' }} 格
        </div>
      </div>
      <div v-if="lots.length === 0" class="empty">尚無資料</div>
    </div>
  </aside>
</template>

<style scoped>
.sidebar {
  width: 260px;
  flex-shrink: 0;
  background: #0f172a;
  border-right: 1px solid #1e293b;
  display: flex;
  flex-direction: column;
  overflow-y: auto;
  overflow-x: hidden;
  padding: 16px;
  gap: 4px;
  transition: width 0.25s ease, padding 0.25s ease;
}
.sidebar.collapsed {
  width: 0;
  padding: 0;
  border-right: none;
  overflow: hidden;
}
.error-banner {
  background: #450a0a;
  border: 1px solid #991b1b;
  color: #fca5a5;
  padding: 8px 12px;
  border-radius: 6px;
  font-size: 12px;
  margin-bottom: 8px;
}
.stats-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 8px;
  margin-bottom: 16px;
}
.stat-card {
  background: #1e293b;
  border-radius: 8px;
  padding: 12px;
  text-align: center;
}
.stat-value { font-size: 22px; font-weight: 700; color: #f1f5f9; }
.stat-label { font-size: 11px; color: #64748b; margin-top: 2px; }
.section-title {
  font-size: 11px;
  font-weight: 600;
  color: #475569;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  margin: 12px 0 8px;
}
.legend { display: flex; flex-direction: column; gap: 6px; margin-bottom: 4px; }
.legend-item { display: flex; align-items: center; gap: 8px; font-size: 13px; color: #94a3b8; }
.dot, .status-dot {
  width: 10px; height: 10px; border-radius: 50%; flex-shrink: 0;
}
.dot.green, .status-dot.green   { background: #22c55e; }
.dot.amber, .status-dot.amber   { background: #f59e0b; }
.dot.red,   .status-dot.red     { background: #ef4444; }
.dot.gray,  .status-dot.gray    { background: #475569; }
.lot-list { display: flex; flex-direction: column; gap: 2px; }
.lot-item {
  padding: 8px 10px;
  border-radius: 6px;
  cursor: default;
  transition: background 0.1s;
}
.lot-item:hover { background: #1e293b; }
.lot-header { display: flex; align-items: center; gap: 8px; }
.lot-name { font-size: 13px; color: #e2e8f0; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.lot-avail { font-size: 11px; color: #64748b; margin-top: 3px; padding-left: 18px; }
.empty { color: #475569; font-size: 13px; padding: 8px 0; }
</style>
