FILE: JOIN-STABILITY/README.md


TYPE: Markdown

PURPOSE: Standalone README for the Join-Stability research package.


# AQARION — Join-Stability of Pullback-Stable Equivalence Relations

**Research status: OPEN**

> **Prove first. Verify exhaustively. Publish third.**
>
> A clean census is corroboration, not a proof.
> A retracted proof is preserved history, not evidence.

---

## 1. Research Question

Let

\[
T:X\to X
\]

be a map on a finite set \(X\), and let \(E,F\) be equivalence
relations on \(X\).

Define pullback stability by

\[
\operatorname{IsPullbackStable}(E)
\iff
T^{-1}(E)\le E.
\]

The central question is:

\[
\boxed{
\operatorname{IsPullbackStable}(E)
\land
\operatorname{IsPullbackStable}(F)
\stackrel{?}{\Longrightarrow}
\operatorname{IsPullbackStable}(E\vee F)
}
\]

where \(E\vee F\) denotes the **join** of the two equivalence
relations.

This package investigates that implication by:

1. exact exhaustive census,
2. targeted falsification,
3. independent obstruction analysis,
4. explicit preservation of failed proofs and buggy checkers,
5. formal-proof preparation.

---

# 2. Current Status

| Item | Status |
|---|---|
| Join-stability theorem | **OPEN** |
| Exhaustive census \(n\le6\) | **CLEAN** |
| Targeted \(n=7\) census | **CLEAN** |
| Targeted \(n=8\) census | **CLEAN** |
| Corrected characterization \(n=2,\ldots,5\) | **166,483 / 166,483** |
| Parent-wandering search | **No range-gap candidates found in current sample** |
| Lemma E: range-gap necessity | **[P]** |
| Original join proof | **RETRACTED** |
| Buggy checker v1 | **PRESERVED FAILURE** |
| Lean formalization | **OPEN** |
| C4 | **BLOCKED** |
| Publication | **BLOCKED** |
| Promotion | **FALSE** |

No census result is being promoted to a theorem.

---

# 3. The Central Target

Write

\[
G=E\vee F.
\]

The unresolved implication is

\[
T^{-1}(E)\le E,\qquad
T^{-1}(F)\le F
\]

implies

\[
T^{-1}(G)\le G\;?
\]

A failure would require points \(x,y\) satisfying

\[
Tx\;G\;Ty
\]

but

\[
x\not G y.
\]

The difficulty is that a \(G\)-path between \(Tx\) and \(Ty\)
may alternate between \(E\)-edges and \(F\)-edges.

Individual \(E\)- and \(F\)-edges lift under the respective
stability assumptions.

The unresolved issue is whether the lifted path can be forced
to remain inside the same \(G\)-class.

This is the **parent-wandering problem**.

---

# 4. Surviving Lemmas

## Lemma A — Single Parent Class

If \(E\) is pullback-stable, then for every \(E\)-class \(C\),

\[
T^{-1}(C)
\]

is contained in a single \(E\)-class.

Importantly, that parent class need not equal \(C\).

This distinction is essential.

Evidence:

\[
\boxed{[V]\quad 166{,}483/166{,}483}
\]

for the corrected finite census at \(n=2,\ldots,5\).

---

## Lemma B — Closed-Class Sufficiency

If every \(E\)-class is \(T^{-1}\)-closed, then

\[
T^{-1}(E)\le E.
\]

This gives a sufficient condition for pullback stability.

Evidence:

\[
\boxed{[V]\quad 166{,}483/166{,}483}
\]

in the corrected census.

---

## Lemma C — Fiber Saturation

Pullback stability implies

\[
\ker T\le E.
\]

Equivalently,

\[
T(x)=T(y)\Longrightarrow xEy.
\]

This is necessary but not sufficient for the join theorem.

---

## Lemma D — Parent-Class Wandering

The remaining obstruction is not whether individual
\(E\)- and \(F\)-edges lift.

They do.

The unresolved question is whether the parent classes selected by
those lifted edges remain inside the same \(G=E\vee F\) class.

This is the exact gap in the original proof attempt.

Evidence state:

\[
\boxed{[P]\text{ for the reduction of the problem}}
\]

but the join theorem itself remains:

\[
\boxed{[C]\text{/OPEN}}
\]

---

# 5. New Lemma E — Range-Gap Necessity

Let

\[
G=E\vee F
\]

and assume \(E\) and \(F\) are pullback-stable.

Suppose \(G\) is not pullback-stable.

Then there exist \(x,y\in X\) such that

\[
x\not G y,
\qquad
Tx\;G\;Ty,
\]

and every \(G\)-path from \(Tx\) to \(Ty\) contains an
internal vertex outside

\[
\operatorname{im}T.
\]

Equivalently:

> A genuine counterexample requires a \(G\)-component whose
> range points are disconnected after restricting \(G\) to
> \(\operatorname{im}T\).

### Proof

Suppose

\[
Tx=z_0,z_1,\ldots,z_k=Ty
\]

is a \(G\)-path entirely contained in \(\operatorname{im}T\).

For every \(z_i\), choose \(w_i\) satisfying

\[
T(w_i)=z_i.
\]

If

\[
z_iEz_{i+1},
\]

then stability of \(E\) gives

\[
w_iEw_{i+1}.
\]

Likewise, every \(F\)-edge lifts to an \(F\)-edge.

Therefore

\[
w_0Gw_1G\cdots Gw_k.
\]

Choosing \(w_0=x\) and \(w_k=y\) gives

\[
xGy,
\]

contradicting \(x\not Gy\).

Therefore every counterexample requires a range-gap.

\[
\boxed{\text{Join failure}\Longrightarrow\text{range-gap}}
\]

**Evidence state: [P]**

This lemma does **not** prove that range-gaps are impossible.

---

# 6. Why the Original Proof Was Retracted

The first proof attempt contained the step

\[
w\in T^{-1}(C)
\quad\Longrightarrow\quad
w\in C.
\]

That implication is false.

Minimal witness:

\[
X=\{0,1\},
\]

\[
T=(1,0),
\]

and \(E\) is equality.

Because \(T\) is bijective,

\[
T^{-1}(E)=E,
\]

so \(E\) is stable.

But for the class

\[
C=\{0\},
\]

we have

\[
T^{-1}(C)=\{1\},
\]

and therefore

\[
T^{-1}(C)\not\subseteq C.
\]

The false inference was exactly the assumption that a preimage of a
class must belong to that same class.

The complete failed argument remains preserved in:

```text
PROOF_v1_retracted.md



It must not be used as evidence for the theorem.



7. Preserved Buggy Checker


The package intentionally retains:


checker_v1_buggy.py



It reports:


n=3
27/27 violations



The corrected census reports:


n=3
0 violations



The v1 checker is therefore a permanent negative-control artifact.


Its purpose is not to support the theorem.


Its purpose is to demonstrate that the verification pipeline can expose
and preserve a false computational result rather than silently replacing
it.


Reproduction:


python checker_v1_buggy.py 3



Expected:


27 violations



This output is wrong by construction and is expected.


Correct census:


python census.py 3



Expected:


0 violations




8. Census Record


Exhaustive


(n\le5)


Corrected conditions:


\[

166{,}483/166{,}483

\]


pairs verified.


(n=6)


All


\[

6^6=46{,}656

\]


maps were checked exhaustively.


Result:


CLEAN




Targeted


(n=7)


60,000
non-surjective-biased maps

seed = 22092026

result = CLEAN



(n=8)


20,000
non-surjective-biased maps

seed = 22092026

result = CLEAN



These computations are corroboration only.


They do not establish the theorem.



9. Parent-Wandering / Range-Gap Search


The new search artifact is:


parent_wandering_search.py



It generates stable equivalence relations first, rather than wasting
the majority of samples on unstable (E,F).


The search then asks whether a stable pair produces the necessary
range-gap obstruction.


Current independent targeted results:




(n)
Maps
Closure seeds/map
Stable-pair samples
Range-gap candidates




7
2,000
500
36,735
0


8
1,000
500
23,663
0


9
500
500
15,493
0


10
200
1,000
4,199
0




Seed:


22092026



These results are targeted corroboration, not proof.



10. Reproduction


Existing exhaustive census:


python census.py 3



python census.py 6



Preserved buggy checker:


python checker_v1_buggy.py 3



Range-gap search:


python parent_wandering_search.py \
    --n 7 \
    --maps 2000 \
    --seeds-per-map 500



python parent_wandering_search.py \
    --n 8 \
    --maps 1000 \
    --seeds-per-map 500



python parent_wandering_search.py \
    --n 9 \
    --maps 500 \
    --seeds-per-map 500



python parent_wandering_search.py \
    --n 10 \
    --maps 200 \
    --seeds-per-map 1000




11. File Inventory


JOIN-STABILITY/
│
├── README.md
│   └── This document
│
├── census.py
│   └── Corrected exact census
│
├── checker_v1_buggy.py
│   └── Preserved false-positive checker
│
├── PROOF.md
│   └── Surviving lemmas and exact open gap
│
├── PROOF_v1_retracted.md
│   └── Preserved failed proof
│
├── receipt.json
│   └── Original machine-readable status
│
├── MANIFEST.json
│   └── SHA-256 manifest
│
├── parent_wandering_search.py
│   └── Range-gap obstruction search
│
├── PARENT_WANDERING.md
│   └── Lemma E and obstruction analysis
│
├── parent_wandering_receipt.json
│   └── Machine-readable targeted-search receipt
│
└── SESSION_2026-09-23.md
    └── Session history and progress record




12. Evidence Policy


This package deliberately distinguishes:


[D] Definition


Formal definitions and conventions.


[P] Proof


Mathematical derivation independent of census results.


[V] Verification


Executable finite computation.


[PV] Proof + Verification


Both independently established.


[C] Conjecture


A proposed mathematical statement not yet proved.


[R] Research


Exploratory work, searches, or hypotheses.



Current boundary


The clean census does not migrate upward into [P].


The retracted proof does not migrate downward into evidence.


The buggy checker does not become a valid negative result.


The current range-gap lemma is [P].


The absence of range-gap examples in the search is [V]/corroboration.


The join theorem remains OPEN.



13. Current Mathematical Bottleneck


The most useful next statement to attack is:


\[

\boxed{

E,F\text{ stable}

\Longrightarrow

\text{every }G\text{-component has }

C\cap\operatorname{im}T

\text{ connected under }G

}

\]


where


\[

G=E\vee F.

\]


If this statement is proved, Lemma E immediately gives:


\[

T^{-1}(G)\le G.

\]


Hence:


\[

\boxed{

T^{-1}(E)\le E,\quad

T^{-1}(F)\le F

\Longrightarrow

T^{-1}(E\vee F)\le E\vee F.

}

\]


If this statement is false, the counterexample should be the next
minimal structural target.


This is preferable to another undirected large census because it
attacks the exact unresolved mechanism.



14. What Has NOT Been Established


The following statements are intentionally not claimed:




The join theorem is true.


The join theorem is false.


The range-gap obstruction is impossible.


The numerical census proves the theorem.


The targeted (n=7)–(10) search proves anything asymptotic.


The retracted proof can be repaired by deleting one line.


Lean certification exists.


Publication readiness exists.


The theorem should be promoted.





15. Governance


JOIN-STABILITY THEOREM     OPEN
C3                          OPEN
C4                          BLOCKED
LEAN                        OPEN
PUBLICATION                 BLOCKED
PROMOTION                   FALSE



The package intentionally contains both:


FAILED COMPUTATION



and


FAILED PROOF



alongside successful verification.


That is part of the reproducibility record.



16. Research Principle


The project does not ask the repository to make the theorem look true.


It asks the repository to make the theorem survive attempts to make it false.


Current strongest statement:


\[

\boxed{

\text{Any counterexample must pass through a range-gap.}

}

\]


Current strongest computational observation:


\[

\boxed{

\text{No range-gap found in the present targeted search.}

}

\]


Those are deliberately different claims.


The first is a proof.


The second is an experiment.


The join theorem remains OPEN.




