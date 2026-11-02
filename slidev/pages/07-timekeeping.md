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

# Démo : interroger un serveur NTP

<Skip />

<div class="ntp-big">
  <NtpDemo />
</div>

<style>
.ntp-big { font-size: 1em; }
</style>

---

# D'où vient l'heure de ma machine ?

<Skip />

<div class="grid grid-cols-2 gap-6 items-start">
<div>

<v-clicks>

* **stratum 0** : horloges de référence (atomique, GPS)
* **stratum 1** : serveurs branchés directement dessus
* **stratum 2** : synchronisés sur un stratum 1
* **stratum 3** : synchronisés sur un stratum 2, ...
* **ma machine** : stratum 2 ou 3,  
  à quelques ms de l'UTC (si tout va bien)

</v-clicks>

</div>
<div>

<div v-click>

```text {1,4}
$ timedatectl timesync-status
       Server: 185.125.190.58 (ntp.ubuntu.com)
      Stratum: 2
       Offset: -34.612ms
        Delay: 47.362ms
       Jitter: 27.628ms
```

</div>

<div v-click>

```text {1,3}
$ chronyc tracking
Stratum         : 3
System time     : 0.049011644 seconds fast of NTP time
Last offset     : -0.000111728 seconds
RMS offset      : 0.012802946 seconds
Frequency       : 4.796 ppm fast
Skew            : 6.584 ppm
```

</div>

<v-click>

* alerter sur seuil (en ms)
* supervision Prometheus : `node_timex_offset_seconds` (node_exporter)
* ou via chrony : `chrony_tracking_system_time_seconds` (chrony_exporter)

</v-click>

</div>
</div>

<!--
Constater (07-00) : la dérive casse des choses. Comprendre : la chaîne de strates. Solution : mesurer l'écart (offset) et alerter dessus.
Sortie de timedatectl relevée sur ma machine (systemd-timesyncd). chronyc tracking donne l'équivalent avec chrony (System time, Frequency en ppm).
Métrique Prometheus vérifiée (collector/timex.go de node_exporter, Linux) : node_timex_offset_seconds, aide « Time offset in between local system and reference clock », lue via adjtimex(2), donc l'état du NOYAU, pas chrony ni ntpd. Même collecteur : node_timex_sync_status, node_timex_maxerror_seconds, node_timex_estimated_error_seconds. Ce n'est pas une convention partagée : le chrony_exporter (SuperQ) émet chrony_tracking_last_offset_seconds (Last offset, pas System time), chrony_tracking_root_dispersion_seconds et chrony_tracking_root_delay_seconds. chrony_tracking_system_time_seconds = champ System time de chronyc tracking (collector/tracking.go : CurrentCorrection, « Chrony tracking System time »), c'est la ligne en évidence dans le bloc chronyc ; d'autres : chrony_tracking_rms_offset_seconds, chrony_tracking_frequency_ppms, chrony_tracking_skew_ppms, chrony_tracking_stratum. Signe de la valeur exportée non vérifié. Non vérifié : si l'offset du noyau coïncide avec System time de chronyc (ne pas l'affirmer).

À dire à l'oral (colonne de droite) :
- Titre : le piège classique, la supervision vérifie que le service tourne, pas que l'heure est juste. Un NTP lancé mais injoignable dérive en silence, comme les deux horloges du début.
- Bloc de commande, trois chiffres à lire : l'offset (l'écart avec la référence, celui qui casse des choses), le stratum (à combien de marches de l'horloge atomique), le jitter (si la mesure elle-même est instable, souvent à cause du réseau).
- Mon offset est de 34 ms : correct, invisible pour un certificat TLS ou un log. Pour du last write wins entre serveurs, quelques dizaines de ms peuvent suffire à perdre une écriture.
- chronyc tracking : mesure faite dans un conteneur podman (chronyd -x, 4 sources du pool pool.ntp.org), après 15 min, sur connexion mobile : System time et RMS offset de 13 à 49 ms viennent de la latence variable du réseau, pas de la dérive. Skew 1 000 000 ppm à 1 min, 6,6 ppm à 15 min : chrony apprend le défaut du quartz.
- Avec chronyc tracking : Frequency en ppm = le défaut de mon quartz, on retrouve les ±20 ppm de la première slide.
- Alertes : sur l'offset avec un seuil adapté à l'usage, pas sur « chronyd est actif ». Seuils = ordres de grandeur de ma part, pas une source (TLS : de l'ordre de la seconde ; bases réparties : quelques ms). Si Prometheus est déjà là, c'est une métrique de plus via node_exporter (offset du noyau) ou chrony_exporter (Last offset de chrony).
-->

---

# Problèmes du temps

<ul>
  <li>Non-unicité : DST, timezones, leap seconds<span v-click>, <span class="text-orange-400">clock drift</span></span></li>
  <li>Non-monotonicité : DST, timezones, leap seconds<span v-click>, <span class="text-orange-400">clock drift</span></span></li>
  <li>Non-continuité : DST, timezones, leap seconds<span v-click>, <span class="text-orange-400">clock drift</span></span></li>
  <li>Non-homogénéité : DST, leap years, timezones, leap seconds<span v-click>, <span class="text-orange-400">clock drift</span></span></li>
  <li>Non-constance : DST, leap years, timezones, leap seconds<span v-click>, <span class="text-orange-400">clock drift</span></span></li>
  <li>Non-standardized : dates and time formats, leap seconds</li>
</ul>

---

# Le GPS c'est compliqué !

<Skip hard />

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

<Skip hard />

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

# Problèmes du temps

<ul>
  <li>Non-unicité : DST, timezones, leap seconds, clock drift</li>
  <li>Non-monotonicité : DST, timezones, leap seconds, clock drift</li>
  <li>Non-continuité : DST, timezones, leap seconds, clock drift</li>
  <li>Non-homogénéité : DST, leap years, timezones, leap seconds, clock drift<span v-click>, <span class="text-orange-400">general and special relativity</span></span></li>
  <li>Non-constance : DST, leap years, timezones, leap seconds, clock drift<span v-click>, <span class="text-orange-400">general and special relativity</span></span></li>
  <li>Non-standardized : dates and time formats, leap seconds</li>
</ul>

---

# Il n'y a pas que la Terre

<Skip hard />

<v-clicks depth="2">

* Temps lunaire
  * 1 jour lunaire ≈ 29,5 jours terrestres
  * LTC : Coordinated Lunar Time
  * TCL : Temps-coordonnée lunaire
  * CGPM 2026 : résolution 6
* Temps martien
  * 1 sol = 24 h 39 min 35 s
* ...

</v-clicks>

<!--
Les sigles ne suivent pas l'ordre des mots
- LTC : le mémo OSTP écrit bien « Coordinated Lunar Time (LTC) » (texte relu : sigle = Lunar Time Coordinated dans l'ordre des lettres, mais le mémo ne l'explique pas). Hypothèse de ma part, non sourcée : calqué sur UTC (Coordinated Universal Time), dont le sigle est lui aussi un compromis entre l'anglais CUT et le français TUC.
- TCL : « Temps-coordonnée lunaire » en français (texte bilingue des projets de résolutions du CGPM 2026), « Lunar Coordinate Time » en anglais. Sigle d'origine française, comme TCG (Temps-coordonnée géocentrique) et TCB (barycentrique) dont il est calqué ; l'IAU a gardé le sigle français en anglais (donc pas « LCT »).
- À ne pas confondre : LTC (mémo américain, étalon opérationnel traçable à UTC) et TCL (IAU, échelle de temps-coordonnée relativiste).

Temps lunaire : qui définit quoi
- LTC (Coordinated Lunar Time) : mémo de la Maison-Blanche (OSTP, Arati Prabhakar), 2 avril 2024, « Policy on Celestial Time Standardization in Support of the National Cislunar S&T Strategy ». La NASA doit livrer une stratégie de standardisation du temps lunaire au plus tard le 31/12/2026, avec Commerce, Défense, État et Transports, et la faire adopter par les organismes de normalisation et les signataires des Accords Artemis. LTC : étalon opérationnel cislunaire, traçable à UTC, « analogue au Temps Terrestre », fixé par un ensemble d'horloges sur la Lune (survivrait à une perte de contact avec la Terre). Source : https://bidenwhitehouse.archives.gov/wp-content/uploads/2024/04/Celestial-Time-Standardization-Policy.pdf (texte lu). Mémo de l'administration Biden, archivé : pas vérifié qu'il est toujours en vigueur.
- NASA : page SCaN, « établir un temps lunaire coordonné (LTC) suite à une directive de la Maison-Blanche » (https://www.nasa.gov/communicating-with-missions/scan-enabling-moon-to-mars). Aucune publication de la stratégie trouvée au 2026-11-02 (absence de preuve, pas preuve d'absence) ; échéance dans deux mois.
- TCL (Lunar Coordinate Time) : IAU, Assemblée générale 2024, résolution II (Lunar Celestial Reference System et TCL) et résolution III (standard de temps lunaire coordonné par accord international). Titres vérifiés sur la liste officielle https://www.iau.org/IAU/Iau/Publications/List-of-Resolutions.aspx ; texte non lu (unité = seconde SI, origine commune avec TT/TCG/TCB au 1er janvier 1977 : presse seulement).
- CGPM : 28e CGPM, résolution 6 adoptée le 15 octobre 2026, « On the definition of an international lunar reference time scale and its traceability to UTC » (https://www.bipm.org/en/cgpm-2026/resolution-6, DOI 10.59161/CGPM2026RES6E). Ton recommandatoire (« encourage », « recommande »), pas de clause « décide » repérée, d'après un résumé de la page BIPM, texte pas lu mot à mot. Le texte français fait foi. Même session que la résolution 5 sur les secondes intercalaires.
- ESA : Moonlight, projet NovaMoon (premières horloges atomiques à la surface de la Lune, laboratoire de référence de temps lunaire), charge candidate d'Argonaut-1, visée vers 2031 (source secondaire pour la date). https://www.esa.int/Applications/Satellite_navigation/Introducing_NovaMoon
- Pas de nom stabilisé : « LTC » côté États-Unis, « TCL » ou « échelle de référence lunaire » côté IAU et BIPM.

Les chiffres
- Jour lunaire (lever du Soleil au lever suivant, jour solaire) = mois synodique moyen, environ 29,53 jours terrestres, soit 29 j 12 h 44 min 3 s : donc environ 14,8 jours de jour puis autant de nuit en un point donné. Rotation propre de la Lune (jour sidéral) : 27,32 jours, égale à sa période orbitale (rotation synchrone) ; l'écart de ~2,2 jours vient de l'orbite de la Terre autour du Soleil. Fait astronomique classique, non issu de la recherche de l'agent, non resourcé ici.
- Écart d'horloge : le mémo OSTP donne 58,7 µs/jour (une horloge terrestre vue de la Lune perd en moyenne, avec des variations périodiques). Ashby et Patla (NIST), arXiv 2402.11150 : 56,02 µs/jour pour une horloge près de l'équateur lunaire. Dire « en moyenne » : l'écart varie dans le temps et selon le lieu.
- 1 ns de lumière = 30 cm, donc des dizaines de µs par jour = des kilomètres d'erreur de position par jour (calcul simple ; « 17 km/jour » vu dans la presse seulement).
- Une horloge posée sur la surface lunaire dérive d'environ 2,7 µs/jour par rapport à TCL, et l'écart entre point bas et point haut de la surface est d'environ 26 ns/jour (Bourgoin, Defraigne, Meynadier, Metrologia 63(1) 015003, janvier 2026, https://iopscience.iop.org/article/10.1088/1681-7575/ae2c03 ; conversions en µs et ns/jour faites par l'agent).
- Aucune horloge en service sur la Lune à ce jour. Pas de test en vol trouvé (Lunar Pathfinder est un relais de communication ; Artemis II a survolé la Lune en avril 2026, aucune expérience de temps lunaire trouvée).
- Une critique existe : arXiv 2602.18641, « The Category Mistake of Cislunar Time » (février 2026), essai non lu en détail.

Pour un développeur
- Base tz de l'IANA : aucune zone lunaire ; la page « theory » a une section sur la Lune (1re proposition formelle de TCL en 2025, éphéméride LTE440 de l'Observatoire de la Montagne Pourpre, arXiv 2509.18511) et dit que la base ne gère pas l'heure des autres planètes. https://www.iana.org/time-zones/theory
- Astropy : échelles TAI, TCB, TCG, TDB, TT, UT1, UTC et local ; pas de TCL. Un crate Rust `deep-time` gèrerait TCL (résultat de recherche, non vérifié).
- Unix time et ISO 8601 : rien de spécifique à la Lune trouvé (absence de résultat, pas une preuve). SOFA et SPICE : non vérifié.

Temps martien
- Un sol dure environ 24 h 39 min 35,244 s, et il n'existe pas de vrai standard de fuseaux martiens : chaque mission d'atterrissage a choisi sa propre référence (page « theory » de l'IANA).

À ne pas dire : que la NASA a « défini » LTC, qu'il y a des horloges atomiques sur la Lune, que Lunar Pathfinder teste l'heure lunaire.
-->
