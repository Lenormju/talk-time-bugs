import { ref } from 'vue'

// Shared state for time visibility toggle
export const isTimeVisible = ref(true)

export function toggleTimeVisibility() {
  isTimeVisible.value = !isTimeVisible.value
}
