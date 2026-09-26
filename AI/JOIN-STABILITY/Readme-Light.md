# AQARION JOIN-STABILITY

## Mathematical Research Package

**Repository path:** `AI/JOIN-STABILITY/`

**Research date:** 2026-09-23

**Current status:** OPEN

**Join theorem:** NOT PROVED

**C3:** OPEN

**C4:** BLOCKED

**Lean formalization:** OPEN

**Publication status:** BLOCKED

---

## 1. Purpose

This directory investigates whether pullback-stable equivalence
relations are closed under equivalence closure, or equivalently,


Status: FROZEN RESEARCH STATE


Mathematical status


Finite theorem — PROVED


For finite X,


[
T^{-1}(E)\subseteq E,\qquad
T^{-1}(F)\subseteq F
]


imply


[
T^{-1}(E\vee F)\subseteq E\vee F.
]


Proof: finite incidence graph of E-classes and F-classes.


Arbitrary-set theorem — FALSE


The unrestricted statement fails for


[
T(n)=n+1
]


with E-class {0,2} and F-class {0,3}.


The failure occurs because 0\notin\operatorname{im}(T) acts as a
hidden join bridge.


Surjective theorem — PROVED CONDITIONALLY


If T is surjective, then join stability follows without requiring
X to be finite.


Compactness


Compactness and continuity alone do not repair the theorem.


Evidence boundary


Finite mathematical proof       PROVED
Infinite counterexample         EXPLICIT
Surjective generalization       PROVED CONDITIONALLY
Lean                             OPEN
C4                              BLOCKED
Publication                     BLOCKED
Promotion                       FALSE



Computational searches are corroborative unless their domain is
explicitly exhaustive.


Historical ZIP/subprocess material is not authoritative.


Canonical files:


README.md
Readme-Light.md
contract.json
Filetree.md
JOIN_STABILITY_PROOF.md
Parent_Wondering.md
Session_2026-09-23.md
parent_wondering_search.py
parent_wondering_receipt.json
join_stability_exact_verifier.py
oracle.py



under joins.

Let

    T : X -> X

be a finite map, and let E and F be equivalence relations on X.

Define pullback stability by

    IsPullbackStable(E) := T^{-1}(E) <= E.

The principal conjectural implication is

    IsPullbackStable(E)
    and
    IsPullbackStable(F)

    ==> IsPullbackStable(E join F).

This implication remains OPEN.

---

## 2. Mathematical target

Write

    G := E join F.

The objective is to determine whether

    T^{-1}(G) <= G

follows from

    T^{-1}(E) <= E
    and
    T^{-1}(F) <= F.

The previous short proof of this statement was retracted.
The retracted proof is preserved in the research history and
must not be silently restored or treated as valid.

---

## 3. Range-Gap Lemma

Assume E and F are pullback-stable.

If G = E join F is not pullback-stable, then there exist x,y such that

    x not G y
    Tx G Ty

and every G-path from Tx to Ty contains an internal vertex
outside im(T).

Equivalently, a counterexample requires a G-component whose
range points are disconnected after restricting G to im(T).

This is a necessary obstruction, not a proof that the obstruction
cannot occur.

Evidence status: [P]

---

## 4. Research interpretation

The obstruction is narrower than the original parent-wandering
description.

A genuine counterexample must contain a G-component with at least
two range-point regions that are connected in G only through
vertices outside im(T).

If every G-component is connected after restriction to im(T),
then the join theorem follows from the Range-Gap Lemma.

The remaining mathematical question is therefore:

    If E and F are pullback-stable under T,
    must every G-component intersect im(T)
    in a G-connected set?

where

    G = E join F.

This intermediate statement is sufficient for join stability.
It is not currently established.

---

## 5. Computational evidence

The targeted search constructs pullback-stable equivalence relations
using repeated exact coarsening under

    P -> P join T^{-1}(P).

It then tests stable pairs for the range-gap obstruction.

Recorded targeted results:

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

They are not exhaustive.
They do not constitute a proof.
They do not establish join stability.
They do not establish that range gaps are impossible.

Evidence status: [V-local/corroborative], not theorem-level [V].

---

## 6. Evidence and governance

This package follows AQARION evidence discipline:

    [D] Definition
    [P] Symbolic proof
    [V] Exhaustive computational verification
    [PV] Proof plus verification
    [C] Conjecture
    [R] Research

No conjecture is promoted to theorem solely because a search
found no counterexample.

No production-readiness claim is made by this mathematical package.

No Lean closure is claimed unless an actual Lean build receipt
and axiom report are available.

---

## 7. Files

    Filetree.md
        Directory inventory.

    Parent_Wondering.md
        Mathematical target, Range-Gap Lemma, search summary,
        limitations, and next theorem obligation.

    Session_2026-09-23.md
        Session-level research record.

    Subprocess.txt
        Execution or subprocess notes.

    parent_wandering_search.py
        Targeted computational search generator and obstruction test.

    parent_wandering_receipt.json
        Computational receipt, subject to independent verification.

    README.md
        This package description.

---

## 8. Next mathematical task

Prove or refute:

    Stable(E) and Stable(F)
    imply that every component of E join F
    intersects im(T) in a connected subgraph
    of the restriction of E join F to im(T).

Possible outcomes:

1. Prove the intermediate range-connectedness statement.
2. Construct a counterexample to range-connectedness.
3. Derive additional hypotheses under which it holds.
4. Reduce the problem to a finite minimal obstruction.

No broad census should be undertaken unless it addresses one
of these exact alternatives.

---

## 9. Final status

Join theorem: OPEN

Range-Gap Lemma: [P]

C3: OPEN

C4: BLOCKED

Lean: OPEN

Publication: BLOCKED

Promotion: FALSE

Retracted proof: PRESERVED

Computational census: CORROBORATION ONLY
```

### 5\. Corrected `Filetree.md` — inline replacement

````markdown
# AQARION JOIN-STABILITY — Filetree

Repository path:

    AI/JOIN-STABILITY/

## Directory layout

```text
AI/JOIN-STABILITY/
├── Filetree.md
├── Parent_Wondering.md
├── README.md
├── Session_2026-09-23.md
├── Subprocess.txt
├── parent_wandering_search.py
└── parent_wandering_receipt.json
````

### File descriptions

### `README.md`

Canonical package overview.

Describes the mathematical research target, current evidence status, limitations, and next theorem obligation.

### `Filetree.md`

This file.

Maintains the verified directory inventory.

### `Parent_Wondering.md`

Primary mathematical analysis.

Contains:

* Pullback-stability definition.

* Join-stability target.

* Range-Gap Lemma.

* Proof of the necessary obstruction.

* Targeted computational results.

* Explicit non-claims.

* Current next mathematical task.

### `Session_2026-09-23.md`

Session-level research record.

### `Subprocess.txt`

Execution notes or subprocess output associated with the research.

### `parent_wandering_search.py`

Targeted search implementation for stable equivalence-relation pairs and range-gap obstructions.

### `parent_wandering_receipt.json`

Machine-readable computational receipt.

Its contents must be independently checked before promotion to authoritative verification evidence.

### Governance

The directory is a mathematical research package.

It is not a production software release.

The join-stability theorem remains OPEN.

The targeted search is corroborative only.

The retracted proof must remain preserved.

No file in this directory should claim:

* production readiness;

* theorem completion;

* Lean closure;

* publication readiness;

* universal absence of counterexamples;

unless separately supported by the required evidence.

````

---

# 6. New mathematical observation: the obstruction is really a quotient-of-the-range problem

The Range-Gap Lemma can be reformulated more sharply.

Let

\[
G=E\vee F
\]

and let

\[
H = G\!\restriction_{\operatorname{im}(T)}
\]

be the graph obtained by restricting the generating \(E\)- and \(F\)-edges to range vertices.

For any \(x,y\in X\),

\[
Tx\;G\;Ty
\]

means that \(Tx\) and \(Ty\) lie in the same connected component of the full \(G\)-graph.

But pullback stability can only lift an edge

\[
T(u)\;E\;T(v)
\]

or

\[
T(u)\;F\;T(v)
\]

when the corresponding edge lies entirely among image vertices.

Therefore the actual missing property is:

\[
\boxed{
\text{Connectivity in }G
\quad\Longrightarrow\quad
\text{connectivity in }G\!\restriction_{\operatorname{im}(T)}
}
\]

for pairs of vertices already in \(\operatorname{im}(T)\).

This is not ordinary connectivity preservation. It is a **convexity-like property of the image subset with respect to the join graph**.

That suggests three potentially useful reformulations.

## 6.1 Image-convexity formulation

Call \(A\subseteq X\) **\(G\)-geodesically closed** if every \(G\)-path between points of \(A\) can be replaced by a \(G\)-path lying in \(A\).

The required intermediate statement is:

\[
\operatorname{im}(T)
\text{ is }G\text{-geodesically closed}.
\]

This is stronger than mere intersection of every component with the image.

The existing Range-Gap Lemma only needs connectedness, not shortest paths, so “path-convexity” should be used cautiously unless proved equivalent in the finite undirected graph setting.

## 6.2 Component-restriction formulation

For every \(G\)-component \(C\),

\[
G[C\cap\operatorname{im}(T)]
\]

must be connected whenever \(C\cap\operatorname{im}(T)\neq\varnothing\).

This is the cleanest finite graph statement and should probably be the canonical formulation in the next research note.

## 6.3 Generator-colored formulation

Construct a two-colored graph:

- red edges from \(E\);
- blue edges from \(F\).

The obstruction is not simply that the full graph requires vertices outside the image. It is that every alternating or non-alternating colored path between two image vertices leaves the image.

This may permit a stronger proof attempt using the fact that each color class is individually pullback-stable.

---

# 7. The next exact theorem attack

The most productive next lemma is likely not the full range-connectedness conjecture, but a **one-step path-shortening lemma**.

Suppose

\[
a,b\in\operatorname{im}(T)
\]

and

\[
a\;E\;z\;F\;b
\]

with \(z\notin\operatorname{im}(T)\).

Can stability of \(E\) and \(F\) force an alternative image-contained connection?

At first glance, no direct pullback is available because \(z\) has no preimage. Thus a proof would need an additional mechanism, such as:

- a structural relation between \(E\) and \(F\);
- surjectivity of \(T\);
- invariance of \(\operatorname{im}(T)\);
- a condition on fibers of \(T\);
- a stronger stability notion than \(T^{-1}(E)\le E\).

This yields a useful conditional theorem.

## Conditional result

If \(T\) is surjective, then

\[
\operatorname{im}(T)=X,
\]

so range gaps are impossible.

Consequently, under surjectivity:

\[
\boxed{
\operatorname{Stable}(E)\land\operatorname{Stable}(F)
\Longrightarrow
\operatorname{Stable}(E\vee F)
}
\]

by the Range-Gap Lemma.

### Proof

If \(T\) is surjective, every vertex lies in \(\operatorname{im}(T)\). Hence every \(G\)-path between \(Tx\) and \(Ty\) already lies in the image. The Range-Gap Lemma says that a failure of pullback stability would require a path with an internal vertex outside the image, which is impossible. Therefore \(T^{-1}(G)\le G\). ∎

Evidence status: **[P] conditional theorem**, assuming the Range-Gap Lemma as already established.

This is important because it identifies a real boundary:

> The difficulty is entirely caused by non-surjectivity and inaccessible intermediate vertices.

It also gives an immediate research split:

| Dynamical map class | Join stability |
|---|---|
| Surjective finite maps | Follows from Range-Gap Lemma |
| Non-surjective maps | OPEN |
| Eventually-surjective maps | Candidate extension |
| Maps with image-convex join components | Follows from Range-Gap Lemma |
| Arbitrary finite maps | OPEN |

---

# 8. New research direction: eventual image stabilization

For a finite map \(T:X\to X\), define

\[
X_k=\operatorname{im}(T^k).
\]

Then

\[
X_{k+1}\subseteq X_k
\]

and because \(X\) is finite, there exists \(m\) such that

\[
X_m=X_{m+1}=\cdots.
\]

The stable image \(X_\infty\) is a union of cycles and is invariant under \(T\). The restriction

\[
T|_{X_\infty}:X_\infty\to X_\infty
\]

is surjective.

This suggests a possible decomposition:

1. Analyze join stability on the eventual image, where surjectivity removes range gaps.
2. Determine whether transient vertices can create a failure before the eventual image.
3. Characterize the transient obstruction separately.

A potentially valuable conjecture is:

\[
\boxed{
\text{Join stability on }X_\infty
\text{ plus a transient lifting condition}
\Longrightarrow
\text{join stability on }X.
}
\]

The transient lifting condition is not yet known and must not be invented. But this decomposition is mathematically natural and may reduce arbitrary finite maps to:

- a surjective core;
- a finite transient forest;
- a precise interface problem.

---

# 9. Recommended next execution

The next computation should not be another unrestricted census. It should classify maps by image structure and test the exact intermediate property.

## Proposed experiment

For each finite map \(T:X\to X\):

1. Generate stable \(E,F\).
2. Form \(G=E\vee F\).
3. Compute each \(G\)-component \(C\).
4. Compute \(C\cap\operatorname{im}(T)\).
5. Test whether the induced restriction is connected.
6. Record:
   - map image size;
   - number of transient vertices;
   - eventual image size;
   - number of \(G\)-components;
   - number of range-gap components;
   - whether \(G\) itself is pullback-stable.

The key distinction in the output must be:

```text
range-gap witness
actual join-stability counterexample
````

A range-gap witness is only a candidate obstruction. It is not necessarily a failure of join stability unless one also finds

x\\not G y,\\qquad Tx\\;G\\;Ty.

### Suggested receipt fields

```json
{
  "experiment": "join_range_component_classification",
  "status": "research",
  "evidence_level": "[V-local/corroborative]",
  "map_size": null,
  "maps_tested": null,
  "stable_pairs_tested": null,
  "range_gap_components": null,
  "actual_join_counterexamples": null,
  "surjective_maps": null,
  "non_surjective_maps": null,
  "eventual_image_statistics": null,
  "seed": null,
  "source_sha256": null,
  "environment": {
    "python": null,
    "platform": null,
    "dependencies": null
  },
  "claim_boundary": [
    "No theorem promotion from zero candidates",
    "No exhaustive claim without complete finite coverage",
    "Range-gap witness is not an actual join counterexample"
  ]
}
```

### 10\. Final adversarial checkpoint

### Confirmed from retrieved repository material

* The mathematical JOIN-STABILITY record exists.

* The Range-Gap Lemma is explicitly documented.

* The previous proof is preserved as retracted.

* The join theorem remains open.

* The targeted search is explicitly non-exhaustive.

* The actual filetree contains seven files.

* The README does not match that actual mathematical package.

### New mathematical result

Under the Range-Gap Lemma:

\\boxed{
T\\text{ surjective}
\\Longrightarrow
\\text{join stability for pullback-stable }E,F.
}

This is a genuine conditional theorem and isolates the unresolved difficulty to non-surjective maps.

### Still not established

* Arbitrary finite-map join stability.

* Im-component connectedness for stable joins.

* Impossibility of range gaps.

* C3.

* C4.

* Lean formalization.

* Publication readiness.

### Highest-value next target

Classify the transient/non-surjective obstruction via the eventual image , while testing range-component connectedness and actual join failure separately.

That is the next mathematically meaningful step—not another broad claim of completion.
