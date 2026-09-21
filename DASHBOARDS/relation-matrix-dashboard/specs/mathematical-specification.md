
***

# `relation-matrix-dashboard/MATHEMATICAL_SPECIFICATION.md`

```markdown
# Mathematical Specification

## 1. Presentation contract

The dashboard accepts an integer matrix:

[
Ainoperatorname{Mat}_{m\times n}(mathbb Z).
]

It interprets that matrix as the homomorphism:

[
A:mathbb Z^nlongrightarrowmathbb Z^m.
]

The (j)-th column of (A) is the image of the standard generator
(e_jinmathbb Z^n). Therefore the relation subgroup is:

[
operatorname{im}(A)
=
leftlangle
A_{ast1},ldots,A_{ast n}

ight
angle
lemathbb Z^m.
]

The group displayed by the dashboard is:

[
\boxed{
operatorname{coker}(A)
=
mathbb Z^m/operatorname{im}(A).
}
]

## 2. Smith normal form contract

For every integer matrix (A), Smith normal form provides unimodular integer
matrices (U) and (V) such that:

[
UAV=D,
]

where:

[
D=
operatorname{diag}(d_1,ldots,d_k,0,ldots,0),
]

with:

[
d_i>0,
qquad
d_imid d_{i+1}.
]

Unimodular row and column transformations preserve the isomorphism class of
the cokernel. Therefore:

[
operatorname{coker}(A)
cong
operatorname{coker}(D).
]

## 3. Quotient decomposition

If (D) has (k) nonzero diagonal entries, then:

[
operatorname{coker}(A)
cong
mathbb Z^{m-k}
oplus
mathbb Z/d_1mathbb Z
opluscdotsoplus
mathbb Z/d_kmathbb Z.
]

The dashboard omits factors with:

[
d_i=1,
]

because:

[
mathbb Z/1mathbb Z
cong
0.
]

Thus the displayed output is:

[
\boxed{
mathbb Z^{m-k}
oplus
\bigoplus_{d_i>1}mathbb Z/d_imathbb Z.
}
]

## 4. Rank

The free rank of the quotient is:

[
operatorname{rank}_{mathbb Z}operatorname{coker}(A)
=
m-operatorname{rank}_{mathbb Q}(A).
]

The Smith diagonal has exactly:

[
k=operatorname{rank}_{mathbb Q}(A)
]

nonzero entries.

Therefore:

[
\boxed{
\text{free rank}=m-k.
}
]

## 5. Finiteness and order

The quotient is finite if and only if its free rank is zero:

[
operatorname{coker}(A)
\text{ finite}
iff
operatorname{rank}_{mathbb Q}(A)=m.
]

When it is finite:

[
left|operatorname{coker}(A)
ight|
=
prod_{d_i>1}d_i.
]

If the free rank is positive, the quotient has infinite order.

## 6. Canonical projection

The quotient map is:

[
pi:mathbb Z^mlongrightarrowoperatorname{coker}(A),
qquad
pi(x)=x+operatorname{im}(A).
]

It is a surjective group homomorphism:

[
pi(x+y)=pi(x)+pi(y).
]

Its kernel is:

[
ker(pi)=operatorname{im}(A).
]

The ambient identity maps to the quotient identity:

[
pi(0)=operatorname{im}(A).
]

## 7. Converting G/H to a relation matrix

Suppose:

[
G
cong
mathbb Z^r
oplus
mathbb Z/n_1mathbb Z
opluscdotsoplus
mathbb Z/n_tmathbb Z.
]

Let (q=r+t) be the number of displayed ambient generators.

To compute (G/H):

1. Start from the free abelian group (mathbb Z^q).
2. Add a relation column (n_i e_{r+i}) for each torsion factor.
3. Add one relation column for each coordinate vector generating (H).
4. Compute the Smith normal form of the full relation matrix.

The resulting cokernel is:

[
G/H.
]

## 8. Cyclic quotient example

For:

[
G=mathbb Z/12mathbb Z,
qquad
H=langle4
angle,
]

use:

[
A=
\begin{bmatrix}
12 & 4
end{bmatrix}.
]

Then:

[
operatorname{im}(A)=langle12,4
angle=4mathbb Z,
]

so:

[
operatorname{coker}(A)
=
mathbb Z/4mathbb Z.
]

This agrees with:

[
(mathbb Z/12mathbb Z)/langle4
angle
cong
mathbb Z/gcd(12,4)mathbb Z
=
mathbb Z/4mathbb Z.
]

## 9. Non-claims

The dashboard does not claim:

```text
- Lean, Coq, Isabelle, or other machine formalization.
- Independent proof of any user-supplied presentation.
- General nonabelian quotient support.
- Arbitrary infinite-dimensional group support.
- Literature priority.
- C4 approval.
- Promotion.
- Publication readiness.
