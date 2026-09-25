# AQARION JOIN-STABILITY

Research target:

    Pullback-stable equivalence relations are closed under join
    on finite sets.

## Current status

| Item | Status |
|---|---|
| Finite join theorem | [P] |
| Exact finite verification n=1..6 | [V] |
| Combined evidence | [PV] |
| Unrestricted infinite theorem | [F] |
| Lean formalization of finite theorem | OPEN |
| C4 | BLOCKED |
| Publication | BLOCKED until formalization/review |

## Theorem

For finite X and T : X -> X, if

    T(x) E T(y) => x E y

and

    T(x) F T(y) => x F y,

then

    T(x) (E ∨ F) T(y) => x (E ∨ F) y.

The proof uses the bipartite incidence graph of E-classes and
F-classes.

Pullback stability makes T induce permutations of the E-class and
F-class sets. These permutations induce an automorphism of the
incidence graph. Its connected components are exactly the
E∨F-classes.

Therefore E∨F is pullback-stable.

See:

    JOIN_STABILITY_PROOF.md
    join_stability_exact_verifier.py

## Exact verification

The independent verifier exhaustively reconstructs every
deterministic map and every stable E,F pair for n=1,...,6.

Results:

    n=1       1 pair
    n=2       8 pairs
    n=3       84 pairs
    n=4       1,276 pairs
    n=5       24,475 pairs
    n=6       582,696 pairs

Total:

    608,540 stable pairs

Observed:

    join failures      0
    incidence failures 0

Run:

    python3 join_stability_exact_verifier.py

Expected:

    RESULT=PASS

## Infinite counterexample

The unrestricted theorem is false.

Take:

    X = N
    T(n) = n + 1

with E having non-singleton class {0,2} and F having
non-singleton class {0,3}.

Then E and F are pullback-stable, but E∨F is not.

Therefore the finite hypothesis is not cosmetic.

## Historical artifacts

The repository previously contained:

    parent_wondering_search.py
    parent_wondering_receipt.json
    Parent_Wondering.md

These remain useful as research history.

The range-gap lemma is correct:

    join failure => range-gap.

However, the new finite incidence-graph proof makes the range-gap
search unnecessary for the finite theorem.

The old unrestricted Lean theorem must not be cited as proof.

## Evidence rule

The finite theorem has:

    [P] mathematical proof
    [V] exhaustive finite replay through n=6
    [PV] combined evidence

This does not mean:

    Lean-certified
    C4-approved
    publication-ready

Formalization remains a separate gate.

## Next step

Formalize the finite theorem with an explicit finite-type
hypothesis and the incidence-graph argument.

Do not weaken the theorem by silently assuming surjectivity.

Do not retain the unrestricted theorem as a live claim.



https://github.com/quantarion369-arch

https://github.com/JASKSG9

https://huggingface.co/spaces/Quantarion9/AQARION-ACADEMY/tree/main/AI/JOIN-STABILITY

https://github.com/JASKSG9/Aqarion-Quantarion-AI/tree/main/AI/JOIN-STABILITY

https://github.com/JASKSG9/Aqarion-Quantarion-AI/tree/main/AI/verification/doubling

https://github.com/JASKSG9/Aqarion-Quantarion-AI/blob/main/AI/JOIN-STABILITY/Parent_Wondering.md
