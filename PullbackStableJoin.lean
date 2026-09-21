import AqarionLean.Pullback

namespace AqarionLean.Pending

open AqarionLean

/-- Join of two equivalences via equivalence closure of union. -/
def joinRel {α : Type} (E F : EquivRel α) : Rel α :=
  EquivGen (fun a b => Or (E.r a b) (F.r a b))

/-- Pullback-stable equivalences are closed under join. -/
theorem pullback_stable_join {α : Type}
    (T : α → α) (E F : EquivRel α)
    (_hE : PullbackStable T E) (_hF : PullbackStable T F) :
    ∀ a b, joinRel E F (T a) (T b) → joinRel E F a b := by
  intro a b h
  induction h with
  | of hab =>
      cases hab with
      | inl hEab =>
          exact EquivGen.of (_hE _ _ hEab)
      | inr hFab =>
          exact EquivGen.of (_hF _ _ hFab)
  | refl c =>
      exact EquivGen.refl c
  | symm _ ih =>
      exact EquivGen.symm ih
  | trans _ _ ih₁ ih₂ =>
      exact EquivGen.trans ih₁ ih₂

end AqarionLean.Pending
