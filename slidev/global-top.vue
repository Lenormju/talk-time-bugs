<script setup lang="ts">
import { useNav } from '@slidev/client'

const { currentPage, total } = useNav()
</script>

<template>
  <div class="slide-indicator">
    Slide {{ currentPage }} / {{ total }}
  </div>
</template>

<style scoped>
.slide-indicator {
  position: fixed;
  top: 1rem;
  right: 1rem;
  font-family: monospace;
  font-size: 0.8rem;
  opacity: 0.3;
  z-index: 100;
}
</style>
