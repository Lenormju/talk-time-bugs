# Les problèmes commencent ...

<ul>
  <li v-click="1">Dimanche 25 Octobre 2026, je rentre de soirée ...</li>
  <li v-click="2">mon Apple Watch affiche : 02 h 30</li>
  <li v-click="3">je marche 45 minutes</li>
  <li v-click="4">
    j'arrive : 02 h 15
    <span v-click="5" class="font-mono text-amber-400 ml-2">😰 avant d'être parti ?</span>
  </li>
  <li v-click="6">
    je vais me coucher : 02 h 30 de nouveau
    <span v-click="7" class="font-mono text-amber-400 ml-2">😰 encore ?!</span>
  </li>
</ul>

<v-click at="8">
Que s'est-il passé ?
</v-click>

<v-click at="9">
  <img src="../images/iphonesoft_apple_watchos_27_bug.png" class="w-96 border-2 border-gray-400" />
</v-click>

<v-click at="10">
Changement d'heure : "daylight saving(s) time"
</v-click>

---
layout: center
---

# Avec du code

<v-click>
<!-- -->
</v-click>

```python {0|1-3|1-4|1-5|1-7|all}
import datetime as dt

depart  = dt.datetime(2026, 10, 25, 2, 30, 0)
arrivee = dt.datetime(2026, 10, 25, 2, 15, 0)
coucher = dt.datetime(2026, 10, 25, 2, 30, 0)
print(arrivee - depart)
# -1 day, 23:45:00 : la marche a duré 45 minutes
print(coucher == depart)
# True : alors qu'il y a 1 heure d'écart
```

<style>
.slidev-code-dishonored {
  visibility: hidden;
}
</style>

---
clicks: 4
class: no-center
---

# Changement d'heure : automne

<DSTTimelineSVGFall />

---

# Problèmes

<ul>
  <li v-click class="text-orange-400">Non-unicité : DST</li>
</ul>

---

# Avec du code

```bash {1|3|3-4|3-5|3-6|3-7|3-8|8|3-9|3-10}
# run something once every 15 minutes, and compute average speed

# current_time=1:54:17  delta_time=15:00  delta_quantity=147  speed=9.8
# current_time=2:09:17  delta_time=15:00  delta_quantity=147  speed=9.8
# current_time=2:24:17  delta_time=15:00  delta_quantity=147  speed=9.8
# current_time=2:39:17  delta_time=15:00  delta_quantity=147  speed=9.8
# current_time=2:54:17  delta_time=15:00  delta_quantity=147  speed=9.8
# current_time=2:09:17  delta_time=-45:00  delta_quantity=147  speed=-2.66667
# current_time=2:24:17  delta_time=15:00  delta_quantity=147  speed=9.8
# current_time=2:39:17  delta_time=15:00  delta_quantity=147  speed=9.8
```

<style>
.slidev-code-dishonored {
  visibility: hidden;
}
</style>

---

# Problèmes

<ul>
  <li>Non-unicité : DST</li>
  <li v-click class="text-orange-400">Non-monotonicité : DST</li>
</ul>

---

# Et dans l'autre sens

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
02 h 30 n'a pas existé ce jour-là : après 01 h 59, il était 03 h 00
</v-click>

---
layout: center
---

# Avec du code

<v-click>
<!-- -->
</v-click>

```python {0|1-3|1-4|1-5|1-6|all}
import datetime as dt

start_time = dt.datetime(2026, 3, 29, 1, 45, 0)
end_time =   dt.datetime(2026, 3, 29, 3, 30, 0)
duration = end_time - start_time
print(duration)
# 1:45:00
```

<style>
.slidev-code-dishonored {
  visibility: hidden;
}
</style>

---
clicks: 3
class: no-center
---

# Changement d'heure : printemps

<DSTTimelineSVG />

---

# Problèmes

<ul>
  <li>Non-unicité : DST</li>
  <li>Non-monotonicité : DST</li>
  <li v-click class="text-orange-400">Non-continuité : DST</li>
</ul>

---

# Et encore dans l'autre sens

<v-click>
    <img src="../images/Aussie-Christmas-700x426.png" class="max-h-96 mx-auto object-contain" />
</v-click>

---

# Problèmes

<ul>
  <li>Non-unicité : DST</li>
  <li>Non-monotonicité : DST</li>
  <li>Non-continuité : DST</li>
  <li v-click class="text-orange-400">Non-homogénéité : DST</li>
</ul>

---
class: no-center
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
    <SunDuration ghost :x="38.2" :y="50" :width="29.4" :height="8" label="Solstice d'hiver" color="rgba(147,197,253,0.3)" border="rgba(147,197,253,0.5)" /> <!-- 8h41 -> 16h56 (8h15) -->
</v-click>
<v-click>
    <SunDuration ghost :x="34.2" :y="58" :width="35.6" :height="8" label="Aujourd'hui (30 octobre)" color="rgba(134,239,172,0.3)" border="rgba(134,239,172,0.5)" /> <!-- 7h34 -> 17h34 (10h) -->
</v-click>
<v-click>
    <SunDuration ghost :x="27.9" :y="66" :width="57.6" :height="8" label="Solstice d'été" color="rgba(253,224,71,0.3)" border="rgba(253,224,71,0.5)" /> <!-- 5h47 -> 21h58 (16h11) -->
</v-click>

<span v-click />

<!--
Sources des rectangles SunDuration (position `ghost` = cible de calage).

Données (Paris, 48.8566 N / 2.3522 E, heure légale) :
https://api.sunrise-sunset.org/json?lat=48.8566&lng=2.3522&date=YYYY-MM-DD&formatted=0&tzid=Europe/Paris
(consulté le 2026-10-29 ; timeanddate.com renvoyait un 403)
- 2026-12-21 (solstice d'hiver, UTC+1) : lever 08:41:09, coucher 16:56:08, durée 29699 s = 8h15
- 2026-10-30 (aujourd'hui, UTC+1)      : lever 07:34:23, coucher 17:34:06, durée 35983 s = 10h00
- 2026-06-21 (solstice d'été, UTC+2)   : lever 05:46:55, coucher 21:57:54, durée 58259 s = 16h11

Calculé (estimé, pas mesuré) à partir de l'axe de WorkAndSchoolSchedule.vue :
- x(h) = 20 + 40·h dans un viewBox de 1000, soit 3,56 % de la slide par heure
  (calibré sur les largeurs d'origine : 28,47 % pour 8 h)
- début de l'axe (0h) à ~7,3 % de la slide (marge du layout ~56 px sur 980 px)
- x% = 7,3 + 3,56 × heure_du_lever ; width% = 3,56 × durée
- hiver : x = 7,3 + 3,56 × 8,68 = 38,2 ; width = 3,56 × 8,25 = 29,4
- aujourd'hui : x = 7,3 + 3,56 × 7,57 = 34,2 ; width = 3,56 × 10,0 = 35,6
- été : x = 7,3 + 3,56 × 5,78 = 27,9 ; width = 3,56 × 16,18 = 57,6
-->

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
  <li>Non-unicité : DST</li>
  <li>Non-monotonicité : DST</li>
  <li>Non-continuité : DST</li>
  <li>Non-homogénéité : DST</li>
  <li v-click class="text-orange-400">Non-constance : DST</li>
</ul>

---

# Éviter / détecter (DST) : comparer deux instants

<v-click>
<!-- -->
</v-click>

```python {0|1-6|1-8|1-9|all}
import datetime as dt
from zoneinfo import ZoneInfo
paris = ZoneInfo("Europe/Paris")

start = dt.datetime(2026, 10, 25, 1, 45, tzinfo=paris)
end   = dt.datetime(2026, 10, 25, 2, 30, tzinfo=paris, fold=1)  # 2e passage
print(start)  # 2026-10-25 01:45:00+02:00
print(end)  #   2026-10-25 02:30:00+01:00
print(end - start)  # 0:45:00
utc = dt.timezone.utc
print(end.astimezone(utc) - start.astimezone(utc))  # 1:45:00
```

<v-clicks>

- Dates **avec fuseau** (`zoneinfo`), `fold` pour lever l'ambiguïté, durées calculées **en UTC**
- Tester les heures ambiguës ou inexistantes (changements d'heure), en figeant l'horloge : `time-machine` (slide suivante), `freezegun`, `libfaketime`, [Symfony Clock](https://symfony.com/doc/current/components/clock.html) (PHP)

</v-clicks>

<style>
.slidev-code-dishonored {
  visibility: hidden;
}
</style>

---

# Éviter / détecter (DST) : mesurer une durée

```python
# processus lancé avec TZ=Europe/Paris
import datetime as dt, time, time_machine
from zoneinfo import ZoneInfo
paris = ZoneInfo("Europe/Paris")
before = dt.datetime(2026, 10, 25, 2, 50, tzinfo=paris)         # 02:50 +02:00
after  = dt.datetime(2026, 10, 25, 2, 5, tzinfo=paris, fold=1)  # 02:05 +01:00
```

<div class="grid grid-cols-2 gap-4 mt-2">

<div v-click="1" class="wall">
<div class="text-red-500 font-bold">Horloge murale</div>

```python {0|1|1-3|1-4|all} {at:1}
with time_machine.travel(before) as clock:
    start = dt.datetime.now()
    time.sleep(15 * 60)
    clock.move_to(after)
    delta = dt.datetime.now() - start
    print(delta.total_seconds())
# -2700.0
```

</div>

<div v-click="5" class="mono">
<div class="text-green-500 font-bold">Horloge monotone</div>

```python {0|1-4|all} {at:5}
with time_machine.travel(before) as clock:
    start = time.monotonic()
    time.sleep(15 * 60)
    clock.move_to(after)
    delta = time.monotonic() - start
    print(delta)
# 900.0006…
```

</div>
</div>

<div v-click="7" class="raw mt-2">

```python
print(round(time.monotonic(), 2))  # 24164.39
```

L'horloge monotone n'est pas une date, juste un compteur qui n'avance que vers l'avant.

</div>

<style>
.slidev-code-dishonored {
  visibility: hidden;
}
.wall .line:is(:nth-child(2), :nth-child(5)) > span:nth-child(n+3):nth-child(-n+8),
.mono .line:is(:nth-child(2), :nth-child(5)) > span:nth-child(n+3):nth-child(-n+6),
.raw .line:first-child > span:nth-child(n+5):nth-child(-n+8) {
  font-weight: bold;
}
</style>

---

# Avez-vous remarqué ?

<SunDuration :x="18" :y="25" :width="28.47" :height="8" label="Solstice d'hiver" color="rgba(147,197,253,0.3)" border="rgba(147,197,253,0.5)" /> <!-- 8h -->
<SunDuration :x="18" :y="33" :width="35.8" :height="8" label="Aujourd'hui (30 octobre)" color="rgba(134,239,172,0.3)" border="rgba(134,239,172,0.5)" /> <!-- 10h03 -->
<SunDuration :x="18" :y="41" :width="57" :height="8" label="Solstice d'été" color="rgba(253,224,71,0.3)" border="rgba(253,224,71,0.5)" /> <!-- 16h -->

<!-- pas la même durée -->
