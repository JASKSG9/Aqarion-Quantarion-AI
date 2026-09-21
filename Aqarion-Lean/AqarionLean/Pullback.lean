/-
AQARION — Pullback closure and equivalence distribution.
Proven in this file: distribution of equivalence closure over pullback.
Open: join preservation (see pending/). Refuted: general closure stability (see killed/).
-/

namespace AqarionLean

/-- Relations on a type. -/
def Rel (α : Type) := α → α → Prop

/-- A bundled equivalence relation. -/
structure EquivRel (α : Type) where
  r     : Rel α
  refl  : ∀ a, r a a
  symm  : ∀ a b, r a b → r b a
  trans : ∀ a b c, r a b → r b c → r a c

/-- Pullback-stability: T a ~ T b implies a ~ b. -/
def PullbackStable {α : Type} (T : α → α) (E : EquivRel α) : Prop :=
  ∀ a b, E.r (T a) (T b) → E.r a b

/-- Definitional restatement. Interface lemma, not a result. -/
theorem pullback_stable_iff {α : Type} (T : α → α) (E : EquivRel α) :
    Iff (PullbackStable T E)
        (∀ a b, E.r (T a) (T b) → E.r a b) :=
  Iff.rfl

/-- Equivalence closure of a relation. -/
inductive EquivGen {α : Type} (r : Rel α) : Rel α where
  | of    : ∀ {a b}, r a b → EquivGen r a b
  | refl  : ∀ a, EquivGen r a a
  | symm  : ∀ {a b}, EquivGen r a b → EquivGen r b a
  | trans : ∀ {a b c}, EquivGen r a b → EquivGen r b c → EquivGen r a c

/-- Pullback of a relation along T. -/
def pullbackRel {α : Type} (T : α → α) (r : Rel α) : Rel α :=
  fun a b => r (T a) (T b)

/-- Pullback and equivalence closure commute in one direction.
    EquivGen ∘ pullback ⊆ pullback ∘ EquivGen. -/
theorem pullback_equivGen_subset {α : Type}
    (T : α → α) (r : Rel α) :
    ∀ a b, EquivGen (pullbackRel T r) a b → EquivGen r (T a) (T b) := by
  intro a b h
  induction h with
  | of hab => exact EquivGen.of hab
  | refl c => exact EquivGen.refl (T c)
  | symm _ ih => exact EquivGen.symm ih
  | trans _ _ ih1 ih2 => exact EquivGen.trans ih1 ih2

end AqarionLean
