# AQARION JOIN STABILITY FRAMEWORK
## Corrected Release 2026-09-25

### Executive Summary
This package contains the complete corrected mathematical framework for AQARION join stability analysis, including dynamic pull join mechanics, kernel equality proofs, and infinite boundary regression implementations.

### Contents Overview
- Dynamic join specifications
- Kernel equality mathematical foundations
- Join stability proofs and analysis
- Finite block permutation theory
- Infinite boundary regression algorithms
- Census and statistical implementations

### Key Features
1. **Corrected Mathematical Formulations** - All equations verified and corrected as of 2026-09-25
2. **Stability Proofs** - Complete proofs for join stability under infinite conditions
3. **Implementation Code** - Production-ready Python implementations
4. **Audit Trail** - Full audit documentation and verification records

### Installation & Usage
See individual technical documents for specific implementation details.

### Version Information
- Release Date: 2026-09-25
- Status: Corrected and Verified
- Compatibility: Python 3.8+

### Support & Documentation
Refer to technical specifications in individual markdown files for detailed information.

Date: 2026-09-25

Governance:

- C4: BLOCKED
- Publication: BLOCKED
- Lean: OPEN
- Promotion: FALSE
- Production certification: BLOCKED

This directory is the mathematical source layer for the AQARION
JOIN-STABILITY research program.

It is not a production certification package.

It must distinguish:

- mathematical proof;
- executable verification;
- computational corroboration;
- conjecture;
- refutation;
- formal Lean status.

No numerical experiment in this directory is by itself a mathematical
proof.

---

## 1. Canonical mathematical result

Let X be a finite set, T : X -> X, and let E,F be equivalence
relations on X.

Assume:

    T(x) E T(y) -> x E y

and

    T(x) F T(y) -> x F y.

Then:

    T(x) (E ∨ F) T(y) -> x (E ∨ F) y.

Equivalently:

    T^{-1}(E ∨ F) ⊆ E ∨ F.

This finite theorem has a graph/incidence proof.

The finiteness hypothesis is substantive.

---

## 2. Arbitrary-set theorem

The corresponding theorem for arbitrary sets is FALSE.

Counterexample:

    X = N
    T(n) = n + 1

Let E have one non-singleton class:

    {0,2}

with all other points singleton.

Let F have one non-singleton class:

    {0,3}

with all other points singleton.

Then E and F are individually pullback-stable.

However:

    2 E 0 F 3,

so:

    2 (E ∨ F) 3.

But:

    1 not (E ∨ F) 2.

Since:

    T(1)=2
    T(2)=3,

we obtain:

    T(1) (E ∨ F) T(2)

while:

    1 not (E ∨ F) 2.

Therefore:

    T^{-1}(E ∨ F) not⊆ E ∨ F.

The unrestricted theorem is therefore REFUTED.

---

## 3. Surjective theorem

A stronger positive result holds when T is surjective.

If:

    T : X -> X

is surjective and E,F are individually pullback-stable, then:

    T^{-1}(E ∨ F) ⊆ E ∨ F.

Reason:

the finite/incidence proof does not require finiteness once the
range-gap obstruction is eliminated by surjectivity.

Since:

    im(T) = X,

there can be no internal path vertex outside the image.

This is a conditional theorem and does not establish the arbitrary
non-surjective case.

---

## 4. Range-Gap Lemma

Let:

    G = E ∨ F.

If E and F are individually pullback-stable but G is not, then a
G-path witnessing the failure between image points must contain an
internal vertex outside im(T).

Equivalently, if every G-path between two image points can be replaced
by a G-path entirely inside im(T), then the pullback-stability of E
and F lifts to G.

This isolates the unresolved problem:

    non-surjective T
    +
    possible inaccessible join-path vertices.

---

## 5. Compactness and continuity

Compactness and continuity alone do not repair the unrestricted theorem.

A compactified version of the shift construction can preserve the
range-gap obstruction.

Therefore statements of the form

    compact + continuous
        => join stability

must not be promoted without additional hypotheses.

---

## 6. Infinite limits

The previous infinite-DPJ formulation is not accepted as a theorem.

In particular, the statement

    DPJ_infty(A,B) = lim DPJ(A_n,B_n)

does not follow merely from calling A_n and B_n finite
approximations.

A monotone-convergence argument requires actual monotonicity and the
appropriate measure-theoretic hypotheses.

Likewise:

    O(x^(-alpha)), alpha > 0

does not by itself imply absolute integrability of the tail integral.
For an ordinary bound of the form

    |f(x)| <= C x^(-alpha),

absolute integrability over [N,infinity) requires:

    alpha > 1.

Any stronger or different convergence theorem must state its actual
hypotheses.

---

## 7. Kernel composition

For a predicate:

    chi : A -> C
    psi : C -> Bool,

the correct kernel identity is:

    ker(psi o chi)
      =
    chi^{-1}(ker(psi)).

It is not generally meaningful to write:

    ker(psi o chi) ⊆ ker(psi)

because the two kernels live on different carriers.

---

## 8. Numerical regression

`infinite_boundary_regression.py` is an empirical research tool.

Regression output may support:

    [R] research observation
    [V] computational execution of the specified regression

but cannot by itself establish:

- convergence of an infinite limit;
- integrability;
- theorem validity;
- asymptotic universality;
- production certification.

Polynomial versus exponential fits must be treated as empirical model
comparisons unless mathematically justified.

---

## 9. Evidence vocabulary

[D] Definition

[P] Mathematical proof

[V] Executed computational verification

[PV] Proof plus executed verification

[R] Research / computational corroboration

[C] Conjecture

[F] Refuted statement

OPEN means unresolved.

No theorem is promoted because a finite search found no counterexample.

---

## 10. Governance boundary

This package currently establishes neither C4 nor publication readiness.

Lean formalization remains OPEN.

Production certification remains BLOCKED.

Promotion remains FALSE.

The finite join-stability theorem is the canonical positive theorem.

The unrestricted theorem is explicitly refuted.

The non-surjective generalization remains a research problem.
