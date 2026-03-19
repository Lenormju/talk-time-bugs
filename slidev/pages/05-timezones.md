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

# Rapide exemple

<v-clicks depth="2">

* "prime meridian" (IERS Reference Meridian) : Greenwich
  * (je vous passe l'histoire de Greenwich)
  * **a servi à définir UTC**
  * (je vous passe l'histoire d'UTC)
* changement d'heure :
  * avant le 29 mars : European Central Time (ECT, UTC+1)
  * après le 29 mars : European Central Summer Time (ECST, UTC+2)
* voyage au Royaume-Uni :
  * UK suit le Greenwich Mean Time (GMT, UTC) ou le British Summer Time (BST, UTC+1)
  * a conservé son changement d'heure synchronisé avec le reste de l'Union Européenne
  * à l'aller je "perds" 1h, au retour je la regagne

</v-clicks>

---

# Un sacré bazar !

<v-clicks depth="2">

* maintenu par l'IANA ("Internet Assigned Numbers Authority", filiale de l'ICANN), aussi connue pour :
  * les DNS root zones
  * les plage d'IP addresses
  * les AS numbers
  * servir de registry pour certains protocoles (port numbers, HTTP status codes, TLS cypher suites, DNS root zones, jeux de caractères pour `Content-Type` UTF-8, ISO-8859-1, ...)
* "IANA Time Zone Database" ou "tz" ou "tzinfo"
  * format riche
  * données historiques
  * mise-à-jour rapide
* inclus dans les OS
* inclus dans les libs des langages de programmation
* à mettre à jour régulièrement

</v-clicks>

TODO problème inconstant

TODO cas tordus, et cas de changement de timezone, DST

TODO tous les problèmes

TODO conclusion : jamais de naive, et privilégier très très fortement UTC, sauf si on sait ce qu'on fait !!
