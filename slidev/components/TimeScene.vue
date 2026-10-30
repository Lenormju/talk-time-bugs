<script setup lang="ts">
import { computed, onMounted, reactive, watch } from 'vue'
import { useSlideContext } from '@slidev/client'
import gsap from 'gsap'
import { useSecondTick } from '../composables/useSecondTick'

// Scène « offset → zone → naïf / offset / zoned » (slide 05, 12 clics).
//  1-3   : couche Offset. 1 ligne UTC + instant (live), 2 trois horloges, 3 offsets + ISO découpé
//  4-9   : couche Zone. 4 axe des dates, 5 bandes +02:00 / +01:00, 6 curseur juste avant le passage (02:59 +02:00),
//          7 curseur juste après (02:00 +01:00), 8 cadre Europe/Paris, 9 Shanghai et Cancun
//  10-12 : couche Naïf / offset / zoned sur 2026-10-25 02:30. 10 naïf (2 candidats), 11 avec offset, 12 zoned (fold)
// Heures locales et offsets calculés par Intl (le tzdata du navigateur), jamais codés en dur.
// Constantes vérifiées par exécution (Node 22 Intl + Python zoneinfo) :
//  Europe/Paris passe de +02:00 à +01:00 le 2026-10-25 à 01:00Z ;
//  02:30 fold=0 → 00:30Z, fold=1 → 01:30Z ; Shanghai +08:00 sans changement d'heure ;
//  New York passe de -04:00 (EDT) à -05:00 (EST) le 2026-11-01 à 06:00Z.

const H = 3_600_000
const SWITCH = Date.UTC(2026, 9, 25, 1) // passage CEST → CET

// Clics de la slide (contexte de la slide : correct aussi dans l'aperçu « clic suivant » du mode présentateur)
const { $clicks } = useSlideContext()
const step = computed(() => $clicks.value)
const layer = computed(() => (step.value >= 10 ? 3 : step.value >= 4 ? 2 : step.value >= 1 ? 1 : 0))

// ---------- Intl ----------
const LOCAL_TZ = Intl.DateTimeFormat().resolvedOptions().timeZone
// « Europe/Paris » → « Paris », « America/Sao_Paulo » → « Sao Paulo » (ville du navigateur, pas codée en dur)
const LOCAL_CITY = LOCAL_TZ.split('/').pop()!.replace(/_/g, ' ')
const fmts = new Map<string, Intl.DateTimeFormat>()
function parts(tz: string, ms: number) {
  let f = fmts.get(tz)
  if (!f) {
    f = new Intl.DateTimeFormat('fr-FR', {
      timeZone: tz, year: 'numeric', month: '2-digit', day: '2-digit', weekday: 'short',
      hour: '2-digit', minute: '2-digit', second: '2-digit', hourCycle: 'h23', timeZoneName: 'longOffset',
    })
    fmts.set(tz, f)
  }
  const p: Record<string, string> = {}
  for (const x of f.formatToParts(ms)) p[x.type] = x.value
  // « UTC+01:00 » → « +01:00 », « UTC » → « +00:00 », signe moins Unicode → « - »
  const offset = (p.timeZoneName ?? '').replace(/^(UTC|GMT)/, '').replace('−', '-') || '+00:00'
  return {
    time: `${p.hour}:${p.minute}:${p.second}`,
    hm: `${p.hour}:${p.minute}`,
    day: `${p.weekday} ${p.day}/${p.month}`,
    iso: `${p.year}-${p.month}-${p.day}T${p.hour}:${p.minute}:${p.second}`,
    offset,
  }
}

// ---------- couche 1 : offset ----------
const now = useSecondTick()
const instant = now

const L_X0 = 145
const L_X1 = 850
const LINE_Y = 62
const anchor = computed(() => Math.floor(now.value / H) * H)
const wStart = computed(() => anchor.value - 12 * H)
const wEnd = computed(() => anchor.value + 12 * H)
const xOf = (ms: number) => L_X0 + ((ms - wStart.value) / (wEnd.value - wStart.value)) * (L_X1 - L_X0)
const ticks = computed(() => {
  const out: { x: number; label: string }[] = []
  for (let t = Math.ceil(wStart.value / (3 * H)) * 3 * H; t <= wEnd.value; t += 3 * H)
    out.push({ x: xOf(t), label: `${String(new Date(t).getUTCHours()).padStart(2, '0')}:00Z` })
  return out
})
const dotX = computed(() => xOf(instant.value))
const utc = computed(() => parts('UTC', instant.value))

const clocks = computed(() => [
  { name: 'Rio', tz: 'America/Sao_Paulo', x: 170 },
  { name: `ici (${LOCAL_CITY})`, tz: LOCAL_TZ, x: 460 },
  { name: 'Shanghai', tz: 'Asia/Shanghai', x: 750 },
].map(c => ({ ...c, ...parts(c.tz, instant.value) })))
const ici = computed(() => clocks.value[1])

// ---------- couche 2 : zone ----------
// Axe UTC du 23/10 au 03/11 : bascule de Paris (25/10 01:00Z) et de New York (01/11 06:00Z, vérifiée par Intl et zoneinfo)
const Z_START = Date.UTC(2026, 9, 23)
const Z_END = Date.UTC(2026, 10, 3)
const Z_X0 = 130
const Z_X1 = 890
const zx = (ms: number) => Z_X0 + ((ms - Z_START) / (Z_END - Z_START)) * (Z_X1 - Z_X0)
const AXIS_Y = 318
const days = Array.from({ length: 12 }, (_, i) => {
  const t = Z_START + i * 24 * H
  const d = new Date(t)
  return { x: zx(t), label: `${String(d.getUTCDate()).padStart(2, '0')}/${String(d.getUTCMonth() + 1).padStart(2, '0')}` }
})
// offsets de Paris avant / après le passage (aussi utilisés par la couche 3)
const parisBefore = parts('Europe/Paris', SWITCH - H).offset
const parisAfter = parts('Europe/Paris', SWITCH + H).offset
const NY_SWITCH = Date.UTC(2026, 10, 1, 6) // America/New_York : EDT -04:00 → EST -05:00
const ROW_H = 70
type Seg = { from: number; to: number; color: string; abbr: string }
type Row = { tz: string; y: number; tagW: number; segs: Seg[] }
// une ligne par zone ; y = haut du cadre ; offsets des bandes calculés par Intl au milieu de chaque bande
const rows: Row[] = [
  { tz: 'Europe/Paris', y: 36, tagW: 128, segs: [
    { from: Z_START, to: SWITCH, color: '#b45309', abbr: 'CEST' },
    { from: SWITCH, to: Z_END, color: '#0369a1', abbr: 'CET' }] },
  { tz: 'Asia/Shanghai', y: 126, tagW: 132, segs: [
    { from: Z_START, to: Z_END, color: '#0f766e', abbr: 'CST' }] },
  { tz: 'America/New_York', y: 216, tagW: 150, segs: [
    { from: Z_START, to: NY_SWITCH, color: '#be185d', abbr: 'EDT' },
    { from: NY_SWITCH, to: Z_END, color: '#475569', abbr: 'EST' }] },
]
const rowsView = rows.map(r => ({
  ...r,
  segs: r.segs.map(g => ({ ...g, x: zx(g.from), w: zx(g.to) - zx(g.from), offset: parts(r.tz, (g.from + g.to) / 2).offset })),
}))
const switches = [
  { x: zx(SWITCH), label: '25/10 01:00Z' },
  { x: zx(NY_SWITCH), label: '01/11 06:00Z' },
]
const CUR_FROM = Date.UTC(2026, 9, 24, 21)
const CUR_BEFORE = SWITCH - 60_000 // 00:59Z = 02:59 +02:00 à Paris
const CUR_AFTER = SWITCH // 01:00Z = 02:00 +01:00 à Paris
// étiquette du curseur sur chaque ligne : heure locale + offset à cet instant, couleur de la bande traversée
const cursorRows = computed(() => rows.map((r) => {
  const p = parts(r.tz, s.cursorMs)
  const seg = r.segs.find(g => s.cursorMs >= g.from && s.cursorMs < g.to) ?? r.segs[0]
  return { y: r.y, text: `${p.day} ${p.hm} ${p.offset}`, color: seg.color }
}))

// ---------- couche 3 : naïf / offset / zoned ----------
const N_START = Date.UTC(2026, 9, 24, 22, 30)
const N_END = Date.UTC(2026, 9, 25, 3, 30)
const N_X0 = 80
const N_X1 = 860
const nx = (ms: number) => N_X0 + ((ms - N_START) / (N_END - N_START)) * (N_X1 - N_X0)
const N_LINE_Y = 250
const nTicks = [23, 0, 1, 2, 3].map((h, i) => ({ x: nx(Date.UTC(2026, 9, 24, 23 + i)), label: `${String(h).padStart(2, '0')}:00Z` }))
const cand = [Date.UTC(2026, 9, 25, 0, 30), Date.UTC(2026, 9, 25, 1, 30)].map(t => ({ t, x: nx(t), ...parts('UTC', t) }))
const nSwitchX = nx(SWITCH)
// heures locales de Paris affichées au-dessus des bandes, toutes les 30 min
const localMarks = Array.from({ length: 9 }, (_, i) => Date.UTC(2026, 9, 24, 23) + i * H / 2)
  .map(t => ({ x: nx(t), label: parts('Europe/Paris', t).hm, hot: parts('Europe/Paris', t).hm === '02:30', color: t === cand[0].t ? '#2563eb' : '#ea580c' }))

// ---------- animations ----------
const s = reactive({
  l1: 0, line: 0, clocks: 0, offsets: 0,
  l2: 0, axis: 0, bands: 0, cur: 0, frame: 0, others: 0, cursorMs: CUR_FROM,
  l3: 0, naive: 0, off: 0, zoned: 0, cand2: 0,
})

// Curseur de date, piloté par clic (aucune pause temporisée) :
// clic 6 → 02:59 +02:00 (juste avant le passage), clic 7 → 02:00 +01:00 (juste après)
const cursorTarget = (n: number) => (n < 6 ? CUR_FROM : n === 6 ? CUR_BEFORE : CUR_AFTER)

function apply(n: number, prev = n) {
  gsap.to(s, {
    l1: n >= 1 && n <= 3 ? 1 : 0,
    line: n >= 1 ? 1 : 0, clocks: n >= 2 ? 1 : 0, offsets: n >= 3 ? 1 : 0,
    l2: n >= 4 && n <= 9 ? 1 : 0,
    axis: n >= 4 ? 1 : 0, bands: n >= 5 ? 1 : 0, cur: n >= 6 ? 1 : 0, frame: n >= 8 ? 1 : 0, others: n >= 9 ? 1 : 0,
    l3: n >= 10 ? 1 : 0,
    naive: n === 10 ? 1 : 0, off: n === 11 ? 1 : 0, zoned: n >= 12 ? 1 : 0,
    cand2: n === 10 || n >= 12 ? 1 : 0, // la zone ne tranche pas : 2 candidats de même poids
    duration: 0.6, ease: 'power2.inOut', overwrite: 'auto',
  })
  gsap.killTweensOf(s, 'cursorMs')
  const target = cursorTarget(n)
  if (n === prev || (n !== 6 && n !== 7)) {
    s.cursorMs = target // arrivée directe (montage, saut de clics, autres couches)
  }
  else {
    if (n === 6 && prev < 6) s.cursorMs = CUR_FROM
    gsap.to(s, { cursorMs: target, duration: n === 6 && prev < 6 ? 1 : 0.6, ease: 'power2.out' })
  }
}

onMounted(() => {
  apply(step.value)
  watch(step, (n, prev) => apply(n, prev))
})
</script>

<template>
  <div class="scene">
    <!-- stepper -->
    <div class="stepper">
      <div class="tab" :class="{ on: layer === 1 }">1 Offset</div>
      <div class="tab" :class="{ on: layer === 2 }">2 Zone</div>
      <div class="tab" :class="{ on: layer === 3 }">3 Naïf / zoned</div>
    </div>

    <div class="stage">
      <svg viewBox="0 0 920 380" width="920" height="380" style="overflow: visible">
        <defs>
          <marker id="ts-arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
            <path d="M0,0 L10,5 L0,10 z" fill="#64748b" />
          </marker>
        </defs>

        <!-- ===================== couche 1 : offset ===================== -->
        <g :style="{ opacity: s.l1 }">
          <g :style="{ opacity: s.line }">
            <text x="0" :y="LINE_Y + 6" class="axis-name">UTC <tspan class="dim-svg">(00:00, Zulu)</tspan></text>
            <line :x1="L_X0" :y1="LINE_Y" :x2="L_X1 + 18" :y2="LINE_Y" stroke="#64748b" stroke-width="3" marker-end="url(#ts-arrow)" />
            <g v-for="t in ticks" :key="t.label + t.x">
              <line :x1="t.x" :y1="LINE_Y - 5" :x2="t.x" :y2="LINE_Y + 5" stroke="#64748b" stroke-width="2" />
              <text :x="t.x" :y="LINE_Y + 24" text-anchor="middle" class="tick">{{ t.label }}</text>
            </g>
          </g>

          <!-- horloges reliées à l'instant -->
          <g :style="{ opacity: s.clocks }">
            <g v-for="c in clocks" :key="c.name">
              <line :x1="dotX" :y1="LINE_Y" :x2="c.x" y2="130" stroke="#2563eb" stroke-width="2" stroke-dasharray="5 4" style="opacity: 0.7" />
              <rect :x="c.x - 110" y="130" width="220" height="94" rx="10" class="clock" />
              <text :x="c.x" y="154" text-anchor="middle" class="clock-name">{{ c.name }}</text>
              <text :x="c.x" y="194" text-anchor="middle" class="clock-time">{{ c.time }}</text>
              <text :x="c.x" y="216" text-anchor="middle" class="clock-day">{{ c.day }}</text>
              <g :style="{ opacity: s.offsets }">
                <rect :x="c.x - 46" y="231" width="92" height="30" rx="15" fill="#ea580c" />
                <text :x="c.x" y="252" text-anchor="middle" class="pill">{{ c.offset }}</text>
              </g>
            </g>
          </g>

          <!-- l'instant -->
          <g :style="{ opacity: s.line }">
            <circle :cx="dotX" :cy="LINE_Y" r="12" fill="#2563eb" stroke="white" stroke-width="3" />
            <text :x="dotX" :y="LINE_Y - 22" text-anchor="middle" class="instant">{{ utc.time }}Z</text>
          </g>
        </g>

        <!-- ===================== couche 2 : zone ===================== -->
        <g :style="{ opacity: s.l2 }">
          <g :style="{ opacity: s.axis }">
            <line :x1="Z_X0 - 10" :y1="AXIS_Y" :x2="Z_X1 + 18" :y2="AXIS_Y" stroke="#64748b" stroke-width="3" marker-end="url(#ts-arrow)" />
            <text x="0" :y="AXIS_Y + 6" class="axis-name">UTC</text>
            <g v-for="d in days" :key="d.label">
              <line :x1="d.x" :y1="AXIS_Y - 6" :x2="d.x" :y2="AXIS_Y + 6" stroke="#64748b" stroke-width="2" />
              <text :x="d.x" :y="AXIS_Y + 26" text-anchor="middle" class="tick">{{ d.label }}</text>
            </g>
          </g>

          <!-- trait du curseur, dessiné sous les lignes (les étiquettes de zone passent devant) -->
          <line :x1="zx(s.cursorMs)" y1="30" :x2="zx(s.cursorMs)" :y2="AXIS_Y" stroke="#2563eb" stroke-width="3" :style="{ opacity: s.cur }" />

          <!-- lignes de zones : Paris (clic 5), Shanghai et New York (clic 9) -->
          <g v-for="(r, ri) in rowsView" :key="r.tz" :style="{ opacity: ri === 0 ? s.bands : s.others }">
            <rect v-for="g in r.segs" :key="g.abbr" :x="g.x" :y="r.y + 34" :width="g.w" height="30" class="band" :fill="g.color" />
            <text v-for="g in r.segs" :key="'l' + g.abbr" :x="g.x + g.w / 2" :y="r.y + 55" text-anchor="middle" class="band-label">{{ g.offset }} · {{ g.abbr }}</text>
            <!-- cadre de la zone (Paris : clic 8, les autres arrivent avec leur cadre) -->
            <g :style="{ opacity: ri === 0 ? s.frame : 1 }">
              <rect :x="Z_X0 - 12" :y="r.y" :width="Z_X1 - Z_X0 + 24" :height="ROW_H" rx="10" class="zone-frame" />
              <rect :x="Z_X0 - 4" :y="r.y - 11" :width="r.tagW" height="22" rx="5" fill="#7c3aed" />
              <text :x="Z_X0 - 4 + r.tagW / 2" :y="r.y + 5" text-anchor="middle" class="zone-tag">{{ r.tz }}</text>
            </g>
          </g>

          <!-- instants de bascule, sous les lignes -->
          <g v-for="(w, wi) in switches" :key="w.label" :style="{ opacity: wi === 0 ? s.bands : s.others }">
            <line :x1="w.x" :y1="AXIS_Y - 26" :x2="w.x" :y2="AXIS_Y" stroke="#64748b" stroke-width="1.5" stroke-dasharray="3 3" />
            <text :x="w.x - 5" :y="AXIS_Y - 10" text-anchor="end" class="tick small-tick">{{ w.label }}</text>
          </g>

          <!-- curseur de date : une étiquette par ligne visible -->
          <g :style="{ opacity: s.cur }">
            <g v-for="(c, ci) in cursorRows" :key="c.y" :style="{ opacity: ci === 0 ? 1 : s.others }">
              <rect :x="zx(s.cursorMs) + 8" :y="c.y + 7" width="212" height="24" rx="5" :fill="c.color" />
              <text :x="zx(s.cursorMs) + 114" :y="c.y + 24" text-anchor="middle" class="cursor-label">{{ c.text }}</text>
            </g>
          </g>
        </g>

        <!-- ===================== couche 3 : naïf / offset / zoned ===================== -->
        <g :style="{ opacity: s.l3 }">
          <!-- bandes de règles (zoned) -->
          <g :style="{ opacity: s.zoned }">
            <rect :x="N_X0 - 10" y="110" :width="N_X1 - N_X0 + 20" height="96" rx="10" class="zone-frame" />
            <rect :x="N_X0 - 2" y="99" width="128" height="22" rx="5" fill="#7c3aed" />
            <text :x="N_X0 + 62" y="115" text-anchor="middle" class="zone-tag">Europe/Paris</text>
            <rect :x="N_X0" y="160" :width="nSwitchX - N_X0" height="34" class="band" fill="#b45309" />
            <rect :x="nSwitchX" y="160" :width="N_X1 - nSwitchX" height="34" class="band" fill="#0369a1" />
            <text :x="(N_X0 + nSwitchX) / 2" y="183" text-anchor="middle" class="band-label">{{ parisBefore }}</text>
            <text :x="(nSwitchX + N_X1) / 2" y="183" text-anchor="middle" class="band-label">{{ parisAfter }}</text>
            <g v-for="m in localMarks" :key="m.x">
              <line :x1="m.x" y1="148" :x2="m.x" y2="160" :stroke="m.hot ? m.color : '#64748b'" stroke-width="2" />
              <text :x="m.x" y="142" text-anchor="middle" class="tick" :class="{ hot: m.hot }" :style="m.hot ? { fill: m.color } : undefined">{{ m.label }}</text>
            </g>
            <!-- 02:30 locale → UTC, via la bande -->
            <line :x1="cand[0].x" y1="194" :x2="cand[0].x" :y2="N_LINE_Y - 14" stroke="#2563eb" stroke-width="2.5" stroke-dasharray="5 4" />
            <line :x1="cand[1].x" y1="194" :x2="cand[1].x" :y2="N_LINE_Y - 14" stroke="#ea580c" stroke-width="2.5" stroke-dasharray="5 4" />
          </g>

          <!-- ligne UTC -->
          <text x="0" :y="N_LINE_Y + 6" class="axis-name">UTC</text>
          <line :x1="N_X0 - 10" :y1="N_LINE_Y" :x2="N_X1 + 18" :y2="N_LINE_Y" stroke="#64748b" stroke-width="3" marker-end="url(#ts-arrow)" />
          <g v-for="t in nTicks" :key="t.label">
            <line :x1="t.x" :y1="N_LINE_Y - 5" :x2="t.x" :y2="N_LINE_Y + 5" stroke="#64748b" stroke-width="2" />
            <text :x="t.x" :y="N_LINE_Y + 24" text-anchor="middle" class="tick">{{ t.label }}</text>
          </g>

          <!-- liens valeur → instants -->
          <line x1="460" y1="62" :x2="cand[0].x" :y2="N_LINE_Y - 16" stroke="#2563eb" stroke-width="2" stroke-dasharray="5 4" :style="{ opacity: Math.max(s.naive, s.off) * 0.8 }" />
          <line x1="460" y1="62" :x2="cand[1].x" :y2="N_LINE_Y - 16" stroke="#ea580c" stroke-width="2" stroke-dasharray="5 4" :style="{ opacity: s.naive * 0.8 }" />

          <!-- candidat 1 : 00:30Z -->
          <circle :cx="cand[0].x" :cy="N_LINE_Y" r="12" fill="none" stroke="#ea580c" stroke-width="4" :style="{ opacity: s.naive }" />
          <circle :cx="cand[0].x" :cy="N_LINE_Y" r="12" fill="#2563eb" stroke="white" stroke-width="3" :style="{ opacity: 1 - s.naive }" />
          <text :x="cand[0].x" :y="N_LINE_Y + 56" text-anchor="middle" class="cand">{{ cand[0].hm }}Z</text>
          <text :x="cand[0].x" :y="N_LINE_Y + 80" text-anchor="middle" class="cand-sub" :style="{ opacity: s.naive }">?</text>
          <text :x="cand[0].x" :y="N_LINE_Y + 80" text-anchor="middle" class="cand-sub" :style="{ opacity: s.zoned, fill: '#2563eb' }">fold=0</text>

          <!-- candidat 2 : 01:30Z -->
          <g :style="{ opacity: s.cand2 }">
            <circle :cx="cand[1].x" :cy="N_LINE_Y" r="12" fill="none" stroke="#ea580c" stroke-width="4" :style="{ opacity: s.naive }" />
            <circle :cx="cand[1].x" :cy="N_LINE_Y" r="12" fill="#ea580c" stroke="white" stroke-width="3" :style="{ opacity: s.zoned }" />
            <text :x="cand[1].x" :y="N_LINE_Y + 56" text-anchor="middle" class="cand">{{ cand[1].hm }}Z</text>
            <text :x="cand[1].x" :y="N_LINE_Y + 80" text-anchor="middle" class="cand-sub" :style="{ opacity: s.naive }">?</text>
            <text :x="cand[1].x" :y="N_LINE_Y + 80" text-anchor="middle" class="cand-sub" :style="{ opacity: s.zoned }">fold=1</text>
          </g>
        </g>
      </svg>

      <!-- ===== textes HTML (positions en px, la scène fait 920 px de large) ===== -->

      <!-- couche 1 : chaînes ISO découpées -->
      <div class="iso-block" :style="{ opacity: s.l1 * s.offsets }">
        <div class="iso-rows">
          <div class="iso-row">
            <span class="seg local">{{ utc.iso }}</span><span class="seg off">Z</span>
            <span class="who">UTC</span>
          </div>
          <div class="iso-row top">
            <span class="segcol"><span class="seg local">{{ ici.iso }}</span><small>heure locale</small></span><span class="segcol"><span class="seg off">{{ ici.offset }}</span><small class="off-l">offset</small></span>
            <span class="who">ici ({{ LOCAL_CITY }})</span>
          </div>
        </div>
      </div>

      <!-- couche 3 : la valeur examinée -->
      <div class="value" :style="{ opacity: s.l3 }">
        <div class="v" :style="{ opacity: s.naive }">
          <span class="seg local">2026-10-25 02:30</span>
        </div>
        <div class="v" :style="{ opacity: s.off }">
          <span class="seg local">2026-10-25T02:30</span><span class="seg off">+02:00</span>
        </div>
        <div class="v" :style="{ opacity: s.zoned }">
          <span class="seg local">2026-10-25 02:30</span>&nbsp;<span class="seg zone">Europe/Paris</span>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.scene { width: 920px; user-select: none; }
/* onglets : fond seul, ni bordure, ni ombre, ni séparateur */
.stepper {
  display: flex; justify-content: center; align-items: center; gap: 14px;
  height: 32px; margin-bottom: 8px; font-size: 17px; font-weight: 600;
}
.tab {
  display: block; margin: 0; padding: 0 14px; height: 30px; line-height: 30px; white-space: nowrap;
  border: none; outline: none; box-shadow: none; background-image: none; text-decoration: none;
  border-radius: 15px; background-color: rgba(100, 116, 139, 0.16); color: inherit; opacity: 0.6;
  transition: background-color 0.4s, color 0.4s, opacity 0.4s;
}
.tab.on { background-color: #2563eb; color: white; opacity: 1; }
.stage { position: relative; width: 920px; height: 380px; }
svg { display: block; }

.axis-name { font-size: 15px; font-weight: bold; fill: currentColor; opacity: 0.8; }
.tick { font-size: 14px; font-family: ui-monospace, monospace; fill: currentColor; opacity: 0.75; }
.small-tick { font-size: 12px; }
.tick.hot { fill: #ea580c; opacity: 1; font-weight: bold; }
.instant { font-size: 19px; font-weight: bold; font-family: ui-monospace, monospace; fill: #2563eb; }

.clock { fill: rgba(100, 116, 139, 0.12); stroke: #64748b; stroke-width: 2; }
.clock-name { font-size: 17px; font-weight: bold; fill: currentColor; }
.clock-time { font-size: 34px; font-weight: bold; font-family: ui-monospace, monospace; fill: currentColor; }
.clock-day { font-size: 14px; fill: currentColor; opacity: 0.75; }
.pill { font-size: 17px; font-weight: bold; font-family: ui-monospace, monospace; fill: white; }

.band { rx: 4; }
.band-label { font-size: 15px; font-weight: bold; font-family: ui-monospace, monospace; fill: white; }
.zone-frame { fill: none; stroke: #7c3aed; stroke-width: 3; }
.zone-tag { font-size: 14px; font-weight: bold; font-family: ui-monospace, monospace; fill: white; }
.cursor-label { font-size: 14px; font-weight: bold; font-family: ui-monospace, monospace; fill: white; }

.cand { font-size: 18px; font-weight: bold; font-family: ui-monospace, monospace; fill: currentColor; }
.cand-sub { font-size: 17px; font-weight: bold; font-family: ui-monospace, monospace; fill: #ea580c; }

.seg { font-family: ui-monospace, monospace; font-weight: bold; padding: 0.05rem 0.3rem; border-radius: 4px; }
.seg.local { background: rgba(37, 99, 235, 0.15); border: 2px solid #2563eb; }
.seg.off { background: #ea580c; color: white; border: 2px solid #ea580c; }
.seg.zone { background: #7c3aed; color: white; border: 2px solid #7c3aed; }

.iso-block {
  pointer-events: none;
  position: absolute; left: 0; right: 0; top: 280px; font-size: 19px;
  display: flex; justify-content: center;
}
.iso-rows { display: flex; flex-direction: column; gap: 6px; }
.iso-row { display: flex; align-items: center; }
.iso-row .who { margin-left: 0.8rem; font-size: 16px; }
.dim-svg { font-weight: normal; fill-opacity: 0.6; }
.iso-row.top { align-items: flex-start; }
.iso-row.top .who { margin-top: 0.2rem; }
.segcol { display: inline-flex; flex-direction: column; align-items: center; }
.segcol small { font-size: 13px; opacity: 0.8; line-height: 1.3; }
.segcol small.off-l { color: #ea580c; font-weight: bold; opacity: 1; }

.value { pointer-events: none; position: absolute; left: 0; right: 0; top: 0; height: 60px; font-size: 28px; }
.value .v { position: absolute; inset: 0; display: flex; justify-content: center; align-items: center; }
</style>
