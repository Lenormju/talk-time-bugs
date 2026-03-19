# Quiz !

<v-click>

1. Quel jour et mois désignent `10/11/2025` ❓

</v-click>

<v-clicks>

* 10 novembre (mois n°11), format US `MM-DD-YYYY`
* 11 octobre (mois n°10), format Européen
* aucun moyen de savoir sans contexte

</v-clicks>

<v-click>

2. L'instant <code><LocalTimeOffset :offsetMinutes="-60" /></code> est-il dans le passé ou le futur ❓

</v-click>

<v-clicks>

* dans le passé dans cette salle, car il est <code><LocalTimeOffset/></code>
* dans le futur à Rio de Janeiro, car il est <code><RioClock /></code>
* aucun moyen de savoir sans contexte

</v-clicks>

<v-click>

3. Quel jour on sera "le mois prochain" ?

</v-click>

<v-clicks>

* Mercredi 1er ? (premier jour)
* Jeudi 16 ? (même jour dans 4 semaines ≈ 1 mois) <!-- FIXME PTC -->
* Dimanche 19 ? (même ordinal) <!-- FIXME PTC -->

</v-clicks>
