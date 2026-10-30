<script setup lang="ts">
import { isTimeVisible, toggleTimeVisibility } from './composables/useTimeVisibility'
import { isHardSkipVisible, toggleHardSkip } from './composables/useSkipVisibility'
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
  <button
    class="slidev-icon-btn"
    :title="isHardSkipVisible ? 'Hide hard-skip overlay' : 'Show hard-skip overlay'"
    @click="toggleHardSkip"
  >
    <carbon:view v-if="isHardSkipVisible" />
    <carbon:view-off v-else />
  </button>
</template>
