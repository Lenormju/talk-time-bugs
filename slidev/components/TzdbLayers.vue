<script setup lang="ts">
// Graphe de dépendances de tzdata : en haut la source (IANA), puis des « grappes » qui en dépendent,
// puis d'autres grappes qui dépendent des précédentes.
// Instantané du 30/10/2026 : versions relevées par exécution (hôte Ubuntu 24.04, conteneurs podman tirés
// le jour même, paquets installés dans des dossiers jetables), index Debian et Repology pour les distros.
// La dernière release IANA est 2026f (28/10/2026 06:16 UTC). Un clic par grappe (avec le trait qui la relie à sa source), dans
// l'ordre : distributions, ce qui lit le système, images ; autres systèmes ; copies embarquées, via Intl ;
// bibliothèques, via PyPI ; clic 9 = comparaison des versions à 2026f et question finale.
const LATEST = '2026f'
// Mini pastilles de langage des bibliothèques
const LANGS: Record<string, string> = { py: 'py', js: 'js', java: 'jv', net: '.n', go: 'go', rs: 'rs', rb: 'rb', php: 'ph', ex: 'ex' }
const ROW = 19 // hauteur d'une ligne d'une grappe (px)
const HEAD = 30 // titre + marges

type Item = { name: string; note?: string; lang?: string; version?: string }
type Cluster = { id: string; click: number; x: number; y: number; w: number; title: string; items: Item[] }

const clusters: Cluster[] = [
  {
    id: 'distros', click: 1, x: 0, y: 95, w: 175, title: 'Distributions',
    items: [
      { name: 'Debian 12', note: 'security', version: '2026f' },
      { name: 'Ubuntu 24.04', version: '2026e' },
      { name: 'Alpine 3.22', version: '2026e' },
    ],
  },
  {
    id: 'autres', click: 4, x: 180, y: 95, w: 205, title: 'Autres systèmes',
    items: [
      { name: 'Windows 11', note: 'KB5127648', version: '≈2026e' },
      { name: 'Android', note: 'module', version: 'n/d' },
    ],
  },
  {
    id: 'node', click: 5, x: 390, y: 95, w: 145, title: 'Node (ICU)',
    items: [
      { name: 'Node 20', version: '2025c' },
      { name: 'Node 22.21', version: '2025b' },
      { name: 'Node 22.23', version: '2026e' },
    ],
  },
  {
    id: 'copies', click: 7, x: 540, y: 95, w: 203, title: 'Autres copies embarquées',
    items: [
      { name: 'JVM 17', note: 'tzdb.dat', version: '2026b' },
      { name: 'Go 1.27', version: '2026c' },
      { name: 'PostgreSQL 18', note: 'par défaut', version: '2026c' },
      { name: 'PHP 8.4', version: '2026e' },
      { name: 'PHP 8.3', version: '2026a' },
    ],
  },
  {
    id: 'libs', click: 8, x: 748, y: 95, w: 192, title: 'Bibliothèques',
    items: [
      { name: 'tzdata', lang: 'py', version: '2026f' },
      { name: 'pytz', lang: 'py', version: '2026f' },
      { name: 'moment-timezone', lang: 'js', version: '2026f' },
      { name: 'Joda-Time', lang: 'java', version: '2026f' },
      { name: 'ICU4J 79', lang: 'java', version: '2026e' },
      { name: 'NodaTime', lang: 'net', version: '2026f' },
      { name: 'chrono-tz', lang: 'rs', version: '2025b' },
      { name: 'jiff-tzdb', lang: 'rs', version: '2026e' },
      { name: 'tzinfo-data', lang: 'rb', version: '2026f' },
      { name: 'tzdata', lang: 'ex', note: 'MAJ auto', version: '2026f' },
    ],
  },
  {
    id: 'systeme', click: 2, x: 0, y: 275, w: 215, title: 'Lisent le système',
    items: [
      { name: 'Python', note: 'zoneinfo' },
      { name: '.NET', note: 'TimeZoneInfo' },
      { name: 'PostgreSQL', note: '--with-system-tzdata' },
      { name: 'MySQL' },
      { name: 'glibc', note: 'localtime(), date' },
      { name: 'Ruby', note: 'tzinfo' },
      { name: 'Rust', note: 'jiff' },
      { name: 'C++', note: 'libstdc++' },
    ],
  },
  {
    id: 'images', click: 3, x: 225, y: 275, w: 190, title: 'Images de conteneurs',
    items: [
      { name: 'python:3.14', version: '2026e' },
      { name: 'node:22', version: '2026e' },
      { name: 'golang:1.27', version: '2026e' },
      { name: 'postgres:17', version: '2026e' },
      { name: 'mysql:9', version: '2026e' },
      { name: 'ubuntu:24.04', version: '∅' },
      { name: 'alpine:3.22', version: '∅' },
    ],
  },
  {
    id: 'intl', click: 6, x: 425, y: 275, w: 215, title: 'Via Intl (ICU de Node)',
    items: [{ name: 'luxon', lang: 'js' }, { name: 'date-fns-tz', lang: 'js' }, { name: 'polyfill Temporal', lang: 'js' }],
  },
  {
    id: 'pypi', click: 9, x: 700, y: 345, w: 240, title: 'Via le paquet PyPI tzdata',
    items: [{ name: 'python-dateutil 3', lang: 'py' }, { name: 'arrow', lang: 'py' }, { name: 'pendulum', lang: 'py' }],
  },
]

const height = (c: Cluster) => HEAD + c.items.length * ROW
const byId = Object.fromEntries(clusters.map((c) => [c.id, c]))
const center = (c: Cluster) => c.x + c.w / 2

// Source en haut
const source = { x: 350, y: 0, w: 240, h: 50 }

type Edge = { click: number; x1: number; y1: number; x2: number; y2: number }
const edges: Edge[] = []
for (const id of ['distros', 'autres', 'node', 'copies', 'libs']) {
  const c = byId[id]
  edges.push({ click: c.click, x1: source.x + source.w / 2, y1: source.y + source.h, x2: center(c), y2: c.y })
}
for (const [from, to] of [['distros', 'systeme'], ['distros', 'images'], ['node', 'intl'], ['libs', 'pypi']]) {
  const a = byId[from]
  const b = byId[to]
  edges.push({ click: b.click, x1: center(a), y1: a.y + height(a), x2: center(b), y2: b.y })
}
const path = (e: Edge) => {
  const dy = (e.y2 - e.y1) / 2
  return `M ${e.x1} ${e.y1} C ${e.x1} ${e.y1 + dy}, ${e.x2} ${e.y2 - dy}, ${e.x2} ${e.y2}`
}

// Niveau d'un badge par rapport à LATEST ; les couleurs ne s'appliquent qu'une fois la question finale
// révélée (voir le CSS : `.question` sans la classe `slidev-vclick-hidden`) ; les badges à jour (`ok`) se colorent en même
// temps que les autres (la source, référence, est verte dès le début)
function level(version?: string): string {
  if (!version) return ''
  if (version === 'n/d') return 'nd'
  if (version.startsWith('≈')) version = version.slice(1)
  if (version === LATEST) return 'ok'
  if (version === '∅') return 'none'
  return version < '2026e' ? 'old' : 'late'
}
</script>

<template>
  <div class="tzdb-wrap">
  <div class="tzdb-graph">
    <svg class="edges" viewBox="0 0 940 480">
      <path
        v-for="(e, i) in edges"
        :key="i"
        v-click="e.click"
        :d="path(e)"
        fill="none"
        stroke="#64748b"
        stroke-width="2"
      />
    </svg>

    <div class="cluster source" :style="{ left: source.x + 'px', top: source.y + 'px', width: source.w + 'px', height: source.h + 'px' }">
      <div class="title">tz (IANA)</div>
      <div class="item"><span>dépôt eggert/tz</span><span class="version">{{ LATEST }}</span></div>
    </div>

    <div
      v-for="c in clusters"
      :key="c.id"
      v-click="c.click"
      class="cluster"
      :style="{ left: c.x + 'px', top: c.y + 'px', width: c.w + 'px', height: height(c) + 'px' }"
    >
      <div class="title">{{ c.title }}</div>
      <div v-for="it in c.items" :key="it.name" class="item">
        <span><span v-if="it.lang" class="lang" :class="`l-${it.lang}`">{{ LANGS[it.lang] }}</span>{{ it.name }}<span v-if="it.note" class="note"> {{ it.note }}</span></span>
        <span v-if="it.version" class="version" :class="level(it.version)">{{ it.version }}</span>
      </div>
    </div>

    <div v-click="10" class="question">Quel est le tzdata de ce que je déploie ?</div>
  </div>
  </div>
</template>

<style scoped>
.tzdb-wrap {
  width: 846px;
  height: 432px;
  margin: 0 auto;
}
.tzdb-graph {
  position: relative;
  width: 940px;
  height: 480px;
  transform: scale(0.9);
  transform-origin: top left;
}
.edges {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  overflow: visible;
}
.cluster {
  position: absolute;
  padding: 0.25rem 0.5rem;
  border: 1px solid #cbd5e1;
  border-radius: 8px;
  background: #f1f5f9;
  color: #0f172a;
  box-sizing: border-box;
}
.cluster.source {
  border: 2px solid #22c55e;
}
.title {
  font-size: 0.7rem;
  font-weight: bold;
  text-transform: uppercase;
  letter-spacing: 0.04em;
  opacity: 0.65;
  line-height: 1.3rem;
}
.item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  height: 19px;
  font-size: 0.78rem;
  white-space: nowrap;
}
.lang {
  display: inline-block;
  width: 15px;
  margin-right: 0.3rem;
  border-radius: 4px;
  font-family: ui-monospace, 'Fira Code', monospace;
  font-size: 0.58rem;
  font-weight: bold;
  line-height: 14px;
  text-align: center;
  color: white;
  vertical-align: 1px;
}
.lang.l-py { background: #3776ab; }
.lang.l-js { background: #f7df1e; color: #1f2937; }
.lang.l-java { background: #e76f00; }
.lang.l-net { background: #512bd4; }
.lang.l-go { background: #00add8; }
.lang.l-rs { background: #b7410e; }
.lang.l-rb { background: #cc342d; }
.lang.l-php { background: #777bb4; }
.lang.l-ex { background: #6e4a7e; }
.note {
  margin-left: 0.3rem;
  font-size: 0.62rem;
  opacity: 0.7;
}
.version {
  margin-left: 0.5rem;
  padding: 0 0.4rem;
  border-radius: 999px;
  font-family: ui-monospace, 'Fira Code', monospace;
  font-size: 0.72rem;
  font-weight: bold;
  background: #e2e8f0;
}
.source .version {
  background: #bbf7d0;
}
.tzdb-graph:has(.question:not(.slidev-vclick-hidden)) .version.ok {
  background: #bbf7d0;
}
.tzdb-graph:has(.question:not(.slidev-vclick-hidden)) .version.late {
  background: #fed7aa;
}
.tzdb-graph:has(.question:not(.slidev-vclick-hidden)) .version.old,
.tzdb-graph:has(.question:not(.slidev-vclick-hidden)) .version.none {
  background: #fecaca;
}
.question {
  position: absolute;
  left: 0;
  right: 0;
  top: 450px;
  text-align: center;
  font-size: 1.25rem;
  font-weight: bold;
}
</style>
