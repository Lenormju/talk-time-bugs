<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import { useSecondTick } from '../composables/useSecondTick'

// « Mesure réelle » : nécessite `uv run scripts/ntp_server.py` sur la machine locale.
// « Mesure simulée » : hors ligne, valeurs plausibles autour de la capture réelle.
// État initial : la capture réelle (public/ntp-capture.json), étiquetée « capture ».
const ENDPOINT = 'http://127.0.0.1:8123/ntp'
const TIMEOUT_MS = 4000

interface Measure {
  source: 'ntp' | 'http-date'
  server: string
  server_ip?: string
  leap?: number
  leap_text?: string
  version?: number
  mode?: number
  mode_text?: string
  stratum: number | null
  poll?: number
  precision?: number
  root_delay_ms?: number
  root_dispersion_ms?: number
  refid: string | null
  refid_raw?: string
  refid_kind?: string
  reference_time?: string | null
  t1_origin?: string | null
  t2_receive?: string | null
  t3_transmit?: string | null
  t4_destination?: string | null
  offset_ms: number
  delay_ms: number
  precision_s?: number
  errors?: string[]
  captured_at?: string
}
type Kind = 'capture' | 'simulée' | 'ntp' | 'http-date'

// Secours si même le fichier de capture est illisible (la simulation doit toujours marcher).
const FALLBACK: Measure = {
  source: 'ntp', server: 'fr.pool.ntp.org', server_ip: '193.42.63.23',
  leap: 0, leap_text: "pas d'alerte", version: 4, mode: 4, mode_text: 'serveur',
  stratum: 2, poll: 0, precision: -25, root_delay_ms: 10.2, root_dispersion_ms: 0.7,
  refid: '216.239.35.8', refid_raw: 'd8ef2308', refid_kind: 'IPv4 du serveur amont (ou hash)',
  reference_time: '2026-10-30T03:12:34.083879Z',
  t1_origin: '2026-10-30T03:19:38.622008Z', t2_receive: '2026-10-30T03:19:38.657160Z',
  t3_transmit: '2026-10-30T03:19:38.657238Z', t4_destination: '2026-10-30T03:19:38.714903Z',
  offset_ms: -11.3, delay_ms: 92.8,
}

const now = useSecondTick()
const base = ref<Measure>(FALLBACK)
const data = ref<Measure | null>(null)
const kind = ref<Kind>('capture')
const busy = ref(false)
const error = ref('')

onMounted(async () => {
  try {
    const r = await fetch(import.meta.env.BASE_URL + 'ntp-capture.json')
    base.value = await r.json()
    data.value = base.value
  } catch {
    data.value = null
  }
})

async function measureReal() {
  busy.value = true
  error.value = ''
  const ctl = new AbortController()
  const t = setTimeout(() => ctl.abort(), TIMEOUT_MS)
  try {
    const r = await fetch(ENDPOINT, { signal: ctl.signal })
    if (!r.ok) throw new Error(`HTTP ${r.status}`)
    const m: Measure = await r.json()
    data.value = m
    kind.value = m.source
  } catch (e) {
    error.value = 'Mesure réelle impossible : le serveur local est-il lancé ? Lancer ./ntp.sh (sinon : délai dépassé, pas de réseau, extension qui bloque).'
  } finally {
    clearTimeout(t)
    busy.value = false
  }
}

function measureSimulated() {
  error.value = ''
  const b = base.value
  const delay = Math.max(5, (b.delay_ms ?? 40) + (Math.random() - 0.5) * 20)
  const offset = (Math.random() - 0.5) * 10
  const t1 = Date.now()
  // le serveur reçoit à mi-délai (+ offset), répond quasi instantanément
  const t2 = t1 + delay / 2 + offset
  const t3 = t2 + 0.1
  const t4 = t1 + delay
  const iso = (ms: number) => new Date(ms).toISOString().replace('Z', '000Z')
  data.value = {
    ...b,
    source: 'ntp',
    errors: undefined,
    root_delay_ms: (b.root_delay_ms ?? 10) * (0.8 + Math.random() * 0.4),
    root_dispersion_ms: (b.root_dispersion_ms ?? 1) * (0.8 + Math.random() * 0.4),
    reference_time: iso(t1 - 60000 - Math.random() * 600000),
    t1_origin: iso(t1), t2_receive: iso(t2), t3_transmit: iso(t3), t4_destination: iso(t4),
    offset_ms: offset,
    delay_ms: delay,
  }
  kind.value = 'simulée'
}

const fmt = (ms: number) => new Date(ms).toLocaleTimeString('fr-FR')
const local = computed(() => fmt(now.value))
const ntpTime = computed(() => (data.value ? fmt(now.value + data.value.offset_ms) : '…'))
const showClocks = computed(() => kind.value !== 'capture' && data.value !== null)
const label = computed(() => {
  switch (kind.value) {
    case 'ntp': return 'réelle (NTP)'
    case 'http-date': return 'réelle (en-tête Date, ±1 s)'
    case 'simulée': return 'simulée (valeurs fictives)'
    default: return `capture du ${data.value?.captured_at?.replace('T', ' ').slice(0, 19) ?? '?'}`
  }
})
const v = (x: unknown) => (x === null || x === undefined || x === '' ? '—' : String(x))
const ms = (x?: number) => (x === undefined ? '—' : x.toFixed(2) + ' ms')
const pow = (x?: number) => (x === undefined ? '—' : `${x} (2^${x} = ${Math.pow(2, x).toPrecision(2)} s)`)
const sign = (n: number) => (n >= 0 ? '+' : '−') + Math.abs(n).toFixed(1)
</script>

<template>
  <div class="ntp-wrap">
    <div class="buttons">
      <button :disabled="busy" @click="measureReal">{{ busy ? 'Mesure en cours…' : 'Interroger un vrai serveur' }}</button>
      <button :disabled="busy" @click="measureSimulated">Simuler (hors ligne)</button>
      <div v-if="showClocks" class="clocks">
        <span>heure locale <b>{{ local }}</b></span>
        <span>heure du serveur <b>{{ ntpTime }}</b></span>
      </div>
    </div>
    <div v-if="error" class="err">
      {{ error }} <a href="#" @click.prevent="measureSimulated">Passer en simulation</a>
    </div>
  <div class="ntp-demo" :class="kind">
    <div v-if="data" class="src">{{ label }}</div>
    <div v-if="data" class="groups">
      <section>
        <h4>Résultat</h4>
        <table>
          <tbody>
            <tr><td>décalage (offset)</td><td>{{ sign(data.offset_ms) }} ms</td></tr>
            <tr><td>délai (delay)</td><td>{{ data.delay_ms.toFixed(1) }} ms</td></tr>
            <tr><td>stratum</td><td>{{ v(data.stratum) }}</td></tr>
            <tr><td>refid</td><td>{{ v(data.refid) }}</td></tr>
            <tr><td>serveur</td><td>{{ v(data.server) }} <small>{{ data.server_ip }}</small></td></tr>
          </tbody>
        </table>
      </section>
      <section class="hdr">
        <h4>En-tête du paquet</h4>
        <table class="dense">
          <tbody>
            <tr><td>leap indicator</td><td>{{ v(data.leap) }} <small>{{ data.leap_text }}</small></td></tr>
            <tr><td>version</td><td>{{ v(data.version) }}</td></tr>
            <tr><td>mode</td><td>{{ v(data.mode) }} <small>{{ data.mode_text }}</small></td></tr>
            <tr><td>poll</td><td>{{ pow(data.poll) }}</td></tr>
            <tr><td>precision</td><td>{{ pow(data.precision) }}</td></tr>
            <tr><td>root delay</td><td>{{ ms(data.root_delay_ms) }}</td></tr>
            <tr><td>root dispersion</td><td>{{ ms(data.root_dispersion_ms) }}</td></tr>
            <tr><td>refid (brut)</td><td>{{ v(data.refid_raw) }} <small>{{ data.refid_kind }}</small></td></tr>
          </tbody>
        </table>
      </section>
      <section class="ts">
        <h4>Horodatages (UTC)</h4>
        <table>
          <tbody>
            <tr><td>reference</td><td>{{ v(data.reference_time) }}</td></tr>
            <tr><td>T1 envoi client</td><td>{{ v(data.t1_origin) }}</td></tr>
            <tr><td>T2 réception serveur</td><td>{{ v(data.t2_receive) }}</td></tr>
            <tr><td>T3 envoi serveur</td><td>{{ v(data.t3_transmit) }}</td></tr>
            <tr><td>T4 réception client</td><td>{{ v(data.t4_destination) }}</td></tr>
            <tr v-if="data.precision_s"><td>précision</td><td>±{{ data.precision_s }} s</td></tr>
            <tr v-if="data.errors?.length"><td>échecs</td><td><small>{{ data.errors.join(' | ') }}</small></td></tr>
          </tbody>
        </table>
      </section>
    </div>
    <div v-else class="src">pas de mesure disponible</div>
  </div>
  </div>
</template>

<style scoped>
.ntp-demo { font-size: 1em; border: 2px solid #4a4; border-radius: 8px; padding: 0.4rem 0.8rem; }
.ntp-demo.capture, .ntp-demo.simulée { border-color: #c80; border-style: dashed; }
.buttons { display: flex; gap: 0.8rem; margin-bottom: 0.5rem; align-items: center; }
.clocks { display: flex; gap: 1.2rem; margin-left: 0.8rem; font-size: 0.95em; font-variant-numeric: tabular-nums; }
.clocks b { font-weight: 600; }
button { border: 1px solid currentColor; border-radius: 6px; padding: 0.1rem 0.6rem; }
button:disabled { opacity: 0.5; }
.err { color: #c33; font-weight: bold; font-size: 0.8em; margin-bottom: 0.4rem; }
.src { font-weight: bold; font-size: 1.15em; margin-bottom: 0.2rem; }
.capture .src, .simulée .src { color: #c80; }
.groups { display: grid; grid-template-columns: auto 1fr; gap: 0.2rem 1.5rem; }
.groups section:first-child { grid-row: 1 / 3; }
h4 { margin: 0.2rem 0; opacity: 0.8; font-size: 0.8em; }
table { border-collapse: collapse; }
td { padding: 0 0.8rem 0 0; font-variant-numeric: tabular-nums; }
td:first-child { opacity: 0.7; }
small { opacity: 0.6; font-size: 0.7em; }
/* Résultat : gros */
section:first-child table { font-size: 1.1em; }
/* Horodatages : taille moyenne */
.ts table { font-size: 0.75em; }
/* En-tête du paquet : petit, atténué, dense sur 2 colonnes de paires */
.hdr { opacity: 0.7; font-size: 0.65em; }
.hdr tbody { display: grid; grid-template-columns: repeat(2, auto auto); column-gap: 1rem; }
.hdr tr { display: contents; }
</style>
