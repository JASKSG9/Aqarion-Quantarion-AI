# Join Stability — Parent-Wandering / Range-Gap Analysis

STATUS: OPEN

This file does not promote the join theorem.

The previous six-line proof remains retracted and is preserved in:

    PROOF_v1_retracted.md

The census remains corroboration only.

---

## 1. Target

Let T : X -> X be a finite map and E,F equivalence relations.

Define:

    IsPullbackStable(E) := T^{-1}(E) <= E.

The open target is:

    IsPullbackStable(E)
    and
    IsPullbackStable(F)

    ==> IsPullbackStable(E join F).

Write:

    G := E join F.

---

## 2. Range-Gap Lemma

### Lemma E

Assume E and F are pullback-stable.

If G = E join F is not pullback-stable, then there exist x,y such that:

    x not G y
    Tx G Ty

and every G-path from Tx to Ty contains an
internal vertex outside im(T).

Equivalently, a counterexample requires a G-component
whose range points are disconnected in the graph

    G restricted to im(T).

### Proof

Suppose instead that Tx and Ty can be connected by

    Tx = z0, z1, ..., zk = Ty

where every zi lies in im(T), and each consecutive pair
is E-related or F-related.

Choose wi with:

    T(wi) = zi.

If zi E z(i+1), then:

    T(wi) E T(w(i+1)).

Since E is pullback-stable:

    wi E w(i+1).

Likewise, if zi F z(i+1), then:

    wi F w(i+1).

Therefore:

    w0 G w1 G ... G wk.

Taking w0 = x and wk = y gives:

    x G y,

contradicting x not G y.

Therefore every counterexample must contain a range-gap.

QED.

Evidence state: [P]

---

## 3. Interpretation

The obstruction is now narrower than the original
"parent wandering" description.

A genuine counterexample requires:

    target G-component
          |
          +-- range point component A
          |
          +-- missing vertices
          |
          +-- range point component B

where A and B are disconnected after restricting G to im(T).

If every G-component remains connected after restriction
to im(T), the join theorem follows immediately from Lemma E.

---

## 4. Independent targeted search

Search generator:

    parent_wandering_search.py

Seed:

    22092026

The generator first constructs stable equivalence relations
using repeated exact coarsening under:

    P -> P join T^{-1}(P)

It then tests stable E,F pairs for the range-gap obstruction.

Results from the independent execution:

    n=7:
        maps = 2,000
        seeds/map = 500
        stable-pair samples = 36,735
        range-gap candidates = 0

    n=8:
        maps = 1,000
        seeds/map = 500
        stable-pair samples = 23,663
        range-gap candidates = 0

    n=9:
        maps = 500
        seeds/map = 500
        stable-pair samples = 15,493
        range-gap candidates = 0

    n=10:
        maps = 200
        seeds/map = 1,000
        stable-pair samples = 4,199
        range-gap candidates = 0

These are targeted samples.

They are not exhaustive and do not constitute a proof.

---

## 5. What this does NOT establish

It does not establish:

    E,F stable ==> E join F stable.

It does not establish that range-gaps are impossible.

It does not replace the n<=6 exhaustive census.

It does not promote C3/C4.

It does not close Lean.

It does not justify publication.

---

## 6. Exact next mathematical target

Prove or refute:

    If E and F are pullback-stable under T,
    then every G-component intersects im(T)
    in a G-connected set,

where:

    G = E join F.

This statement is sufficient for the join theorem.

A counterexample to this intermediate statement would
provide a substantially sharper target for constructing
an actual join-stability counterexample.

---

## 7. Governance

Join theorem: OPEN

C3: OPEN

C4: BLOCKED

Lean: OPEN

Publication: BLOCKED

Promotion: FALSE

Clean census: corroboration only

Retracted proof: preserved negative evidence/history
