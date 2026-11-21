import Mathlib

/-!
Exemples de développement « sous hypothèse RH / GRH » (ne dépend que de Mathlib).
On branche ensuite la preuve d'Alpöge via `riemannHypothesis` et `LFunction_eq_zero_re`
(fichier final `import Main`), voir comprendre/05-utiliser-la-preuve-en-lean.md.
-/

open Complex

/-- Copie de la définition de `Statements.lean` (archive d'Alpöge), qui n'importe que Mathlib. -/
def DirichletLZerosOnLine' : Prop :=
  ∀ (N : ℕ) [NeZero N] (χ : DirichletCharacter ℂ N) (s : ℂ),
    0 < s.re → s.re < 1 → DirichletCharacter.LFunction χ s = 0 → s.re = 1 / 2

/-- Sous RH : aucun zéro de ζ dans la bande 1/2 < Re s (hors s = 1). -/
theorem pas_de_zero_droite (hRH : RiemannHypothesis) (s : ℂ)
    (h₁ : 1 / 2 < s.re) (hz : riemannZeta s = 0) (hs : s ≠ 1) : False := by
  have htriv : ¬∃ n : ℕ, s = -2 * ((n : ℂ) + 1) := by
    rintro ⟨n, rfl⟩
    have : (-2 * ((n : ℂ) + 1)).re = -2 * ((n : ℝ) + 1) := by simp
    rw [this] at h₁
    have : (0 : ℝ) ≤ n := Nat.cast_nonneg n
    linarith
  have := hRH s hz htriv hs
  linarith

/-- Sous RH : un zéro non trivial ρ a son « symétrique » 1 - ρ̄ égal à lui-même. -/
theorem zero_egal_symetrique (hRH : RiemannHypothesis) (s : ℂ) (hz : riemannZeta s = 0)
    (htriv : ¬∃ n : ℕ, s = -2 * ((n : ℂ) + 1)) (hs : s ≠ 1) :
    1 - (starRingEnd ℂ) s = s := by
  have h := hRH s hz htriv hs
  apply Complex.ext
  · simp [h]; norm_num
  · simp

/-- Sous GRH (Dirichlet) : aucun zéro de L(χ, s) avec 1/2 < Re s < 1. -/
theorem pas_de_zero_L (hGRH : DirichletLZerosOnLine') (N : ℕ) [NeZero N]
    (χ : DirichletCharacter ℂ N) (s : ℂ) (h₁ : 1 / 2 < s.re) (h₂ : s.re < 1) :
    DirichletCharacter.LFunction χ s ≠ 0 := by
  intro hz
  have := hGRH N χ s (by linarith) h₂ hz
  linarith

#print axioms pas_de_zero_droite
#print axioms zero_egal_symetrique
#print axioms pas_de_zero_L
