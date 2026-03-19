<script setup lang="ts">
import { onMounted, nextTick, watch } from 'vue'
import { useNav } from '@slidev/client'
import gsap from 'gsap'
import {
  SVG_WIDTH,
  LINE_Y,
  TICK_RADIUS,
} from '../composables/useSVGCoordinates'

// 5 ticks in initial layout: 23:59:57, 23:59:58, 23:59:59, 00:00:00, 00:00:01
const TOTAL = 5

const leftTicks  = ['23:59:57', '23:59:58', '23:59:59']
const rightTicks = ['00:00:00', '00:00:01']
const leapTick   = '23:59:60'

// Use larger local padding so ticks are compact and stay within the viewBox
const LOCAL_PADDING = 300
const gx = (i: number) => LOCAL_PADDING + ((SVG_WIDTH - 2 * LOCAL_PADDING) * i / (TOTAL - 1))
const TICK_STEP = gx(1) - gx(0)  // 400/4 = 100

const LINE_START_X = gx(0) - 15
const LINE_END_X   = gx(4) + 100  // short tail after last tick

// Split point between 23:59:59 and 00:00:00
const SPLIT_X  = (gx(2) + gx(3)) / 2
// How far right group slides (one tick step) — leap tick lands at gx(3)
const SPLIT_DX = TICK_STEP
// Center of gap = gx(3) exactly
const LEAP_X   = SPLIT_X + SPLIT_DX / 2

const arrowPoints = `${LINE_END_X},${LINE_Y} ${LINE_END_X - 10},${LINE_Y - 6} ${LINE_END_X - 10},${LINE_Y + 6}`

const viewBox = `0 0 ${SVG_WIDTH} 120`

const nav = useNav()

// This slide has 2 v-clicks before the animation starts
const CLICK_OFFSET = 2

onMounted(async () => {
  await nextTick()

  const rightGroup = document.querySelector('#ls-right-group')!
  const leapGroup  = document.querySelector('#ls-leap-group')!

  const tl = gsap.timeline({ paused: true })

  // Step 1: split — right group slides right, revealing the gap
  tl.to(rightGroup, { x: SPLIT_DX, duration: 0.5, ease: 'power2.inOut' })
  tl.addLabel('end-1')

  // Step 2: leap second tick fades in inside the gap
  tl.to(leapGroup, { opacity: 1, duration: 0.4 })
  tl.addLabel('end-2')

  watch(nav.clicks, (clicks) => {
    const c = clicks - CLICK_OFFSET
    if (c <= 0) {
      tl.seek(0).pause()
    } else if (c === 1) {
      tl.tweenTo('end-1')
    } else {
      tl.tweenTo('end-2')
    }
  })
})
</script>

<template>
  <div class="w-full py-4">
    <svg :viewBox="viewBox" class="w-full" style="overflow: visible">

      <!-- Static left line: LINE_START_X → SPLIT_X -->
      <line
        :x1="LINE_START_X" :y1="LINE_Y"
        :x2="SPLIT_X" :y2="LINE_Y"
        stroke="#555" stroke-width="3"
      />

      <!-- Left ticks: 23:59:57, 23:59:58, 23:59:59 (always visible) -->
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

      <!-- Leap second group: hidden until click 2 of animation -->
      <g id="ls-leap-group" opacity="0">
        <!-- Orange lines through the leap tick -->
        <line :x1="SPLIT_X" :y1="LINE_Y" :x2="LEAP_X" :y2="LINE_Y" stroke="#ff6b35" stroke-width="3" />
        <line :x1="LEAP_X" :y1="LINE_Y" :x2="SPLIT_X + SPLIT_DX" :y2="LINE_Y" stroke="#ff6b35" stroke-width="3" />
        <!-- Leap tick circle and label -->
        <circle
          :cx="LEAP_X" :cy="LINE_Y" :r="TICK_RADIUS"
          fill="#fff" stroke="#ff6b35" stroke-width="3"
        />
        <text
          :x="LEAP_X" :y="LINE_Y + 20"
          text-anchor="middle" dominant-baseline="hanging"
          fill="#ff6b35" class="tick-label"
        >{{ leapTick }}</text>
        <!-- Annotation above: downward arrow + "61ème" label -->
        <line
          :x1="LEAP_X" :y1="LINE_Y - TICK_RADIUS - 5"
          :x2="LEAP_X" :y2="LINE_Y - 30"
          stroke="#ff6b35" stroke-width="2"
        />
        <text
          :x="LEAP_X" :y="LINE_Y - 34"
          text-anchor="middle" dominant-baseline="auto"
          fill="#ff6b35" class="tick-label"
        >↓ 61ème</text>
      </g>

      <!-- Right group: 00:00:00, 00:00:01 — slides right on click 1 -->
      <g id="ls-right-group">
        <line
          :x1="SPLIT_X" :y1="LINE_Y"
          :x2="LINE_END_X" :y2="LINE_Y"
          stroke="#555" stroke-width="3"
        />
        <polygon :points="arrowPoints" fill="#555" />
        <g v-for="(label, i) in rightTicks" :key="label">
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
