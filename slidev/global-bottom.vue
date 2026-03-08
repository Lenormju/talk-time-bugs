<script setup lang="ts">
import { ref, onMounted, onUnmounted, computed } from 'vue'
import { useNav } from '@slidev/client'
import { isTimeVisible } from './composables/useTimeVisibility'

// Configuration: when to show the time
// - number alone: show for all clicks on that slide (e.g., 1)
// - [slide, click]: show only for specific click (e.g., [3, 1])
// - [slide, [clicks]]: show for multiple clicks (e.g., [4, [0, 2, 3]])
const timeVisibleOn: (number | [number, number | number[]])[] = [
  2,
  3,
  4,
  5,
  6,
  7,
]

// Configuration: when to show the PTC logo (bottom right)
// Same format as timeVisibleOn
const logoVisibleOn: (number | [number, number | number[]])[] = [
  3,
  4,
  5,
  6,
  7,
]

const { currentPage, clicks } = useNav()

function matchesRule(rules: (number | [number, number | number[]])[], page: number, click: number): boolean {
  for (const rule of rules) {
    if (typeof rule === 'number') {
      if (page === rule) return true
    } else {
      const [slide, clickRule] = rule
      if (page === slide) {
        if (typeof clickRule === 'number') {
          if (click === clickRule) return true
        } else {
          if (clickRule.includes(click)) return true
        }
      }
    }
  }
  return false
}

const shouldShow = computed(() => matchesRule(timeVisibleOn, currentPage.value, clicks.value))
const shouldShowLogo = computed(() => matchesRule(logoVisibleOn, currentPage.value, clicks.value))

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
  <img v-if="shouldShowLogo" src="./images/logo_ptc.png" class="logo-display" />
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

.logo-display {
  position: fixed;
  bottom: 1rem;
  right: 1rem;
  height: 3rem;
  opacity: 0.8;
  z-index: 100;
}
</style>
