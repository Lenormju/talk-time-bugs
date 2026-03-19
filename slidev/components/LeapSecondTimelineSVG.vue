<script setup lang="ts">
import { onMounted, nextTick, watch } from 'vue'
import { useNav } from '@slidev/client'
import gsap from 'gsap'
import {
  SVG_WIDTH,
  LINE_Y,
  TICK_RADIUS,
} from '../composables/useSVGCoordinates'

// 10 ticks: 23:59:54 … 23:59:59 | 00:00:00 … 00:00:03
const TOTAL = 10

const leftTicks  = ['23:59:54', '23:59:55', '23:59:56', '23:59:57', '23:59:58', '23:59:59']
const rightTicks = ['00:00:00', '00:00:01', '00:00:02', '00:00:03']
const leapTick   = '23:59:60'

const LOCAL_PADDING = 100
const gx = (i: number) => LOCAL_PADDING + ((SVG_WIDTH - 2 * LOCAL_PADDING) * i / (TOTAL - 1))
const TICK_STEP = gx(1) - gx(0)  // 800/9 ≈ 88.9

const LINE_START_X = gx(0) - 15
const LINE_END_X   = gx(9) + 50

// Split between 23:59:59 (index 5) and 00:00:00 (index 6)
const SPLIT_X  = (gx(5) + gx(6)) / 2
const SPLIT_DX = TICK_STEP
// Leap tick lands at gx(6) exactly
const LEAP_X   = SPLIT_X + SPLIT_DX / 2

const arrowPoints = `${LINE_END_X},${LINE_Y} ${LINE_END_X - 10},${LINE_Y - 6} ${LINE_END_X - 10},${LINE_Y + 6}`

const viewBox = `0 0 ${SVG_WIDTH} 120`

const nav = useNav()

// click layout: 1=Ca dépend, 2=Ajout section, 3=split, 4=leap tick
const CLICK_OFFSET = 2

onMounted(async () => {
  await nextTick()

  const rightGroup = document.querySelector('#ls-right-group')!
  const leapGroup  = document.querySelector('#ls-leap-group')!

  const tl = gsap.timeline({ paused: true })

  tl.to(rightGroup, { x: SPLIT_DX, duration: 0.5, ease: 'power2.inOut' })
  tl.addLabel('end-1')

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
  <div class="w-full">
    <svg :viewBox="viewBox" class="w-full" style="overflow: visible">

      <!-- Static left line: LINE_START_X → SPLIT_X -->
      <line
        :x1="LINE_START_X" :y1="LINE_Y"
        :x2="SPLIT_X" :y2="LINE_Y"
        stroke="#555" stroke-width="3"
      />

      <!-- Left ticks: 23:59:54 … 23:59:59 -->
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

      <!-- Leap second group: hidden until click 2 -->
      <g id="ls-leap-group" opacity="0">
        <line :x1="SPLIT_X" :y1="LINE_Y" :x2="LEAP_X" :y2="LINE_Y" stroke="#ff6b35" stroke-width="3" />
        <line :x1="LEAP_X" :y1="LINE_Y" :x2="SPLIT_X + SPLIT_DX" :y2="LINE_Y" stroke="#ff6b35" stroke-width="3" />
        <circle :cx="LEAP_X" :cy="LINE_Y" :r="TICK_RADIUS" fill="#fff" stroke="#ff6b35" stroke-width="3" />
        <text
          :x="LEAP_X" :y="LINE_Y + 20"
          text-anchor="middle" dominant-baseline="hanging"
          fill="#ff6b35" class="tick-label"
        >{{ leapTick }}</text>
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

      <!-- Right group: 00:00:00 … 00:00:03 — slides right on click 1 -->
      <g id="ls-right-group">
        <line :x1="SPLIT_X" :y1="LINE_Y" :x2="LINE_END_X" :y2="LINE_Y" stroke="#555" stroke-width="3" />
        <polygon :points="arrowPoints" fill="#555" />
        <g v-for="(label, i) in rightTicks" :key="label">
          <circle
            :cx="gx(6 + i)" :cy="LINE_Y" :r="TICK_RADIUS"
            fill="#fff" stroke="#555" stroke-width="3"
          />
          <text
            :x="gx(6 + i)" :y="LINE_Y + 20"
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
