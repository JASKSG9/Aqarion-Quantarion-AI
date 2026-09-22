theorem pullback_equivGen_subset {α : Type}
    (T : α → α) (r : Rel α) :
    ∀ a b, EquivGen (pullbackRel T r) a b → EquivGen r (T a) (T b) := by
  intro a b h
  induction h with
  | of hab => exact EquivGen.of hab
  | refl c => exact EquivGen.refl (T c)
  | symm _ ih => exact EquivGen.symm ih
  | trans _ _ ih1 ih2 => exact EquivGen.trans ih1 ih2

---

theorem pullback_stable_join {α : Type}
    (T : α → α) (E F : EquivRel α)
    (hE : PullbackStable T E)
    (hF : PullbackStable T F) :
    ∀ a b, joinRel E F (T a) (T b) → joinRel E F a b := by
  intro a b h
  induction h with
  | of hab =>
      exact EquivGen.of (Or.elim hab
        (fun h => Or.inl (hE _ _ h))
        (fun h => Or.inr (hF _ _ h)))
  | refl c =>
      exact EquivGen.refl c
  | symm _ ih =>
      exact EquivGen.symm ih
  | trans _ _ ih1 ih2 =>
      exact EquivGen.trans ih1 ih2
