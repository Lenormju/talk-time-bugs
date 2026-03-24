<template>
  <img
    :src="src"
    :alt="alt"
    v-bind="$attrs"
    class="cursor-zoom-in"
    @click="open = true"
  />

  <Teleport to="body">
    <div
      v-if="open"
      class="lightbox-overlay"
      @click.self="close"
    >
      <button class="lightbox-close" @click="close">✕</button>
      <div class="lightbox-inner" @wheel.prevent="onWheel" @mousedown="onMouseDown" @mousemove="onMouseMove" @mouseup="stopDrag" @mouseleave="stopDrag">
        <img
          :src="src"
          :alt="alt"
          class="lightbox-img"
          :style="imgStyle"
          draggable="false"
        />
      </div>
      <div class="lightbox-hint">scroll to zoom · drag to pan · double-click to reset</div>
    </div>
  </Teleport>
</template>

<script setup>
import { ref, computed, watch, onMounted, onUnmounted } from 'vue'

defineOptions({ inheritAttrs: false })

const props = defineProps({
  src: { type: String, required: true },
  alt: { type: String, default: '' },
})

const open = ref(false)
const scale = ref(1)
const translateX = ref(0)
const translateY = ref(0)
const isDragging = ref(false)
const lastX = ref(0)
const lastY = ref(0)

const imgStyle = computed(() => ({
  transform: `translate(${translateX.value}px, ${translateY.value}px) scale(${scale.value})`,
  cursor: isDragging.value ? 'grabbing' : 'grab',
}))

function close() {
  open.value = false
}

function onKeyDown(e) {
  if (e.key === 'Escape') close()
}

onMounted(() => window.addEventListener('keydown', onKeyDown))
onUnmounted(() => window.removeEventListener('keydown', onKeyDown))

watch(open, (val) => {
  if (val) {
    scale.value = 1
    translateX.value = 0
    translateY.value = 0
  }
})

function onWheel(e) {
  const delta = e.deltaY > 0 ? 0.9 : 1.1
  const newScale = Math.min(10, Math.max(0.2, scale.value * delta))
  const rect = e.currentTarget.getBoundingClientRect()
  const mouseX = e.clientX - rect.left - rect.width / 2
  const mouseY = e.clientY - rect.top - rect.height / 2
  translateX.value = mouseX + (translateX.value - mouseX) * (newScale / scale.value)
  translateY.value = mouseY + (translateY.value - mouseY) * (newScale / scale.value)
  scale.value = newScale
}

function onMouseDown(e) {
  isDragging.value = true
  lastX.value = e.clientX
  lastY.value = e.clientY
}

function onMouseMove(e) {
  if (!isDragging.value) return
  translateX.value += e.clientX - lastX.value
  translateY.value += e.clientY - lastY.value
  lastX.value = e.clientX
  lastY.value = e.clientY
}

function stopDrag() {
  isDragging.value = false
}
</script>

<style scoped>
.lightbox-overlay {
  position: fixed;
  inset: 0;
  z-index: 9999;
  background: rgba(0, 0, 0, 0.85);
  display: flex;
  align-items: center;
  justify-content: center;
}

.lightbox-inner {
  width: 90vw;
  height: 90vh;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
}

.lightbox-img {
  max-width: none;
  max-height: none;
  transform-origin: center center;
  user-select: none;
}

.lightbox-close {
  position: absolute;
  top: 16px;
  right: 24px;
  background: transparent;
  border: none;
  color: white;
  font-size: 28px;
  cursor: pointer;
  line-height: 1;
  opacity: 0.8;
}
.lightbox-close:hover {
  opacity: 1;
}

.lightbox-hint {
  position: absolute;
  bottom: 16px;
  left: 50%;
  transform: translateX(-50%);
  color: rgba(255,255,255,0.5);
  font-size: 12px;
  pointer-events: none;
}
</style>
