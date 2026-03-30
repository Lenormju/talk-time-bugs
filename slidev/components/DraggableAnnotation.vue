<script setup>
import { ref, reactive, computed } from 'vue'

const props = defineProps({
  labelX: { type: Number, default: 50 },
  labelY: { type: Number, default: 30 },
  tipX:   { type: Number, default: 60 },
  tipY:   { type: Number, default: 50 },
  color:  { type: String, default: '#22c55e' },
})

const uid = Math.random().toString(36).slice(2, 8)
const root = ref(null)
const dragging = ref(false)
const hovering = ref(false)
let hideTimer = null
function onEnter() { clearTimeout(hideTimer); hovering.value = true }
function onLeave() { hideTimer = setTimeout(() => { hovering.value = false }, 100) }
const lPos = reactive({ x: props.labelX, y: props.labelY })
const tPos = reactive({ x: props.tipX,   y: props.tipY   })

function makeDrag(pos) {
  let sm, sp
  const onMove = (e) => {
    const r = root.value.getBoundingClientRect()
    pos.x = +Math.max(0, Math.min(100, sp.x + (e.clientX - sm.x) / r.width  * 100)).toFixed(1)
    pos.y = +Math.max(0, Math.min(100, sp.y + (e.clientY - sm.y) / r.height * 100)).toFixed(1)
  }
  const onUp = () => {
    dragging.value = false
    console.log(`labelX="${lPos.x}" labelY="${lPos.y}" tipX="${tPos.x}" tipY="${tPos.y}"`)
    window.removeEventListener('mousemove', onMove)
    window.removeEventListener('mouseup', onUp)
  }
  return (e) => {
    dragging.value = true
    sm = { x: e.clientX, y: e.clientY }
    sp = { x: pos.x, y: pos.y }
    window.addEventListener('mousemove', onMove)
    window.addEventListener('mouseup', onUp)
    e.preventDefault()
    e.stopPropagation()
  }
}

const dragLabel = makeDrag(lPos)
const dragTip   = makeDrag(tPos)

const path = computed(() => `M${lPos.x},${lPos.y} L${tPos.x},${tPos.y}`)
</script>

<template>
  <div ref="root" class="absolute inset-0" style="pointer-events: none">
    <!-- Arrow -->
    <svg
      class="absolute inset-0 w-full h-full"
      viewBox="0 0 100 100"
      preserveAspectRatio="none"
      style="pointer-events: none"
    >
      <defs>
        <marker :id="uid" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto">
          <path d="M4,2.5 L7,4 L4,5.5" fill="none" :stroke="color" stroke-width="0.8" stroke-linecap="round" stroke-linejoin="round" />
        </marker>
      </defs>
      <path :d="path" fill="none" :stroke="color" stroke-width="0.8" stroke-linecap="round" :marker-end="`url(#${uid})`" />
    </svg>

    <!-- Label (drag to reposition) -->
    <div
      class="absolute w-fit bg-black/75 text-white text-xs p-0 rounded whitespace-nowrap cursor-move select-none"
      :style="{ left: lPos.x + '%', top: lPos.y + '%', transform: 'translate(-50%, -50%)', zIndex: 99, pointerEvents: 'all' }"
      @mouseenter="onEnter" @mouseleave="onLeave"
      @mousedown="dragLabel"
    >
      <slot />
      <!-- <span v-if="dragging" class="font-mono text-yellow-300 text-[9px] ml-1 opacity-80">
        {{ lPos.x }},{{ lPos.y }}
      </span> -->
    </div>

    <!-- Arrowhead handle (visible on hover only) -->
    <div
      class="absolute rounded-full cursor-crosshair transition-opacity duration-200"
      :style="{
        left: `calc(${tPos.x}% - 4px)`,
        top:  `calc(${tPos.y}% - 4px)`,
        width: '8px', height: '8px',
        background: color,
        opacity: hovering || dragging ? 1 : 0,
        zIndex: 100,
        pointerEvents: 'all',
      }"
      @mouseenter="onEnter" @mouseleave="onLeave"
      @mousedown="dragTip"
    >
      <!-- <span v-if="dragging" class="absolute left-3 top-0 font-mono text-yellow-300 text-[9px] whitespace-nowrap opacity-80">
        {{ tPos.x }},{{ tPos.y }}
      </span> -->
    </div>
  </div>
</template>
