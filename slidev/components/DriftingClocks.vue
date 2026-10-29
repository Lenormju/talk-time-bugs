<script setup lang="ts">
import { computed, ref, watch } from 'vue'

// Deux horloges réglées au même instant ; l'écart entre elles grandit avec `step`.
// À chaque changement de step, les deux horloges font un tour complet (12 h) :
// A retombe sur 12:00 pile, B s'arrête un peu avant (écart cumulé de l'étape).
// Écarts volontairement exagérés (à dire à l'oral, pas de légende affichée).
const props = withDefaults(defineProps<{
  step?: number
  // écart de l'horloge B, en minutes, pour chaque étape
  offsets?: number[]
  // légende de chaque étape
  labels?: string[]
}>(), {
  step: 0,
  offsets: () => [0, 1, 7, 25],
  labels: () => ['réglées au même instant', '1 jour plus tard', '1 mois plus tard', '1 an plus tard'],
})

const index = computed(() => Math.max(0, Math.min(props.step, props.offsets.length - 1)))
const offset = computed(() => props.offsets[index.value])

// minutes depuis 00:00, en continu pour que les aiguilles reculent sans faire le tour
function hands(minutes: number) {
  return { hour: minutes * 0.5, minute: minutes * 6 }
}

function digital(minutes: number) {
  // cadran de 12 h : on affiche 12:00 et non 00:00
  const m = ((Math.round(minutes) % 720) + 720) % 720
  const h = Math.floor(m / 60) || 12
  return `${String(h).padStart(2, '0')}:${String(m % 60).padStart(2, '0')}`
}

// Nombre de tours déjà effectués : n'augmente jamais, même en revenant en
// arrière dans les clics, pour que les aiguilles tournent toujours dans le
// sens horaire (angles continus, jamais ramenés modulo 360°).
const turns = ref(0)
watch(index, () => { turns.value += 1 })

const clocks = computed(() => [
  { name: 'machine A', minutes: 720 * (1 + turns.value) },
  { name: 'machine B', minutes: 720 * (1 + turns.value) - offset.value },
].map(c => ({ ...c, ...hands(c.minutes), text: digital(c.minutes) })))

const ticks = Array.from({ length: 12 }, (_, i) => i * 30)
</script>

<template>
  <div class="drifting-clocks">
    <div class="flex justify-center gap-8">
      <div v-for="c in clocks" :key="c.name" class="flex flex-col items-center">
        <svg viewBox="-50 -50 100 100" class="w-32 h-32">
          <circle r="46" fill="none" stroke="currentColor" stroke-width="3" />
          <line v-for="t in ticks" :key="t" x1="0" y1="-40" x2="0" y2="-35"
            stroke="currentColor" stroke-width="2" :transform="`rotate(${t})`" />
          <line class="hand" x1="0" y1="4" x2="0" y2="-22" stroke="currentColor"
            stroke-width="5" stroke-linecap="round" :style="{ transform: `rotate(${c.hour}deg)` }" />
          <line class="hand" x1="0" y1="6" x2="0" y2="-34" stroke="currentColor"
            stroke-width="3" stroke-linecap="round" :style="{ transform: `rotate(${c.minute}deg)` }" />
          <circle r="3" fill="currentColor" />
        </svg>
        <div class="font-mono text-xl">{{ c.text }}</div>
        <div class="text-sm opacity-70">{{ c.name }}</div>
      </div>
    </div>
    <div class="text-center mt-2">
      {{ labels[index] }}
      <span v-if="offset > 0"> : <strong>{{ offset }} min</strong> d'écart</span>
    </div>
  </div>
</template>

<style scoped>
.hand {
  transition: transform 1.6s ease-in-out;
}
</style>
