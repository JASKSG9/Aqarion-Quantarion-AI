# AQ-CYCLE-DELTA-001 — Adversarial Mutation Contract

## Purpose

The mutation suite tests whether the evidence mechanism detects
mathematically incorrect implementations at the layer where the
mutation actually matters.

A mutation is not required to break every observable.

The receipt must identify which evidence layer was affected.

---

## M01 — Wrong defect scale

Correct:

D = 1/2 u w^T

Mutation:

D = 1/4 u w^T

Required result:

- matrix object comparison: FAIL
- operator-level crosscheck: FAIL
- first-zero lag: MAY REMAIN UNCHANGED

This mutation tests the distinction between operator equality and
zero-set equivalence.

---

## M02 — Wrong shift direction

Correct:

K^m e_j = e_(j-m)

Mutation:

K^m e_j = e_(j+m)

Required result:

- scalar sequence comparison: FAIL
- matrix/scalar crosscheck: FAIL

The verifier must compare the complete scalar sequence, not only
the final first-zero value.

---

## M03 — GCD lag conjecture

Mutation:

delta(k,d) = k/gcd(k,d)

Required result:

- theorem-vs-oracle mismatch
- mutation detected

This is a deliberately killed conjecture.

---

## M04 — Generic formula leaked into adjacent branch

Mutation:

apply the generic d >= 2 formula to d = 1 or d = k-1.

Required result:

- adjacent-branch counterexample
- mutation detected

---

## M05 — Wrong small-k threshold

Correct:

k >= 6

Mutation:

k >= 5

Required result:

- k = 5 counterexample
- mutation detected

---

## M06 — Collision-sign mutation

Alter one modular collision condition in the scalar oracle.

Required result:

- complete scalar sequence mismatch
- mutation detected

---

## M07 — Delete explicit small-k exceptions

Required result:

- k = 3, 4, or 5 mismatch
- mutation detected

---

## M08 — Semantic model mutation

Change the partition convention or cycle orientation while retaining
syntactically valid arithmetic.

Required result:

- semantic/specification mismatch

A mathematically correct calculation under the wrong model is not a
successful reproduction of AQ-CYCLE-DELTA-001.
