<script setup lang="ts">
import { onMounted, nextTick, watch } from 'vue'
import { useNav } from '@slidev/client'
import gsap from 'gsap'
import { SVG_WIDTH, LINE_Y, TICK_RADIUS } from '../composables/useSVGCoordinates'

const allTicks = ['23:59:57', '23:59:58', '23:59:59', '00:00:00', '00:00:01']

const LOCAL_PADDING = 300
const TOTAL = 5
const gx = (i: number) => LOCAL_PADDING + ((SVG_WIDTH - 2 * LOCAL_PADDING) * i / (TOTAL - 1))

// Initial positions — same as LeapSecondTimelineSVG
const ix = allTicks.map((_, i) => gx(i))  // [300, 400, 500, 600, 700]

// Final positions — same total span as LeapSecondTimelineSVG after insertion (300→800)
const fx = allTicks.map((_, i) => 300 + 125 * i)  // [300, 425, 550, 675, 800]

const LINE_START_X    = ix[0] - 15
const INITIAL_ARROW_X = ix[4] + 100   // 800
const FINAL_ARROW_X   = fx[4] + 100   // 900

const arrowPts = (ax: number) =>
  `${ax},${LINE_Y} ${ax - 10},${LINE_Y - 6} ${ax - 10},${LINE_Y + 6}`

const viewBox = `0 0 ${SVG_WIDTH} 120`

const nav = useNav()

// Click layout on this slide:
//   1 = Ca dépend!
//   2 = Ajout section mounts (LeapSecondTimelineSVG)
//   3 = LeapSecond step 1 (split)
//   4 = LeapSecond step 2 (leap tick)
//   5 = Smearing section mounts (this component)
//   6 = step 1 (color middle ticks)
//   7 = step 2 (smear / spread)
const CLICK_OFFSET = 5

const COLOR = '#ff6b35'

onMounted(async () => {
  await nextTick()

  const tl = gsap.timeline({ paused: true })

  // Step 1: color middle ticks (23:59:58, 23:59:59, 00:00:00)
  tl.to(['#ls2-circle-1', '#ls2-circle-2', '#ls2-circle-3'],
    { attr: { stroke: COLOR }, duration: 0.3 })
  tl.to(['#ls2-label-1', '#ls2-label-2', '#ls2-label-3'],
    { attr: { fill: COLOR }, duration: 0.3 }, '<')
  tl.addLabel('end-1')

  // Step 2: all ticks spread out simultaneously — first tween starts after end-1, rest use '<'
  tl.to('#ls2-circle-1', { attr: { cx: fx[1] }, duration: 0.6, ease: 'power2.inOut' })
  tl.to('#ls2-circle-2', { attr: { cx: fx[2] }, duration: 0.6, ease: 'power2.inOut' }, '<')
  tl.to('#ls2-circle-3', { attr: { cx: fx[3] }, duration: 0.6, ease: 'power2.inOut' }, '<')
  tl.to('#ls2-circle-4', { attr: { cx: fx[4] }, duration: 0.6, ease: 'power2.inOut' }, '<')
  tl.to('#ls2-label-1',  { attr: { x: fx[1] },  duration: 0.6, ease: 'power2.inOut' }, '<')
  tl.to('#ls2-label-2',  { attr: { x: fx[2] },  duration: 0.6, ease: 'power2.inOut' }, '<')
  tl.to('#ls2-label-3',  { attr: { x: fx[3] },  duration: 0.6, ease: 'power2.inOut' }, '<')
  tl.to('#ls2-label-4',  { attr: { x: fx[4] },  duration: 0.6, ease: 'power2.inOut' }, '<')
  tl.to('#ls2-line-0',   { attr: { x2: fx[1] }, duration: 0.6, ease: 'power2.inOut' }, '<')
  tl.to('#ls2-line-1',   { attr: { x1: fx[1], x2: fx[2] }, duration: 0.6, ease: 'power2.inOut' }, '<')
  tl.to('#ls2-line-2',   { attr: { x1: fx[2], x2: fx[3] }, duration: 0.6, ease: 'power2.inOut' }, '<')
  tl.to('#ls2-line-3',   { attr: { x1: fx[3], x2: fx[4] }, duration: 0.6, ease: 'power2.inOut' }, '<')
  tl.to('#ls2-tail',     { attr: { x1: fx[4], x2: FINAL_ARROW_X }, duration: 0.6, ease: 'power2.inOut' }, '<')
  tl.to('#ls2-arrow',    { attr: { points: arrowPts(FINAL_ARROW_X) }, duration: 0.6, ease: 'power2.inOut' }, '<')
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

      <!-- Static lead-in line before tick 0 -->
      <line :x1="LINE_START_X" :y1="LINE_Y" :x2="ix[0]" :y2="LINE_Y" stroke="#555" stroke-width="3" />

      <!-- Connector lines between consecutive ticks -->
      <line
        v-for="i in [0, 1, 2, 3]" :key="i"
        :id="`ls2-line-${i}`"
        :x1="ix[i]" :y1="LINE_Y" :x2="ix[i + 1]" :y2="LINE_Y"
        stroke="#555" stroke-width="3"
      />

      <!-- Tail line + arrow -->
      <line id="ls2-tail"  :x1="ix[4]" :y1="LINE_Y" :x2="INITIAL_ARROW_X" :y2="LINE_Y" stroke="#555" stroke-width="3" />
      <polygon id="ls2-arrow" :points="arrowPts(INITIAL_ARROW_X)" fill="#555" />

      <!-- Tick circles and labels -->
      <g v-for="(label, i) in allTicks" :key="label">
        <circle
          :id="`ls2-circle-${i}`"
          :cx="ix[i]" :cy="LINE_Y" :r="TICK_RADIUS"
          fill="#fff" stroke="#555" stroke-width="3"
        />
        <text
          :id="`ls2-label-${i}`"
          :x="ix[i]" :y="LINE_Y + 20"
          text-anchor="middle" dominant-baseline="hanging"
          fill="#ccc" class="tick-label"
        >{{ label }}</text>
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
