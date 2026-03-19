<script setup lang="ts">
import { onMounted, nextTick, watch } from 'vue'
import { useNav } from '@slidev/client'
import gsap from 'gsap'
import { SVG_WIDTH, LINE_Y, TICK_RADIUS } from '../composables/useSVGCoordinates'

// 10 ticks: same layout as LeapSecondTimelineSVG
const allTicks = ['23:59:54', '23:59:55', '23:59:56', '23:59:57', '23:59:58', '23:59:59', '00:00:00', '00:00:01', '00:00:02', '00:00:03']

const TOTAL = 10
const LOCAL_PADDING = 100
const gx = (i: number) => LOCAL_PADDING + ((SVG_WIDTH - 2 * LOCAL_PADDING) * i / (TOTAL - 1))
const TICK_STEP = gx(1) - gx(0)  // 800/9 ≈ 88.9

// Initial positions — same as LeapSecondTimelineSVG
const ix = allTicks.map((_, i) => gx(i))

// Smeared window: indices 3–7 (23:59:57 … 00:00:01)
// Ticks 0–3: unchanged (anchor at 3)
// Ticks 4–7: spread proportionally, each gap widens by TICK_STEP/4
// Ticks 8–9: shift right by full TICK_STEP (follow the smeared section)
const fx = allTicks.map((_, i) => {
  if (i <= 3) return ix[i]
  if (i <= 7) return ix[i] + (i - 3) * TICK_STEP / 4
  return ix[i] + TICK_STEP
})

const LINE_START_X    = ix[0] - 15
const INITIAL_ARROW_X = ix[9] + 50
const FINAL_ARROW_X   = fx[9] + 50

const arrowPts = (ax: number) =>
  `${ax},${LINE_Y} ${ax - 10},${LINE_Y - 6} ${ax - 10},${LINE_Y + 6}`

const viewBox = `0 0 ${SVG_WIDTH} 120`

const nav = useNav()

// click layout: 1=Ca dépend, 2=Ajout, 3=split, 4=leap tick, 5=Smearing mounts, 6=color, 7=spread
const CLICK_OFFSET = 5

const COLOR = '#ff6b35'

// Indices that get colored (ticks "around" 23:59:59, not too far)
const COLORED = [3, 4, 5, 6, 7]

onMounted(async () => {
  await nextTick()

  const tl = gsap.timeline({ paused: true })

  // Step 1: color the smeared window ticks
  tl.to(COLORED.map(i => `#ls2-circle-${i}`), { attr: { stroke: COLOR }, duration: 0.3 })
  tl.to(COLORED.map(i => `#ls2-label-${i}`),  { attr: { fill: COLOR },   duration: 0.3 }, '<')
  tl.addLabel('end-1')

  // Step 2: all ticks that move animate to their final positions simultaneously
  // Ticks 4–9 move (tick 3 is anchor, ticks 0–2 are unchanged)
  for (let i = 4; i < allTicks.length; i++) {
    tl.to(`#ls2-circle-${i}`, { attr: { cx: fx[i] }, duration: 0.6, ease: 'power2.inOut' },
      i === 4 ? '>0' : '<')
    tl.to(`#ls2-label-${i}`,  { attr: { x: fx[i] },  duration: 0.6, ease: 'power2.inOut' }, '<')
  }
  // Connector lines: line i connects tick i to tick i+1
  // Lines 3–8 need updating (line between tick 3→4 has moving x2, rest have both endpoints moving)
  tl.to('#ls2-line-3', { attr: { x2: fx[4] }, duration: 0.6, ease: 'power2.inOut' }, '<')
  for (let i = 4; i <= 8; i++) {
    tl.to(`#ls2-line-${i}`, { attr: { x1: fx[i], x2: fx[i + 1] }, duration: 0.6, ease: 'power2.inOut' }, '<')
  }
  tl.to('#ls2-tail',  { attr: { x1: fx[9], x2: FINAL_ARROW_X }, duration: 0.6, ease: 'power2.inOut' }, '<')
  tl.to('#ls2-arrow', { attr: { points: arrowPts(FINAL_ARROW_X) }, duration: 0.6, ease: 'power2.inOut' }, '<')
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

      <!-- Static lead-in line -->
      <line :x1="LINE_START_X" :y1="LINE_Y" :x2="ix[0]" :y2="LINE_Y" stroke="#555" stroke-width="3" />

      <!-- Connector lines between consecutive ticks (0→1, 1→2, …, 8→9) -->
      <line
        v-for="i in [0,1,2,3,4,5,6,7,8]" :key="i"
        :id="`ls2-line-${i}`"
        :x1="ix[i]" :y1="LINE_Y" :x2="ix[i + 1]" :y2="LINE_Y"
        stroke="#555" stroke-width="3"
      />

      <!-- Tail line + arrow -->
      <line id="ls2-tail"  :x1="ix[9]" :y1="LINE_Y" :x2="INITIAL_ARROW_X" :y2="LINE_Y" stroke="#555" stroke-width="3" />
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
