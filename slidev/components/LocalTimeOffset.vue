<template>
  <span>{{ time }}</span>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'

const props = defineProps({
  offsetMinutes: { type: Number, default: 0 }
})

const time = ref('')
let interval

function pad(n) {
  return String(n).padStart(2, '0')
}

function update() {
  const d = new Date(Date.now() + props.offsetMinutes * 60000)
  time.value = `${pad(d.getHours())}:${pad(d.getMinutes())}:${pad(d.getSeconds())}`
}

onMounted(() => {
  update()
  interval = setInterval(update, 1000)
})

onUnmounted(() => clearInterval(interval))
</script>
