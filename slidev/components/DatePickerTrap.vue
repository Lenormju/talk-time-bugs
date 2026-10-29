<script setup lang="ts">
import { ref, computed } from 'vue'

// Jour courant en heure LOCALE (pas toISOString, qui donne le jour UTC)
function todayLocal(): string {
  const now = new Date()
  const pad = (n: number) => String(n).padStart(2, '0')
  return `${now.getFullYear()}-${pad(now.getMonth() + 1)}-${pad(now.getDate())}`
}

const value = ref(todayLocal())

// new Date("YYYY-MM-DD") = minuit UTC ; null si saisie vide ou invalide
const instant = computed<Date | null>(() => {
  if (!value.value) return null
  const instant = new Date(value.value)
  return isNaN(instant.getTime()) ? null : instant
})

const iso = computed(() => (instant.value ? instant.value.toISOString() : '—'))

const fmt = { dateStyle: 'long', timeStyle: 'short' } as const

function render(timeZone: string): string {
  if (!instant.value) return '—'
  return instant.value.toLocaleString('fr-FR', { ...fmt, timeZone })
}

const paris = computed(() => render('Europe/Paris'))
const newYork = computed(() => render('America/New_York'))
</script>

<template>
  <div class="date-picker-trap">
    <div class="badge">Démo</div>

    <input type="date" v-model="value" class="picker" />

    <div v-click="1" class="row">
      <div class="label">Valeur brute</div>
      <code>"{{ value }}"</code>
      <div class="caption">une date : ni heure, ni fuseau</div>
    </div>

    <div v-click="2" class="row">
      <div class="label">Instant</div>
      <code>{{ iso }}</code>
      <div class="caption"><code>Date</code> en fait un instant : heure (00:00) et fuseau (UTC) inventés</div>
    </div>

    <div v-click="3" class="row">
      <div class="label">Paris</div>
      <code>{{ paris }}</code>
    </div>

    <div v-click="3" class="row text-orange-400 ny">
      <div class="label">New York</div>
      <code>{{ newYork }}</code>
      <div class="caption">lu dans un autre fuseau, la date change</div>
    </div>
  </div>
</template>

<style scoped>
.date-picker-trap {
  position: relative;
  display: flex;
  flex-direction: column;
  gap: 0.45rem;
  padding: 1.4rem 1rem 0.8rem;
  border: 2px solid #94a3b8;
  border-radius: 14px;
  background: #f1f5f9;
  box-shadow: 0 4px 14px rgba(0, 0, 0, 0.12);
}
.badge {
  position: absolute;
  top: -0.8rem;
  left: 1rem;
  padding: 0.1rem 0.7rem;
  border-radius: 999px;
  background: #334155;
  color: white;
  font-size: 0.8rem;
  font-weight: bold;
  letter-spacing: 0.05em;
  text-transform: uppercase;
}
.picker {
  align-self: flex-start;
  font-size: 1.3rem;
  padding: 0.3rem 0.7rem;
  border: 2px solid #3b82f6;
  border-radius: 8px;
  background: white;
  color: #0f172a;
}
.row {
  padding: 0.4rem 0.7rem;
  border-radius: 8px;
  background: white;
  border: 1px solid #cbd5e1;
}
.label {
  font-size: 0.75rem;
  font-weight: bold;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  opacity: 0.65;
}
.row code {
  display: block;
  font-family: ui-monospace, 'Fira Code', monospace;
  font-size: 1.05rem;
  padding: 0.15rem 0.4rem;
  border-radius: 4px;
  background: #e2e8f0;
}
.caption {
  margin-top: 0.2rem;
  font-size: 0.8rem;
  opacity: 0.8;
}
.caption code {
  display: inline;
  font-size: 0.8rem;
  padding: 0 0.2rem;
}
.ny {
  border: 2px solid #fb923c;
  background: #fff7ed;
}
.ny code {
  background: #ffedd5;
  font-weight: bold;
}
.ny .label,
.ny .caption {
  opacity: 1;
}
</style>
