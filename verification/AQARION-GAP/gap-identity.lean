/-
Copyright (c) 2026 AQARION Research.
-/
import AQARIONGap.Defs
import AQARIONGap.Restriction
import AQARIONGap.Defect

namespace AQARIONGap

/-!
# Main theorem: gap identity

Proof structured exactly as the paper case analysis on `c_S ∈ {1,2,3}`.
-/

/-- Predicate: M is SEP-pure and neither P nor Q is SEP-pure. -/
def exceptionalGap {n : ℕ} (hn : n ≥ 3)
    (P Q : Finpartition (Set.univ : Set (Fin n))) : Prop :=
  IsSepPure hn (P ⊓ₚ Q) ∧ ¬ IsSepPure hn P ∧ ¬ IsSepPure hn Q

/-- **Main Theorem (AQ-GAP-001).**
    For all partitions P, Q of Fin n (n ≥ 3) under the fixed 3-cycle action,
    the gap equals 2 on the exceptional purity locus and 0 otherwise. -/
theorem gap_identity {n : ℕ} (hn : n ≥ 3)
    (P Q : Finpartition (Set.univ : Set (Fin n))) :
    gapDiff hn P Q = if exceptionalGap hn P Q then (2 : ℤ) else 0 := by
  -- Case analysis on cS
  have hCS : cS hn P Q = 1 ∨ cS hn P Q = 2 ∨ cS hn P Q = 3 := by
    -- cS is the number of blocks of a partition of a 3-set, hence ∈ {1,2,3}
    sorry
  rcases hCS with h1 | h2 | h3
  · -- Case cS = 1
    -- Forces τ(U) = ALL3, dT(U) = 0, cG = 1, cS - cG = 0
    -- gapDiff reduces to dT(P) + dT(Q) - dT(M)
    -- Finite check on local types of P, Q, M yields the claim
    sorry
  · -- Case cS = 2
    -- Cancellation: dT(U) - cG = -1
    -- Reduced formula: gapDiff = dT(P) + dT(Q) - dT(M) - 1
    -- Local type pairs: (PAIR,PAIR) or (PAIR,SEP) up to labelling
    -- Subcases match the exceptional predicate
    sorry
  · -- Case cS = 3
    -- Both τ(P), τ(Q) discrete
    -- Subcase one input SEP-pure ⇒ meet SEP-pure ⇒ gap = 0
    -- Subcase both SEP-ext:
    --   dT(P) = dT(Q) = 2, and dT(U) = cG - 1 in all subcases
    --   ⇒ gapDiff = 2 - dT(M) which is 2 iff M SEP-pure
    sorry

/-- Corollary: the gap is always in {0, 2}. -/
theorem gapDiff_mem {n : ℕ} (hn : n ≥ 3)
    (P Q : Finpartition (Set.univ : Set (Fin n))) :
    gapDiff hn P Q = 0 ∨ gapDiff hn P Q = 2 := by
  rw [gap_identity hn P Q]
  split_ifs <;> simp

/-- Cancellation lemma used in the cS = 2 case. -/
theorem cancellation_cS_two {n : ℕ} (hn : n ≥ 3)
    (P Q : Finpartition (Set.univ : Set (Fin n)))
    (hc : cS hn P Q = 2) :
    (dT hn (P ⊔ₚ Q) : ℤ) - (cG hn P Q : ℤ) = -1 := by
  -- τ(U) is PAIR or ALL3; in both subcases dT(U) = cG - 1
  sorry

/-- Inheritance of extension: if one input is SEP-ext and τ(U) stays discrete,
    then U is SEP-ext. -/
theorem inherit_sep_ext {n : ℕ} (hn : n ≥ 3)
    (P Q : Finpartition (Set.univ : Set (Fin n)))
    (hP : IsSepExt hn P)
    (hU : (restrict hn (P ⊔ₚ Q)).parts.card = 3) :
    IsSepExt hn (P ⊔ₚ Q) := by
  sorry

end AQARIONGap
