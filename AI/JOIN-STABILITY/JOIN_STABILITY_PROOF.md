# AQARION JOIN-STABILITY — Finite Join Theorem

Status: [P] mathematical proof

## Theorem

Let X be finite, let T : X -> X, and let E,F be equivalence relations on X.

Assume

    T(x) E T(y) => x E y

and

    T(x) F T(y) => x F y.

Then

    T(x) (E ∨ F) T(y) => x (E ∨ F) y.

Equivalently,

    T^{-1}(E ∨ F) ⊆ E ∨ F.

The finiteness hypothesis is essential.

---

## 1. Stable equivalence classes are permuted

Let Q_E be the finite set of E-classes.

For an E-class A define

    S_A = { [T(x)]_E : x ∈ A }.

Each S_A is nonempty.

Suppose A and B are distinct E-classes and some E-class C belongs
to both S_A and S_B.

Then there exist x ∈ A and y ∈ B such that

    T(x) E T(y).

Pullback stability gives

    x E y,

contradicting A ≠ B.

Therefore the nonempty sets S_A are pairwise disjoint.

There are exactly |Q_E| source classes and |Q_E| target classes.
Hence every S_A contains exactly one target class.

Therefore T induces a map

    σ_E : Q_E -> Q_E

and σ_E is a permutation.

The same argument gives a permutation

    σ_F : Q_F -> Q_F.

---

## 2. Incidence graph

Construct the bipartite graph H(E,F):

Left vertices:
    E-classes.

Right vertices:
    F-classes.

There is an edge A-B iff

    A ∩ B ≠ ∅.

For x ∈ X define its incidence edge

    e_x = ([x]_E, [x]_F).

Every graph edge occurs as e_x for some x.

If e_x = (A,B), then

    T(x) ∈ σ_E(A) ∩ σ_F(B).

Therefore

    Φ(A,B) = (σ_E(A), σ_F(B))

maps every incidence edge to an incidence edge.

Because σ_E and σ_F are permutations, Φ is injective.
The incidence-edge set is finite, so Φ is bijective.

Thus Φ is a graph automorphism.

Consequently Φ permutes the connected components of H(E,F).

---

## 3. Components are join classes

Two points x,y are E∨F-related exactly when their incidence
edges e_x and e_y belong to the same connected component of H(E,F).

This is precisely the definition of equivalence closure of the
union E ∪ F.

Suppose now that

    T(x) (E∨F) T(y).

Then

    e_{T(x)}

and

    e_{T(y)}

belong to the same connected component of H(E,F).

But

    e_{T(x)} = Φ(e_x)
    e_{T(y)} = Φ(e_y).

Since Φ is a graph automorphism, two edges lie in the same component
iff their Φ-images lie in the same component.

Therefore

    e_x

and

    e_y

belong to the same component.

Hence

    x (E∨F) y.

Therefore

    T^{-1}(E∨F) ⊆ E∨F.

QED.

---

## 4. Why the old unrestricted Lean theorem is invalid

The theorem is NOT valid for arbitrary Type.

Take

    X = N

and

    T(n) = n + 1.

Let E have the unique non-singleton class

    {0,2}

and let F have the unique non-singleton class

    {0,3}.

Both E and F are pullback-stable.

The image of T is

    {1,2,3,...},

so the exceptional class containing 0 never creates a violation
of the pullback condition.

However

    2 E∨F 3

through

    2 E 0 F 3.

But

    1 not E∨F 2.

Since

    T(1)=2
    T(2)=3,

we obtain

    T(1) E∨F T(2)

while

    1 not E∨F 2.

Thus

    T^{-1}(E∨F) not⊆ E∨F.

Therefore the current unrestricted Lean statement must not be
promoted.

The finite theorem is the correct theorem.

---

## 5. Computational verification

Independent exact enumeration:

    n=1:       1 stable pair
    n=2:       8
    n=3:       84
    n=4:       1,276
    n=5:       24,475
    n=6:       582,696

Total:

    608,540 stable E,F pairs.

Results:

    join failures       = 0
    incidence failures  = 0

This is [V], not a substitute for the proof.

Together with the proof:

    theorem status = [PV]

Formal Lean certification remains separate:

    Lean = OPEN

---

## 6. Important semantic firewall

This theorem does NOT establish

    T^{-1}(E∨F)
        =
    T^{-1}(E) ∨ T^{-1}(F).

That stronger distribution identity remains a separate statement.

The theorem established here is only:

    E,F individually pullback-stable
        =>
    E∨F pullback-stable.

Do not merge these claims.

---

## 7. Repository disposition

The existing unrestricted:

    PullbackStableJoin.lean

should be treated as a historical/formalization candidate and
NOT as a certified theorem.

The replacement target is:

    finite_pullback_stable_join

with an explicit finite-type hypothesis.

The next formalization should encode the incidence-graph argument,
not attempt to force the old EquivGen induction through a non-image
transitivity node.



