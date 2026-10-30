<script setup lang="ts">
import { computed } from 'vue'
import { useSecondTick } from '../composables/useSecondTick'

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

const now = useSecondTick()
const date = computed(() => formatMailDate(new Date(now.value)))
</script>

<template>
  <code>{{ date }}</code>
</template>
