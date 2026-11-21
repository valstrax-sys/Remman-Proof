# Synthèse — vérification de l'archive Lean d'Alpöge (RH/GRH)

Généré automatiquement (`scripts/summary.py`). Détails par chunk : `reports/P*.md`, état : `state/STATE.md`.

## Résultat

- Chunks (packets de ≤ 64 modules) **vérifiés** : **281** — principale 255 (5.7 h de build), portable 26 (0.9 h).
- Chunks en échec / non concluants : **0** 
- Modules **cibles** distincts vérifiés (compilés exit 0 avec ligne `Built`, + audit d'axiomes) : **17924** / 175 187.
- Modules distincts compilés au total (cibles + imports reconstruits) : **17924**.
- Profondeurs couvertes (cibles) : {0: 5927, 1: 4979, 2: 4138, 3: 2880}
- Axiomes : pour **chaque** chunk vérifié, l'union des axiomes atteints depuis toutes les déclarations des modules cibles est exactement `propext`, `Classical.choice`, `Quot.sound`. Aucun `sorryAx`, `Lean.ofReduceBool`/`ofReduceNat` (native_decide), `Lean.trustCompiler`, aucun `axiom` déclaré, aucun `@[extern]` / `@[implemented_by]` dans ces modules.
- Scan statique de toute l'archive (175 187 fichiers) : aucune occurrence de `native_decide`, `implemented_by`, `@[extern`, `axiom `, `unsafe `, `sorry`/`admit` ; seuls `run_cmd` : `BuildAid/D1..D5.lean` (ajout de noms à la deny-list de `LibrarySuggestions`, sans effet logique).

## Ce que cela établit — et ce que cela n'établit pas

- Établi : ces 17924 modules de l'archive épinglée (hash `9631b4f0…`, Lean 4.33.1, Mathlib `0df444a3`) compilent sans erreur avec la toolchain officielle vérifiée par hash, et leurs déclarations ne dépendent que des trois axiomes standard.
- **Non établi** : le théorème final (`Main.riemannHypothesis`) — il exige les ~175 000 modules ; pas de rejeu `leanchecker --fresh` (noyau frais) ni de vérification des énoncés. Le verdict global appartient à l'audit final (README du projet distribué, page MIT).
- Les modules dépendent du cache Mathlib officiel téléchargé (`lake exe cache get`), non recompilé.

## Statut de ces modules dans l'instantané du projet distribué (tracker `0ca43af`)

Cibles : {'open': 2350, 'volunteer-build-reviewed': 9660, 'build-observed': 2142, 'wave-reused': 3601, 'assigned': 110, 'pilot-reused': 61}
Toutes compilées : {'volunteer-build-reviewed': 9660, 'wave-reused': 3601, 'open': 2350, 'build-observed': 2142, 'assigned': 110, 'pilot-reused': 61}

Les modules `open` étaient sans preuve enregistrée dans l'instantané : ce sont des contributions nouvelles potentielles ; les autres sont des **réplications indépendantes**. Aucun n'a été soumis (pas de claim possible : voir bloquants dans `state/STATE.md`).
