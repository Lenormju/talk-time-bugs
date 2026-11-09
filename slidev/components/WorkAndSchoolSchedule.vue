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

    <!-- Middle segment: 2h–3h (stays in place) + its tick at 3h -->
    <line :x1="x(2)" y1="30" :x2="x(3)" y2="30" stroke="#ccc" stroke-width="2" />
    <line :x1="x(3)" y1="23" :x2="x(3)" y2="37" stroke="#ccc" stroke-width="1.5" />

    <!-- Repeated hour 2h–3h (fades in when animated, fills the gap left by the shift) -->
    <line
      :x1="x(3)" y1="30" :x2="x(4)" y2="30"
      stroke="#ccc" stroke-width="2"
      :style="{ opacity: animated ? 1 : 0, transition: 'opacity 0.35s ease' }"
    />

    <!-- Right part: 3h–24h (shifts right by one hour when animated: fall back, 25h day) -->
    <g
      :transform="animated ? 'translate(40, 0)' : 'translate(0, 0)'"
      style="transition: transform 0.6s ease"
    >
      <line :x1="x(3)" y1="30" :x2="x(24)" y2="30" stroke="#ccc" stroke-width="2" stroke-linecap="round" />
      <g v-for="h in rightHours" :key="'r' + h">
        <line :x1="x(h)" y1="23" :x2="x(h)" y2="37" stroke="#ccc" stroke-width="1.5" />
        <text v-if="labeled.includes(h)" :x="x(h)" y="60" text-anchor="middle" font-size="6" fill="#aaa" font-family="monospace">{{ fmt(h) }}</text>
      </g>
    </g>

    <!-- Lever/coucher du soleil (Paris), repères pour caler les SunDuration.
         Hors du groupe qui glisse : le soleil ne bouge pas, ce sont les libellés qui se décalent. -->
    <g v-for="(s, i) in sunMarks.slice(0, shown)" :key="'s' + i">
      <line
        v-for="h in [s.rise, s.set]" :key="h"
        :x1="x(h)" :y1="s.y" :x2="x(h)" :y2="s.y + 6"
        :stroke="s.color" stroke-width="1.5" stroke-linecap="round" opacity="0.85"
      />
    </g>
  </svg>
</template>

<script setup>
defineProps({
  animated: { type: Boolean, default: false },
  // Nombre de périodes dont on affiche les repères (0 à 3)
  shown: { type: Number, default: 0 },
})

// Heures décimales, toutes en heure d'été (UTC+2) : la frise part de l'heure
// d'été avant le retour à l'heure d'hiver (voir note de pages/02-dst.md)
const sunMarks = [
  { y: 2,  color: '#93c5fd', rise: 9.686, set: 17.936 },  // solstice d'hiver (UTC+1 plus 1 h)
  { y: 9,  color: '#86efac', rise: 8.573, set: 18.568 },  // 30 octobre (UTC+1 plus 1 h)
  { y: 16, color: '#fde047', rise: 5.782, set: 21.965 },  // solstice d'été
]

const labeled = [0, 7, 9, 12, 16, 19, 22, 24]
const leftHours  = [0, 1, 2]
const rightHours = Array.from({ length: 22 }, (_, i) => i + 3)

const x = (h) => 20 + (h / 24) * 960
const fmt = (h) => `${String(h).padStart(2, '0')}h`
</script>
