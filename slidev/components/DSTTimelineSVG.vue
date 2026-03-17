<script setup lang="ts">
import { onMounted, nextTick, watch } from 'vue'
import { useNav } from '@slidev/client'
import gsap from 'gsap'
import {
  SVG_WIDTH,
  PADDING_X,
  LINE_Y,
  TICK_RADIUS,
  getTickX,
  getArrowPoints,
} from '../composables/useSVGCoordinates'

const TOTAL = 11

const leftTicks   = ['01:59:57', '01:59:58', '01:59:59']
const middleTicks = ['02:00:00', '02:15:00', '02:30:00', '02:45:00', '02:59:59']
const rightTicks  = ['03:00:00', '03:00:01', '03:00:02']

const gx = (i: number) => getTickX(i, TOTAL)

// The middle line is split into two short connectors:
//   left-connector:  LEFT_LINE_X2 → gx(3)   (continuous: 01:59:59 → 02:00:00)
//   right-connector: gx(7)        → MID_LINE_X2  (continuous: 02:59:59 → 03:00:00)
// Between middle ticks (gx(3)→gx(7)) there is NO line — only dots.
const LEFT_LINE_X2  = (gx(2) + gx(3)) / 2   // 300  — left line ends here
const MID_LINE_X2   = (gx(7) + gx(8)) / 2   // 700  — right line starts here
const RIGHT_LINE_X2 = SVG_WIDTH - PADDING_X  // 900

// Dot clusters sitting in the gap between each pair of non-continuous middle ticks
// 3 circles per gap, centered, no line behind them
const DOT_R = 3
const DOT_SPACING = 10
const middleDotGroups = [3, 4, 5, 6].map(i => {
  const cx = (gx(i) + gx(i + 1)) / 2
  return [cx - DOT_SPACING, cx, cx + DOT_SPACING]
})

// After stitch, right group translates so gx(8) lands on gx(3)
const STITCH_DX = gx(3) - gx(8)  // -400

const viewBox = `0 0 ${SVG_WIDTH} 120`
const arrowPoints = getArrowPoints()

const nav = useNav()

onMounted(async () => {
  await nextTick()

  const middleGroup = document.querySelector('#dst-mid-group')!
  const rightGroup  = document.querySelector('#dst-right-group')!

  const tl = gsap.timeline({ paused: true })

  // Section 1: highlight the missing hour in orange
  tl.to('#dst-mid-group circle', { attr: { fill: '#ff6b35', stroke: '#ff6b35' }, duration: 0.3 })
  tl.to('#dst-mid-group text',   { attr: { fill: '#ff6b35' }, duration: 0.3 }, '<')
  tl.to('#dst-mid-group line',   { attr: { stroke: '#ff6b35' }, duration: 0.3 }, '<')
  tl.addLabel('end-1')

  // Section 2: cut — the missing hour disappears
  tl.to(middleGroup, { opacity: 0, duration: 0.4, ease: 'power2.out' })
  tl.addLabel('end-2')

  // Section 3: stitch — right group slides left to close the gap
  tl.to(rightGroup, { x: STITCH_DX, duration: 0.6, ease: 'power2.inOut' })
  tl.addLabel('end-3')

  // tweenTo plays only up to the target label, then stops
  watch(nav.clicks, (clicks) => {
    if (clicks === 0) {
      tl.seek(0).pause()
    } else if (clicks === 1) {
      tl.tweenTo('end-1')
    } else if (clicks === 2) {
      tl.tweenTo('end-2')
    } else {
      tl.tweenTo('end-3')
    }
  })
})
</script>

<template>
  <div class="w-full py-4">
    <svg :viewBox="viewBox" class="w-full" style="overflow: visible">

      <!-- Always-visible left line -->
      <line
        :x1="PADDING_X" :y1="LINE_Y"
        :x2="LEFT_LINE_X2" :y2="LINE_Y"
        stroke="#555" stroke-width="3"
      />

      <!-- Left ticks (always visible) -->
      <g v-for="(label, i) in leftTicks" :key="label">
        <circle
          :cx="gx(i)" :cy="LINE_Y" :r="TICK_RADIUS"
          fill="#fff" stroke="#555" stroke-width="3"
        />
        <text
          :x="gx(i)" :y="LINE_Y + 20"
          text-anchor="middle" dominant-baseline="hanging"
          fill="#ccc" class="tick-label"
        >{{ label }}</text>
      </g>

      <!-- Middle group: short connectors + ticks + dots (orange click 1, fade click 2) -->
      <g id="dst-mid-group">

        <!-- Short connector: LEFT_LINE_X2 → first middle tick (continuous 01:59:59 → 02:00:00) -->
        <line
          :x1="LEFT_LINE_X2" :y1="LINE_Y"
          :x2="gx(3)" :y2="LINE_Y"
          stroke="#555" stroke-width="3"
        />

        <!-- Short connector: last middle tick → MID_LINE_X2 (continuous 02:59:59 → 03:00:00) -->
        <line
          :x1="gx(7)" :y1="LINE_Y"
          :x2="MID_LINE_X2" :y2="LINE_Y"
          stroke="#555" stroke-width="3"
        />

        <!-- No line between middle ticks — only dot clusters to show non-continuity -->
        <circle
          v-for="x in middleDotGroups.flat()" :key="x"
          :cx="x" :cy="LINE_Y" :r="DOT_R"
          fill="#555"
        />

        <!-- Middle ticks -->
        <g v-for="(label, i) in middleTicks" :key="label">
          <circle
            :cx="gx(3 + i)" :cy="LINE_Y" :r="TICK_RADIUS"
            fill="#fff" stroke="#555" stroke-width="3"
          />
          <text
            :x="gx(3 + i)" :y="LINE_Y + 20"
            text-anchor="middle" dominant-baseline="hanging"
            fill="#ccc" class="tick-label"
          >{{ label }}</text>
        </g>

      </g>

      <!-- Right group: right line + arrow + right ticks — slides on click 3 -->
      <g id="dst-right-group">
        <line
          :x1="MID_LINE_X2" :y1="LINE_Y"
          :x2="RIGHT_LINE_X2" :y2="LINE_Y"
          stroke="#555" stroke-width="3"
        />
        <polygon :points="arrowPoints" fill="#555" />

        <g v-for="(label, i) in rightTicks" :key="label">
          <circle
            :cx="gx(8 + i)" :cy="LINE_Y" :r="TICK_RADIUS"
            fill="#fff" stroke="#555" stroke-width="3"
          />
          <text
            :x="gx(8 + i)" :y="LINE_Y + 20"
            text-anchor="middle" dominant-baseline="hanging"
            fill="#ccc" class="tick-label"
          >{{ label }}</text>
        </g>
      </g>

    </svg>
  </div>
</template>

<style scoped>
.tick-label {
  font-size: 11px;
  font-weight: 500;
  font-family: ui-monospace, monospace;
  pointer-events: none;
}
</style>
