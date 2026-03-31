# Solution : data

<v-click>

Principe : éviter la perte d'information

</v-click>

<v-clicks>

1. toujours prendre en input un datetime AVEC timezone, refuser autrement
2. immédiatement convertir ce datetime en UTC, avant tout traitement
3. ne faire que des traitements en UTC
4. stocker le datetime, avec sa timezone originale à-côté
5. ne faire que des traitements en UTC
6. seulement au moment de l'affichage, convertir dans la timezone locale du user

</v-clicks>

---

# Solution : data++

1. toujours prendre en input un datetime AVEC timezone, refuser autrement
2. immédiatement convertir ce datetime en UTC, avant tout traitement<span v-click>, <span class="text-orange-400">et noter la version IANA utilisée</span></span>
3. ne faire que des traitements en UTC
4. stocker le datetime, avec sa timezone originale à côté<span v-click>, <span class="text-orange-400">et la version IANA correspondante</span></span>
   <span v-click class="text-orange-400"><br/>et à chaque changement de version IANA, re-convertir le datetime UTC vers sa nouvelle valeur</span>
5. ne faire que des traitements en UTC
6. seulement au moment de l'affichage, convertir dans la timezone locale du user

---

# Solution : outillage

<v-click>

> Temporal [...] learned from the many failures and dead bodies that came before it. And it had lots of good implementations to look at: Joda Time, Chrono, etc.
> -- [news.ycombinator.com](https://news.ycombinator.com/item?id=46597195)

</v-click>

<v-clicks depth="2">

* JavaScript
  * ⚠️ danger ! ([jsdate.wtf](https://jsdate.wtf/))
  * utiliser [Temporal (TC39)](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Temporal) ([CanIUse](https://caniuse.com/temporal) ou polyfills), ou sinon Moment.js, Luxon, js-joda, ...
* Rust crates : std chrono+time, datetime, jiff, speedate, hifitime, ...
* Python : ~~stdlib datetime~~, stdlib zoneinfo (3.9), **Whenever**, Pendulum, Arrow, pytz, ...
* Java : ~~java.util~~, java.time, Joda, ~~Time4j~~
* C++ : Chrono
* .Net : Noda (cf Joda)
* libs spécifiques pour l'astronomie (Astropy), l'histoire, ...
* [ICU framework](https://unicode-org.github.io/icu/userguide/datetime/timezone/) (Chrome, Firefox, Qt, Android, MacOS/iOS, ...)
* Ruby : std time, Rails time
* comportement par défaut pour les DBs (Mongo renvoie des naïve par défaut, SQL `WITH TIMEZONE`)

</v-clicks>

---

# Test

<v-clicks depth="2">

* connaître les risques ✔️
* les IAs font très souvent des erreurs basiques<br/>(dépend de la qualité pré-existante de la codebase)
* mais sont très pratiques pour :
  * générer des tests de couverture
  * brainstormer des test cases
  * générer des tests property-based
* `freezetime` et autres
* [`libfaketime`](https://github.com/wolfcw/libfaketime) (syscall-level) via `LD_PRELOAD`

</v-clicks>
