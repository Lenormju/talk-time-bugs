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

<v-click>

```text {1,4}
$ timedatectl timesync-status
       Server: 185.125.190.58 (ntp.ubuntu.com)
      Stratum: 2
       Offset: -34.612ms
        Delay: 47.362ms
       Jitter: 27.628ms
```

</v-click>

<v-click>

```text {1,3}
$ chronyc tracking
Stratum         : 3
System time     : 0.049011644 seconds fast of NTP time
Last offset     : -0.000111728 seconds
RMS offset      : 0.012802946 seconds
Frequency       : 4.796 ppm fast
Skew            : 6.584 ppm
```

</v-click>

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

<Skip hard />

* Temps Lunaire
* Temps martien
* ...
