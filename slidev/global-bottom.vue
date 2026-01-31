<script setup lang="ts">
import { ref, onMounted, onUnmounted, computed } from 'vue'
import { useNav } from '@slidev/client'
import { isTimeVisible } from './composables/useTimeVisibility'

// Configuration: when to show the time
// - number alone: show for all clicks on that slide (e.g., 1)
// - [slide, click]: show only for specific click (e.g., [3, 1])
// - [slide, [clicks]]: show for multiple clicks (e.g., [4, [0, 2, 3]])
const visibleOn: (number | [number, number | number[]])[] = [
  1,           // slide 1, all clicks
  [3, 1],      // slide 3, only click 1
  4,           // slide 4, all clicks
  7,           // slide 7, all clicks
]

const { currentPage, clicks } = useNav()

const shouldShow = computed(() => {
  for (const rule of visibleOn) {
    if (typeof rule === 'number') {
      // Just a slide number: show for all clicks
      if (currentPage.value === rule) return true
    } else {
      // [slide, click(s)]: check both slide and click
      const [slide, clickRule] = rule
      if (currentPage.value === slide) {
        if (typeof clickRule === 'number') {
          if (clicks.value === clickRule) return true
        } else {
          // Array of clicks
          if (clickRule.includes(clicks.value)) return true
        }
      }
    }
  }
  return false
})

const currentTime = ref('')

function updateTime() {
  const now = new Date()
  currentTime.value = now.toLocaleTimeString('fr-FR', {
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit',
  })
}

let intervalId: number

onMounted(() => {
  updateTime()
  intervalId = setInterval(updateTime, 1000)
})

onUnmounted(() => {
  clearInterval(intervalId)
})
</script>

<template>
  <div v-if="shouldShow && isTimeVisible" class="time-display">
    {{ currentTime }}
  </div>
</template>

<style scoped>
.time-display {
  position: fixed;
  bottom: 1rem;
  left: 1rem;
  font-family: monospace;
  font-size: 1rem;
  opacity: 0.4;
  z-index: 100;
}
</style>
