/-
PENDING: join preservation under pullback-stability, with T surjective.
Status: statement formulated; proof sketched; Lean syntax not yet compiled.

With Surjective T, the trans case of the induction closes:
given intermediate node z, choose c with T c = z via surjectivity.

The remaining work is the exact Lean 4 induction syntax over EquivGen
with endpoint hypotheses carried through.
-/
import AqarionLean.Pullback

namespace AqarionLean.Pending

open AqarionLean

def joinRel {α : Type} (E F : EquivRel α) : Rel α :=
  EquivGen (fun a b => Or (E.r a b) (F.r a b))

/-- OPEN: with T surjective, pullback-stable equivalences are closed under join. -/
theorem pullback_stable_join_surjective {α : Type}
    (T : α → α) (E F : EquivRel α)
    (_hE : PullbackStable T E) (_hF : PullbackStable T F)
    (_hT : Function.Surjective T) :
    ∀ a b, joinRel E F (T a) (T b) → joinRel E F a b := by
  sorry

end AqarionLean.Pending
