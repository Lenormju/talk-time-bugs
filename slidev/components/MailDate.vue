<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'

const DAYS = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']
const MONTHS = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

function pad(n: number): string {
  return String(n).padStart(2, '0')
}

function formatMailDate(d: Date): string {
  const offset = -d.getTimezoneOffset()
  const sign = offset >= 0 ? '+' : '-'
  const absOffset = Math.abs(offset)
  const offsetStr = `${sign}${pad(Math.floor(absOffset / 60))}${pad(absOffset % 60)}`
  return `${DAYS[d.getDay()]}, ${pad(d.getDate())} ${MONTHS[d.getMonth()]} ${d.getFullYear()} ${pad(d.getHours())}:${pad(d.getMinutes())}:${pad(d.getSeconds())} ${offsetStr}`
}

const date = ref(formatMailDate(new Date()))

let interval: ReturnType<typeof setInterval>

onMounted(() => {
  interval = setInterval(() => {
    date.value = formatMailDate(new Date())
  }, 1000)
})

onUnmounted(() => {
  clearInterval(interval)
})
</script>

<template>
  <code>{{ date }}</code>
</template>
