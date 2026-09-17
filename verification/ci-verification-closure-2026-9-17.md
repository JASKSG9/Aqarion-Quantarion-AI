# AQARION CI Verification Closure

Date: 2026-09-17

## Scope

This receipt records the mathematical verification evidence and
the CI infrastructure state.

It does not promote any result to formal theorem status.

---

## Layer 1 — Operator Mutation

Canonical convention:

    K[i,T(i)] = 1

Deliberate mutant:

    K[T(i),i] = 1

Independent rerun:

    canonical: 5000/5000 PASS
    mutant:       0/5000 PASS

Mutation detected:

    TRUE

Disposition:

    PASS

Meaning:

    The test detects the known operator-index mutation.

It does not establish the underlying mathematical theorem.

---

## Layer 2 — Canonical Receipt

### R1 — BRT

    rank(D) = m - c_bip

Independent rerun:

    200/200 PASS

Disposition:

    PASS

### R2 — AQ-001

    D = 0 <-> transition congruence

Independent rerun:

    0 violations

Disposition:

    PASS

### R3 — Depth quotient

Independent rerun:

    rank(D) = 0

Disposition:

    PASS

### R4 — Frobenius formula

    ||D||_F² = 2mr(k-r)/k²

Independent rerun:

    0/90 failures

Disposition:

    PASS

---

## Layer 3

Support-spectrum:

    exploratory workload

T10:

    exploratory workload

Disposition:

    NOT A FROZEN MATHEMATICAL RECEIPT

No theorem promotion.

---

## Layer 4 — Reproduction Contract

ARO-1 adversarial cases:

    M1 false independence
    M2 rerun
    M3 independent agreement
    M4 independent disagreement
    M5 input drift
    M6 stale receipt
    M7 equal output does not imply independence
    M8 incomplete provenance
    M9 same output is not independence

Disposition:

    PASS

Meaning:

    The reproduction classification logic rejects the identified
    semantic failure modes.

It does not establish that a real-world human or organizational
reproduction is independent merely because a boolean says so.

---

## Repository CI

The workflow must invoke the actual repository paths:

    tests/mutation-tests.py
    tests/test-brt-q54.py
    tests/aq-001.py
    tests/test-depth-exact.py
    tests/test-frob-equal.py

The previous workflow referenced:

    TESTS/mutation_test.py
    TESTS/test_brt_q54.py
    TESTS/test_aq001.py
    TESTS/test_depth_exact.py
    TESTS/test_frob_equal.py

Those paths do not correspond to the currently committed filenames.

Therefore:

    previous workflow = NOT CLOSED

After correction:

    workflow correctness = READY FOR GITHUB EXECUTION

A GitHub Actions PASS must still be observed on the corrected
commit before claiming repository-level CI execution.

---

## Governance

C3:

    OPEN

C4:

    BLOCKED

Publication:

    BLOCKED

Lean:

    OPEN

SDS-002:

    FROZEN-QUARANTINED

EK-001:

    QUARANTINED

No theorem promotion.

No publication promotion.
