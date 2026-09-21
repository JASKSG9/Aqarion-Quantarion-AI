/-
REFUTED: the general claim "R pullback-stable ⟹ EquivGen R pullback-stable"
for an arbitrary relation R.

Counterexample:
  α := Bool
  T := fun _ => false
  R := fun _ _ => False

Then:
  - R (T a) (T b) is always False, so the antecedent is vacuously true.
  - EquivGen R (T false) (T true) = EquivGen R false false = EquivGen.refl false.
  - But EquivGen R false true is uninhabited: R is empty, and the only
    refl witness would require false = true.

So the general statement fails. The correct specialization uses
equivalence relations E, F and the join closure, not arbitrary R.

This file is not imported by the library.
-/
import AqarionLean.Pullback

namespace AqarionLean.Killed

open AqarionLean

/-- The general stability-under-closure claim is FALSE. -/
theorem pullback_stable_equivGen_false :
    ¬ (∀ (α : Type) (T : α → α) (R : Rel α),
        (∀ a b, R (T a) (T b) → R a b) →
        (∀ a b, EquivGen R (T a) (T b) → EquivGen R a b)) := by
  intro h
  -- Instantiate at α := Bool, T := fun _ => false, R := fun _ _ => False
  have h' := h Bool (fun _ => false) (fun _ _ => False)
      (fun _ _ (hR : False) => hR)
  -- h' : ∀ a b, EquivGen (fun _ _ : Bool => False) false false → EquivGen (fun _ _ : Bool => False) a b
  -- Apply to a := false, b := true
  have key := h' false true (EquivGen.refl false)
  -- key : EquivGen (fun _ _ : Bool => False) false true
  -- This is uninhabited
  exact (nomatch key)

end AqarionLean.Killed
