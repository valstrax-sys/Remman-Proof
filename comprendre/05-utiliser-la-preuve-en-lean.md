# 5. Utiliser la preuve dans Lean

## 5.1 Ce que l'archive exporte

Une fois `Main` compilé, ces cinq constantes sont disponibles. Leurs énoncés sont donnés en [01](01-ce-qui-est-prouve.md).

```lean
riemannHypothesis : RiemannHypothesis                       -- définition de Mathlib
riemannZeta_eq_zero_re : RiemannZetaZerosOnLine
LFunction_ne_zero_of_half_lt_re : DirichletLNonvanishingRightOfHalf
LFunction_eq_zero_re : DirichletLZerosOnLine
LFunction_eq_zero_re_of_isPrimitive : PrimitiveDirichletLZerosOnLine
```

Il faut exactement **Lean 4.33.1** et **Mathlib `0df444a3`** : un `.olean` n'est lisible que par la version de Lean qui l'a produit. La page du MIT signale que les contrôles en 4.36.0 passent par un export du terme de preuve, pas par les `.olean`.

## 5.2 Le problème pratique : compiler `Main` coûte cher

`import Main` oblige à compiler les 175 187 modules :

| Machine | Temps |
|---|---|
| Ryzen 7 5800X, 11 threads (mesure de cette réplique) | environ 2 400 à 3 200 modules/h, soit **plus de 2 jours** |
| Ryzen 7 4800HS (portable) | environ 1 500 modules/h |
| Machines cloud du MIT | quelques heures |

Il faut aussi de la place : environ 30 Go de `.olean` (estimation), plus Mathlib.

## 5.3 La bonne méthode : développer « sous hypothèse », brancher la preuve à la fin

On écrit tout son développement en prenant RH comme **hypothèse explicite**. Il ne dépend alors que de Mathlib et compile en secondes. La preuve d'Alpöge n'est branchée que dans **un seul fichier final**. C'est exactement ce qu'a fait le projet `kimihiro64/Robin1984`, combiné à l'archive sur la page du MIT.

```lean
-- MonProjet/Conditionnel.lean : ne dépend que de Mathlib
import Mathlib

open Complex

/-- Exemple : sous RH, aucun zéro non trivial dans la bande 1/2 < Re s < 1. -/
theorem pas_de_zero_droite (hRH : RiemannHypothesis) (s : ℂ)
    (h₁ : 1 / 2 < s.re) (hz : riemannZeta s = 0) (hs : s ≠ 1) :
    False := by
  have htriv : ¬∃ n : ℕ, s = -2 * ((n : ℂ) + 1) := by
    rintro ⟨n, rfl⟩
    have : (-2 * ((n : ℂ) + 1)).re = -2 * ((n : ℝ) + 1) := by simp
    rw [this] at h₁
    have : (0 : ℝ) ≤ n := Nat.cast_nonneg n
    linarith
  have := hRH s hz htriv hs
  linarith
```

```lean
-- MonProjet/Inconditionnel.lean : le seul fichier qui importe l'archive
import Main
import MonProjet.Conditionnel

theorem pas_de_zero_droite' (s : ℂ) (h₁ : 1 / 2 < s.re) (hz : riemannZeta s = 0) (hs : s ≠ 1) :
    False :=
  pas_de_zero_droite riemannHypothesis s h₁ hz hs

#print axioms pas_de_zero_droite'   -- attendu : propext, Classical.choice, Quot.sound
```

Avantages :

- le développement se vérifie en quelques secondes ;
- il reste valable avec **n'importe quelle** future preuve de RH, par exemple une version simplifiée ;
- un relecteur voit exactement où la preuve d'Alpöge intervient : à une seule ligne.

Pour GRH, on prend de la même manière une hypothèse `(hGRH : DirichletLZerosOnLine)`. On recopie alors la définition depuis `Statements.lean`, qui n'importe que Mathlib.

Le premier fichier (`pas_de_zero_droite`) a été compilé contre Mathlib `0df444a3` dans notre sandbox (voir 5.5). Le second exige que `Main` soit compilé en entier : il n'a **pas** été compilé ici.

## 5.4 Mise en place d'un projet

```toml
# lakefile.toml de MonProjet (esquisse)
name = "MonProjet"

[[require]]
name = "mathlib"
git = "https://github.com/leanprover-community/mathlib4"
rev = "0df444a360eaa60ab8c11dca51a86af692955474"

# Seulement pour le fichier final : l'archive d'Alpöge comme dépendance locale
[[require]]
name = "grh"          # nom du paquet défini dans le lakefile de l'archive
path = "../lean"
```

Le nom exact du paquet de l'archive est celui qui est déclaré dans son `lakefile`. On vérifie aussi que `lean-toolchain` contient `leanprover/lean4:v4.33.1`.

## 5.5 Vérification faite ici

Voir [`code/Conditionnel.lean`](code/Conditionnel.lean) et le journal [`code/Conditionnel.log`](code/Conditionnel.log). Le fichier a été compilé avec `lake env lean` dans la sandbox `rhbuild` : Lean 4.33.1, Mathlib `0df444a3`. Le journal est rempli quand la compilation a eu lieu.
