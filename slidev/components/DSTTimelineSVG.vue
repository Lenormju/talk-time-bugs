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

const leftTicks  = ['01:59:57', '01:59:58', '01:59:59']
const middleTicks = ['02:00:00', '02:15:00', '02:30:00', '02:45:00', '02:59:59']
const rightTicks  = ['03:00:00', '03:00:01', '03:00:02']

const gx = (i: number) => getTickX(i, TOTAL)

// "..." midpoints between each pair of non-continuous middle ticks
const middleDotXs = [3, 4, 5, 6].map(i => (gx(i) + gx(i + 1)) / 2)

const LEFT_LINE_X2   = (gx(2) + gx(3)) / 2  // 300
const MIDDLE_LINE_X1 = LEFT_LINE_X2
const MIDDLE_LINE_X2 = (gx(7) + gx(8)) / 2  // 700
const RIGHT_LINE_X1  = MIDDLE_LINE_X2
const RIGHT_LINE_X2  = SVG_WIDTH - PADDING_X  // 900

// After stitch, right group translates so gx(8) lands on gx(3)
const STITCH_DX = gx(3) - gx(8)  // -400

// Post-stitch "..." lives inside the right group at x=700 so after -400 translation it lands at x=300,
// which is the midpoint between 01:59:59 (x=260) and 03:00:00 (x=340)
const STITCH_DOTS_X = RIGHT_LINE_X1  // 700

const viewBox = `0 0 ${SVG_WIDTH} 120`
const arrowPoints = getArrowPoints()

const nav = useNav()

onMounted(async () => {
  await nextTick()

  const middleGroup  = document.querySelector('#dst-mid-group')!
  const middleLine   = document.querySelector('#dst-mid-line')!
  const rightGroup   = document.querySelector('#dst-right-group')!
  const stitchDots   = document.querySelector('#dst-stitch-dots')!

  const tl = gsap.timeline({ paused: true })

  // Click 1: highlight the missing hour in orange
  tl.addLabel('click-1')
  tl.to('#dst-mid-group circle', { attr: { fill: '#ff6b35', stroke: '#ff6b35' }, duration: 0.3 }, 'click-1')
  tl.to('#dst-mid-group text',   { attr: { fill: '#ff6b35' }, duration: 0.3 }, 'click-1')
  tl.to(middleLine, { attr: { stroke: '#ff6b35' }, duration: 0.3 }, 'click-1')

  // Click 2: cut — the missing hour disappears
  tl.addLabel('click-2')
  tl.to([middleGroup, middleLine], { opacity: 0, duration: 0.4, ease: 'power2.out' }, 'click-2')

  // Click 3: stitch — right group slides left, gap "..." appears between the rejoined ticks
  tl.addLabel('click-3')
  tl.to(rightGroup,  { x: STITCH_DX, duration: 0.6, ease: 'power2.inOut' }, 'click-3')
  tl.to(stitchDots,  { opacity: 1, duration: 0.3 }, 'click-3')

  watch(nav.clicks, (clicks) => {
    if (clicks === 0) {
      tl.pause().time(0)
    } else {
      const label = `click-${clicks}`
      const t = tl.labels[label]
      if (t !== undefined) {
        tl.pause().time(t).play()
      } else {
        tl.pause().progress(1)
      }
    }
  })
})
</script>

<template>
  <div class="w-full py-4">
    <svg :viewBox="viewBox" class="w-full" style="overflow: visible">

      <!-- Left line segment (always visible) -->
      <line
        :x1="PADDING_X" :y1="LINE_Y"
        :x2="LEFT_LINE_X2" :y2="LINE_Y"
        stroke="#555" stroke-width="3"
      />

      <!-- Middle line segment (turns orange on click 1, fades on click 2) -->
      <line
        id="dst-mid-line"
        :x1="MIDDLE_LINE_X1" :y1="LINE_Y"
        :x2="MIDDLE_LINE_X2" :y2="LINE_Y"
        stroke="#555" stroke-width="3"
      />

      <!-- Left ticks (always visible) -->
      <g v-for="(label, i) in leftTicks" :key="label">
        <circle
          :cx="gx(i)" :cy="LINE_Y" :r="TICK_RADIUS"
          fill="#fff" stroke="#555" stroke-width="3"
        />
        <text
          :x="gx(i)" :y="LINE_Y + 22"
          text-anchor="middle" dominant-baseline="hanging"
          fill="#ccc" class="tick-label"
        >{{ label }}</text>
      </g>

      <!-- Middle ticks + dots between them (turn orange on click 1, fade on click 2) -->
      <g id="dst-mid-group">
        <!-- "..." between each pair of non-continuous ticks -->
        <text
          v-for="x in middleDotXs" :key="x"
          :x="x" :y="LINE_Y + 22"
          text-anchor="middle" dominant-baseline="hanging"
          fill="#555" class="tick-label"
        >···</text>

        <g v-for="(label, i) in middleTicks" :key="label">
          <circle
            :cx="gx(3 + i)" :cy="LINE_Y" :r="TICK_RADIUS"
            fill="#fff" stroke="#555" stroke-width="3"
          />
          <text
            :x="gx(3 + i)" :y="LINE_Y + 22"
            text-anchor="middle" dominant-baseline="hanging"
            fill="#ccc" class="tick-label"
          >{{ label }}</text>
        </g>
      </g>

      <!-- Right group: right line + arrow + right ticks + post-stitch "..." — slides on click 3 -->
      <g id="dst-right-group">
        <line
          :x1="RIGHT_LINE_X1" :y1="LINE_Y"
          :x2="RIGHT_LINE_X2" :y2="LINE_Y"
          stroke="#555" stroke-width="3"
        />
        <polygon :points="arrowPoints" fill="#555" />

        <!-- Post-stitch "..." hidden initially, fades in on click 3 alongside the slide.
             Placed at x=700 so after -400 translation it lands at x=300 (midpoint between
             01:59:59 at x=260 and 03:00:00 at x=340). -->
        <text
          id="dst-stitch-dots"
          :x="STITCH_DOTS_X" :y="LINE_Y + 22"
          text-anchor="middle" dominant-baseline="hanging"
          fill="#888" class="tick-label"
          opacity="0"
        >···</text>

        <g v-for="(label, i) in rightTicks" :key="label">
          <circle
            :cx="gx(8 + i)" :cy="LINE_Y" :r="TICK_RADIUS"
            fill="#fff" stroke="#555" stroke-width="3"
          />
          <text
            :x="gx(8 + i)" :y="LINE_Y + 22"
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
