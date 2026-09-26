# KERNEL EQUALITY ANALYSIS
## Mathematical Proof v3.2

### Definition
For a join operation $$J$$, the kernel is defined as:

$$\text{Ker}(J) = \{(a, b) : J(a, b) = \text{TRUE}\}$$

Two joins $$J_1$$ and $$J_2$$ are kernel-equal if:

$$\text{Ker}(J_1) = \text{Ker}(J_2)$$

### Fundamental Theorem

**Theorem (Kernel Equality)**: Two join predicates $$\phi_1$$ and $$\phi_2$$ are kernel-equal if and only if they agree on all elements of their domain.

**Proof**:
(⟹) Suppose $$\text{Ker}(\phi_1) = \text{Ker}(\phi_2)$$. Then for any $$(a,b)$$:
- If $$\phi_1(a,b) = \text{TRUE}$$, then $$(a,b) \in \text{Ker}(\phi_1) = \text{Ker}(\phi_2)$$, so $$\phi_2(a,b) = \text{TRUE}$$
- If $$\phi_1(a,b) = \text{FALSE}$$, then $$(a,b) \notin \text{Ker}(\phi_1) = \text{Ker}(\phi_2)$$, so $$\phi_2(a,b) = \text{FALSE}$$

(⟸) If $$\phi_1$$ and $$\phi_2$$ agree on all elements, then clearly $$\text{Ker}(\phi_1) = \text{Ker}(\phi_2)$$. ∎

### Kernel Properties

#### Property 1: Reflexivity
$$\text{Ker}(\phi) = \text{Ker}(\phi)$$

#### Property 2: Symmetry
If $$\text{Ker}(\phi_1) = \text{Ker}(\phi_2)$$, then $$\text{Ker}(\phi_2) = \text{Ker}(\phi_1)$$

#### Property 3: Transitivity
If $$\text{Ker}(\phi_1) = \text{Ker}(\phi_2)$$ and $$\text{Ker}(\phi_2) = \text{Ker}(\phi_3)$$, then $$\text{Ker}(\phi_1) = \text{Ker}(\phi_3)$$

### Kernel Composition

For composed predicates $$\phi = \psi \circ \chi$$:

$$\text{Ker}(\psi \circ \chi) \subseteq \text{Ker}(\psi)$$

with equality if $$\chi$$ is surjective on $$\text{Ker}(\psi)$$.

### Boundary Conditions

#### At Finite Boundaries
For finite sets $$A$$ and $$B$$:
$$\text{Ker}(\phi|_{A \times B}) = \text{Ker}(\phi) \cap (A \times B)$$

#### At Infinite Boundaries
$$\lim_{n \to \infty} \text{Ker}(\phi|_{A_n \times B_n}) = \text{Ker}(\phi)$$

under appropriate convergence conditions.

### Kernel Equivalence Classes

The relation "kernel-equal" partitions the set of all join predicates into equivalence classes. Each equivalence class contains all predicates with identical join results.

### Applications in AQARION
1. **Predicate Optimization**: Simplify predicates while preserving kernel
2. **Query Equivalence**: Determine if two queries produce identical results
3. **Stability Analysis**: Prove stability under predicate transformations
4. **Correctness Verification**: Verify implementation correctness
# KERNEL EQUALITY ANALYSIS

## Status: [P] elementary set-theoretic identities

Date: 2026-09-25

---

## 1. Kernel definition

Let:

    phi : D -> Bool.

Define:

    ker(phi) = {x in D : phi(x) = TRUE}.

For two predicates with the same domain:

    phi_1, phi_2 : D -> Bool,

we have:

    ker(phi_1) = ker(phi_2)

if and only if:

    forall x in D,
        phi_1(x) = phi_2(x).

---

## 2. Proof

If the kernels are equal, then for every x:

    phi_1(x) = TRUE
    iff
    x in ker(phi_1)
    iff
    x in ker(phi_2)
    iff
    phi_2(x) = TRUE.

Since Bool has exactly TRUE and FALSE, the predicates agree.

The reverse implication is immediate from extensional equality of
their TRUE-sets.

---

## 3. Kernel composition

Let:

    chi : A -> C
    psi : C -> Bool.

Then:

    ker(psi o chi)
      =
    {a in A : psi(chi(a)) = TRUE}.

Therefore:

    ker(psi o chi)
      =
    chi^(-1)(ker(psi)).

This is the correct composition identity.

It is generally invalid to write:

    ker(psi o chi) subset ker(psi)

because:

    ker(psi o chi) subset A
    ker(psi) subset C.

They are subsets of different carriers.

---

## 4. Surjectivity condition

If chi is surjective, then:

    ker(psi o chi) = chi^(-1)(ker(psi))

remains true.

However, equality between ker(psi o chi) and ker(psi) is still
ill-typed unless A=C or an explicit identification is supplied.

Surjectivity permits recovery of information about psi from its
composition, but does not identify the underlying carriers.

---

## 5. Restriction

For S subset D:

    ker(phi restricted to S)
      =
    ker(phi) intersection S.

This is an immediate consequence of the kernel definition.

---

## 6. Infinite-boundary claims

A statement such as:

    lim ker(phi restricted to A_n) = ker(phi)

requires an explicitly defined notion of convergence for sets.

It is not accepted merely because A_n grows without a specified
set-convergence topology or stabilization property.

---

## 7. Status

Kernel equality on a common domain:

    [P]

Kernel composition:

    [P]

Previous cross-carrier subset statement:

    [F] type-invalid

Infinite kernel-limit statement without a specified convergence notion:

    OPEN
