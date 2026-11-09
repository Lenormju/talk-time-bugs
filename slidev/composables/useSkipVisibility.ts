import { ref } from 'vue'

// Shared state for the "hard skip" overlay toggle
export const isHardSkipVisible = ref(true)

export function toggleHardSkip() {
  isHardSkipVisible.value = !isHardSkipVisible.value
}
