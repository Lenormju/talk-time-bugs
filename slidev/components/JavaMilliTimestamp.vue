<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'

const timestamp = ref(Date.now())

let interval: ReturnType<typeof setInterval>

onMounted(() => {
  interval = setInterval(() => {
    timestamp.value = Date.now()
  }, 100)
})

onUnmounted(() => {
  clearInterval(interval)
})
</script>

<template>
  <code>{{ timestamp }}</code>
</template>
