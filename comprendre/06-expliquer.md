# 6. Comment l'expliquer : quatre niveaux

## Niveau 1 — à tout le monde (2 minutes)

> Les nombres premiers (2, 3, 5, 7, 11…) semblent tomber au hasard, mais leur nombre total suit une courbe très régulière. Riemann a découvert en 1859 que **l'écart** entre la vraie quantité et la courbe est piloté par une liste de nombres spéciaux, les « zéros » de sa fonction ζ. Il a conjecturé qu'ils sont **tous alignés sur une même droite**. Si c'est vrai, les premiers ne s'écartent jamais de la courbe de plus qu'une « racine carrée » : ils sont aussi réguliers qu'ils peuvent l'être.
>
> En novembre 2026, le mathématicien Levent Alpöge, travaillant avec l'IA Claude, a publié une preuve **écrite pour un ordinateur**, dans le langage Lean. Le logiciel a vérifié chacun des milliards de pas logiques, et plusieurs vérificateurs indépendants ont donné le même verdict. On est donc quasi certain que c'est **vrai**. En revanche, aucun humain ne comprend encore **pourquoi**.

**Image parlante.** Imaginez une marche aléatoire, pile ou face, un pas à gauche ou à droite. Après $x$ pas, on est en général à environ $\sqrt x$ du départ. RH dit que les nombres premiers ne s'écartent pas plus de leur moyenne que cette marche : environ $\sqrt x$ pour un total de l'ordre de $x/\ln x$.

## Niveau 2 — lycée / licence

1. **La fonction zêta.** Pour $s > 1$, on pose $\zeta(s) = 1 + \frac1{2^s} + \frac1{3^s} + \cdots$. Euler a montré que $\zeta(s) = \prod_p \frac{1}{1-p^{-s}}$, un produit sur les nombres premiers. C'est le lien entre $\zeta$ et les premiers.
2. **Le prolongement.** Riemann prolonge $\zeta$ à tout le plan complexe, sauf en $s = 1$.
   - Elle s'annule en $-2, -4, -6, \dots$ : ce sont les zéros *triviaux*.
   - Elle s'annule aussi une infinité de fois dans la bande $0 < \operatorname{Re}s < 1$.
3. **La formule explicite.**
   $$\psi(x) = x - \sum_\rho \frac{x^\rho}{\rho} - \cdots$$
   Chaque zéro $\rho = \beta + i\gamma$ ajoute une « onde » de taille $x^\beta$. Si tous les $\beta$ valent $1/2$, les ondes sont toutes de taille $\sqrt x$.
4. **L'énoncé.** RH : tous les zéros non triviaux ont $\beta = 1/2$.
5. **La vérification numérique avant la preuve.** Plus de $10^{13}$ zéros avaient déjà été calculés, tous sur la droite. Mais un calcul ne prouve jamais un énoncé infini.

**Démonstration à montrer.** Lancez `comprendre/code/rh_algos.py`. Pour $x = 10^7$, on a $\pi(x) = 664\,579$, $\operatorname{li}(x) \approx 664\,918$, et l'écart vaut 339, alors que $\sqrt x = 3162$.

## Niveau 3 — étudiant en mathématiques

- **Énoncé formel** : [01](01-ce-qui-est-prouve.md). On a RH pour $\zeta$, et GRH pour toutes les $L(s,\chi)$ de Dirichlet, primitives ou non.
- **Conséquences** : [03](03-consequences-et-formules.md). Il y a von Koch, Schoenfeld et Cramér ; les critères de Robin et Lagarias ; les bornes de Bach sur les non-résidus et les témoins de Miller ; les groupes de classes des corps quadratiques.
- **L'idée de la preuve, en analogie** : [02](02-strategie-de-la-preuve.md).
  - *Sur un corps fini*, on prouve l'analogue de RH (Weil) par la méthode de Stepanov. On construit un polynôme qui s'annule **avec multiplicité** en chaque point, puis on compte les zéros grâce au degré.
  - *Sur les entiers*, la multiplicité n'a pas de sens : on ne sait pas « dériver un nombre ». Alpöge la remplace par une **chaîne de relèvements thêta**, chaque relèvement valant « un ordre de multiplicité ». Avec environ $\sqrt X$ relèvements, on retrouve l'exposant $1/2$.
  - La positivité nécessaire est celle du **critère de Weil**. Elle est obtenue comme positivité de **déterminants de périodes** automorphes.

## Niveau 4 — chercheur

À lire avec les réserves de [02](02-strategie-de-la-preuve.md) : la seule source est la remarque de 4 pages, et l'archive Lean fait 17 M de lignes. Points saillants :

- une preuve de Weil et Deligne par « signe seul », via la quadrique chemin $x_1x_2 + \dots + x_{k-1}x_k$ et Parseval itéré ;
- l'automorphie via la sixième couverture de $GL_5$ et les séries thêta sur une courbe CM ;
- des relèvements thêta itérés entre groupes unitaires définis, $\pi \mapsto \pi \boxplus \mu_j[t]$, dont la période est une période de Bessel (seesaw, Rallis) ;
- des divisibilités via Chowla–Selberg et la formule de masse de Siegel, l'inégalité de pente de Bost et une tour d'Iwasawa choisie avec des ensembles de Behrend ;
- un affaiblissement de Vandiver pour les classes de $H^1$ résiduelles ;
- une barrière intermédiaire à « 2/3 », à rapprocher du préprint arXiv 2608.13637 (Alpöge–Furman) : « plus de deux tiers des zéros sont simples et sur la droite critique ».

Questions ouvertes intéressantes :

1. Quelle est la plus petite partie de l'archive réellement utilisée ? On peut l'élaguer en suivant le graphe de dépendances de `Main`.
2. Peut-on extraire de l'archive un **énoncé intermédiaire lisible**, comme `UpperTheory.EveryCharacter` ou `Formalism.VW.rh_of_every`, et l'expliquer seul ?
3. L'argument s'étend-il à ERH (Dedekind), comme l'annonce l'auteur ?

## Erreurs fréquentes à éviter quand on explique

| Phrase entendue | Correction |
|---|---|
| « La cryptographie est cassée » | Non. RH ne donne aucun algorithme de factorisation. Elle *garantit* certains algorithmes (voir [04](04-algorithmes.md)). |
| « Tout GRH est démontré » | Non : seulement Dirichlet, donc les corps abéliens. Ni ERH, ni les L automorphes, ni Artin. |
| « Les mathématiciens ont relu la preuve » | Non. Les ordinateurs l'ont vérifiée, plusieurs vérificateurs indépendants, et la communauté Lean l'a certifiée. La relecture humaine reste à faire. |
| « Une IA a prouvé RH seule » | Selon l'auteur, c'est une collaboration. Il a choisi l'approche (Stepanov et modèle jouet), et Claude a mené la partie automorphe technique. |
| « Lean peut se tromper, donc rien n'est sûr » | Le risque résiduel est très faible : plusieurs noyaux écrits indépendamment, axiomes standard seulement, énoncé de Mathlib relu par des experts. Ce n'est pas zéro, mais c'est bien plus fiable qu'une relecture humaine de 250 000 pages. |
