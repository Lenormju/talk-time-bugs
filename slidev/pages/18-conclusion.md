# Conclusion

<v-clicks>

* déterminer le temps dans le passé n'est pas simple
* déterminer si deux instants passés sont simultanés n'est pas simple
* déterminer dans combien de temps se produira un instant futur est impossible
* en fait, le temps est toujours très délicat à manipuler
* complexité essentielle méconnue
* complexité accidentelle méconnue
* les IA font ces erreurs aussi, dans le code et les tests
* si vous voulez vous entrainer : FalsehoodsAboutTime.com
  * [Falsehoods programmers believe about time](https://infiniteundo.com/post/25326999628/falsehoods-programmers-believe-about-time) (34)
  * [More falsehoods programmers believe about time; “wisdom of the crowd” edition](https://infiniteundo.com/post/25509354022/more-falsehoods-programmers-believe-about-time) (79)

</v-clicks>

---

# Pour survivre dans la jungle

<div class="grid grid-cols-2 gap-x-12 gap-y-2 text-sm">

<div v-click>

### Vocabulaire

* instant, UTC, offset
* naïf contre zoned
* date seule
* durée contre période calendaire

</div>

<div v-click>

### Stocker et échanger

* stocker l'intention
* types de base de données
* unités et epoch
* RFC 3339 / RFC 9557

</div>

<div v-click>

### Tester et détecter

* injecter l'horloge dans le code
* contrôler l'horloge dans les tests
* tester avec un autre `TZ`
* tester les cas limites

</div>

<div v-click>

### Exploitation

* mettre à jour tzdata
* surveiller la dérive d'horloge
* TZ=UTC

</div>

<div v-click class="opacity-40">

### Secondes

* secondes intercalaires et smearing

</div>

</div>
