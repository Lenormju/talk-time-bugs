<script setup lang="ts">
import { computed } from 'vue'
import { useSecondTick } from '../composables/useSecondTick'

const now = useSecondTick()
const timestamp = computed(() => Math.floor(now.value / 1000))
</script>

<template>
  <code>{{ timestamp }}</code>
</template>
