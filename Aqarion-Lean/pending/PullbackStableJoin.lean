/-
PENDING: join preservation under pullback-stability (unconditional).
Status: statement formulated; proof OPEN.

Obstruction: the trans constructor of EquivGen produces an intermediate
node z that need not lie in im(T). Without surjectivity of T, we cannot
choose a preimage c with T c = z, so the induction does not close.

Do not import from AqarionLean.lean.
-/
import AqarionLean.Pullback

namespace AqarionLean.Pending

open AqarionLean

/-- Join of two equivalences via equivalence closure of union. -/
def joinRel {α : Type} (E F : EquivRel α) : Rel α :=
  EquivGen (fun a b => Or (E.r a b) (F.r a b))

/-- OPEN: pullback-stable equivalences are closed under join. -/
theorem pullback_stable_join {α : Type}
    (T : α → α) (E F : EquivRel α)
    (_hE : PullbackStable T E) (_hF : PullbackStable T F) :
    ∀ a b, joinRel E F (T a) (T b) → joinRel E F a b := by
  sorry

end AqarionLean.Pending
