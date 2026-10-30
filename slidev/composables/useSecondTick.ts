import { ref, onMounted, onUnmounted } from 'vue'

// Shared "now" (ms), refreshed exactly on each wall-clock second boundary,
// so every live clock using it changes at the same instant.
const now = ref(Date.now())
let users = 0
let timer: ReturnType<typeof setTimeout> | undefined

function schedule() {
  timer = setTimeout(() => {
    now.value = Date.now()
    schedule()
  }, 1000 - (Date.now() % 1000))
}

export function useSecondTick() {
  onMounted(() => {
    now.value = Date.now()
    if (users++ === 0) schedule()
  })
  onUnmounted(() => {
    if (--users === 0) clearTimeout(timer)
  })
  return now
}
