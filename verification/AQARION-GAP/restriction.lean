/-
Copyright (c) 2026 AQARION Research.
-/
import AQARIONGap.Defs
import Mathlib.Data.Set.Basic

namespace AQARIONGap

/-!
# Restriction of partitions to the support S = {0,1,2}
-/

/-- Restrict a partition of `Fin n` (n ≥ 3) to the first three coordinates.
    Returns a partition of `Fin 3`. -/
noncomputable def restrict {n : ℕ} (hn : n ≥ 3)
    (P : Finpartition (Set.univ : Set (Fin n))) :
    Finpartition (Set.univ : Set (Fin 3)) :=
  -- Implementation sketch: take intersections of blocks with the embedded S
  -- and reindex. Full construction left as a definitional obligation.
  sorry

/-- Meet of partitions (common refinement). Mathlib `Finpartition` provides this
    via the lattice structure when available; we axiomatize the needed facts. -/
axiom meet_parts {X : Type*} [DecidableEq X] [Fintype X]
    (P Q : Finpartition (Set.univ : Set X)) :
    Finpartition (Set.univ : Set X)

/-- Join of partitions (transitive closure of union of equivalences). -/
axiom join_parts {X : Type*} [DecidableEq X] [Fintype X]
    (P Q : Finpartition (Set.univ : Set X)) :
    Finpartition (Set.univ : Set X)

/-- Notation. -/
scoped infix:70 " ⊓ₚ " => meet_parts
scoped infix:65 " ⊔ₚ " => join_parts

/-- Restriction preserves meet. -/
theorem restrict_meet {n : ℕ} (hn : n ≥ 3)
    (P Q : Finpartition (Set.univ : Set (Fin n))) :
    restrict hn (P ⊓ₚ Q) = restrict hn P ⊓ₚ restrict hn Q := by
  sorry

/-- Restriction of join is coarser than join of restrictions (external bridges). -/
theorem restrict_join_le {n : ℕ} (hn : n ≥ 3)
    (P Q : Finpartition (Set.univ : Set (Fin n))) :
    -- rank of join of restrictions ≥ rank of restriction of join
    -- (fewer or equal blocks after possible external bridging)
    (restrict hn (P ⊔ₚ Q)).parts.card ≤
      (restrict hn P ⊔ₚ restrict hn Q).parts.card := by
  sorry

/-- Local block counts. -/
def cS {n : ℕ} (hn : n ≥ 3)
    (P Q : Finpartition (Set.univ : Set (Fin n))) : ℕ :=
  (restrict hn P ⊔ₚ restrict hn Q).parts.card

def cG {n : ℕ} (hn : n ≥ 3)
    (P Q : Finpartition (Set.univ : Set (Fin n))) : ℕ :=
  (restrict hn (P ⊔ₚ Q)).parts.card

/-- Always cS ≥ cG. -/
theorem cS_ge_cG {n : ℕ} (hn : n ≥ 3)
    (P Q : Finpartition (Set.univ : Set (Fin n))) :
    cS hn P Q ≥ cG hn P Q := by
  simpa [cS, cG] using restrict_join_le hn P Q

end AQARIONGap
