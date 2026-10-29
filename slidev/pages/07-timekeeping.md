# Deux horloges ne sont jamais d'accord

<div class="grid grid-cols-2 gap-6 items-start">
<div>

<DriftingClocks :step="$clicks" />

<span v-click="1" />
<span v-click="2" />
<span v-click="3" />

</div>
<div class="drift-text">

<ul>
  <li v-click="4">des logs dans le désordre d'une machine à l'autre</li>
  <li v-click="5">un certificat TLS «&nbsp;pas encore valide&nbsp;» ou «&nbsp;expiré&nbsp;»</li>
  <li v-click="6">un commit ou une release antidaté</li>
  <li v-click="7">l'heure qui saute d'un coup, parfois en arrière !</li>
</ul>

<p v-click="8">➡️ qui remet les pendules à l'heure ?</p>

</div>
</div>

<style>
.drift-text p {
  margin: 0.4rem 0;
}
.drift-text ul {
  margin-top: 0;
  font-size: 0.9em;
}
</style>

<!--
Constater seulement : pas de solution ici, la slide suivante explique.
Clics 1 à 3 : les deux horloges font un tour, B finit un peu en retard (1 jour, 1 mois, 1 an). Écarts exagérés (le dire à l'oral, ce n'est plus écrit) : ce ne sont pas des mesures.
À dire à l'oral : deux oscillateurs ne sont jamais identiques, la dérive est inévitable ; parfois elle devient assez grande pour casser quelque chose (clics 4 à 7).
Ordre de grandeur (plus affiché) : ±20 ppm = tolérance max à 25 °C d'un quartz 32,768 kHz (datasheet Abracon AB26T) ; 20e-6 × 86 400 s = 1,728 s/jour (calcul). La datasheet donne aussi un coefficient de température de -0,034 ppm/°C² et un vieillissement de ±3 ppm la 1re année.
TODO Julien : ton cas vécu (quelle machine, quel écart, ce qui a cassé) ; capture de la release korlabs (runner désynchronisé, commit antidaté) à retrouver et valider avant de la montrer (B12).
-->

---

# Comment être toujours à l'heure ?

<v-clicks>

* ~~appeler "l'horloge parlante"~~ (ah non, plus depuis 2022)
* avoir sa propre horloge atomique (💸)
* avoir une montre mécanique ou au quartz
* calendrier solaire
* se brancher à un serveur NTP ("network time protocol")<br/>
  OS, FAI, Français, ...
* se brancher à un serveur PTP ("precise time protocol")
* monter son propre serveur (stratum)
* écouter la fréquence radio adéquate ([SFTS : Standard frequency and time signal service](https://en.wikipedia.org/wiki/Standard_frequency_and_time_signal_service))
* écouter les signaux GPS
* ...

</v-clicks>

---

# Le GPS c'est compliqué !

<v-clicks>

* ce sont des horloges atomiques en orbite autour de la terre
* elles signalent leur position orbitale, et leur "GPS Time" :<br/>
  nombre de secondes atomiques depuis le 6 Janvier, 1980, 00:00:00 UTC
* atomiques et pas UTC, donc il y a un décalage entre les deux !
* et il s'agit de quadrianguler la position du récepteur dans l'espace/temps 😛
* <img src="../images/Albert_Einstein_sticks_his_tongue_1951.jpg">

</v-clicks>

---

# Tout est relatif !

<img src="../images/skip.png" class="absolute top-8 right-4 w-24" />

<v-clicks depth="2">

* la relativité restreinte : référentiels inertiels (sans gravité)
  * espace-temps
  * paradoxe des jumeaux
  * satellites GPS ou ISS
  * Interstellar (spoiler !)
* la relativité générale : référentiels en accélération (gravité)
  * espace-temps courbé
  * lignes droites hyperboliques dans l'espace
  * vitesse constante dans l'espace-temps
  * satellites GPS (45 µs/jour) ou dans l'ISS
  * Interstellar (spoiler !)
* voyage dans le temps :
  * uniquement vers le futur, plus ou moins vite que les autres
  * Oleg Kononenko (1111 jours) : a veilli 0.02+ secondes de moins

</v-clicks>

---

# Problèmes

<ul>
  <li>Non-unicité : DST, timezones, leap seconds</li>
  <li>Non-monotonicité : DST, timezones, leap seconds</li>
  <li>Non-continuité : DST, timezones, leap seconds</li>
  <li>Non-homogénéité : DST, leap years, timezones, leap seconds, general and special relativity</li>
  <li>Non-constance : DST, leap years, timezones, leap seconds, general and special relativity</li>
  <li>Non-standardized : dates and time formats, leap seconds</li>
</ul>

---

# Il n'y a pas que la Terre

<img src="../images/skip.png" class="absolute top-8 right-4 w-24" />

* Temps Lunaire
* Temps martien
* ...
