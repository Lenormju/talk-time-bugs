<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'

const date = ref(new Date().toUTCString())

let interval: ReturnType<typeof setInterval>

onMounted(() => {
  interval = setInterval(() => {
    date.value = new Date().toUTCString()
  }, 1000)
})

onUnmounted(() => {
  clearInterval(interval)
})
</script>

<template>
  <code>{{ date }}</code>
</template>
