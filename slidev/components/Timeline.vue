<script setup lang="ts">
import { computed } from 'vue'

const props = withDefaults(defineProps<{
  name: string
  unit: string
  start: number
  count: number
  highlights?: number[]
  chunks?: number[][]
}>(), {
  highlights: () => [],
  chunks: () => [],
})

// Generate tick values from start and count
const ticks = computed(() => {
  return Array.from({ length: props.count }, (_, i) => props.start + i)
})

// Check if a value is highlighted
const isHighlighted = (value: number) => props.highlights.includes(value)

// Get the click index for a given value (for v-click directive)
// Returns the 1-based click index (v-click directive uses 1-based)
const getClickIndex = (value: number): number | undefined => {
  if (props.chunks.length === 0) return undefined
  const index = props.chunks.findIndex(chunk => chunk.includes(value))
  return index >= 0 ? index + 1 : undefined
}
</script>

<template>
  <div class="timeline-container">
    <div class="timeline-name">{{ name }}</div>
    <div class="timeline-line-container">
      <div class="timeline-line" />
      <div class="timeline-ticks">
        <!-- With chunks: progressive reveal -->
        <template v-if="chunks.length > 0">
          <div
            v-for="tick in ticks"
            :key="tick"
            class="timeline-tick-wrapper"
            v-click="getClickIndex(tick)"
          >
            <div :class="['timeline-tick', { highlighted: isHighlighted(tick) }]" />
            <div :class="['timeline-label', { highlighted: isHighlighted(tick) }]">
              {{ tick }}{{ unit }}
            </div>
          </div>
        </template>
        <!-- Without chunks: show all immediately -->
        <template v-else>
          <div
            v-for="tick in ticks"
            :key="tick"
            class="timeline-tick-wrapper"
          >
            <div :class="['timeline-tick', { highlighted: isHighlighted(tick) }]" />
            <div :class="['timeline-label', { highlighted: isHighlighted(tick) }]">
              {{ tick }}{{ unit }}
            </div>
          </div>
        </template>
      </div>
    </div>
  </div>
</template>

<style scoped>
.timeline-container {
  position: relative;
  width: 100%;
  padding: 1rem 0 1.5rem 0;
}

.timeline-name {
  font-size: 0.875rem;
  font-weight: 600;
  color: #888;
  margin-bottom: 0.5rem;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.timeline-line-container {
  position: relative;
  width: 100%;
  height: 50px;
}

.timeline-line {
  position: absolute;
  top: 8px; /* Half of tick height (16px / 2) to center line on ticks */
  left: 0;
  right: 0;
  height: 3px;
  background: #555;
}

/* Arrow heads */
.timeline-line::before,
.timeline-line::after {
  content: '';
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  border: 6px solid transparent;
}

.timeline-line::before {
  left: -10px;
  border-right: 10px solid #555;
}

.timeline-line::after {
  right: -10px;
  border-left: 10px solid #555;
}

.timeline-ticks {
  position: relative;
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  height: 100%;
  padding: 0 2rem;
}

.timeline-tick-wrapper {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.5rem;
  z-index: 1;
}

/* Pop animation for v-click reveals */
.timeline-tick-wrapper.slidev-vclick-target {
  transition: all 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
}

.timeline-tick-wrapper.slidev-vclick-hidden {
  opacity: 0;
  transform: scale(0);
}

.timeline-tick-wrapper.slidev-vclick-current,
.timeline-tick-wrapper.slidev-vclick-prior {
  opacity: 1;
  transform: scale(1);
}

.timeline-tick {
  width: 16px;
  height: 16px;
  border-radius: 50%;
  background: #fff;
  border: 3px solid #555;
  flex-shrink: 0;
}

.timeline-tick.highlighted {
  background: #ff6b35;
  border-color: #ff6b35;
  box-shadow: 0 0 12px rgba(255, 107, 53, 0.6);
}

.timeline-label {
  font-size: 0.9rem;
  font-weight: 500;
  color: #ccc;
  font-family: ui-monospace, monospace;
}

.timeline-label.highlighted {
  color: #ff6b35;
  font-weight: 700;
}
</style>
