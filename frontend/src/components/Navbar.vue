<script setup lang="ts">
defineProps<{ loading: boolean; lastUpdated: Date | null; sidebarOpen: boolean }>()
defineEmits<{ refresh: []; toggleSidebar: [] }>()
</script>

<template>
  <header class="navbar">
    <button class="toggle-btn" :title="sidebarOpen ? '收起側欄' : '展開側欄'" @click="$emit('toggleSidebar')">
      <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
        <rect x="3" y="3" width="18" height="18" rx="2"/>
        <path d="M9 3v18"/>
        <path v-if="sidebarOpen" d="M5 9l-2 3 2 3"/>
        <path v-else d="M13 9l2 3-2 3"/>
      </svg>
    </button>
    <div class="brand">
      <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
        <circle cx="12" cy="12" r="10"/><path d="M12 8v4l3 3"/>
      </svg>
      <span>台中停車場即時儀表板</span>
    </div>
    <div class="controls">
      <span v-if="lastUpdated" class="updated">
        更新：{{ lastUpdated.toLocaleTimeString('zh-TW', { hour: '2-digit', minute: '2-digit', second: '2-digit' }) }}
      </span>
      <button class="refresh-btn" :disabled="loading" @click="$emit('refresh')">
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"
          :style="loading ? 'animation: spin 1s linear infinite' : ''">
          <path d="M23 4v6h-6M1 20v-6h6"/><path d="M3.51 9a9 9 0 0 1 14.85-3.36L23 10M1 14l4.64 4.36A9 9 0 0 0 20.49 15"/>
        </svg>
        {{ loading ? '更新中' : '重新整理' }}
      </button>
    </div>
  </header>
</template>

<style scoped>
.toggle-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 36px;
  height: 36px;
  background: transparent;
  border: 1px solid #334155;
  border-radius: 6px;
  color: #94a3b8;
  cursor: pointer;
  flex-shrink: 0;
  transition: all 0.15s;
  margin-right: 4px;
}
.toggle-btn:hover { background: #1e293b; color: #f1f5f9; }
.navbar {
  height: 56px;
  background: #0f172a;
  border-bottom: 1px solid #1e293b;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 20px;
  flex-shrink: 0;
  z-index: 1000;
}
.brand {
  display: flex;
  align-items: center;
  gap: 10px;
  color: #f1f5f9;
  font-size: 15px;
  font-weight: 600;
}
.controls {
  display: flex;
  align-items: center;
  gap: 16px;
}
.updated {
  font-size: 12px;
  color: #64748b;
}
.refresh-btn {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 6px 14px;
  background: #1e293b;
  border: 1px solid #334155;
  border-radius: 6px;
  color: #94a3b8;
  font-size: 13px;
  cursor: pointer;
  transition: all 0.15s;
}
.refresh-btn:hover:not(:disabled) {
  background: #334155;
  color: #f1f5f9;
}
.refresh-btn:disabled { opacity: 0.5; cursor: default; }
@keyframes spin { to { transform: rotate(360deg); } }
</style>
