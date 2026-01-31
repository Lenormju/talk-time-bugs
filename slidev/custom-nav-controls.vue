<script setup lang="ts">
import { isTimeVisible, toggleTimeVisibility } from './composables/useTimeVisibility'
</script>

<template>
  <button
    class="slidev-icon-btn"
    :title="isTimeVisible ? 'Hide time' : 'Show time'"
    @click="toggleTimeVisibility"
  >
    <carbon:time v-if="isTimeVisible" />
    <carbon:time-filled v-else />
  </button>
</template>
