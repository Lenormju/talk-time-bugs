# Les problèmes continuent

<Skip />

<v-clicks>

* Pourquoi il y a 2 dates de début du Ramadan en 2026 ?
* le mois commence avec l'apparition dans le ciel du premier quartier de lune
* l'observation peut donc différer d'un jour ou deux selon la longitude d'observation

* <details><summary>Détails des difficultés, d’après Wikipedia</summary>

  <blockquote style="font-size: 0.5em">
  Or, le croissant lunaire ne devient généralement visible que 15h à 18h après la conjonction, avec impérativement l’existence de conditions favorables résultant de nombreux facteurs tels que :
  <ul>
  <li>la date julienne de la conjonction au moment des calculs</li>
  <li>son heure exacte ; le nombre d’heures écoulées depuis la conjonction (âge de la Lune)</li>
  <li>la durée en minutes séparant le coucher du Soleil de celui de la Lune</li>
  <li>les coordonnées équatoriales du Soleil et du croissant lunaire sur la sphère céleste (ascension droite et déclinaison)</li>
  <li>les coordonnées géographiques (latitude et longitude) de l’observateur</li>
  <li>les coordonnées horizontales telles que l’altitude de la Lune au coucher du soleil, l’altitude relative entre la Lune et le Soleil à ce même moment, les azimuts respectifs du Soleil et de la Lune, l’azimut relatif entre les deux astres</li>
  <li>la mesure de l’élongation (distance angulaire séparant la Lune du Soleil au moment du coucher)</li>
  <li>l’angle de phase</li>
  <li>la nature du lieu où l’on procède à l’observation</li>
  <li>les conditions d’observation (pollution, humidité, température de l’air, altitude)</li>
  <li>la limite de détection de l’œil humain</li>
  <li>etc ...</li>
  </ul>
  </blockquote>

  </details>

* donc désaccords entre pays et communautés
* contribué aux recherches astronomiques par les scientifiques du monde arabe
* est-ce que l'observatoire d'Arabie Saoudite a plus raison que les autres ?
* la Grande Mosquée de Paris se base sur une méthode traditionnelle (mi-observation, mi-scientifique)
* alors que le Conseil français du culte musulman préfère une méthode seulement scientifique

</v-clicks>

---

# Choix politiques

<v-clicks depth="2">

* Arrêter les secondes intercalaires : **décidé** le 15 octobre 2026 (CGPM)
* Arrêter les DST dans l'UE : consultation en 2018 (84 % pour), voté au Parlement en 2019, **bloqué au Conseil** depuis fin 2019, puis éclipsé par le Covid-19
* Changer les règles d'un pays (**surtout avec un préavis très court**) :
  * Égypte (2016f) : **2 jours**
  * Mexique (2022f) : **2 jours**
  * Colombie-Britannique (2026b)
  * Maroc (2026c)
  * Alberta (2026c)
  * Territoires du Nord-Ouest (2026d)
  * Manitoba (2026e)
  * Cuba (2026f) : **5 jours**

</v-clicks>

<style>
li {
  font-size: 0.95em;
}
</style>

<!--
Préavis = délai entre la publication tzdata et le changement (pas la date de la loi).

Dates des préavis courts (publication tzdata → changement) : Mexique 28/10/2022 → 30/10/2022 ; Égypte 05/07/2016 → 07/07/2016 ; Cuba 27/10/2026 → 01/11/2026.

Préavis négatif (BC, Alberta, TNO) : tzdata publié APRÈS la date légale du changement (BC −44 j : légal 09/03, publié 22/04 ; Alberta −20 j : 18/06 → 08/07 ; TNO −21 j : 21/08 → 11/09). Aucun effet sur les horodatages passés : ils étaient déjà à cet offset en été et ne reculent simplement plus, donc pas de changement de règle de dernière minute comme Mexique / Égypte / Cuba. Manitoba : +32 j (publié 29/09, légal 31/10).

Autres exemples, pas sur la slide :
- Kazakhstan (2024a, 01/02/2024) : tout le pays à UTC+5 le 01/03 : 1 mois
- Manitoba (2026e, 29/09/2026) : UTC−5 permanent légalement le 31/10, donc pas de retour en arrière le 01/11 : ~1 mois
- Alberta (2026c, 08/07/2026) : UTC−6 permanent en vigueur le 18/06, publié 3 semaines après, comme les TNO
- Colombie-Britannique (2026b, 22/04/2026) : UTC−7 permanent en vigueur le 09/03 (lendemain du dernier passage à l'heure d'été du 08/03), publié ~6 semaines après
- TNO (2026d, 11/09/2026) : UTC−6 permanent en vigueur le 21/08, publié 3 semaines après (America/Inuvik ; le reste du territoire est couvert par America/Edmonton, déjà fait en 2026c)
- Même contournement temporaire pour BC, Alberta, TNO, Manitoba : tzdata place le changement au 01/11 à 02:00 (limite de CLDR / ICU)
- Nord-ouest de l'Ontario : suit finalement le Manitoba (2026f), réglementation provinciale publiée
- Saskatchewan : nouvelle Time Act 2026 en vigueur le 30/10/2026, aucun changement attendu
- Moldavie (2026a) : correction historique (heures de transition UE depuis 2022), pas un changement de 2026, donc pas sur la slide
- TNO et Alberta : rien ne change dans le passé (déjà en UTC−6 l'été), mais la règle arrive après la loi. tzdata modélise le changement au 01/11 à 02:00 (contournement temporaire pour CLDR / ICU)
- Maroc : depuis le décret du 26/10/2018, UTC+1 = heure standard, UTC+0 pendant le Ramadan (modélisé en DST négatif). Même impact dev qu'un DST (tzdata à déployer), mais ce n'est pas un DST. Absent de la carte « Evolutions » qui ne montre que le DST
- 2026f dit aussi : plus de secondes intercalaires, les tables leap-seconds n'expirent plus

UE : la dernière discussion au Conseil date du 02/12/2019 (avant le Covid). Le Covid (puis l'Ukraine) a fait passer le sujet au second plan, mais le blocage vient du désaccord heure d'été / heure d'hiver.
Vote au Parlement : 26/03/2019, 410 pour, 192 contre, 51 abstentions. Consultation 2018 : 4,6 M de réponses, 84 % pour la suppression.

Sources :
- https://data.iana.org/time-zones/tzdb/NEWS (2016f, 2022f, 2024a, 2026a, 2026b, 2026c, 2026d, 2026e, 2026f)
- https://www.europarl.europa.eu/legislative-train/theme-union-of-democratic-change/file-discontinuing-seasonal-changes-of-time
- https://www.euronews.com/2026/10/22/eu-planned-to-scrap-clock-changes-why-are-they-still-happening
- https://www.thelocal.com/20241024/whatever-happened-to-the-eu-plan-to-ditch-the-changing-of-the-clocks
-->
