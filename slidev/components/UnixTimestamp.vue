<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'

const timestamp = ref(Math.floor(Date.now() / 1000))

let interval: ReturnType<typeof setInterval>

onMounted(() => {
  interval = setInterval(() => {
    timestamp.value = Math.floor(Date.now() / 1000)
  }, 1000)
})

onUnmounted(() => {
  clearInterval(interval)
})
</script>

<template>
  <code>{{ timestamp }}</code>
</template>
