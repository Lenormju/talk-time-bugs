# Talk: le temps c'est de l'argent ... et des bugs

[🎬 **Voir les slides** 🎬](https://lenormju.github.io/talk-time-bugs/index.html)

> De tout temps, les devs ont écrit du code qui manipule les dates, heures, date-heures, durées, fuseaux horaires, ..., et ont introduit des bugs dans leur code. Pourquoi ? Parce que le temps, c'est compliqué, vraiment très compliqué.
>
> À partir d'un simple exemple de commande de viennoiseries en livraison, vous découvrirez la quantité hallucinante de bugs qui se cachent dans tout code qui traite des temps, dates, durées, fréquences, ... Certains sont de l'ordre technique (nos outils sont faillibles ou mal conçus), d'autres de l'ordre humain (des choix contestables, ambigüs et néanmoins répétés). Nous déconstruirons ainsi nos idées reçues, de manière ludique et instructive, à l'aide d'exemples de code concrets, de bugs que j'ai rencontré, et de films célèbres.
>
> Vous repartirez avec la conviction que le temps est un sujet épineux, à ne pas prendre à la légère, mais surtout mieux armés pour en résoudre ou éviter les bugs.

## Versions archivées

Chaque version est archivée en PDF et en zip (site statique, à servir à la racine d'un serveur web), publiées sur GitHub Pages.

| Version | Public | PDF | Zip |
|---|---|---|---|
| BDX I/O (30 octobre 2026) | développeurs | [PDF](https://lenormju.github.io/talk-time-bugs/slides-bdxio.pdf) | [zip](https://lenormju.github.io/talk-time-bugs/slides-bdxio.zip) |
| Paris Test Conf (31 mars 2026) | testeurs | [PDF](https://lenormju.github.io/talk-time-bugs/slides-ptc.pdf) | [zip](https://lenormju.github.io/talk-time-bugs/slides-ptc.zip) |
| Meetup QA (19 mars 2026) | testeurs | [PDF](https://lenormju.github.io/talk-time-bugs/slides-meetup-qa.pdf) | [zip](https://lenormju.github.io/talk-time-bugs/slides-meetup-qa.zip) |

## TODO

- Partie « timezones » : ajouter une slide de solution pour « Une date, ce n'est pas un instant » : `Temporal.PlainDate`
