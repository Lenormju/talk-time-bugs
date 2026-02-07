<script setup lang="ts">
import { computed, ref, onMounted, nextTick } from 'vue'

interface TimelineDefinition {
  name: string
  unit?: string
  start?: number
  values: number[]
  highlights?: number[]
}

interface BranchDefinition {
  name: string
  splitAt: number
  values: number[]
  highlights?: number[]
}

interface TimelineReveal {
  timeline: 'main' | number
  values: number[]
}

interface ChunkDefinition {
  // New format (recommended): per-timeline values
  reveals?: TimelineReveal[]

  // Old format (deprecated but still supported): shared values
  timeline?: 'main' | number | ('main' | number)[]
  values?: number[]
}

const props = withDefaults(defineProps<{
  main: TimelineDefinition
  branches: BranchDefinition[]
  chunks?: ChunkDefinition[]
  branchSpacing?: number
}>(), {
  chunks: () => [],
  branchSpacing: 80,
})

// Refs for DOM elements
const containerRef = ref<HTMLElement | null>(null)
const mainTickRefs = ref<Record<number, HTMLElement>>({})
const branchTickRefs = ref<Record<string, HTMLElement>>({}) // key: `${branchIdx}-${value}`

// Connector positions (calculated from actual DOM positions)
interface ConnectorLine {
  x1: number
  y1: number
  x2: number
  y2: number
}
const connectorLines = ref<Record<number, ConnectorLine>>({}) // key: branchIdx

// Set ref for main tick
const setMainTickRef = (value: number) => (el: any) => {
  if (el) mainTickRefs.value[value] = el
}

// Set ref for branch tick
const setBranchTickRef = (branchIdx: number, value: number) => (el: any) => {
  if (el) branchTickRefs.value[`${branchIdx}-${value}`] = el
}

// Calculate connector positions from actual DOM elements
const updateConnectorPositions = () => {
  if (!containerRef.value) {
    console.log('No container ref')
    return
  }

  const containerRect = containerRef.value.getBoundingClientRect()
  console.log('Updating connector positions, containerRect:', containerRect)
  console.log('mainTickRefs:', mainTickRefs.value)
  console.log('branchTickRefs:', branchTickRefs.value)

  props.branches.forEach((branch, branchIdx) => {
    // Get the main timeline tick at splitAt position
    const mainTick = mainTickRefs.value[branch.splitAt]
    // Get the first tick of the branch timeline
    const branchFirstTick = branchTickRefs.value[`${branchIdx}-${branch.values[0]}`]

    console.log(`Branch ${branchIdx}: mainTick=${!!mainTick}, branchFirstTick=${!!branchFirstTick}`)

    if (mainTick && branchFirstTick) {
      const mainRect = mainTick.getBoundingClientRect()
      const branchRect = branchFirstTick.getBoundingClientRect()

      console.log(`Branch ${branchIdx} positions:`, {
        mainRect,
        branchRect,
      })

      // Calculate positions relative to container
      connectorLines.value[branchIdx] = {
        x1: mainRect.left + mainRect.width / 2 - containerRect.left,
        y1: mainRect.top + mainRect.height / 2 - containerRect.top,
        x2: branchRect.left + branchRect.width / 2 - containerRect.left,
        y2: branchRect.top + branchRect.height / 2 - containerRect.top,
      }

      console.log(`Connector line ${branchIdx}:`, connectorLines.value[branchIdx])
    } else {
      console.log(`Missing refs for branch ${branchIdx}`)
    }
  })

  console.log('Final connectorLines:', connectorLines.value)
}

// Update positions on mount and after DOM updates
onMounted(() => {
  // Try multiple times with delays to ensure elements are rendered
  setTimeout(() => updateConnectorPositions(), 100)
  setTimeout(() => updateConnectorPositions(), 500)
  setTimeout(() => updateConnectorPositions(), 1000)

  nextTick(() => {
    updateConnectorPositions()
  })

  // Watch for v-click changes and update positions
  // Use MutationObserver to detect when elements appear/disappear
  const observer = new MutationObserver(() => {
    setTimeout(() => updateConnectorPositions(), 50)
  })

  if (containerRef.value) {
    observer.observe(containerRef.value, {
      childList: true,
      subtree: true,
      attributes: true,
      attributeFilter: ['class'], // Watch for v-click class changes
    })
  }
})

// Check if a value is highlighted in a timeline
const isHighlighted = (timeline: TimelineDefinition | BranchDefinition, value: number) => {
  return timeline.highlights?.includes(value) ?? false
}

// Get the click index for a given value in a timeline
const getClickIndex = (timeline: 'main' | number, value: number): number | undefined => {
  if (!props.chunks || props.chunks.length === 0) return undefined

  const chunkIndex = props.chunks.findIndex(chunk => {
    // New format: check reveals array
    if (chunk.reveals) {
      return chunk.reveals.some(reveal =>
        reveal.timeline === timeline && reveal.values.includes(value)
      )
    }

    // Old format: backward compatibility
    if (chunk.values && chunk.timeline !== undefined) {
      if (!chunk.values.includes(value)) return false

      // Check if timeline matches
      if (Array.isArray(chunk.timeline)) {
        return chunk.timeline.includes(timeline)
      } else {
        return chunk.timeline === timeline
      }
    }

    return false
  })

  return chunkIndex >= 0 ? chunkIndex + 1 : undefined
}

// Calculate the starting position for branch timeline line
const getBranchLineStart = (branch: BranchDefinition) => {
  const splitIndex = props.main.values.indexOf(branch.splitAt)
  if (splitIndex === -1) return '0px'

  const tickCount = props.main.values.length
  const containerPadding = 2 // rem
  const position = splitIndex / (tickCount - 1)

  return `calc(${containerPadding}rem + (100% - ${containerPadding * 2}rem) * ${position})`
}

// Calculate tick position for branch timeline (absolute positioning)
const getTickPosition = (branch: BranchDefinition, tickIdx: number) => {
  const splitIndex = props.main.values.indexOf(branch.splitAt)
  const mainTickCount = props.main.values.length
  const containerPadding = 2 // rem

  // Calculate normalized position (0 to 1) on main timeline for splitAt
  const splitPosition = splitIndex / (mainTickCount - 1)

  // Calculate position for this tick relative to branch start
  const branchTickCount = branch.values.length
  if (branchTickCount === 1) {
    // Single tick - position at splitAt
    return {
      position: 'absolute' as const,
      left: `calc(${containerPadding}rem + (100% - ${containerPadding * 2}rem) * ${splitPosition})`,
    }
  }

  const tickPosition = tickIdx / (branchTickCount - 1)

  // Simplified math:
  // Final position = padding + usableWidth * finalPosition
  // finalPosition = splitPosition + (1 - splitPosition) * tickPosition
  // This spreads ticks from splitPosition to 1.0 (end)
  const finalPosition = splitPosition + (1 - splitPosition) * tickPosition

  return {
    position: 'absolute' as const,
    left: `calc(${containerPadding}rem + (100% - ${containerPadding * 2}rem) * ${finalPosition})`,
  }
}
</script>

<template>
  <div class="timeline-bifurcating-container" ref="containerRef">
    <!-- Main timeline -->
    <div class="main-timeline">
      <div class="timeline-name">{{ main.name }}</div>
      <div class="timeline-line-container">
        <div class="timeline-line" />
        <!-- Arrow head (right side only) -->
        <div class="timeline-line-arrow" />
        <div class="timeline-ticks">
          <!-- With chunks: progressive reveal -->
          <template v-if="chunks && chunks.length > 0">
            <div
              v-for="tick in main.values"
              :key="`main-${tick}`"
              class="timeline-tick-wrapper"
              v-click="getClickIndex('main', tick)"
            >
              <div
                :class="['timeline-tick', { highlighted: isHighlighted(main, tick) }]"
                :ref="setMainTickRef(tick)"
              />
              <div :class="['timeline-label', { highlighted: isHighlighted(main, tick) }]">
                {{ tick }}{{ main.unit }}
              </div>
            </div>
          </template>
          <!-- Without chunks: show all immediately -->
          <template v-else>
            <div
              v-for="tick in main.values"
              :key="`main-${tick}`"
              class="timeline-tick-wrapper"
            >
              <div
                :class="['timeline-tick', { highlighted: isHighlighted(main, tick) }]"
                :ref="setMainTickRef(tick)"
              />
              <div :class="['timeline-label', { highlighted: isHighlighted(main, tick) }]">
                {{ tick }}{{ main.unit }}
              </div>
            </div>
          </template>
        </div>
      </div>
    </div>

    <!-- SVG overlay for connectors -->
    <svg class="connectors-overlay">
      <line
        v-for="(line, branchIdx) in connectorLines"
        :key="branchIdx"
        :x1="line.x1"
        :y1="line.y1"
        :x2="line.x2"
        :y2="line.y2"
        stroke="#555"
        stroke-width="3"
      />
    </svg>

    <!-- Branches -->
    <div class="branches-container">
      <div
        v-for="(branch, idx) in branches"
        :key="idx"
        class="branch-row"
        :style="{ marginTop: branchSpacing + 'px' }"
      >
        <div class="branch-content">
          <div class="branch-label">{{ branch.name }}</div>
          <div class="branch-timeline">
            <div class="timeline-line-container">
              <div class="timeline-line" :style="{ left: getBranchLineStart(branch) }" />
              <!-- Arrow head on right side -->
              <div class="timeline-line-arrow" />
              <div class="timeline-ticks">
                <!-- With chunks: progressive reveal -->
                <template v-if="chunks && chunks.length > 0">
                  <div
                    v-for="(tick, tickIdx) in branch.values"
                    :key="`branch-${idx}-${tick}`"
                    class="timeline-tick-wrapper"
                    :style="getTickPosition(branch, tickIdx)"
                    v-click="getClickIndex(idx, tick)"
                  >
                    <div
                      :class="['timeline-tick', { highlighted: isHighlighted(branch, tick) }]"
                      :ref="setBranchTickRef(idx, tick)"
                    />
                    <div :class="['timeline-label', { highlighted: isHighlighted(branch, tick) }]">
                      {{ tick }}{{ main.unit }}
                    </div>
                  </div>
                </template>
                <!-- Without chunks: show all immediately -->
                <template v-else>
                  <div
                    v-for="(tick, tickIdx) in branch.values"
                    :key="`branch-${idx}-${tick}`"
                    class="timeline-tick-wrapper"
                    :style="getTickPosition(branch, tickIdx)"
                  >
                    <div
                      :class="['timeline-tick', { highlighted: isHighlighted(branch, tick) }]"
                      :ref="setBranchTickRef(idx, tick)"
                    />
                    <div :class="['timeline-label', { highlighted: isHighlighted(branch, tick) }]">
                      {{ tick }}{{ main.unit }}
                    </div>
                  </div>
                </template>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.timeline-bifurcating-container {
  position: relative;
  width: 100%;
  padding: 1rem 0 1.5rem 0;
}

.connectors-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
  z-index: 0;
}

/* Main timeline styles */
.main-timeline {
  position: relative;
  width: 100%;
  margin-bottom: 0.5rem;
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

/* Arrow head (right side only) */
.timeline-line-arrow::after {
  content: '';
  position: absolute;
  top: 8px;
  right: -10px;
  transform: translateY(-50%);
  border: 6px solid transparent;
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

/* Branches container */
.branches-container {
  position: relative;
  width: 100%;
}

.branch-row {
  position: relative;
  width: 100%;
}

/* Vertical connectors now drawn with SVG - see .connectors-overlay */

.branch-content {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.branch-label {
  font-size: 0.875rem;
  font-weight: 600;
  color: #888;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.branch-timeline {
  position: relative;
  width: 100%;
}

.branch-timeline .timeline-ticks {
  position: relative;
  /* Ticks use absolute positioning within this container */
}
</style>
