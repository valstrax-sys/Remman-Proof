# 1. Ce qui est prouvé, exactement

Source : `Statements.lean` et `Main.lean`, à la racine de l'archive (hash `9631b4f0…`). Ce sont les deux seuls fichiers lisibles par un humain qui fixent ce que l'archive démontre. Les 175 185 autres modules ne servent qu'à la preuve.

## Les cinq théorèmes de `Main.lean`

```lean
theorem riemannHypothesis               : RiemannHypothesis
theorem riemannZeta_eq_zero_re          : RiemannZetaZerosOnLine
theorem LFunction_ne_zero_of_half_lt_re : DirichletLNonvanishingRightOfHalf
theorem LFunction_eq_zero_re            : DirichletLZerosOnLine
theorem LFunction_eq_zero_re_of_isPrimitive : PrimitiveDirichletLZerosOnLine
```

`RiemannHypothesis` est la définition **de Mathlib**, pas une définition de l'auteur. C'est le point que `comparator` et `con-leche --compare` ont contrôlé. Les quatre autres énoncés sont définis dans `Statements.lean`, qui n'importe que Mathlib.

## Traduction mathématique

**(1) et (2) — Hypothèse de Riemann (RH).** Pour tout nombre complexe $s$ :

$$\zeta(s) = 0,\quad s \notin \{-2,-4,-6,\dots\},\quad s \neq 1 \;\Longrightarrow\; \operatorname{Re}(s) = \tfrac12 .$$

- Les « zéros triviaux » $-2,-4,\dots$ sont exclus.
- $s = 1$ est exclu pour une raison technique propre à Mathlib : $\zeta$ y a un pôle, mais Mathlib lui donne quand même une valeur.
- (2) est la même affirmation, écrite sans passer par la définition de Mathlib.

**(3) — Non-annulation à droite de 1/2.** Pour tout module $N \ge 1$, tout caractère de Dirichlet $\chi$ modulo $N$ (primitif ou non) et tout $s$ avec $\operatorname{Re}(s) > \tfrac12$, on a $L(s,\chi) \neq 0$. Le seul cas exclu est $\chi = 1$, $s = 1$, qui est le pôle.

**(4) — Hypothèse de Riemann généralisée (GRH) pour les fonctions L de Dirichlet.** Pour tout $\chi$ modulo $N$ et tout $s$ dans la bande critique $0 < \operatorname{Re}(s) < 1$ :

$$L(s,\chi) = 0 \Longrightarrow \operatorname{Re}(s) = \tfrac12.$$

**(5)** est le même énoncé, restreint aux caractères primitifs. Les zéros d'un caractère non primitif dans la bande sont ceux du caractère primitif associé. Les facteurs d'Euler supplémentaires $(1-\chi^*(p)p^{-s})$ ne s'annulent que sur la droite $\operatorname{Re}(s) = 0$.

## Portée : ce qui est couvert et ce qui ne l'est pas

| Fonction L | Couverte ? | Remarque |
|---|---|---|
| $\zeta(s)$ (Riemann) | **Oui** | théorèmes (1) et (2) |
| $L(s,\chi)$ de Dirichlet, tout module $N$ | **Oui** | théorèmes (3) à (5) |
| $\zeta_K$, pour $K$ quadratique ou cyclotomique (plus généralement $K$ abélien sur $\mathbb{Q}$) | **Oui, par conséquence** | $\zeta_K$ est un produit de fonctions L de Dirichlet ; par exemple $\zeta_{\mathbb{Q}(\sqrt d)} = \zeta \cdot L(\cdot,\chi_d)$ |
| $\zeta_K$, pour $K$ non abélien (par exemple les corps de Kummer $\mathbb{Q}(\zeta_n, a^{1/n})$) | **Non** | ce serait l'« ERH » (Extended RH), qu'Alpöge annonce comme probablement accessible plus tard |
| L de Hecke, de formes modulaires, de courbes elliptiques, automorphes | **Non** | |

L'appellation « GRH » de l'annonce désigne donc la GRH **de Dirichlet**. C'est la version dont dépendent la plupart des résultats d'arithmétique élémentaire et d'algorithmique (voir [03](03-consequences-et-formules.md)).

## Ce qui garantit ces énoncés (état au 21/11/2026)

- **Compilation.** Les 175 187 modules compilent : c'est le constat du MIT, et notre réplique indépendante en a refait 13 % avec `lake build` dans une sandbox.
- **Axiomes.** La preuve ne repose que sur `propext`, `Classical.choice` et `Quot.sound`. Il n'y a ni `sorry` ni axiome ajouté.
- **Énoncé.** Le théorème prouvé est bien celui de Mathlib : `comparator` et `con-leche --compare` l'ont confirmé.
- **Vérificateurs.** Plusieurs noyaux indépendants acceptent la preuve exportée : `nanoda`, `con-leche`, `lean4lean` (module par module) et `leanchecker`.
- **Statut.** La communauté Lean et Mathlib l'a certifiée le 21/11/2026.
- **Ce qui manque.** Aucune relecture humaine des mathématiques n'a été faite, et aucune version lisible n'existe.

Une preuve formelle garantit qu'un énoncé est vrai **pour la définition donnée**. Ici, la définition est celle de Mathlib, que des experts ont relue. On sait donc *que* c'est vrai, avec un niveau de certitude rare. On ne sait pas encore *pourquoi*, au sens où un mathématicien l'entend : voir [02](02-strategie-de-la-preuve.md).
