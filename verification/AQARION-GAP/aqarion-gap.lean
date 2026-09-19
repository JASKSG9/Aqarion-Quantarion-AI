import AQARIONGap.Defs
import AQARIONGap.Restriction
import AQARIONGap.Defect
import AQARIONGap.GapIdentity

/-!
# AQARION Gap Identity (AQ-GAP-001)

Formalization of the gap identity for the 3-cycle support action.

## Statement

Under the fixed action `T = (0 1 2)` on `S = {0,1,2}`, for all partitions `P, Q`
of a finite set `X` with `|X| ≥ 3`,

```
Δ_d(P,Q) - (c_S - c_G) =
  2  if M is SEP-pure and neither P nor Q is SEP-pure
  0  otherwise
```

where `M = P ∧ Q`, `U = P ∨ Q`, `c_S = |τ(P) ∨ τ(Q)|`, `c_G = |τ(U)|`,
and `Δ_d = d_T(P) + d_T(Q) - d_T(M) - d_T(U)`.

## Status

- Definitions: complete
- Four-way `d_T` lemma: stated; proof by cases on restriction type
- Main theorem: stated; proof structured by `c_S ∈ {1,2,3}`
- Lean kernel receipt / full discharge of all `sorry`: OPEN
- C4 / publication / promotion: BLOCKED

Evidence class: [P] algebraic (paper proof) · [FV] pending full Lean build
-/
