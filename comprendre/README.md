# Comprendre et utiliser la preuve d'Alpöge (RH + GRH de Dirichlet)

Dossier de travail ouvert le 21/11/2026. On cherche à comprendre ce qui est prouvé, comment, ce que cela permet (formules, applications, algorithmes) et comment l'expliquer.

| Fichier | Contenu |
|---|---|
| [01-ce-qui-est-prouve.md](01-ce-qui-est-prouve.md) | Les 5 théorèmes de `Main.lean`, leur traduction, leur portée (ce qui est couvert ou non), l'état de la certification |
| [02-strategie-de-la-preuve.md](02-strategie-de-la-preuve.md) | Contexte (Weil, Stepanov, formule explicite, critère de Weil), idée centrale (relèvements thêta ≈ multiplicité, $m \approx \sqrt X$), chronologie de l'auteur, carte de l'archive |
| [03-consequences-et-formules.md](03-consequences-et-formules.md) | Ce qui devient inconditionnel : termes d'erreur sur les premiers, Robin et Lagarias, progressions arithmétiques, groupes de classes ; ce qui **ne** découle **pas** de la preuve |
| [04-algorithmes.md](04-algorithmes.md) | Algorithmes désormais garantis : Miller déterministe, racines modulaires, groupes de classes quadratiques… ; impact réel sur la cryptographie |
| [05-utiliser-la-preuve-en-lean.md](05-utiliser-la-preuve-en-lean.md) | Utiliser les théorèmes en Lean : méthode « sous hypothèse, puis branchement final », coût de compilation |
| [06-expliquer.md](06-expliquer.md) | Explications à quatre niveaux (grand public → chercheur), erreurs fréquentes |
| [code/rh_algos.py](code/rh_algos.py) | Implémentations et contrôles numériques en Python pur (`--test`) ; sortie dans `code/demo-output.txt` |
| [code/Conditionnel.lean](code/Conditionnel.lean) | Exemples Lean « sous RH » et « sous GRH » ; compilation et journal décrits en 05 |

## Sources primaires

- `Statements.lean`, `Main.lean`, `Supplements/Kernels/*.lean` de l'archive : sha256 de `lean.tar.gz` = `9631b4f0…49c7fc`.
- Remarque de l'auteur : `https://alpo.ge/remark.pdf`, 4 pages, sha256 `3fc97784b71ddd44ff8aa0a177e99622a1c61b13cfa843a0989ee4a7a0cfeb8d`, lue le 21/11/2026.
- Page de vérification du MIT (A. Sutherland) : `https://math.mit.edu/~drew/grh/`.
- Déclaration de certification Lean/Mathlib : `https://leanprover-community.github.io/blog/posts/riemann-hypothesis/`.

## Règle de rédaction

Chaque affirmation relève de l'une de ces catégories :

- **certifiée** : énoncés Lean ;
- **classique** : théorèmes publiés, avec auteur et année ;
- **interprétation** : lecture de la remarque d'Alpöge, signalée comme telle.

Personne, à ce jour, n'a d'explication humaine complète de la preuve.
