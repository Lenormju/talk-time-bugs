<template>
  <div
    ref="container"
    class="zoomable-container"
    @wheel.prevent="onWheel"
    @mousedown="onMouseDown"
    @mousemove="onMouseMove"
    @mouseup="onMouseUp"
    @mouseleave="onMouseUp"
    @dblclick="resetTransform"
  >
    <img
      :src="src"
      :alt="alt"
      class="zoomable-image"
      :style="imgStyle"
      draggable="false"
    />
    <div class="zoom-hint" v-if="showHint">scroll to zoom · drag to pan · double-click to reset</div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'

const props = defineProps({
  src: { type: String, required: true },
  alt: { type: String, default: '' },
  initialScale: { type: Number, default: 1 },
  minScale: { type: Number, default: 0.2 },
  maxScale: { type: Number, default: 5 },
})

const scale = ref(props.initialScale)
const translateX = ref(0)
const translateY = ref(0)
const isDragging = ref(false)
const lastMouseX = ref(0)
const lastMouseY = ref(0)
const showHint = ref(true)
const container = ref(null)

const imgStyle = computed(() => ({
  transform: `translate(${translateX.value}px, ${translateY.value}px) scale(${scale.value})`,
  cursor: isDragging.value ? 'grabbing' : 'grab',
}))

function onWheel(e) {
  showHint.value = false
  const delta = e.deltaY > 0 ? 0.9 : 1.1
  const newScale = Math.min(props.maxScale, Math.max(props.minScale, scale.value * delta))

  // Zoom toward mouse cursor
  const rect = container.value.getBoundingClientRect()
  const mouseX = e.clientX - rect.left - rect.width / 2
  const mouseY = e.clientY - rect.top - rect.height / 2

  translateX.value = mouseX + (translateX.value - mouseX) * (newScale / scale.value)
  translateY.value = mouseY + (translateY.value - mouseY) * (newScale / scale.value)
  scale.value = newScale
}

function onMouseDown(e) {
  isDragging.value = true
  lastMouseX.value = e.clientX
  lastMouseY.value = e.clientY
}

function onMouseMove(e) {
  if (!isDragging.value) return
  showHint.value = false
  translateX.value += e.clientX - lastMouseX.value
  translateY.value += e.clientY - lastMouseY.value
  lastMouseX.value = e.clientX
  lastMouseY.value = e.clientY
}

function onMouseUp() {
  isDragging.value = false
}

function resetTransform() {
  scale.value = props.initialScale
  translateX.value = 0
  translateY.value = 0
}

onMounted(() => {
  setTimeout(() => { showHint.value = false }, 3000)
})
</script>

<style scoped>
.zoomable-container {
  width: 100%;
  height: 100%;
  overflow: hidden;
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
  background: transparent;
}

.zoomable-image {
  max-width: none;
  max-height: none;
  transform-origin: center center;
  transition: none;
  user-select: none;
}

.zoom-hint {
  position: absolute;
  bottom: 8px;
  left: 50%;
  transform: translateX(-50%);
  background: rgba(0, 0, 0, 0.5);
  color: white;
  padding: 4px 10px;
  border-radius: 4px;
  font-size: 11px;
  pointer-events: none;
  animation: fadeout 3s forwards;
}

@keyframes fadeout {
  0%   { opacity: 1; }
  70%  { opacity: 1; }
  100% { opacity: 0; }
}
</style>
