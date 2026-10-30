<script setup lang="ts">
// Frise (proportionnelle) de l'annonce cubaine du 24/10/2026 à la date du retour en arrière prévu.
// Sources : commit tz 5b5b39dae1 (26/10 18:09:17Z) et tag 2026f (28/10 06:16:49Z) du dépôt eggert/tz,
// communiqué MINEM + MTSS du samedi 24/10 (heure inconnue : placé à 18:00 UTC, juste avant l'article
// de CiberCuba de 18:16 UTC, sans afficher d'heure). Distances proportionnelles au temps réel.
// Les clics (v-click) sont ceux de la slide : le premier clic de la frise est le 5.
const DAY = 92
const X0 = 40
const x = (jours: number) => X0 + jours * DAY

const annonce = x(0.75)
const commit = x(2 + 18.15 / 24)
const release = x(4 + 6.28 / 24)
const echeance = x(8 + 5 / 24)
</script>

<template>
  <svg viewBox="0 0 920 300" class="w-full">
    <line :x1="x(0)" y1="150" :x2="x(8.6)" y2="150" stroke="#94a3b8" stroke-width="4" stroke-linecap="round" />

    <!-- 1. annonce -->
    <g v-click="5">
      <circle :cx="annonce" cy="150" r="10" fill="#3b82f6" />
      <line :x1="annonce" y1="140" :x2="annonce" y2="95" stroke="#3b82f6" stroke-width="2" />
      <text :x="annonce" y="55" text-anchor="middle" class="date">sam. 24/10</text>
      <text :x="annonce" y="78" text-anchor="middle" class="what">annonce officielle</text>
    </g>

    <!-- 2. commit -->
    <g v-click="6">
      <circle :cx="commit" cy="150" r="10" fill="#3b82f6" />
      <line :x1="commit" y1="160" :x2="commit" y2="205" stroke="#3b82f6" stroke-width="2" />
      <text :x="commit" y="230" text-anchor="middle" class="date">lun. 26/10, 18:09 UTC</text>
      <text :x="commit" y="253" text-anchor="middle" class="what">commit tz</text>
      <text :x="(annonce + commit) / 2" y="142" text-anchor="middle" class="gap">≈ 2 jours</text>
    </g>

    <!-- 3. release -->
    <g v-click="7">
      <circle :cx="release" cy="150" r="10" fill="#3b82f6" />
      <line :x1="release" y1="140" :x2="release" y2="95" stroke="#3b82f6" stroke-width="2" />
      <text :x="release" y="55" text-anchor="middle" class="date">mer. 28/10, 06:16 UTC</text>
      <text :x="release" y="78" text-anchor="middle" class="what">release 2026f</text>
      <text :x="(commit + release) / 2" y="142" text-anchor="middle" class="gap">≈ 36 h</text>
    </g>

    <!-- 4. échéance -->
    <g v-click="8">
      <circle :cx="echeance" cy="150" r="12" fill="#fb923c" />
      <line :x1="echeance" y1="160" :x2="echeance" y2="205" stroke="#fb923c" stroke-width="2" />
      <text :x="echeance + 40" y="230" text-anchor="end" class="date warn">dim. 1er/11, 05:00 UTC</text>
      <text :x="echeance + 40" y="253" text-anchor="end" class="what warn">retour en arrière prévu</text>
      <text :x="(release + echeance) / 2" y="142" text-anchor="middle" class="gap warn">moins de 4 jours pour déployer</text>
    </g>
  </svg>
</template>

<style scoped>
.date {
  font-size: 20px;
  font-weight: bold;
  fill: currentColor;
}
.what {
  font-size: 18px;
  fill: currentColor;
  opacity: 0.8;
}
.gap {
  font-size: 17px;
  font-style: italic;
  fill: currentColor;
  opacity: 0.8;
}
.warn {
  fill: #fb923c;
  opacity: 1;
}
</style>
