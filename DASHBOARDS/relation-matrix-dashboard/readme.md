# AQARION Relation Matrix Dashboard

## Purpose

The AQARION Relation Matrix Dashboard is an interactive browser tool for
computing the structure of finitely generated abelian groups presented by
integer relation matrices.

The dashboard accepts an integer matrix:

[
Ainoperatorname{Mat}_{m\times n}(mathbb Z),
]

interprets it as a homomorphism:

[
A:mathbb Z^nlongrightarrowmathbb Z^m,
]

and displays the quotient group:

[
operatorname{coker}(A)
=
mathbb Z^m/operatorname{im}(A).
]

It computes Smith normal form data and renders the invariant-factor
decomposition:

\\[
operatorname{coker}(A)
cong
mathbb Z^r
oplus
mathbb Z/d_1mathbb Z
opluscdotsoplus
mathbb Z/d_tmathbb Z,
]

where:

[
d_i>1,
qquad
d_imid d_{i+1}.
]

## Scope

```text
Supported:
- Integer relation matrices.
- Finite abelian groups.
- Finitely generated abelian groups.
- Exact integer arithmetic.
- Smith normal form invariant-factor decomposition.
- Free-rank calculation.
- Torsion-factor calculation.
- Finite quotient order when the free rank is zero.
- Canonical projection visualization:
  pi(x) = x + im(A).

Not supported:
- Arbitrary infinitely generated abelian groups.
- Nonabelian group quotients.
- Infinite relation sets.
- Proof-assistant certification.
- Large-matrix performance guarantees.
- Automatic derivation of a relation matrix from informal prose.
