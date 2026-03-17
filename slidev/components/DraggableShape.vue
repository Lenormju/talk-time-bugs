<script setup>
import { ref, reactive } from 'vue'

const props = defineProps({
  x:      { type: Number, default: 30 },
  y:      { type: Number, default: 30 },
  width:  { type: Number, default: 20 },
  height: { type: Number, default: 15 },
  color:  { type: String, default: 'rgba(255, 220, 0, 0.35)' },
  border: { type: String, default: 'rgba(255, 200, 0, 0.8)' },
})

const root = ref(null)
const dragging = ref(false)
const pos = reactive({ x: props.x, y: props.y })

const onMousedown = (e) => {
  dragging.value = true
  const start = { x: e.clientX, y: e.clientY }
  const orig  = { x: pos.x,     y: pos.y     }

  const onMove = (e) => {
    const r = root.value.getBoundingClientRect()
    pos.x = +Math.max(0, Math.min(100 - props.width,  orig.x + (e.clientX - start.x) / r.width  * 100)).toFixed(1)
    pos.y = +Math.max(0, Math.min(100 - props.height, orig.y + (e.clientY - start.y) / r.height * 100)).toFixed(1)
  }
  const onUp = () => {
    dragging.value = false
    console.log(`x="${pos.x}" y="${pos.y}"`)
    window.removeEventListener('mousemove', onMove)
    window.removeEventListener('mouseup', onUp)
  }
  window.addEventListener('mousemove', onMove)
  window.addEventListener('mouseup', onUp)
  e.preventDefault()
  e.stopPropagation()
}
</script>

<template>
  <div ref="root" class="absolute inset-0" style="pointer-events: none">
    <div
      class="absolute cursor-move select-none rounded"
      :style="{
        left:   pos.x + '%',
        top:    pos.y + '%',
        width:  width + '%',
        height: height + '%',
        background: color,
        border: `2px solid ${border}`,
        pointerEvents: 'all',
        zIndex: 50,
        transition: dragging ? 'none' : undefined,
      }"
      @mousedown="onMousedown"
    >
      <span v-if="dragging" class="absolute bottom-1 right-1 font-mono text-[9px] text-yellow-800 opacity-70">
        {{ pos.x }},{{ pos.y }}
      </span>
    </div>
  </div>
</template>
