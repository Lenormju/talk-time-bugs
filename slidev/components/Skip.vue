<script setup lang="ts">
import { isHardSkipVisible } from '../composables/useSkipVisibility'

// soft : petit logo dans le coin (comportement historique)
// hard : gros « skip » translucide par-dessus la slide (masquable depuis la barre d'options, jamais imprimé)
defineProps<{ hard?: boolean }>()
</script>

<template>
  <div v-if="hard && isHardSkipVisible" class="skip-hard">
    <img src="/images/skip.png" />
  </div>
  <img v-else-if="!hard" src="/images/skip.png" class="absolute top-8 right-4 w-24" />
</template>

<style scoped>
.skip-hard {
  position: absolute;
  inset: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  pointer-events: none;
  z-index: 50;
}

.skip-hard img {
  height: 80%;
  opacity: 0.3;
}

@media print {
  .skip-hard {
    display: none;
  }
}
</style>
