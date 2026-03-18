# Les problèmes commencent ...

<ul>
  <li v-click>Heure de livraison : 02 h 30 (du matin), le Dimanche 29 Mars 2026</li>
  <li v-click>Durée du trajet :
    45 minutes
    <span v-if="$clicks >= 5" class="text-red-500"> + 1 heure !!!</span>
  </li>
  <li v-click>Heure de départ : 01 h 45</li>
  <li v-click>
    Heure d'arrivée : 03 h 30
    <span v-if="$clicks >= 5" class="font-mono text-amber-400 ml-2">😰</span>
  </li>
</ul>

<span v-click class="hidden" />

<v-click>
Que s'est-il passé ?
</v-click>

<v-click>
Décalage horaire : "daylight saving(s) time"
</v-click>

---
clicks: 3
---

# Décalage horaire

<DSTTimelineSVG />

---

# Problèmes

<ul>
  <li v-click class="text-orange-400">Non-continuité : DST</li>
</ul>

---
clicks: 4
---

# Et dans l'autre sens

<DSTTimelineSVGFall />

---

# Problèmes

<ul>
  <li >Non-continuité : DST</li>
  <li v-click class="text-orange-400">Non-unicité : DST</li>
  <li v-click class="text-orange-400">Non-monotonicité : DST</li>
</ul>

---

# Et encore dans l'autre sens

<v-click>
    <img src="../images/Aussie-Christmas-700x426.png" class="max-h-96 mx-auto object-contain" />
</v-click>

---

# Problèmes

<ul>
  <li>Non-continuité : DST</li>
  <li>Non-unicité : DST</li>
  <li>Non-monotonicité : DST</li>
  <li v-click class="text-orange-400">Non-homogénéité : DST</li>
</ul>

---

# Pourquoi s'infliger ça ?

<v-click>
Réponse n°1 : 🛢️ 💲
</v-click>

<v-click>

> Le changement d'heure a été instauré en France à la suite du choc pétrolier de 1973-1974.
> — [service-public.gouv.fr](https://www.service-public.gouv.fr/particuliers/actualites/A18820)

</v-click>

<v-click>
Réponse n°2 : 🌅 ☃️
</v-click>

<v-click>
<WorkAndSchoolSchedule :animated="$clicks >= 8" />
</v-click>

<v-click>
    <SunDuration :x="18" :y="45" :width="28.47" :height="8" label="Solstice d'hiver" color="rgba(147,197,253,0.3)" border="rgba(147,197,253,0.5)" /> <!-- 8h -->
</v-click>
<v-click>
    <SunDuration :x="18" :y="53" :width="45" :height="8" label="Aujourd'hui (31 mars)" color="rgba(134,239,172,0.3)" border="rgba(134,239,172,0.5)" /> <!-- 12h46 -->
</v-click>
<v-click>
    <SunDuration :x="18" :y="61" :width="57" :height="8" label="Solstice d'été" color="rgba(253,224,71,0.3)" border="rgba(253,224,71,0.5)" /> <!-- 16h -->
</v-click>

<span v-click />

<!-- 31 mars : lever 7h32 coucher 20h18 -->

---

# Evolutions

<div class="relative w-full" style="height: 420px">
  <!-- Images at odd clicks: 1, 3, 5, 7, 9, 11, 13 -->
  <img v-click="1" src="../images/20221130064830!DST_Countries_Map.png" class="absolute inset-0 w-full h-full object-contain" />
  <img v-click="3" src="../images/20230301205820!DST_Countries_Map.png" class="absolute inset-0 w-full h-full object-contain" />
  <img v-click="5" src="../images/20230327133024!DST_Countries_Map.png" class="absolute inset-0 w-full h-full object-contain" />
  <img v-click="7" src="../images/20250324003440!DST_Countries_Map.png" class="absolute inset-0 w-full h-full object-contain" />
  <img v-click="9" src="../images/20251114224057!DST_Countries_Map.png" class="absolute inset-0 w-full h-full object-contain" />
  <img v-click="11" src="../images/20260308192300!DST_Countries_Map.png" class="absolute inset-0 w-full h-full object-contain" />

  <!-- Empty steps at even clicks: 2, 4, 6, 8, 10, 12 — add DraggableAnnotations here -->
  <span v-click="2" />
  <DraggableAnnotation v-click="2" :labelX="10" :labelY="46" :tipX="18.5" :tipY="38.5">2022 : Mexico</DraggableAnnotation>
  <span v-click="4" />
  <DraggableAnnotation v-click="4" :labelX="60" :labelY="51.5" :tipX="57" :tipY="43.5">2023 : Egypt</DraggableAnnotation>
  <span v-click="6" />
  <DraggableAnnotation v-click="6" :labelX="52" :labelY="0" :tipX="45.5" :tipY="9">2023 : Greenland</DraggableAnnotation>
  <DraggableAnnotation v-click="6" :labelX="64.5" :labelY="9.5" :tipX="57.7" :tipY="23.7">2023 : Ukraine</DraggableAnnotation>
  <DraggableAnnotation v-click="6" :labelX="47.5" :labelY="69" :tipX="33.5" :tipY="71.5">2024 : Paraguay</DraggableAnnotation>
  <span v-click="8" />
  <DraggableAnnotation v-click="8" :labelX="46.5" :labelY="78.5" :tipX="30.5" :tipY="86.5">2025 : Chile</DraggableAnnotation>
  <span v-click="10" />
  <DraggableAnnotation v-click="10" :labelX="19" :labelY="4" :tipX="19" :tipY="17">2026 : British Columbia</DraggableAnnotation>
  <span v-click="12" />
</div>

---

# Problèmes

<ul>
  <li>Non-continuité : DST</li>
  <li>Non-unicité : DST</li>
  <li>Non-monotonicité : DST</li>
  <li>Non-homogénéité : DST</li>
  <li v-click class="text-orange-400">Non-constance : DST</li>
</ul>

---

# Avez-vous remarqué ?

<SunDuration :x="18" :y="25" :width="28.47" :height="8" label="Solstice d'hiver" color="rgba(147,197,253,0.3)" border="rgba(147,197,253,0.5)" /> <!-- 8h -->
<SunDuration :x="18" :y="33" :width="45" :height="8" label="Aujourd'hui (31 mars)" color="rgba(134,239,172,0.3)" border="rgba(134,239,172,0.5)" /> <!-- 12h46 -->
<SunDuration :x="18" :y="41" :width="57" :height="8" label="Solstice d'été" color="rgba(253,224,71,0.3)" border="rgba(253,224,71,0.5)" /> <!-- 16h -->

<!-- pas la même durée -->
