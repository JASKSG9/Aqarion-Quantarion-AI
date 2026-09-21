# AqarionLean

Lean 4 formalization of AQARION pullback closure results.

## Status

**Kernel-accepted, zero axioms (AqarionLean/Pullback.lean):**

- `AqarionLean.pullback_stable_iff` — definitional restatement of pullback-stability. Interface lemma.
- `AqarionLean.pullback_equivGen_subset` — pullback commutes with equivalence closure in one direction.

**Open (pending/):**

- `pullback_stable_join` — pullback-stable equivalences are closed under join. Proof OPEN. `trans` case requires an intermediate preimage that does not exist without surjectivity.
- `pullback_stable_join_surjective` — same theorem under `Function.Surjective T`. Proof sketched; not yet compiled.

**Refuted (killed/):**

- `pullback_stable_equivGen` for arbitrary relation `R` — FALSE.
  Counterexample: `T := fun _ => false` on `Bool`, `R := fun _ _ => False`.

## Build

    lake build

## Verification

Two independent gates:

    scripts/verify.sh          # fails if sorry/admit appears in public library
    scripts/verify_axioms.sh   # fails if any public theorem depends on axioms

Both are run by:

    scripts/verify_all.sh

`verify.sh` was sanity-checked against a deliberately broken library and exits
1 when it finds `sorry`. `verify_axioms.sh` was sanity-checked against a
deliberately introduced `error:` and exits 1.

## Environment

- Lean 4.14.0 (pinned in `lean-toolchain`)
- No Mathlib dependency
- Verified on aarch64-linux-gnu via Termux + proot-distro Ubuntu

## Verification discipline

Every gate in `scripts/` must be sanity-checked by introducing a deliberate
failure, confirming the gate exits non-zero, and then restoring.

**A gate that has not been shown to fail is not a gate.**

## Governance

C3 OPEN · C4 BLOCKED · Promotion FALSE

No claim in this repository is a theorem unless Lean reports zero `sorry` and
`#print axioms` lists no axioms. A clean `lake build` is necessary but not
sufficient.

## License

Apache-2.0
