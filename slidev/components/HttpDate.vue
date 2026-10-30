<script setup lang="ts">
import { computed } from 'vue'
import { useSecondTick } from '../composables/useSecondTick'

const now = useSecondTick()
const date = computed(() => new Date(now.value).toUTCString())
</script>

<template>
  <code>{{ date }}</code>
</template>
