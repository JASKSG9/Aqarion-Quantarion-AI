/-
Copyright (c) 2026 AQARION Research.
-/
import AQARIONGap.Defs
import AQARIONGap.Restriction

namespace AQARIONGap

/-!
# Orbit-join defect d_T
-/

/-- Apply the 3-cycle to a partition of `Fin n` by acting on the support labels
    and fixing the rest. (Definitional sketch.) -/
noncomputable def mapPartition {n : ℕ} (hn : n ≥ 3)
    (f : Fin 3 → Fin 3)
    (P : Finpartition (Set.univ : Set (Fin n))) :
    Finpartition (Set.univ : Set (Fin n)) :=
  sorry

/-- Orbit join J_T(P) = P ∨ T(P) ∨ T²(P). -/
noncomputable def orbitJoin {n : ℕ} (hn : n ≥ 3)
    (P : Finpartition (Set.univ : Set (Fin n))) :
    Finpartition (Set.univ : Set (Fin n)) :=
  let TP := mapPartition hn T3 P
  let T2P := mapPartition hn T3 TP
  P ⊔ₚ TP ⊔ₚ T2P

/-- Defect d_T(P) = |P| - |J_T(P)|. -/
noncomputable def dT {n : ℕ} (hn : n ≥ 3)
    (P : Finpartition (Set.univ : Set (Fin n))) : ℕ :=
  P.parts.card - (orbitJoin hn P).parts.card

/-- Four-way evaluation of d_T (the key lemma). -/
theorem dT_four_way {n : ℕ} (hn : n ≥ 3)
    (P : Finpartition (Set.univ : Set (Fin n))) :
    dT hn P =
      match classify3 (restrict hn P) with
      | RestrType.ALL3 => 0
      | RestrType.PAIR => 1
      | RestrType.SEP  => if IsSepPure hn P then 0 else 2 := by
  -- Proof by direct orbit computation on the support, as in AQ-GAP-001 §3.
  -- Cases:
  -- ALL3: unique block on S is T-invariant → no merge → dT = 0
  -- PAIR: one additional identification under the orbit → dT = 1
  -- SEP-pure: singletons merely permuted → J_T(P) = P → dT = 0
  -- SEP-ext: external attachment E chains the three local blocks → drop 2
  sorry

/-- Δ_d(P,Q) = d_T(P) + d_T(Q) - d_T(M) - d_T(U). -/
noncomputable def deltaD {n : ℕ} (hn : n ≥ 3)
    (P Q : Finpartition (Set.univ : Set (Fin n))) : ℤ :=
  (dT hn P : ℤ) + (dT hn Q : ℤ)
    - (dT hn (P ⊓ₚ Q) : ℤ) - (dT hn (P ⊔ₚ Q) : ℤ)

/-- The gap quantity. -/
noncomputable def gapDiff {n : ℕ} (hn : n ≥ 3)
    (P Q : Finpartition (Set.univ : Set (Fin n))) : ℤ :=
  deltaD hn P Q - ((cS hn P Q : ℤ) - (cG hn P Q : ℤ))

end AQARIONGap
