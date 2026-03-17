<template>
  <svg
    viewBox="0 0 1000 60"
    xmlns="http://www.w3.org/2000/svg"
    class="w-full"
    style="max-height: 80px; overflow: visible"
  >
    <!-- Left part: 0h–2h (stays in place) -->
    <line :x1="x(0)" y1="30" :x2="x(2)" y2="30" stroke="#ccc" stroke-width="2" stroke-linecap="round" />
    <g v-for="h in leftHours" :key="'l' + h">
      <line :x1="x(h)" y1="23" :x2="x(h)" y2="37" stroke="#ccc" stroke-width="1.5" />
      <text v-if="labeled.includes(h)" :x="x(h)" y="60" text-anchor="middle" font-size="6" fill="#aaa" font-family="monospace">{{ fmt(h) }}</text>
    </g>

    <!-- Middle segment: 2h–3h (fades out when animated) -->
    <line
      :x1="x(2)" y1="30" :x2="x(3)" y2="30"
      stroke="#ccc" stroke-width="2"
      :style="{ opacity: animated ? 0 : 1, transition: 'opacity 0.35s ease' }"
    />

    <!-- Right part: 3h–24h (shifts left when animated) -->
    <g
      :transform="animated ? 'translate(-40, 0)' : 'translate(0, 0)'"
      style="transition: transform 0.6s ease"
    >
      <line :x1="x(3)" y1="30" :x2="x(24)" y2="30" stroke="#ccc" stroke-width="2" stroke-linecap="round" />
      <g v-for="h in rightHours" :key="'r' + h">
        <line :x1="x(h)" y1="23" :x2="x(h)" y2="37" stroke="#ccc" stroke-width="1.5" />
        <text v-if="labeled.includes(h)" :x="x(h)" y="60" text-anchor="middle" font-size="6" fill="#aaa" font-family="monospace">{{ fmt(h) }}</text>
      </g>
    </g>
  </svg>
</template>

<script setup>
defineProps({
  animated: { type: Boolean, default: false },
})

const labeled = [0, 7, 9, 12, 16, 19, 22, 24]
const leftHours  = [0, 1, 2]
const rightHours = Array.from({ length: 22 }, (_, i) => i + 3)

const x = (h) => 20 + (h / 24) * 960
const fmt = (h) => `${String(h).padStart(2, '0')}h`
</script>
