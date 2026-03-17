<template>
  <svg
    viewBox="0 0 1000 60"
    xmlns="http://www.w3.org/2000/svg"
    class="w-full"
    style="max-height: 80px; overflow: visible"
  >
    <!-- Main line -->
    <line x1="20" y1="30" x2="980" y2="30" stroke="#ccc" stroke-width="2" stroke-linecap="round" />

    <!-- Ticks and labels -->
    <g v-for="h in 25" :key="h - 1">
      <line
        :x1="x(h - 1)" y1="23"
        :x2="x(h - 1)" y2="37"
        stroke="#ccc" stroke-width="1.5"
      />
      <text
        v-if="labeled.includes(h - 1)"
        :x="x(h - 1)"
        y="60"
        text-anchor="middle"
        font-size="6"
        fill="#aaa"
        font-family="monospace"
      >{{ fmt(h - 1) }}</text>
    </g>
  </svg>
</template>

<script setup>
const labeled = [0, 7, 9, 12, 16, 19, 22, 24]

const x = (h) => 20 + (h / 24) * 960
const fmt = (h) => `${String(h).padStart(2, '0')}h`
</script>
