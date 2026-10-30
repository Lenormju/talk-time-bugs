<script setup lang="ts">
// Instantané du 30/10/2026 : versions relevées par exécution sur ma machine (Ubuntu 24.04) et dans
// des conteneurs podman tirés le jour même ; versions des dépôts d'après les index Debian et Repology.
// La dernière release IANA est 2026f (28/10/2026 06:16 UTC).
const LATEST = '2026f'

type Box = { name: string; how: string; version?: string }
type Layer = { click: number; label: string; boxes: Box[] }

const layers: Layer[] = [
  {
    click: 1,
    label: 'Systèmes',
    boxes: [
      { name: 'Debian 12', how: 'paquet (apt, sécurité)', version: '2026f' },
      { name: 'Ubuntu 24.04', how: 'paquet (apt)', version: '2026e' },
      { name: 'Windows', how: 'Windows Update' },
      { name: 'Android', how: 'module Mainline' },
    ],
  },
  {
    click: 2,
    label: 'Langages',
    boxes: [
      { name: 'Python', how: 'lit le système (sinon PyPI tzdata)', version: '2026e' },
      { name: 'Node / ICU', how: 'copie embarquée', version: '2025c' },
      { name: 'Java 17', how: 'copie embarquée (tzdb.dat)', version: '2026b' },
    ],
  },
  {
    click: 3,
    label: 'Bases de données',
    boxes: [
      { name: 'MySQL', how: 'tables à charger, puis redémarrer' },
      { name: 'PostgreSQL', how: 'copie embarquée' },
    ],
  },
  {
    click: 4,
    label: 'Conteneurs',
    boxes: [
      { name: 'python:3.14', how: 'figée à la construction (28/10)', version: '2026e' },
      { name: 'ubuntu:24.04', how: 'aucun tzdata : UTC, sans erreur', version: '∅' },
      { name: 'alpine:3.22', how: 'aucun tzdata : UTC, sans erreur', version: '∅' },
    ],
  },
]

// Niveau d'un badge par rapport à LATEST ; les couleurs ne s'appliquent qu'une fois la question finale
// révélée (voir le CSS : `.question` sans la classe `slidev-vclick-hidden`)
function level(version?: string): string {
  if (!version) return ''
  if (version === LATEST) return 'ok'
  if (version === '∅') return 'none'
  return version < '2026e' ? 'old' : 'late'
}
</script>

<template>
  <div class="tzdb-layers">
    <div class="layer">
      <div class="label">Source</div>
      <div class="boxes">
        <div class="box upstream">
          <div class="name">tz (IANA)</div>
          <div class="how">dépôt eggert/tz</div>
          <div class="version">{{ LATEST }}</div>
        </div>
      </div>
    </div>

    <div v-for="layer in layers" :key="layer.label" v-click="layer.click" class="layer">
      <div class="label">{{ layer.label }}</div>
      <div class="boxes">
        <div v-for="box in layer.boxes" :key="box.name" class="box">
          <div class="name">{{ box.name }}</div>
          <div class="how">{{ box.how }}</div>
          <div v-if="box.version" class="version" :class="level(box.version)">{{ box.version }}</div>
        </div>
      </div>
    </div>

    <div v-click="5" class="question">Quel est le tzdata de ce que je déploie ?</div>
  </div>
</template>

<style scoped>
.tzdb-layers {
  display: flex;
  flex-direction: column;
  gap: 0.55rem;
}
.layer {
  display: flex;
  align-items: stretch;
  gap: 0.8rem;
}
.label {
  flex: 0 0 8.5rem;
  display: flex;
  align-items: center;
  font-size: 0.85rem;
  font-weight: bold;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  opacity: 0.7;
}
.boxes {
  display: flex;
  flex: 1;
  gap: 0.6rem;
}
.box {
  position: relative;
  flex: 1;
  padding: 0.35rem 0.6rem;
  border: 1px solid #cbd5e1;
  border-radius: 8px;
  background: #f1f5f9;
  color: #0f172a;
}
.upstream {
  max-width: 14rem;
  border: 2px solid #22c55e;
}
.name {
  font-weight: bold;
  font-size: 0.95rem;
}
.how {
  font-size: 0.75rem;
  opacity: 0.75;
  padding-right: 3.2rem;
}
.version {
  position: absolute;
  top: 0.35rem;
  right: 0.45rem;
  padding: 0 0.45rem;
  border-radius: 999px;
  font-family: ui-monospace, 'Fira Code', monospace;
  font-size: 0.85rem;
  font-weight: bold;
  background: #e2e8f0;
}
.upstream .version {
  background: #bbf7d0;
}
.tzdb-layers:has(.question:not(.slidev-vclick-hidden)) .version.ok {
  background: #bbf7d0;
}
.tzdb-layers:has(.question:not(.slidev-vclick-hidden)) .version.late {
  background: #fed7aa;
}
.tzdb-layers:has(.question:not(.slidev-vclick-hidden)) .version.old,
.tzdb-layers:has(.question:not(.slidev-vclick-hidden)) .version.none {
  background: #fecaca;
}
.question {
  margin-top: 0.4rem;
  text-align: center;
  font-size: 1.25rem;
  font-weight: bold;
}
</style>
