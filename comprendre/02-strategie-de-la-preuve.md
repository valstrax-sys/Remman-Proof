# 2. La stratégie de la preuve

> **Niveau de certitude de cette note.**
> - **Lean (certifié)** : le contenu exact des énoncés vient de [01](01-ce-qui-est-prouve.md).
> - **La stratégie** vient de la *remarque* de 4 pages d'Alpöge (`alpo.ge/remark.pdf`, sha256 `3fc97784…`). Alpöge précise lui-même que sa chronologie est un résumé « avec perte » fourni par Claude, et que certaines parties « might make zero sense ». Elle reste donc **une interprétation**.
> - **Le contexte classique** (Weil, Stepanov, formule explicite, relèvements thêta) est standard et vérifiable dans la littérature.
>
> Aucune explication humaine complète de la preuve n'existe à ce jour. La « version papier » dépasserait 250 000 pages.

## 2.1 Le point de départ : comment on prouve RH « dans le monde des corps finis »

Il existe un analogue de RH qui est **démontré depuis longtemps** : celui des courbes sur un corps fini $\mathbb{F}_q$.

- **Weil (1948)** : une courbe lisse $C$ de genre $g$ sur $\mathbb{F}_q$ a un nombre de points qui vérifie
  $$\bigl|\#C(\mathbb{F}_q) - (q+1)\bigr| \le 2g\sqrt q .$$
  Cette inégalité *est* l'hypothèse de Riemann pour la fonction zêta de $C$ : les zéros ont tous une partie réelle égale à $1/2$.
- **Deligne (1974)** a étendu le résultat à toutes les variétés.
- **Stepanov (1969)**, puis **Bombieri** (simplification), en ont donné une preuve *élémentaire* :
  1. On construit un **polynôme auxiliaire** qui s'annule **avec une grande multiplicité** en chaque point de $C(\mathbb{F}_q)$.
  2. Son degré est contrôlé.
  3. Un polynôme de degré $D$ ne peut avoir que $D$ zéros comptés avec multiplicité. Donc *nombre de points × multiplicité ≤ degré*, d'où la majoration.
  4. La multiplicité s'obtient en **dérivant** : il faut des dérivées, plus exactement des dérivées de Hasse, nulles en chaque point.

**L'obstacle historique.** Sur les entiers $\mathbb{Z}$, il n'y a pas de « dérivée » naturelle d'un nombre entier. Alpöge parle de *« differentiating whole numbers »*. C'est l'un des rêves associés au « corps à un élément » $\mathbb{F}_1$ : transposer la preuve de Weil à $\mathbb{Z}$. Personne n'avait trouvé de substitut à la multiplicité.

## 2.2 L'idée centrale annoncée : remplacer la multiplicité par une chaîne de relèvements thêta

Selon la remarque, l'argument **descend de celui de Stepanov**, mais la multiplicité est obtenue autrement :

- Un **relèvement thêta** (*theta lift*, correspondance de Howe) transporte une forme automorphe d'un groupe à un autre. Ici, il s'agit de groupes unitaires définis $U(X_0) \to U(X_1) \to \dots \to U(X_m)$.
- **Chaque relèvement joue le rôle d'un ordre de multiplicité.** Une chaîne de $m$ relèvements donne une « multiplicité » $m$. En paramètres d'Arthur, chaque pas s'écrit $\pi \mapsto \pi \boxplus \mu_j[t]$.
- La phrase qui doit, selon l'auteur, faire « tomber de leur chaise » les mathématiciens : pour une somme de von Mangoldt de longueur $X$, la longueur de chaîne suggérée par Claude est $m \approx \sqrt X$. Dans Stepanov, la multiplicité optimale est aussi de l'ordre de $\sqrt q$, et c'est exactement ce qui donne l'exposant $1/2$.

C'est un argument **« nativement automorphe »** : la dérivation impossible sur $\mathbb{Z}$ est remplacée par une opération qui existe sur les formes automorphes.

## 2.3 Ce qu'on borne : la formule explicite et la positivité de Weil

L'objet arithmétique visé est la somme de von Mangoldt, où $\Lambda(n) = \log p$ si $n = p^k$, et $0$ sinon. L'étape 5 de la remarque vise sous une forme lissée :

$$\sum_{n \le X} \Lambda(n)\Bigl(\frac{X}{n} - 1\Bigr) \;-\; X\log X \;+\; (1+\gamma)\,X .$$

RH équivaut à ce qu'un tel terme d'erreur soit de taille $X^{1/2+o(1)}$. Le lien passe par la **formule explicite** de Riemann–von Mangoldt, où $\rho$ parcourt les zéros non triviaux de $\zeta$ :

$$\psi(x) = \sum_{n\le x}\Lambda(n) = x - \sum_{\rho} \frac{x^\rho}{\rho} - \log 2\pi - \tfrac12\log\bigl(1-x^{-2}\bigr).$$

Si $\operatorname{Re}\rho = 1/2$, alors $|x^\rho| = \sqrt x$, d'où l'erreur en $\sqrt x$.

**Critère de Weil (Guinand–Weil).** RH équivaut à la **positivité** d'une forme quadratique $W(f * \tilde f) \ge 0$, calculée à partir de la formule explicite pour toute fonction test $f$. La remarque procède ainsi :

- elle obtient des inégalités du type $W(\mathbf 1_S) \ge 0$ **via un déterminant**. Un déterminant de Gram est positif, et ce déterminant contient les *périodes* voulues (périodes de Gan–Gross–Prasad, périodes de Bessel) ;
- elle interprète ce déterminant comme « Stepanov avec multiplicité un ». Les relèvements thêta font ensuite monter la multiplicité ;
- à l'étape 6, une positivité du type $W\bigl(\mathbf 1_{(0,1]} + (\sim X^\eta)\,\mathbf 1_{(0,1/X]}\bigr) \ge 0$ donne une région $> 1-\eta$. Il s'agit sans doute d'une région sans zéro, mais l'interprétation exacte est incertaine.

## 2.4 Le « modèle jouet » : une preuve de Weil/Deligne « par le signe seulement »

Avant le cas des entiers, l'auteur dit avoir trouvé une preuve nouvelle des bornes de Weil et de Deligne, qu'il écrit $q^N = M^k + R$. Notre lecture :

1. On compte, avec des sommes de caractères, les solutions de la **quadrique « chemin »** $x_1x_2 + x_2x_3 + \dots + x_{k-1}x_k$ sur $\mathbb{F}_q$.
2. Le membre de gauche a un **signe défini**, venant de la cohomologie du milieu (théorème de Bertini).
3. Le membre de droite est un « mode zéro » $M^k$ plus un reste $R$.
4. On itère Parseval $k$ fois, ce qui donne une annulation en racine carrée.
5. Des signes opposés interdisent aux racines inverses de se compenser, ce qui force la borne.

L'esprit ressemble au *tensor power trick*, mais ce n'est pas une affirmation vérifiée.

La remarque décrit ensuite le passage au cas automorphe :

- la quadrique sur une courbe CM (par exemple $\mathbb{C}/\mathbb{Z}[\omega]$), avec le fibré de Poincaré, donne des séries thêta ;
- la « sixième couverture » de $GL_5$ donne l'automorphie de la mesure $\mu$, via une intégrale de périodes de thêtas.

## 2.5 La chronologie fournie par la remarque (6 oct. → 16 nov. 2026)

| Date | Étape (paraphrase) | Domaine mathématique mobilisé |
|---|---|---|
| 6/10 | Déterminant de Stepanov | méthode de Stepanov, déterminants |
| 9/10 | $D^p \equiv 0$ sur une courbe CM pour $p$ inerte ; divisibilités | courbes à multiplication complexe, dérivation invariante |
| 19/10+ | $q^N = M^k + R$ avec la quadrique chemin ; automorphie via la 6e couverture de $GL_5$ | formes automorphes métaplectiques, thêta |
| 6/10+ | $W(\mathbf 1_S) \ge 0$ via un déterminant = Stepanov multiplicité 1 ; « bootstrap » | positivité de Weil |
| 20/10 | Passage définitif à la somme de von Mangoldt lissée ; « Guinand–Weil avait le signe » | formule explicite |
| 8/10 | $W(\dots) \ge 0 \Rightarrow > 1-\eta$ | région sans zéro |
| 14/10 | Déterminants contenant des périodes GGP | conjectures et théorèmes de Gan–Gross–Prasad |
| 15/11 | **Relèvements thêta itérés** entre groupes unitaires définis, multiplicité $m$ ; « prendre $m$ comme $\sqrt X$ » | correspondance de Howe, paramètres d'Arthur |
| 15/11 | Normes des relèvements, niveau, annulation des termes d'ordre $m$ ; divisibilité via Chowla–Selberg, Weyl, masse de Siegel | périodes CM, formule de masse |
| 6/10 | Tour d'Iwasawa, par analogie avec le principe des tiroirs sur $\mathbb{F}_{q^n}/\mathbb{F}_q$ | théorie d'Iwasawa |
| 15/11 | *Seesaw* : la période du relèvement itéré est une période de Bessel indépendante des caractères de Hecke (Rallis) | dualités seesaw |
| 6/10 | Inégalité de pente de Bost | géométrie d'Arakelov |
| 15/11 | Coût précis de chaque relèvement : on s'arrêterait *a priori* à 2/3 ; il faut une « division » | (cf. le préprint « 2/3 des zéros », arXiv 2608.13637) |
| 15/11 | Structure entière recollée entre caractères de Hecke (« pgcd », moyenne supplémentaire) | |
| 14/10 | Formule des traces relative, Cauchy–Schwarz, séries de Poincaré projetées | formule des traces relative |
| 15/11 | Classes de $H^1$ non tuées par torsion : affaiblissement de la conjecture de Vandiver | cohomologie galoisienne, $K$-théorie de $\mathbb{Z}$ |
| 15/11 | Covolumes, indices de séries thêta, congruences entre relèvements et formes | |
| 19/10 | Choix précis de la tour d'Iwasawa, avec les **ensembles de Behrend** (sans progression arithmétique de longueur 3) | combinatoire additive |
| **16/11** | **GRH** | |

## 2.6 Correspondance avec l'archive Lean

| Dossier | Modules | Thèmes visibles dans les noms (échantillon) |
|---|---:|---|
| `Development/` | 141 928 | `AbelianVarietyTheory`, `AutomorphicArithmetic` (dont `CharacterBoxes`, `SmallClassNumbers`), `AutomorphicSpectrum`, `DiscreteGroups`, `EtaleCohomology`, `ResolutionOfSingularities`, `WeilBound` |
| `Formalism/` | 18 254 | 116 sous-thèmes, dont `BehrendSets`, `ArtinHasse`, `CMTypeGalois`, `CyclotomicNorms`, `GammaFactorNonvanishing` |
| `GroundTheory/` | 8 507 | `AutomorphicForms`, `Brauer`, `FunctionField`, `GlobalFields`, `HeightsAndTheta`, `LocalFields`, `PAdicHodge`, `TateCohomology` |
| `ReciprocityTheory/` | 3 845 | `ClassFieldTheory`, `Chebotarev`, `GeometryOfNumbers`, `GroupCohomology`, `AdeleApproximation` |
| `CompanionTheory/` | 2 027 | `HarishChandraModules`, `RealGroups`, `SpectralGeometry`, `AutomorphicTheory` |
| `PositivityTheory/` | 449 | `AutomorphicForms`, `PublishedTheorems`, `Representations` |
| `Lemmata/` | 167 | lemmes généraux |

Le sommet de la preuve, dans `Supplements/Kernels/MainTheorems.lean` :

```lean
theorem allChi : UpperTheory.EveryCharacter := UpperTheory.FinalTheorems.everyCharacter
theorem rhOfAll : RiemannHypothesis := Formalism.VW.rh_of_every allChi
```

Le cœur est donc un énoncé portant sur **tous les caractères** (`EveryCharacter`). RH pour $\zeta$ s'en déduit comme cas du caractère trivial. On note aussi que `MainTheoremsAll` importe des modules sur les **petits nombres de classes** (`SmallClassNumbers`, `ClassNumberThree`), des cas particuliers traités à part.

On retrouve dans les noms de dossiers les ingrédients de la remarque : variétés abéliennes et CM, borne de Weil, Behrend, Chebotarev, formes automorphes, modules de Harish-Chandra. Cela **suggère** que la remarque décrit bien l'archive. Ce n'est pas une preuve de correspondance.

## 2.7 Résumé en une phrase

> La preuve transpose la méthode de Stepanov, qui démontre l'analogue de RH sur les corps finis grâce à un polynôme auxiliaire à grande multiplicité, au cas des nombres entiers. Elle remplace la multiplicité, impossible à définir sur $\mathbb{Z}$, par une chaîne d'environ $\sqrt X$ relèvements thêta entre groupes unitaires. La positivité recherchée est celle du critère de Weil, obtenue comme positivité de déterminants de périodes.
