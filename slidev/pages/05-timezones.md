# L'histoire des timezones

<v-click>
Pour faire (très) court :
</v-click>

<v-clicks depth="2">

* avant, le temps était très local
  * on suivait principalement le soleil
  * chaque ville avait son heure
  * on voyageait lentement
* puis les trains ont tout chamboulé
  * (les accidents mortels ont contribué)
* on a décidé d'unifier le temps, progressivement
* (je passe l'histoire chaotique pour chaque pays)
* aujourd'hui, le monde entier est découpé en timezones clairement définies

</v-clicks>

---

<img src="../images/Timezone-boundary-builder_release_2023d.png" class="max-h-96 mx-auto object-contain" />

---

# Bases et exemples

<v-clicks depth="2" class="tight-list">

* "prime meridian" (IERS Reference Meridian) : Greenwich
  * (je vous passe l'histoire de Greenwich)
  * **a servi à définir UTC**
  * (je vous passe l'histoire d'UTC)
  * UTC = Universel Temps Coordonné / Universal Time Coordinated
* changement d'heure :
  * avant le 25 octobre : Central European Summer Time (CEST, UTC+2)
  * après le 25 octobre : Central European Time (CET, UTC+1)
* voyage au Royaume-Uni :
  * UK suit le Greenwich Mean Time (GMT, UTC+0) ou le British Summer Time (BST, UTC+1)
  * a conservé son changement d'heure synchronisé avec le reste de l'Union Européenne
  * à l'aller je "perds" 1h, au retour je la regagne
* "offset" versus "zoned" :
  * China Standard Time (CST) = `+08:00` ou `Asia/Shanghai`
  * Eastern Standard Time (EST) = `-05:00` ou `America/Cancun`
* ni offset ni timezone = "naïve"

</v-clicks>

<style>
.tight-list li {
  margin-top: 0.15em;
  margin-bottom: 0.15em;
  line-height: 1.3;
  font-size: 0.82em;
}
.tight-list li li {
  font-size: 1em;
}
.tight-list ul {
  margin-top: 0.1em;
  margin-bottom: 0.1em;
}
.tight-list code {
  font-size: 0.82em;
}
</style>

---
clicks: 8
class: no-center
---

# Un sacré bazar !

<div v-click.hide="5" class="grid grid-cols-[minmax(0,1fr)_minmax(0,1.3fr)] gap-6 mt-6 items-start">
<ul>
  <li v-click="1">écrit par des volontaires : liste <code>tz@iana.org</code>, dépôt <code>eggert/tz</code>, publié par l'IANA</li>
  <li v-click="2">des fichiers texte de règles (<code>europe</code>, <code>northamerica</code>…)</li>
  <li v-click="3">compilés par <code>zic</code> en fichiers binaires, installés dans <code>/usr/share/zoneinfo</code></li>
  <li v-click="4">des releases fréquentes : 3 en 2025, 6 en 2026 (déjà)</li>
</ul>
<div v-click="2">

```diff
-Rule Cuba 2012 max  - Nov Sun>=1 0:00s 0 S
+Rule Cuba 2012 2025 - Nov Sun>=1 0:00s 0 S
+Rule Cuba 2027 max  - Nov Sun>=1 0:00s 0 S
```

<div class="text-sm opacity-80">extrait du commit du 26/10/2026 : Cuba ne reculera pas l'heure le 1er novembre</div>
</div>
</div>

<div v-click="5" class="absolute left-8 right-8 top-28">
  <CubaTzdbTimeline />
</div>

<!--
Qui : des volontaires. Le fil `tz@iana.org` reçoit les annonces (ici, un contributeur a signalé celle de Cuba), `eggert/tz` est le dépôt, l'IANA publie les releases sur data.iana.org/time-zones. Paul Eggert signe les tags (2026f : 28/10/2026 06:16:49 UTC, soit le soir du 27 à Los Angeles, où NEWS date la release du 27/10).
Quoi : des fichiers texte (`africa`, `europe`, `northamerica`…) avec des lignes `Rule` : `NOM DE À - MOIS JOUR HEURE DÉCALAGE LETTRE`. Pour Cuba, la règle « retour en heure standard le 1er dimanche de novembre » s'arrête en 2025 (donc pas de retour en 2026) et reprend en 2027, le 7 novembre. Le commit contient aussi un commentaire sourcé (annonce du 24/10, retard de 30 minutes des horaires d'école et de travail).
Comment : `zic` (« zone information compiler », `man zic`) lit ces fichiers texte et produit des fichiers binaires TZif (`/usr/share/zoneinfo`). C'est ce que lisent glibc, Python…
Releases : 3 en 2025 (2025a/b/c), 6 en 2026 au 30/10 (2026a à 2026f). Vérifié dans NEWS : https://data.iana.org/time-zones/tzdb/NEWS

Frise Cuba (heures UTC) :
* sam. 24/10 : communiqué conjoint MINEM + MTSS (heure inconnue ; CiberCuba l'a relayé à 18:16 UTC) ; motif officiel : crise électrique
* lun. 26/10 18:09:17 : commit `5b5b39dae1` de Tim Parenti, « Cuba will not fall back 2026-11-01; stays on -04 through 2027-11-07 »
* mer. 28/10 06:16:49 : tag `2026f` signé par Paul Eggert
* dim. 1er/11 05:00 : retour en arrière prévu (00:00 heure standard d'après la règle `Sun>=1 0:00s`, dérivé de la règle)
Sur le fil tz du 26/10, Tim Parenti prévoit que les vendeurs (Apple, Android) n'auront pas livré de données à jour avant la fin de la semaine ; Robert Bastian (CLDR) : « it's impossible for CLDR to get changes out to devices before Nov 1 ». https://lists.iana.org/hyperkitty/list/tz@iana.org/message/JZJE3ZCEFFSK6AM26BORTWICNSXWTUSE/
Vérifier : `git show 5b5b39dae1` dans eggert/tz ; `git tag -v 2026f`.
-->

---
clicks: 10
class: no-center
---

# Qui a une copie de tzdata ?

<TzdbLayers class="mt-4" />

<!--
Lecture : en haut la source, puis des grappes qui en dépendent, puis des grappes qui dépendent des précédentes. Instantané du 30/10/2026 (ma machine Ubuntu 24.04, conteneurs podman tirés le jour même, paquets installés dans des dossiers jetables). Test de référence : l'offset d'America/Havana au 2026-11-02 12:00Z vaut -05:00 jusqu'à la 2026e et -04:00 avec la 2026f.

Ce qui suit la source directement :
* distributions : Debian 12 a déjà la 2026f (`bookworm-security`), Ubuntu 22.04/24.04/26.04, Fedora, Alpine, Arch sont en 2026e (Launchpad, index Debian, Repology)
* Windows : base propre dans le registre (`HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Time Zones`), mise à jour par Windows Update, **aucun numéro de version tzdata publié**. Le badge « ≈2026e » est une **estimation de ma part** : le KB5127648 (Windows 11 24H2/25H2, sécurité du 13/10/2026) apporte la zone Manitoba, qui correspond à tzdata 2026e (29/09/2026) ; il ne contient pas Cuba (2026f). Un KB par version de Windows pour un même changement : Windows 11 23H2 KB5126653, Server 2025 KB5126646, Server 2022 KB5126655, Server 2019 KB5126651, Server 2016 KB5126868, Windows 10 LTSC 2021 KB5126657 ; pour la Colombie-Britannique et l'Alberta sur Windows 11 24H2/25H2, la préversion KB5124010 du 22/09. Vérifiés sur support.microsoft.com. Cuba : aucune trace chez Microsoft au 30/10 (blog DST, pages KB)
* Android : module Mainline « Time Zone Data » (Android 10+), téléchargé puis redémarrage (« weeks » pour appliquer un changement, source Google). La version se lit dans `tz_version` (format `009.001|2025a|001`) : `adb shell cat /apex/com.android.tzdata/etc/tz/tz_version` (déduit du code AOSP, non testé sur appareil) ; sur Android 10 à 13 : `adb shell head -c 11 /apex/com.android.tzdata/etc/tz/tzdata`. Aucune trace d'une 2026f dans AOSP (le dernier commit tz public est 2025a) ni d'annonce Google pour Cuba
* copies embarquées : Node embarque son ICU en statique (même avec un dossier vide monté sur `/usr/share/zoneinfo` il répond 2026e) : Node 20.20 = 2025c, Node 22.21 = 2025b, Node 22.23+ = 2026e ; une JVM a sa copie `lib/tzdb.dat` (`eclipse-temurin:17` annonce 2026b alors que son système est en 2026e ; correctif 2026f dans JDK 28 seulement, JDK-8396048) ; Go 1.27.3 embarque 2026c (`lib/time/zoneinfo.zip`), aucun commit 2026e/f pour l'instant
* bibliothèques avec leur copie : `tzdata` PyPI 2026.6 (2026f), `pytz` 2026.6, `moment-timezone` 0.6.6 (`moment.tz.dataVersion` = 2026f), Joda-Time 2.15.1 (2026f), NodaTime 3.3.7 (2026f), ICU4J 79.1 (2026e) : seules celles-ci répondent -04:00 pour Cuba aujourd'hui

Ce qui dépend de ces grappes :
* lisent le système : Python `zoneinfo`, .NET `TimeZoneInfo` (`TimeZoneNotFoundException` si tzdata absent), glibc (`TZ` inconnu : UTC sans erreur), PostgreSQL **compilé avec `--with-system-tzdata`** (c'est le cas des images officielles (vérifié avec `pg_config --configure` : 2026e ; l'image utilise le paquet PGDG `17.11-1.pgdg13+2`) et du paquet Debian : le fichier `server/postgresql.mk` de `postgresql-common` (trixie, version 278), inclus par le `debian/rules` de `postgresql-17`, passe `--with-system-tzdata=/usr/share/zoneinfo`, lu sur sources.debian.org ; bookworm non lu ; par défaut, PostgreSQL utilise la copie fournie avec ses sources (grappe « copies embarquées » : 2026c d'après les release notes des dernières mineures 14.24 à 18.6). MySQL est à part : `mysql_tzinfo_to_sql` **copie** les fichiers système dans ses propres tables, une commande à lancer, et la doc conseille de redémarrer ensuite. Plus généralement, un processus déjà lancé peut garder l'ancienne règle : testé seulement pour Python (`ZoneInfo.clear_cache()`), à ne pas généraliser aux autres sans test
* images de conteneurs : figées à la construction (images tirées le 28/10 ou avant). `python:3.14`, `node:22`, `golang` (latest, Go 1.27), `postgres:17` (Debian 13), `mysql:9` (Oracle Linux, `2026e-rearguard` : même release dans un autre format) : 2026e. `ubuntu:22.04/24.04/26.04` et `alpine:3.22` : le paquet `tzdata` n'est pas installé (`TZ=Europe/Paris date` répond UTC, sans erreur) ; `apt-get install tzdata` donne 2026e ; `node:22-alpine` aussi sans zoneinfo. À l'inverse `mariadb:11` (Ubuntu 24.04) a tzdata installé (2026e). Raison officielle non trouvée
* via Intl : `luxon`, `date-fns-tz` et le polyfill Temporal n'ont pas de données de fuseaux : ils interrogent `Intl` (l'API d'internationalisation de JavaScript, implémentée par ICU), donc le tzdata du runtime. Vérifié seulement avec **Node** (ICU embarqué, d'où la grappe « Node (ICU) » qui l'alimente) : sous Node 22.21 (tz 2025b), ils répondent -05:00 pour Cuba. Pour les navigateurs, Deno et Bun, je n'ai pas vérifié l'origine de leur tzdata (l'implication de `Intl` sur leur doc n'a pas non plus été lue)
* via le paquet PyPI `tzdata` : python-dateutil 3, arrow, pendulum en dépendent

Autres langages (testés le 30/10, conteneurs podman, test Cuba : -05:00 jusqu'à la 2026e, -04:00 avec la 2026f) :
* Ruby : `tzinfo` 2.0.6 lit le système d'abord ; sans zoneinfo système ni gem, `TZInfo::DataSourceNotFound` ; avec le gem `tzinfo-data` 1.2026.6 (28/10/2026, 2026f) seul : -04:00
* Rust : `chrono-tz` 0.10.4 (juillet 2025) embarque la tz **2025b** à la compilation, sans lire le système : -05:00, en retard de plus d'un an ; `jiff` 0.2.38 lit le système sous Unix, `jiff-tzdb` 0.1.9 (06/10/2026, 2026e) seulement si on active la feature ; sans système ni bundle : erreur « no time zone database configured »
* PHP : la base est dans le cœur de PHP (jamais le système) : `php:8.4-cli` (8.4.27) = `timezone_version_get()` `2026.5` (2026e), `php:8.3-cli` (8.3.36) = `2026.1` (2026a) ; correspondance « 2026.N = lettre N » : lecture de ma part, non confirmée par la doc
* Elixir : le paquet hex `tzdata` 1.2.2 embarque la 2026d et **télécharge les mises à jour depuis l'IANA à l'exécution** (testé : 2026d avec `autoupdate: :disabled`, 2026f après quelques secondes sinon) ; il lui faut un accès réseau
* C++ : `std::chrono::tzdb` (libstdc++, GCC 16.2.0) lit `/usr/share/zoneinfo/tzdata.zi` ; sans lui, une copie embarquée figée à la date du compilateur (2026b) sans erreur. Non testés : libc++, MSVC, la bibliothèque « date » de Hinnant
* Perl (`DateTime::TimeZone` 2.72 du 28/10) et Dart (`timezone` 0.11.2 du 12/10) : non vérifiés, absents de la slide

Python, le piège : `zoneinfo` cherche chaque clé dans `TZPATH` (système) d'abord, et ne se rabat sur le paquet PyPI `tzdata` que si la zone est introuvable. Installer `tzdata` 2026.6 ne change donc rien si le système a déjà `America/Havana` : -05:00 (testé avec zoneinfo, dateutil 3, arrow, pendulum, whenever). Il faut `zoneinfo.reset_tzpath(to=[])` ou `PYTHONTZPATH=""` pour forcer la copie PyPI (-04:00). Un processus déjà lancé garde l'ancienne règle tant qu'on n'appelle pas `ZoneInfo.clear_cache()` (testé).

Go, la recherche d'une zone (`time.LoadLocation`, doc `pkg.go.dev/time`) : 1) `ZONEINFO` (dossier ou zip), 2) l'emplacement système (Unix), 3) `$GOROOT/lib/time/zoneinfo.zip`, 4) le paquet `time/tzdata` s'il est importé. Les trois premiers lisent des fichiers à l'exécution. Le 4e est une copie compilée dans le binaire (`-tags timetzdata` ou `import _ "time/tzdata"`, environ +450 Ko) : au build, mais consultée en dernier à l'exécution. Testé : binaire sans le tag dans une image Alpine sans tzdata : `unknown time zone America/Havana` (une `error`, pas un panic) ; avec le tag : -05:00 (copie en 2026c).

Vérifier chez soi :
* `head -1 /usr/share/zoneinfo/tzdata.zi` ou `apt-cache policy tzdata` ; `rmadison tzdata` (devscripts) ; https://launchpad.net/ubuntu/+source/tzdata ; https://tracker.debian.org/pkg/tzdata
* `node -p "process.versions.tz + ' ' + process.versions.icu"`
* Python : `uv run python -c "import zoneinfo; print(zoneinfo.TZPATH)"` et `importlib.metadata.version('tzdata')`
* JVM : `ZoneRulesProvider.getVersions("Europe/Paris")` contre `head -1 /usr/share/zoneinfo/tzdata.zi`
* `podman image inspect --format '{{.Created}}' IMAGE` et `podman run --rm IMAGE head -1 /usr/share/zoneinfo/tzdata.zi`
* test Cuba : `TZ=America/Havana date -d 2026-11-02T12:00:00Z +%z` : `-0500` sans la 2026f, `-0400` avec.
-->

---

# Un bazar infini !

<div class="absolute inset-0">
  <img v-click="[1, 2]" src="../images/arizona-time-zone.eddc9932.png" alt="Timezone-ception" class="absolute inset-0 w-full h-full object-contain" />
  <img v-click="2" src="../images/wikipedia_international_date_line_cropped.png" alt="International date line" class="absolute inset-0 w-full h-full object-contain" />
</div>

<!--
International date line :
* discontinuité de 24 heures (changement de jour)
* demi-heure
* trois-quart d'heure (rare !)
* kiribati -11/-10 devenu +13/+14
-->

---

# Problèmes

<ul>
  <li>Non-unicité : DST<span v-click>, <span class="text-orange-400">timezones</span></span></li>
  <li>Non-monotonicité : DST<span v-click>, <span class="text-orange-400">timezones</span></span></li>
  <li>Non-continuité : DST<span v-click>, <span class="text-orange-400">timezones</span></span></li>
  <li>Non-homogénéité : DST, leap years<span v-click>, <span class="text-orange-400">timezones</span></span></li>
  <li>Non-constance : DST, leap years<span v-click>, <span class="text-orange-400">timezones</span></span></li>
  <li>Non-standardized : dates and time formats</li>
</ul>

---

# Conseils : stocker et conserver

<v-clicks depth="2">

* saisie utilisateur : datetime dans le bon fuseau (zoned)
  * obligatoire, jamais de datetime "naïf" !
* convertir en 2 valeurs distinctes : datetime en UTC + fuseau voulu
  * (noter la version de tzdata utilisée pour le calcul)
* faire toutes les opérations sur la valeur UTC
* à la présentation, reconvertir la valeur UTC dans le fuseau voulu

</v-clicks>

<!--
bases de données : le fuseau n'est presque jamais conservé (`timestamptz` le perd), il faut le stocker sans support natif
-->

---

# Conseils : l'intention versus l'offset

<v-clicks>

* l'intention : « 10h à Mexico City » = une heure + un lieu
* un offset (`-05:00`) est un résultat calculé, pas une intention
  * réunion hebdo à `09:00+02:00` (CEST) : 08:00 à Paris dès le 28 octobre
* une zone stocke un lieu plutôt qu'une valeur : bien plus stable
* l'UTC est un cache dérivé : le garder, mais le recalculer quand tzdata change
  * recalculer les événements postérieurs à la date d'effet de la règle (+ valeurs dérivées : compteurs à rebours…)
  * métier : décider quoi faire des événements déplacés ou déjà déclenchés à la mauvaise heure
* échanger : RFC 9557 (2024), `2027-03-03T09:00+01:00[Europe/Paris]`, support parcellaire

</v-clicks>

<!--
Mexique, tzdata 2022f (28/10/2022) : le DST est abrogé, 2 jours de préavis pour Chihuahua.
10 h à Mexico le 12/04/2023 = 15:00 UTC avec tzdata 2022e, 16:00 UTC avec 2022f.
L'UTC stocké en 2022 est faux d'une heure, l'intention (10 h + zone) reste juste ; un offset `-05:00` figé donnerait 09 h à Mexico.
Offset ou zone : l'offset est figé et casse au prochain changement d'heure ou de règle ; la zone suit tzdata, d'où la version de tzdata notée avec l'UTC.
Pourquoi garder l'UTC : les bases ne gardent presque jamais la zone (PostgreSQL, MySQL, MongoDB, SQL Server ; seul Oracle garde la région ; `timestamptz` la perd), donc une colonne dédiée pour la zone,
RFC 9557 : stdlib Python ne le supporte pas, Temporal / Java / whenever oui. Z = instant connu, offset inconnu ; +00:00 n'est pas un fuseau (Londres l'hiver).
-->

---

# Conseils : maintenir tzdata

<v-clicks>

* inventorier : où tourne mon code, et quelles couches ont leur propre copie
* savoir d'où vient chaque tzdata : paquet, runtime, image, base de données (cf. le schéma)
* mettre à jour : les releases sont fréquentes et le préavis court
  * reconstruire les images, redémarrer ce qui garde un cache

</v-clicks>

<!--
Le lien avec le schéma précédent : chaque boîte est une copie à mettre à jour séparément. Exemples : MySQL (charger les tables puis redémarrer), JVM (nouvelle version du JDK ou outil `tzupdater`, non vérifié), `zoneinfo` (cache : `ZoneInfo.clear_cache()` ou redémarrage), image de conteneur (reconstruire).
-->

---

# Une date, ce n'est pas un instant

<img src="../images/skip.png" class="absolute top-8 right-4 w-24" />

<div class="grid grid-cols-[minmax(0,1fr)_25rem] gap-4 items-start mt-5">
<div>

```html
<input type="date" id="input" />
```

```js {none|1|2-3|4-10}
const value = input.value
const instant = new Date(value)
instant.toISOString()
const fmt = { dateStyle: 'long', timeStyle: 'short' }
instant.toLocaleString('fr-FR', {
  ...fmt, timeZone: 'Europe/Paris',
})
instant.toLocaleString('fr-FR', {
  ...fmt, timeZone: 'America/New_York',
})
```

</div>

<DatePickerTrap />

</div>

<style>
.slidev-code, .slidev-code code, .slidev-code pre { font-size: 0.85rem !important; }
</style>

<!--
JS n'a pas de type « date seule » : `Date` est toujours un instant, d'où l'heure et le fuseau inventés. Une chaîne date seule est lue en UTC, alors qu'une date-heure sans offset est lue en heure locale.

* `valueAsDate` donne le même résultat que `new Date(value)`
* `"2025/03/01"` (non standard) est interprété en heure locale (vérifié par exécution, Node 20 et 26)
* `Temporal.PlainDate` règle le problème → voir la solution 05-10 plus tard
* le navigateur du speaker est à Paris, d'où le fuseau forcé à l'affichage
-->

---
class: no-center
---

# Quand tzdata change : des questions à trancher

<img src="../images/skip.png" class="absolute top-8 right-4 w-24" />

* Intention (heure + zone) : E<sub>ancien</sub> et E<sub>nouveau</sub> sont l'UTC calculé avec l'ancienne et la nouvelle tzdata, U l'instant de la mise à jour

<div class="absolute left-8 right-8 top-36">
  <TzdbChangeTimeline />
</div>

<div class="absolute left-8 right-8 bottom-6 text-sm">

<v-click at="7">

* fait observé (log, paiement) : l'UTC est le fait, on ne le recalcule jamais

</v-click>
<v-click at="8">

* une heure locale peut devenir inexistante ou ambiguë : Python choisit `fold=0` sans rien dire

</v-click>
<v-click at="9">

* mise à jour avant la date d'effet : seul le premier cas existe

</v-click>

</div>

<!--
Mexique, tzdata 2022f : 10 h à Mexico le 12/04/2023 = 15:00Z (2022e) puis 16:00Z (2022f), l'événement recule ; U = 12/04 15:30Z → le passé repasse dans le futur.
Égypte, tzdata 2023a : 10 h au Caire le 15/06/2023 = 08:00Z (2022g) puis 07:00Z (2023a), l'événement avance ; U = 15/06 07:30Z → le futur devient passé.
Date d'effet D = premier instant (UTC) où l'ancienne et la nouvelle règle donnent un décalage différent (Mexique : 2023-04-02 08:00Z, pas la date de la loi). Les cas 2 à 4 n'existent que si U est après D.
Les cas 3 et 4 ne concernent que les événements à moins de Δ (ampleur du décalage, 1 h ici) de U. Le vrai dégât : tous les événements entre D et U ont déclenché leurs alertes à la mauvaise heure.
Heure inexistante : Le Caire, 28/04/2023 00:30 (tzdata 2023a saute de 00:00 à 01:00) ; fold=0 → 22:30Z, fold=1 → 21:30Z, avant D.
Heure ambiguë : Kazakhstan, tzdata 2024a (01/02/2024) : Almaty passe de +06 à +05 le 01/03/2024 à 00:00 ; 29/02/2024 23:30 : fold=0 → 17:30Z (+06), fold=1 → 18:30Z (+05). Python ne lève aucune erreur ; Temporal : `disambiguation: 'reject'`.
Corrections rétroactives de l'historique : Colombie (2022g), 12:00 le 01/03/1993 → 16:00Z puis 17:00Z ; Vietnam (2024a).
Ne pas filtrer par `UTC_cache > now()` (rate le cas 3, recalcule le cas 4 en silence). Détails et sources : HANDOFF_05_conseils_stockage.md.
-->

---

# Petit bonus : décalage solaire

<img src="../images/skip.png" class="absolute top-8 right-4 w-24" />

<v-click>

<ZoomableImage src="/images/solartimevsstandardtime.png" :initial-scale="0.5" />

</v-click>
