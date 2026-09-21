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

end AqarionLean.Pendingtheorem pullback_stable_join {α : Type}
    (T : α → α) (E F : EquivRel α)
    (hE : PullbackStable T E) (hF : PullbackStable T F) :
    ∀ a b, joinRel E F (T a) (T b) → joinRel E F a b := by
  -- Strengthen: for any x y, EquivGen r x y → ∀ a b, T a = x → T b = y → EquivGen r a b
  let r : Rel α := fun x y => E.r x y ∨ F.r x y
  suffices ∀ x y, EquivGen r x y →
      ∀ a b, T a = x → T b = y → EquivGen r a b by
    intro a b h
    exact this (T a) (T b) h a b rfl rfl
  intro x y h
  induction h with
  | of hab =>
      intro a b ha hb
      subst ha; subst hb
      cases hab with
      | inl hEab => exact EquivGen.of (Or.inl (hE a b hEab))
      | inr hFab => exact EquivGen.of (Or.inr (hF a b hFab))
  | refl c =>
      intro a b ha hb
      -- T a = c and T b = c so T a = T b
      have hEq : T a = T b := ha.trans hb.symm
      have hET : E.r (T a) (T b) := hEq ▸ E.refl (T a)
      exact EquivGen.of (Or.inl (hE a b hET))
  | symm _ ih =>
      intro a b ha hb
      -- h : EquivGen r x y, ih : ∀ a b, T a = x → T b = y → EquivGen r a b
      -- After symm, endpoints are y, x. Given T a = y, T b = x.
      -- We want EquivGen r a b. Use ih with a' = b, b' = a: ih b a hb ha : EquivGen r b a
      exact EquivGen.symm (ih b a hb ha)
  | trans _ _ ih1 ih2 =>
      intro a b ha hb
      -- h1 : EquivGen r x z, h2 : EquivGen r z y (for some z)
      -- ih1 : ∀ a b, T a = x → T b = z → EquivGen r a b
      -- ih2 : ∀ a b, T a = z → T b = y → EquivGen r a b
      -- Need to find a middle point c with T c = z
      -- We don't have surjectivity, so this case may fail
      sorry
