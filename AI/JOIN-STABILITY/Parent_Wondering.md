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

JOIN-STABILITY — RANGE-GAP / PARENT-WANDERING ANALYSIS


Status


Finite join theorem:        PROVED
Arbitrary-set theorem:      REFUTED
Surjective theorem:         PROVED CONDITIONALLY
Range-Gap Lemma:             PROVED
Lean:                        OPEN
C4:                          BLOCKED
Publication:                 BLOCKED
Promotion:                   FALSE




1. Original target


Let


[
T:X\to X
]


and let E,F be equivalence relations.


The target was


[
T^{-1}(E)\subseteq E
\quad\land\quad
T^{-1}(F)\subseteq F
]


implies


[
T^{-1}(E\vee F)\subseteq E\vee F.
]


The unrestricted statement is false.


The finite statement is proved by the incidence-graph argument.



2. Range-Gap Lemma


Put


[
G=E\vee F.
]


If E,F are pullback-stable but G is not, then a witness


[
x\not Gy,\qquad Tx,G,Ty
]


must have a G-path from Tx to Ty that leaves
\operatorname{im}(T).


If the entire path remained in the image, every edge could be
lifted using pullback stability and would produce a G-path from
x to y.


Thus:


[
\boxed{
\text{join failure}\Longrightarrow\text{range gap}.
}
]


This is a necessary condition only.



3. Explicit range-gap counterexample


The unrestricted theorem is actually refuted.


Take


[
X=\mathbb N,\qquad T(n)=n+1.
]


Let


[
E:{0,2}\text{ is one class},
]


and let


[
F:{0,3}\text{ is one class}.
]


All remaining points are singleton classes.


Then


[
2E0F3,
]


so


[
2(E\vee F)3.
]


But


[
1\not(E\vee F)2.
]


Since


[
T(1)=2,\qquad T(2)=3,
]


join stability fails.


The missing point is 0\notin\operatorname{im}(T).


This is the canonical infinite witness.



4. Surjective boundary


If T is surjective, then


[
\operatorname{im}(T)=X.
]


The range-gap obstruction cannot occur.


Therefore the Range-Gap Lemma immediately gives:


[
T^{-1}(E)\subseteq E,\quad
T^{-1}(F)\subseteq F
\Longrightarrow
T^{-1}(E\vee F)\subseteq E\vee F.
]


Thus the research problem is specifically a non-surjective
problem once the surjective case is separated.



5. Finite maps and eventual image


For finite X, define


[
X_k=\operatorname{im}(T^k).
]


Then


[
X_{k+1}\subseteq X_k.
]


Because X is finite, this sequence eventually stabilizes:


[
X_m=X_{m+1}=X_{m+2}=\cdots.
]


The stable image X_\infty is invariant under T, and


[
T|{X\infty}:X_\infty\to X_\infty
]


is surjective.


This gives a useful structural decomposition:


finite dynamical system
        |
        +-- eventual surjective core
        |
        +-- transient vertices



The surjective core has no range-gap problem.


The remaining research question is whether transient vertices can
create a join failure compatible with individual pullback stability.


The explicit infinite example demonstrates that non-surjectivity can
do exactly that.



6. Computational search boundary


The existing targeted searches at n=7,8,9,10 found no sampled
range-gap candidates.


Those searches are useful corroboration only.


They do not prove:




range gaps cannot occur;


arbitrary finite maps satisfy join stability;


the finite theorem beyond its mathematical proof;


any infinite theorem.




A future search should classify:


range-gap candidate
actual join-stability failure



as separate outcomes.



7. Best next mathematical attack


The next exact target is:




Characterize the transient non-surjective structure that can permit
a join path between two image points to leave the image.




Useful variables are:




|\operatorname{im}(T)|;


eventual-image size;


transient depth;


number of G-components;


image intersection with each G-component;


connectedness of G restricted to the image.




Do not collapse these into one “counterexample” statistic.



8. Governance


Range-Gap Lemma          PROVED
Infinite counterexample  EXPLICIT
Surjective theorem       PROVED CONDITIONALLY
Finite theorem           PROVED
Lean                     OPEN
C4                      BLOCKED
Publication              BLOCKED
Promotion                FALSE


