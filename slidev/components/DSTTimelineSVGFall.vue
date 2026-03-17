<script setup lang="ts">
import { onMounted, nextTick, watch } from 'vue'
import { useNav } from '@slidev/client'
import gsap from 'gsap'
import {
  SVG_WIDTH,
  LINE_Y,
  TICK_RADIUS,
  getTickX,
} from '../composables/useSVGCoordinates'

const TOTAL = 9

const leftTicks   = ['01:59:57', '01:59:58', '01:59:59']
const middleTicks = ['02:00:00', '02:00:01', '02:59:59']
const dupTicks    = ['02:00:00', '02:00:01', '02:59:59']
const rightTicks  = ['03:00:00', '03:00:01', '03:00:02']

const gx = (i: number) => getTickX(i, TOTAL)

// TICK_STEP: spacing between consecutive ticks (= 100 with TOTAL=9)
const TICK_STEP = gx(1) - gx(0)

// Trim left padding by shifting the visible area right in coordinate space.
// gx(0)=100 will appear ~2% from the left edge instead of 10%.
const VIEW_MIN_X = 80

// Line: short lead-in before the first tick, arrow extension past the last.
const LINE_START_X = gx(0) - 15   // 15 units before gx(0)=100
const LINE_END_X   = SVG_WIDTH - 50  // 950

// Boundary between static left line and middle group
const LEFT_LINE_X2 = (gx(2) + gx(3)) / 2  // 350

// Boundary between middle group and right group line
const MID_LINE_X2  = (gx(5) + gx(6)) / 2  // 650

// Middle group: line from LEFT_LINE_X2 → gx(4) (02:00:00→02:00:01, adjacent),
// then dots between gx(4) and gx(5), then line gx(5) → MID_LINE_X2.
const DOT_R       = 3
const DOT_SPACING = 10
const midDotCx    = (gx(4) + gx(5)) / 2  // 550
const midDots     = [midDotCx - DOT_SPACING, midDotCx, midDotCx + DOT_SPACING]

// Duplicate segment: positions mirror the mid section but offset after MID_LINE_X2.
// dupGx(i) = gx(5) + (i+1)*TICK_STEP  →  700, 800, 900
const dupGx = (i: number) => gx(5) + (i + 1) * TICK_STEP

// Animation deltas — defined first so DUP_LINE_END can reference them.
// Right group overshoots by one TICK_STEP on split so the reconnect is visible.
const SPLIT_DX     = 4 * TICK_STEP   // 400
const RECONNECT_DX = -TICK_STEP      // -100  →  final offset = 300

// Dup group lines: flush with mid group end on the left, flush with right group
// line start (MID_LINE_X2 + final_offset) on the right — ensures no gaps.
const DUP_LINE_START = MID_LINE_X2                              // 650
const DUP_LINE_END   = MID_LINE_X2 + SPLIT_DX + RECONNECT_DX   // 950

const dupDotCx = (dupGx(1) + dupGx(2)) / 2  // 850
const dupDots  = [dupDotCx - DOT_SPACING, dupDotCx, dupDotCx + DOT_SPACING]

// Arrow at the end of the right group line
const arrowX      = LINE_END_X
const arrowPoints = `${arrowX},${LINE_Y} ${arrowX - 10},${LINE_Y - 6} ${arrowX - 10},${LINE_Y + 6}`

const viewBox = `${VIEW_MIN_X} 0 ${SVG_WIDTH} 120`

const nav = useNav()

onMounted(async () => {
  await nextTick()

  const rightGroup = document.querySelector('#fall-right-group')!

  const tl = gsap.timeline({ paused: true })

  // Step 1: mark appears above 03:00:00
  tl.to('#fall-mark', { opacity: 1, duration: 0.3 })
  tl.addLabel('end-1')

  // Step 2: split — right group slides right
  tl.to(rightGroup, { x: SPLIT_DX, duration: 0.5, ease: 'power2.inOut' })
  tl.addLabel('end-2')

  // Step 3: dup segment fades in + original mid gets a slight orange tint
  tl.to('#fall-dup-group',        { opacity: 1, duration: 0.4 })
  tl.to('#fall-mid-group circle', { attr: { stroke: '#7eb8f7' }, duration: 0.3 }, '<')
  tl.to('#fall-mid-group text',   { attr: { fill:   '#7eb8f7' }, duration: 0.3 }, '<')
  tl.to('#fall-mid-group line',   { attr: { stroke: '#7eb8f7' }, duration: 0.3 }, '<')
  tl.addLabel('end-3')

  // Step 4: reconnect — right group slides back to join the dup segment
  tl.to(rightGroup, { x: SPLIT_DX + RECONNECT_DX, duration: 0.4, ease: 'power2.inOut' })
  tl.addLabel('end-4')

  watch(nav.clicks, (clicks) => {
    if (clicks === 0) {
      tl.seek(0).pause()
    } else if (clicks === 1) {
      tl.tweenTo('end-1')
    } else if (clicks === 2) {
      tl.tweenTo('end-2')
    } else if (clicks === 3) {
      tl.tweenTo('end-3')
    } else {
      tl.tweenTo('end-4')
    }
  })
})
</script>

<template>
  <div class="w-full py-4">
    <svg :viewBox="viewBox" class="w-full" style="overflow: visible">

      <!-- Static left line (before first tick → LEFT_LINE_X2) -->
      <line
        :x1="LINE_START_X" :y1="LINE_Y"
        :x2="LEFT_LINE_X2" :y2="LINE_Y"
        stroke="#555" stroke-width="3"
      />

      <!-- Left ticks (always visible) -->
      <g v-for="(label, i) in leftTicks" :key="label">
        <circle :cx="gx(i)" :cy="LINE_Y" :r="TICK_RADIUS" fill="#fff" stroke="#555" stroke-width="3" />
        <text :x="gx(i)" :y="LINE_Y + 20" text-anchor="middle" dominant-baseline="hanging" fill="#ccc" class="tick-label">{{ label }}</text>
      </g>

      <!-- Middle group: line LEFT_LINE_X2→gx(4), dots, line gx(5)→MID_LINE_X2. Tinted in step 3. -->
      <g id="fall-mid-group">
        <!-- Line: 01:59:59 region → 02:00:01 (adjacent seconds, continuous) -->
        <line :x1="LEFT_LINE_X2" :y1="LINE_Y" :x2="gx(4)" :y2="LINE_Y" stroke="#555" stroke-width="3" />
        <!-- Dots between 02:00:01 and 02:59:59 (non-continuous display) -->
        <circle v-for="x in midDots" :key="x" :cx="x" :cy="LINE_Y" :r="DOT_R" fill="#555" />
        <!-- Line: 02:59:59 → MID_LINE_X2 region -->
        <line :x1="gx(5)" :y1="LINE_Y" :x2="MID_LINE_X2" :y2="LINE_Y" stroke="#555" stroke-width="3" />
        <!-- Middle ticks -->
        <g v-for="(label, i) in middleTicks" :key="label">
          <circle :cx="gx(3 + i)" :cy="LINE_Y" :r="TICK_RADIUS" fill="#fff" stroke="#555" stroke-width="3" />
          <text :x="gx(3 + i)" :y="LINE_Y + 20" text-anchor="middle" dominant-baseline="hanging" fill="#ccc" class="tick-label">{{ label }}</text>
        </g>
      </g>

      <!-- Duplicate colored segment (initially hidden, fades in step 3) -->
      <g id="fall-dup-group" opacity="0">
        <!-- Line: dup start → 02:00:01 -->
        <line :x1="DUP_LINE_START" :y1="LINE_Y" :x2="dupGx(1)" :y2="LINE_Y" stroke="#ff6b35" stroke-width="3" />
        <!-- Dots between 02:00:01 and 02:59:59 -->
        <circle v-for="x in dupDots" :key="x" :cx="x" :cy="LINE_Y" :r="DOT_R" fill="#ff6b35" />
        <!-- Line: 02:59:59 → dup end -->
        <line :x1="dupGx(2)" :y1="LINE_Y" :x2="DUP_LINE_END" :y2="LINE_Y" stroke="#ff6b35" stroke-width="3" />
        <!-- Dup ticks -->
        <g v-for="(label, i) in dupTicks" :key="'dup-' + i">
          <circle :cx="dupGx(i)" :cy="LINE_Y" :r="TICK_RADIUS" fill="#fff" stroke="#ff6b35" stroke-width="3" />
          <text :x="dupGx(i)" :y="LINE_Y + 20" text-anchor="middle" dominant-baseline="hanging" fill="#ff6b35" class="tick-label">{{ label }}</text>
        </g>
      </g>

      <!-- Right group: mark + line + arrow + ticks. Slides right on split, back on reconnect. -->
      <g id="fall-right-group">
        <!-- Mark above 03:00:00 (initially hidden, appears in step 1, moves with group) -->
        <g id="fall-mark" opacity="0">
          <line :x1="gx(6)" :y1="LINE_Y - TICK_RADIUS - 5" :x2="gx(6)" :y2="LINE_Y - 30" stroke="#ff6b35" stroke-width="2" />
          <text :x="gx(6)" :y="LINE_Y - 34" text-anchor="middle" dominant-baseline="auto" fill="#ff6b35" class="tick-label">↓ DST</text>
        </g>
        <!-- Line from MID_LINE_X2 to LINE_END_X, arrow at end -->
        <line :x1="MID_LINE_X2" :y1="LINE_Y" :x2="LINE_END_X" :y2="LINE_Y" stroke="#555" stroke-width="3" />
        <polygon :points="arrowPoints" fill="#555" />
        <!-- Right ticks -->
        <g v-for="(label, i) in rightTicks" :key="label">
          <circle :cx="gx(6 + i)" :cy="LINE_Y" :r="TICK_RADIUS" fill="#fff" stroke="#555" stroke-width="3" />
          <text :x="gx(6 + i)" :y="LINE_Y + 20" text-anchor="middle" dominant-baseline="hanging" fill="#ccc" class="tick-label">{{ label }}</text>
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
