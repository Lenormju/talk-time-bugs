<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'

const ribbonRef = ref<HTMLElement | null>(null)

const CELL_WIDTH = 76

function onWheel(e: WheelEvent) {
  if (!ribbonRef.value) return
  e.preventDefault()
  ribbonRef.value.scrollLeft += e.deltaY
}

onUnmounted(() => {
  ribbonRef.value?.removeEventListener('wheel', onWheel)
})

// Simple date arithmetic over Sep / Oct / Nov (all we need for 1582)
const DAYS_IN: Record<string, number> = { Sep: 30, Oct: 31, Nov: 30 }
const MONTH_ORDER = ['Sep', 'Oct', 'Nov']

function addDays(month: string, day: number, delta: number): { month: string; day: number } {
  let m = month
  let d = day + delta
  while (d > DAYS_IN[m]) {
    d -= DAYS_IN[m]
    m = MONTH_ORDER[MONTH_ORDER.indexOf(m) + 1]
  }
  return { month: m, day: d }
}

// 30 days starting from Julian Sep 20 (Gregorian Sep 30 = Sep 20 + 10)
const TOTAL_DAYS = 30
const JULIAN_START  = { month: 'Sep', day: 20 }
const GREG_START    = { month: 'Sep', day: 30 }

// Transition: Julian Oct 4 is at offset 14 from Sep 20
const TRANSITION_IDX = 14

const columns = Array.from({ length: TOTAL_DAYS }, (_, i) => ({
  julian:     addDays(JULIAN_START.month, JULIAN_START.day, i),
  gregorian:  addDays(GREG_START.month,  GREG_START.day,   i),
  highlight:  i === TRANSITION_IDX ? 'last' : i === TRANSITION_IDX + 1 ? 'first' : null,
}))

onMounted(() => {
  if (ribbonRef.value) {
    const transitionCol = ribbonRef.value.querySelector<HTMLElement>('.col-last')
    if (transitionCol) {
      transitionCol.scrollIntoView({ inline: 'center', block: 'nearest' })
    } else {
      ribbonRef.value.scrollLeft = (TRANSITION_IDX - 2) * CELL_WIDTH
    }
    ribbonRef.value.addEventListener('wheel', onWheel, { passive: false })
  }
})
</script>

<template>
  <div class="wrapper">
    <!-- Fixed label column -->
    <div class="labels">
      <div class="label">Julien</div>
      <div class="row-divider" />
      <div class="label">Grégorien</div>
    </div>

    <!-- Scrollable day ribbon -->
    <div ref="ribbonRef" class="ribbon-container">
      <div class="ribbon">
        <div
          v-for="(col, i) in columns"
          :key="i"
          :class="['column', col.highlight && `col-${col.highlight}`]"
        >
          <!-- Julian cell -->
          <div class="cell">
            <span class="month">{{ col.julian.month }}</span>
            <span class="day">{{ col.julian.day }}</span>
          </div>

          <!-- Row divider inside column -->
          <div class="cell-divider" />

          <!-- Gregorian cell -->
          <div class="cell">
            <span class="month">{{ col.gregorian.month }}</span>
            <span class="day">{{ col.gregorian.day }}</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.wrapper {
  display: flex;
  flex-direction: row;
  height: 110px;
  border: 1px solid #d0d0d0;
  border-radius: 8px;
  overflow: hidden;
  background: #f8f8f8;
  font-family: ui-monospace, 'Cascadia Code', 'JetBrains Mono', monospace;
}

/* ── Labels ─────────────────────────────────────────────── */
.labels {
  display: flex;
  flex-direction: column;
  flex-shrink: 0;
  width: 112px;
  border-right: 1px solid #d0d0d0;
  background: #f0f0f0;
}

.label {
  flex: 1;
  display: flex;
  align-items: center;
  padding: 0 16px;
  font-size: 0.78rem;
  font-weight: 600;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: #777;
}

.row-divider {
  height: 1px;
  background: #d0d0d0;
  flex-shrink: 0;
}

/* ── Ribbon ──────────────────────────────────────────────── */
.ribbon-container {
  flex: 1;
  overflow-x: auto;
  overflow-y: hidden;
  scrollbar-width: thin;
  scrollbar-color: #bbb transparent;
}

.ribbon-container::-webkit-scrollbar {
  height: 4px;
}
.ribbon-container::-webkit-scrollbar-track {
  background: transparent;
}
.ribbon-container::-webkit-scrollbar-thumb {
  background: #bbb;
  border-radius: 2px;
}

.ribbon {
  display: flex;
  flex-direction: row;
  height: 100%;
}

/* ── Columns ─────────────────────────────────────────────── */
.column {
  display: flex;
  flex-direction: column;
  flex-shrink: 0;
  width: 76px;
  border-right: 1px solid #e0e0e0;
  transition: background 0.2s;
}

.column:last-child {
  border-right: none;
}

/* Last Julian day — warm amber tint */
.col-last {
  background: rgba(245, 158, 11, 0.12);
}

.col-last .month {
  color: #c07800;
}

.col-last .day {
  color: #c07800;
}

/* First Gregorian day — orange, strong */
.col-first {
  background: rgba(255, 107, 53, 0.1);
  border-left: 2px solid #ff6b35;
}

.col-first .month {
  color: #e04800;
}

.col-first .day {
  color: #e04800;
}

/* ── Cells ───────────────────────────────────────────────── */
.cell {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 1px;
}

.cell-divider {
  height: 1px;
  background: #e0e0e0;
  flex-shrink: 0;
}

.month {
  font-size: 0.62rem;
  letter-spacing: 0.06em;
  color: #aaa;
  text-transform: uppercase;
}

.day {
  font-size: 1.15rem;
  font-weight: 700;
  color: #333;
  line-height: 1;
}
</style>
