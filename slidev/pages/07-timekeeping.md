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
* écouter la fréquence radio adéquate ([SFTS](Standard frequency and time signal service))
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
