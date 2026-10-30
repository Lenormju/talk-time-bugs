<script setup lang="ts">
import { computed, onMounted, reactive, watch } from 'vue'
import { useNav } from '@slidev/client'
import gsap from 'gsap'

// Frise UTC des cas « Quand tzdata change ». Les clics (v-click) sont ceux de la slide :
//  1-2 : E_ancien, E_nouveau (Mexique, 10 h à Mexico le 12/04/2023, tzdata 2022e puis 2022f)
//  3-5 : U glisse de gauche à droite (cas 1, 3, 2 du tableau)
//  6   : Égypte, tzdata 2023a (10 h au Caire le 15/06/2023) : E_nouveau avant E_ancien (cas 4)
//  7   : Colombie, tzdata 2022g : l'UTC est un fait, seule l'heure locale affichée change
//  8   : Kazakhstan, tzdata 2024a : une heure locale devient ambiguë
// Valeurs exécutées avec le paquet PyPI tzdata (voir HANDOFF_05_conseils_stockage.md §3-4).
const tx = (i: number) => 100 + i * 175
const AXIS_Y = 110

const mexTicks = ['14:30Z', '15:00Z', '15:30Z', '16:00Z', '16:30Z']
const egyTicks = ['06:30Z', '07:00Z', '07:30Z', '08:00Z', '08:30Z']
const kazTicks = ['17:00Z', '17:30Z', '18:00Z', '18:30Z', '19:00Z']

const nav = useNav()

const s = reactive({
  sceneA: 0, sceneB: 0, sceneC: 0, egy: 0,
  oldX: tx(1), newX: tx(3), uX: 50,
  oldOp: 0, newOp: 0, uOp: 0,
  b2: 0, c2: 0, cards: 0,
})

const step = computed(() => nav.clicks.value)
// sens de la flèche du delta : +1 (vers la droite, DST abrogé) ou −1 (vers la gauche, DST rétabli)
const dir = computed(() => (s.newX >= s.oldX ? 1 : -1))

// cas 1 à 4 dans l'ordre d'apparition de U ; le dernier est l'Égypte
const cards = [
  { n: 1, titre: 'encore à venir', reaction: 'replanifier', quand: 3 },
  { n: 3, titre: 'le passé repasse dans le futur', reaction: 'alerter', quand: 4 },
  { n: 2, titre: 'déjà passé', reaction: 'logger', quand: 5 },
  { n: 4, titre: 'le futur devient passé', reaction: 'manqué', quand: 6 },
]
const activeCard = computed(() => (step.value >= 3 && step.value <= 6 ? step.value - 3 : -1))

const caption = computed(() => {
  switch (step.value) {
    case 0: return ''
    case 1: return 'Mexique, 12/04/2023 : 10 h à Mexico, calculé avec tzdata 2022e'
    case 2: return 'tzdata 2022f : le Mexique abroge le DST, le même rendez-vous recule d’une heure'
    case 3: return 'U : on met à jour tzdata avant les deux instants'
    case 4: return 'U : on met à jour entre les deux (retard de déploiement)'
    case 5: return 'U : on met à jour après les deux'
    case 6: return 'Égypte, 15/06/2023 : 10 h au Caire, tzdata 2023a rétablit le DST, le rendez-vous avance'
    case 7: return 'Colombie, tzdata 2022g : l’historique est corrigé, l’UTC (le fait) ne bouge pas, l’heure affichée si'
    default: return 'Kazakhstan, tzdata 2024a : 29/02/2024 à 23:30 locale, deux instants possibles, Python prend fold=0 sans rien dire'
  }
})

const uLabel = computed(() => {
  switch (step.value) {
    case 3: return 'U : bien avant'
    case 4: return 'U : 15:30Z'
    case 5: return 'U : bien après'
    default: return 'U : 07:30Z'
  }
})

function apply(n: number) {
  const egy = n >= 6 && n <= 6
  const a = n >= 1 && n <= 6
  const uX = n === 3 ? 50 : n === 5 ? 860 : tx(2)
  gsap.to(s, {
    sceneA: a ? 1 : 0, sceneB: n === 7 ? 1 : 0, sceneC: n >= 8 ? 1 : 0,
    egy: egy ? 1 : 0,
    oldX: egy ? tx(3) : tx(1), newX: egy ? tx(1) : tx(3),
    uX,
    oldOp: n >= 1 ? 1 : 0, newOp: n >= 2 ? 1 : 0, uOp: n >= 3 && n <= 6 ? 1 : 0,
    cards: n >= 3 && n <= 6 ? 1 : 0,
    duration: 0.7, ease: 'power2.inOut', overwrite: 'auto',
  })
  gsap.to(s, { b2: n === 7 ? 1 : 0, duration: 0.5, delay: n === 7 ? 0.9 : 0, overwrite: 'auto' })
  gsap.to(s, { c2: n >= 8 ? 1 : 0, duration: 0.5, delay: n >= 8 ? 0.9 : 0 })
}

onMounted(() => {
  apply(step.value)
  watch(step, apply)
})
</script>

<template>
  <div class="w-full">
    <svg viewBox="0 0 900 200" class="w-full" style="overflow: visible">
      <!-- axe UTC -->
      <line x1="60" :y1="AXIS_Y" x2="860" :y2="AXIS_Y" stroke="#64748b" stroke-width="3" />
      <polygon :points="`870,${AXIS_Y} 858,${AXIS_Y - 7} 858,${AXIS_Y + 7}`" fill="#64748b" />
      <g v-for="i in 5" :key="i">
        <line :x1="tx(i - 1)" :y1="AXIS_Y - 6" :x2="tx(i - 1)" :y2="AXIS_Y + 6" stroke="#64748b" stroke-width="2" />
        <text :x="tx(i - 1)" :y="AXIS_Y + 24" text-anchor="middle" class="tick" :style="{ opacity: 0.7 * s.sceneA * (1 - s.egy) }">{{ mexTicks[i - 1] }}</text>
        <text :x="tx(i - 1)" :y="AXIS_Y + 24" text-anchor="middle" class="tick" :style="{ opacity: 0.7 * s.sceneA * s.egy }">{{ egyTicks[i - 1] }}</text>
        <text :x="tx(i - 1)" :y="AXIS_Y + 24" text-anchor="middle" class="tick" :style="{ opacity: 0.7 * s.sceneC }">{{ kazTicks[i - 1] }}</text>
      </g>

      <!-- scène A : Mexique puis Égypte -->
      <g :opacity="s.sceneA">
        <!-- delta -->
        <g :opacity="s.newOp">
          <line :x1="s.oldX" y1="62" :x2="s.newX - dir * 12" y2="62" stroke="#94a3b8" stroke-width="2" stroke-dasharray="5 4" />
          <polygon :points="`${s.newX},62 ${s.newX - dir * 14},55 ${s.newX - dir * 14},69`" fill="#94a3b8" />
          <text :x="(s.oldX + s.newX) / 2" y="52" text-anchor="middle" class="gap">{{ s.egy > 0.5 ? 'DST rétabli : −1 h' : 'DST abrogé : +1 h' }}</text>
        </g>
        <!-- E ancien -->
        <g :opacity="s.oldOp">
          <circle :cx="s.oldX" :cy="AXIS_Y" r="11" fill="none" stroke="#94a3b8" stroke-width="4" />
          <text :x="s.oldX" y="88" text-anchor="middle" class="what">E<tspan dy="4" class="sub">ancien</tspan><tspan dy="-4"> {{ s.egy > 0.5 ? '08:00Z' : '15:00Z' }}</tspan></text>
        </g>
        <!-- E nouveau -->
        <g :opacity="s.newOp">
          <circle :cx="s.newX" :cy="AXIS_Y" r="11" fill="#3b82f6" />
          <text :x="s.newX" y="160" text-anchor="middle" class="what" fill="#3b82f6">E<tspan dy="4" class="sub">nouveau</tspan><tspan dy="-4"> {{ s.egy > 0.5 ? '07:00Z' : '16:00Z' }}</tspan></text>
        </g>
        <!-- U -->
        <g :opacity="s.uOp">
          <line :x1="s.uX" y1="68" :x2="s.uX" y2="150" stroke="#fb923c" stroke-width="3" stroke-dasharray="6 4" />
          <text :x="Math.min(Math.max(s.uX, 100), 800)" y="192" text-anchor="middle" class="what warn">{{ uLabel }}</text>
        </g>
      </g>

      <!-- scène B : Colombie, fait observé -->
      <g :opacity="s.sceneB">
        <circle :cx="tx(2)" :cy="AXIS_Y" r="12" fill="#3b82f6" />
        <text :x="tx(2)" y="85" text-anchor="middle" class="what">16:00Z, 01/03/1993 : fait observé</text>
        <text :x="tx(2)" y="150" text-anchor="middle" class="what">tzdata 2022f : s’affiche 12:00 (−04:00)</text>
        <text :x="tx(2)" y="178" text-anchor="middle" class="what warn" :opacity="s.b2">tzdata 2022g : s’affiche 11:00 (−05:00)</text>
      </g>

      <!-- scène C : Kazakhstan, heure ambiguë -->
      <g :opacity="s.sceneC">
        <rect :x="tx(0)" y="72" :width="tx(2) - tx(0)" height="24" rx="4" fill="#3b82f6" opacity="0.85" />
        <text :x="(tx(0) + tx(2)) / 2" y="89" text-anchor="middle" class="bar">23:00 → 24:00 locale (+06:00)</text>
        <circle :cx="tx(1)" :cy="AXIS_Y" r="9" fill="#3b82f6" />
        <text :x="tx(1)" y="62" text-anchor="middle" class="what">23:30, fold=0 → 17:30Z</text>
        <g :opacity="s.c2">
          <rect :x="tx(2)" y="124" :width="tx(4) - tx(2)" height="24" rx="4" fill="#fb923c" opacity="0.9" />
          <text :x="(tx(2) + tx(4)) / 2" y="141" text-anchor="middle" class="bar">23:00 → 24:00 locale (+05:00)</text>
          <circle :cx="tx(3)" :cy="AXIS_Y" r="9" fill="#fb923c" />
          <text :x="tx(3)" y="172" text-anchor="middle" class="what warn">23:30, fold=1 → 18:30Z</text>
        </g>
      </g>
    </svg>

    <div class="caption">{{ caption }}</div>

    <div class="cards" :style="{ opacity: s.cards }">
      <div v-for="(c, i) in cards" :key="c.n" class="card" :class="{ active: i === activeCard }">
        <div class="titre">{{ c.titre }}</div>
        <div class="reaction">règle métier : {{ c.reaction }}</div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.tick { font-size: 14px; font-family: ui-monospace, monospace; fill: currentColor; }
.what { font-size: 17px; font-weight: bold; fill: currentColor; }
.sub { font-size: 12px; }
.gap { font-size: 16px; font-style: italic; fill: currentColor; opacity: 0.8; }
.bar { font-size: 14px; font-weight: bold; fill: white; }
.warn { fill: #fb923c; }
.caption { min-height: 1.8rem; text-align: center; font-size: 1.05rem; margin-top: 0.25rem; }
.cards { display: grid; grid-template-columns: repeat(4, 1fr); gap: 0.5rem; margin-top: 0.5rem; }
.card { border: 2px solid #475569; border-radius: 0.5rem; padding: 0.35rem 0.5rem; font-size: 0.85rem; opacity: 0.45; transition: all 0.4s; }
.card.active { border-color: #fb923c; opacity: 1; }
.titre { font-weight: bold; }
.reaction { opacity: 0.8; }
</style>
