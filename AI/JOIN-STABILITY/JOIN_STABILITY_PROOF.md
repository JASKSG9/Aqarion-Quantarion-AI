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

AQARION JOIN-STABILITY — CANONICAL MATHEMATICAL RECORD


Status


Finite theorem:        PROVED
Arbitrary-set theorem: REFUTED
Surjective theorem:    PROVED CONDITIONALLY
Lean:                  OPEN
C4:                    BLOCKED
Promotion:             FALSE




1. Finite theorem


Let X be finite.


Let


[
T:X\to X
]


and let E,F be equivalence relations on X.


Assume


[
T(x)E T(y)\Longrightarrow xEy
]


and


[
T(x)F T(y)\Longrightarrow xFy.
]


Then


[
T(x)(E\vee F)T(y)\Longrightarrow x(E\vee F)y.
]


Equivalently,


[
T^{-1}(E\vee F)\subseteq E\vee F.
]



2. Induced permutation on E-classes


Let Q_E=X/E.


For an E-class A, define


[
S_A={[T(x)]_E:x\in A}.
]


Each S_A is nonempty.


Suppose A\ne B and


[
C\in S_A\cap S_B.
]


Then there exist


[
x\in A,\qquad y\in B
]


such that


[
T(x)E T(y).
]


Pullback stability gives


[
xEy,
]


contradicting A\ne B.


Thus the nonempty sets S_A are pairwise disjoint.


There are finitely many E-classes and the same number of target
E-classes. Therefore every S_A contains exactly one target
class.


Hence T induces a permutation


[
\sigma_E:Q_E\to Q_E.
]


The identical argument gives a permutation


[
\sigma_F:Q_F\to Q_F.
]



3. Incidence graph


Construct the bipartite graph H(E,F).


Its left vertices are the E-classes.


Its right vertices are the F-classes.


There is an edge between A\in Q_E and B\in Q_F iff


[
A\cap B\ne\varnothing.
]


Every x\in X determines an incidence edge


[
e_x=([x]_E,[x]_F).
]


Because


[
x\in A\cap B
]


implies


[
T(x)\in\sigma_E(A)\cap\sigma_F(B),
]


the map


[
(A,B)\mapsto
(\sigma_E(A),\sigma_F(B))
]


maps incidence edges to incidence edges.


Since \sigma_E and \sigma_F are permutations, this edge map
is injective.


The incidence graph is finite.


Therefore the edge map is bijective and hence an automorphism.



4. Incidence components equal join classes


Two points x,y\in X are related by E\vee F exactly when
their incidence edges e_x,e_y lie in the same connected component
of H(E,F).


Suppose


[
T(x)(E\vee F)T(y).
]


Then


[
e_{T(x)}
]


and


[
e_{T(y)}
]


are in the same connected component.


But


[
e_{T(x)}=\Phi(e_x),
\qquad
e_{T(y)}=\Phi(e_y),
]


where \Phi is the graph automorphism above.


Graph automorphisms preserve connected components.


Therefore e_x,e_y are in the same component.


Hence


[
x(E\vee F)y.
]


Thus


[
\boxed{
T^{-1}(E\vee F)\subseteq E\vee F.
}
]


QED.



5. Why the unrestricted theorem fails


Take


[
X=\mathbb N,
\qquad
T(n)=n+1.
]


Let E have one non-singleton class


[
{0,2},
]


with all other classes singleton.


Let F have one non-singleton class


[
{0,3},
]


with all other classes singleton.


Since


[
\operatorname{im}(T)={1,2,3,\ldots},
]


there are no image points a,b with


[
aEb
]


through the exceptional E-class {0,2}, except for the
trivial situation involving the reachable point 2 and the
unreachable point 0.


Likewise for F.


Hence both E and F are pullback-stable.


But


[
2E0F3,
]


so


[
2(E\vee F)3.
]


Meanwhile


[
1\not(E\vee F)2.
]


Since


[
T(1)=2,\qquad T(2)=3,
]


we have


[
T(1)(E\vee F)T(2)
]


but


[
1\not(E\vee F)2.
]


Therefore


[
\boxed{
T^{-1}(E\vee F)\not\subseteq E\vee F.
}
]


The unrestricted theorem is false.



6. Range-Gap Lemma


Let


[
G=E\vee F.
]


Assume E and F are pullback-stable.


If


[
T^{-1}(G)\not\subseteq G,
]


then there exist x,y such that


[
x\not Gy,
\qquad
Tx,G,Ty,
]


and every G-path from Tx to Ty has an internal vertex
outside


[
\operatorname{im}(T).
]


Proof


Assume instead that a G-path exists entirely inside the image:


[
Tx=z_0,z_1,\ldots,z_k=Ty.
]


For every z_i, choose w_i with


[
T(w_i)=z_i.
]


Every consecutive pair is either E-related or F-related.


If


[
z_iEz_{i+1},
]


then pullback stability gives


[
w_iEw_{i+1}.
]


Similarly for F.


Thus


[
w_0Gw_1G\cdots Gw_k.
]


Since w_0=x and w_k=y,


[
xGy,
]


contradiction.


Therefore a genuine failure requires a range gap.


QED.



7. Surjective generalization


Let X be arbitrary.


Suppose T:X\to X is surjective and


[
T^{-1}(E)\subseteq E,
\qquad
T^{-1}(F)\subseteq F.
]


Then


[
T^{-1}(E\vee F)\subseteq E\vee F.
]


Proof


Because T is surjective,


[
\operatorname{im}(T)=X.
]


Therefore no join path can contain a vertex outside the image.


By the Range-Gap Lemma, a failure of join stability is impossible.


Hence


[
T^{-1}(E\vee F)\subseteq E\vee F.
]


QED.


This theorem shows that surjectivity is a sufficient replacement for
finiteness.



8. Compactness does not suffice


Compactness plus continuity is not enough.


A one-point compactification of the infinite construction gives a
compact Hausdorff space and continuous T while preserving the
hidden range bridge.


Therefore no claim of the form


compact X + continuous T
    => join stability



is valid without additional hypotheses.



9. Formalization status


The mathematical finite proof is complete at the paper-proof level.


The following remain OPEN:


Lean implementation
Lean compilation
Lean axiom report
independent formal verification
C4
publication



The old unrestricted Lean statement must not be promoted.


The correct formal target is the finite theorem with an explicit
finite hypothesis, plus a separate surjective theorem.



10. Evidence boundary


Computational enumeration can verify finite instances.


It cannot by itself establish the mathematical theorem unless the
enumeration is tied to a complete proof or complete formal model.


Likewise:


zero sampled counterexamples



does not mean


no counterexample exists.



The explicit infinite counterexample prevents that interpretation
for the unrestricted theorem.



