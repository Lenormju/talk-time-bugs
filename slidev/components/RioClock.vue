<template>
  <span>{{ time }}</span>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'

const time = ref('')
let interval

function update() {
  time.value = new Date().toLocaleTimeString('fr-FR', { timeZone: 'America/Sao_Paulo' })
}

onMounted(() => {
  update()
  interval = setInterval(update, 1000)
})

onUnmounted(() => clearInterval(interval))
</script>
