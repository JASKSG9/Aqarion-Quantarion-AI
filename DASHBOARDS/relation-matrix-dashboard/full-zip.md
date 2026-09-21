relation-matrix-dashboard/
```

It includes a full README, mathematical specification, input/output schema, example files, test checklist, generated-file policy, and a folder-local `.gitignore`.

The dashboard’s core convention is:

$$
A:\mathbb Z^n\longrightarrow\mathbb Z^m,
\qquad
\operatorname{coker}(A)
=
\mathbb Z^m/\operatorname{im}(A).
$$

If the Smith normal form is:

$$
UAV
=
D
=
\operatorname{diag}(d_1,\ldots,d_k,0,\ldots,0),
\qquad
d_i>0,
\qquad
d_i\mid d_{i+1},
$$

then:

$$
\operatorname{coker}(A)
\cong
\mathbb Z^{m-k}
\oplus
\bigoplus_{\substack{1\le i\le k\\d_i>1}}
\mathbb Z/d_i\mathbb Z.
$$

This is the standard invariant-factor decomposition obtained from integer row and column operations.[1][2]

## Final folder tree

```text
relation-matrix-dashboard/
├── README.md
├── MATHEMATICAL_SPECIFICATION.md
├── INPUT_OUTPUT_SCHEMA.md
├── TESTING.md
├── .gitignore
├── index.html
├── styles.css
├── app.js
├── examples/
│   ├── README.md
│   ├── cyclic-z12-mod-4.json
│   ├── diagonal-z4-z12.json
│   ├── free-plus-torsion.json
│   ├── zero-matrix.json
│   ├── noncyclic-z2-z2.json
│   └── mixed-relation-example.json
├── fixtures/
│   ├── README.md
│   └── snf-fixtures.json
└── artifacts/
    └── .gitkeep
```

Generated files belong only here:

```text
relation-matrix-dashboard/artifacts/
├── dashboard-receipt.sha256
├── dashboard-test-report.json
├── dashboard-test.log
└── local-session-notes.txt
```

***

# `relation-matrix-dashboard/README.md`

```markdown
# AQARION Relation Matrix Dashboard

## Purpose

The AQARION Relation Matrix Dashboard is an interactive browser tool for
computing the structure of finitely generated abelian groups presented by
integer relation matrices.

The dashboard accepts an integer matrix:

\[
A\in\operatorname{Mat}_{m\times n}(\mathbb Z),
\]

interprets it as a homomorphism:

\[
A:\mathbb Z^n\longrightarrow\mathbb Z^m,
\]

and displays the quotient group:

\[
\operatorname{coker}(A)
=
\mathbb Z^m/\operatorname{im}(A).
\]

It computes Smith normal form data and renders the invariant-factor
decomposition:

\\[
\operatorname{coker}(A)
\cong
\mathbb Z^r
\oplus
\mathbb Z/d_1\mathbb Z
\oplus\cdots\oplus
\mathbb Z/d_t\mathbb Z,
\]

where:

\[
d_i>1,
\qquad
d_i\mid d_{i+1}.
\]

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
```

## Matrix convention

The dashboard uses the **cokernel convention**:

\[
A:\mathbb Z^n\to\mathbb Z^m.
\]

The columns of \(A\) are relation vectors in the ambient free abelian group
\(\mathbb Z^m\).

The quotient represented by the matrix is:

\[
G
=
\operatorname{coker}(A)
=
\mathbb Z^m/\operatorname{im}(A).
\]

If a user begins with a group quotient \(G/H\), they must first form an
integer presentation whose relation subgroup includes:

1. The original torsion relations of \(G\).
2. The coordinate vectors generating \(H\).

The dashboard then computes the cokernel of that combined relation matrix.

## Smith normal form

The dashboard computes diagonal Smith data:

\[
UAV
=
D
=
\operatorname{diag}(d_1,\ldots,d_k,0,\ldots,0),
\]

where:

\[
d_i>0,
\qquad
d_i\mid d_{i+1}.
\]

The result is interpreted as:

\[
\operatorname{coker}(A)
\cong
\mathbb Z^{m-k}
\oplus
\bigoplus_{d_i>1}\mathbb Z/d_i\mathbb Z.
\]

Interpretation of diagonal entries:

| Smith diagonal entry | Quotient contribution |
|---|---|
| Missing pivot / trailing zero | One free \(\mathbb Z\) factor |
| \(1\) | Trivial \(\mathbb Z/1\mathbb Z\) factor; omitted |
| \(d>1\) | Torsion factor \(\mathbb Z/d\mathbb Z\) |

## Run locally

The dashboard is static HTML, CSS, and JavaScript. No package installation or
server framework is required.

From the repository root:

```bash
cd relation-matrix-dashboard
python -m http.server 8080
```

Open:

```text
http://localhost:8080
```

For Termux:

```bash
pkg install python
cd ~/Aqarion-Quantarion-AI/relation-matrix-dashboard
python -m http.server 8080
```

Then open:

```text
http://localhost:8080
```

## Quick examples

### Cyclic quotient

Use the relation matrix:

\[
A=
\begin{bmatrix}
12 & 4
\end{bmatrix}.
\]

This represents:

\[
\mathbb Z/\langle12,4\rangle.
\]

Since:

\[
\gcd(12,4)=4,
\]

the dashboard should display:

\[
\operatorname{coker}(A)
\cong
\mathbb Z/4\mathbb Z.
\]

This is the presentation-matrix form of:

\[
(\mathbb Z/12\mathbb Z)/\langle4\rangle.
\]

### Finite non-cyclic group

Use:

\[
A=
\begin{bmatrix}
2 & 0\\
0 & 2
\end{bmatrix}.
\]

The quotient is:

\[
\mathbb Z^2/
\left\langle
(2,0),(0,2)
\right\rangle
\cong
\mathbb Z/2\mathbb Z
\oplus
\mathbb Z/2\mathbb Z.
\]

This quotient is finite but not cyclic.

### Free plus torsion

Use:

\[
A=
\begin{bmatrix}
0\\
6
\end{bmatrix}.
\]

The quotient is:

\[
\mathbb Z^2/\langle(0,6)\rangle
\cong
\mathbb Z\oplus\mathbb Z/6\mathbb Z.
\]

### Free group

Use a matrix with two rows and zero columns:

\[
A:\mathbb Z^0\to\mathbb Z^2.
\]

Then:

\[
\operatorname{coker}(A)
\cong
\mathbb Z^2.
\]

## Canonical projection

The dashboard displays the canonical quotient projection:

\[
\pi:\mathbb Z^m\longrightarrow\operatorname{coker}(A),
\qquad
\pi(x)=x+\operatorname{im}(A).
\]

It records:

\[
\ker(\pi)=\operatorname{im}(A),
\]

and:

\[
\pi(0)=\operatorname{im}(A),
\]

which is the identity element of the quotient group.

The map preserves addition:

\[
\pi(x+y)
=
(x+y)+\operatorname{im}(A)
=
\pi(x)+\pi(y).
\]

## Folder map

```text
relation-matrix-dashboard/
├── README.md
├── MATHEMATICAL_SPECIFICATION.md
├── INPUT_OUTPUT_SCHEMA.md
├── TESTING.md
├── index.html
├── styles.css
├── app.js
├── examples/
├── fixtures/
└── artifacts/
```

| Path | Purpose |
|---|---|
| `index.html` | Dashboard layout and labels |
| `styles.css` | Dashboard visual styling |
| `app.js` | Matrix editor, exact integer arithmetic, SNF logic, rendering |
| `MATHEMATICAL_SPECIFICATION.md` | Formal convention and mathematical contract |
| `INPUT_OUTPUT_SCHEMA.md` | JSON-style input and output format |
| `TESTING.md` | Manual, fixture, and CI test procedures |
| `examples/` | Reusable relation-matrix examples |
| `fixtures/` | Expected structural outputs for regression checks |
| `artifacts/` | Generated local or CI receipts and logs |

## Generated artifact policy

The following files are generated and should not normally be committed:

```text
artifacts/*.json
artifacts/*.log
artifacts/*.sha256
artifacts/*.txt
```

The file:

```text
artifacts/.gitkeep
```

is retained so the directory exists in Git.

## Mathematical boundaries

The dashboard computes:

\[
\operatorname{coker}(A)=\mathbb Z^m/\operatorname{im}(A).
\]

It does not prove that a user-entered matrix correctly models an external
mathematical system. The user remains responsible for constructing the intended
presentation matrix.

The result is exact only relative to:

```text
- the entered integer matrix,
- the declared cokernel convention,
- the implemented Smith-normal-form algorithm,
- the browser's BigInt integer arithmetic.
```

## Governance status

```text
Mathematical scope:
Finitely generated abelian groups presented by finite integer matrices.

Formal proof:
OPEN.

Independent reproduction:
NOT CLAIMED.

C4:
BLOCKED.

Promotion:
false.

Publication readiness:
NOT CLAIMED.

Literature priority:
NOT CLAIMED.
```
```

***

# `relation-matrix-dashboard/MATHEMATICAL_SPECIFICATION.md`

```markdown
# Mathematical Specification

## 1. Presentation contract

The dashboard accepts an integer matrix:

\[
A\in\operatorname{Mat}_{m\times n}(\mathbb Z).
\]

It interprets that matrix as the homomorphism:

\[
A:\mathbb Z^n\longrightarrow\mathbb Z^m.
\]

The \(j\)-th column of \(A\) is the image of the standard generator
\(e_j\in\mathbb Z^n\). Therefore the relation subgroup is:

\[
\operatorname{im}(A)
=
\left\langle
A_{\ast1},\ldots,A_{\ast n}
\right\rangle
\le\mathbb Z^m.
\]

The group displayed by the dashboard is:

\[
\boxed{
\operatorname{coker}(A)
=
\mathbb Z^m/\operatorname{im}(A).
}
\]

## 2. Smith normal form contract

For every integer matrix \(A\), Smith normal form provides unimodular integer
matrices \(U\) and \(V\) such that:

\[
UAV=D,
\]

where:

\[
D=
\operatorname{diag}(d_1,\ldots,d_k,0,\ldots,0),
\]

with:

\[
d_i>0,
\qquad
d_i\mid d_{i+1}.
\]

Unimodular row and column transformations preserve the isomorphism class of
the cokernel. Therefore:

\[
\operatorname{coker}(A)
\cong
\operatorname{coker}(D).
\]

## 3. Quotient decomposition

If \(D\) has \(k\) nonzero diagonal entries, then:

\[
\operatorname{coker}(A)
\cong
\mathbb Z^{m-k}
\oplus
\mathbb Z/d_1\mathbb Z
\oplus\cdots\oplus
\mathbb Z/d_k\mathbb Z.
\]

The dashboard omits factors with:

\[
d_i=1,
\]

because:

\[
\mathbb Z/1\mathbb Z
\cong
0.
\]

Thus the displayed output is:

\[
\boxed{
\mathbb Z^{m-k}
\oplus
\bigoplus_{d_i>1}\mathbb Z/d_i\mathbb Z.
}
\]

## 4. Rank

The free rank of the quotient is:

\[
\operatorname{rank}_{\mathbb Z}\operatorname{coker}(A)
=
m-\operatorname{rank}_{\mathbb Q}(A).
\]

The Smith diagonal has exactly:

\[
k=\operatorname{rank}_{\mathbb Q}(A)
\]

nonzero entries.

Therefore:

\[
\boxed{
\text{free rank}=m-k.
}
\]

## 5. Finiteness and order

The quotient is finite if and only if its free rank is zero:

\[
\operatorname{coker}(A)
\text{ finite}
\iff
\operatorname{rank}_{\mathbb Q}(A)=m.
\]

When it is finite:

\[
\left|\operatorname{coker}(A)\right|
=
\prod_{d_i>1}d_i.
\]

If the free rank is positive, the quotient has infinite order.

## 6. Canonical projection

The quotient map is:

\[
\pi:\mathbb Z^m\longrightarrow\operatorname{coker}(A),
\qquad
\pi(x)=x+\operatorname{im}(A).
\]

It is a surjective group homomorphism:

\[
\pi(x+y)=\pi(x)+\pi(y).
\]

Its kernel is:

\[
\ker(\pi)=\operatorname{im}(A).
\]

The ambient identity maps to the quotient identity:

\[
\pi(0)=\operatorname{im}(A).
\]

## 7. Converting G/H to a relation matrix

Suppose:

\[
G
\cong
\mathbb Z^r
\oplus
\mathbb Z/n_1\mathbb Z
\oplus\cdots\oplus
\mathbb Z/n_t\mathbb Z.
\]

Let \(q=r+t\) be the number of displayed ambient generators.

To compute \(G/H\):

1. Start from the free abelian group \(\mathbb Z^q\).
2. Add a relation column \(n_i e_{r+i}\) for each torsion factor.
3. Add one relation column for each coordinate vector generating \(H\).
4. Compute the Smith normal form of the full relation matrix.

The resulting cokernel is:

\[
G/H.
\]

## 8. Cyclic quotient example

For:

\[
G=\mathbb Z/12\mathbb Z,
\qquad
H=\langle4\rangle,
\]

use:

\[
A=
\begin{bmatrix}
12 & 4
\end{bmatrix}.
\]

Then:

\[
\operatorname{im}(A)=\langle12,4\rangle=4\mathbb Z,
\]

so:

\[
\operatorname{coker}(A)
=
\mathbb Z/4\mathbb Z.
\]

This agrees with:

\[
(\mathbb Z/12\mathbb Z)/\langle4\rangle
\cong
\mathbb Z/\gcd(12,4)\mathbb Z
=
\mathbb Z/4\mathbb Z.
\]

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
```
```

***

# `relation-matrix-dashboard/INPUT_OUTPUT_SCHEMA.md`

```markdown
# Input and Output Schema

## Input matrix schema

The dashboard accepts a finite integer matrix.

```json
{
  "schema": "aqarion-relation-matrix-v1",
  "convention": "A: Z^n -> Z^m; output group is coker(A)=Z^m/im(A)",
  "matrix": [
[4][12]
  ]
}
```

## Input requirements

```text
- matrix must be an array of rows.
- every row must have the same number of columns.
- every entry must be a signed base-10 integer.
- a zero-column matrix is allowed.
- the dashboard UI currently limits matrix dimensions for browser usability.
```

## Meaning of dimensions

For:

```text
matrix shape = m × n
```

the dashboard uses:

```text
m = number of ambient generators in Z^m
n = number of relation columns
```

The relation subgroup is generated by the columns.

## Output schema

```json
{
  "schema": "aqarion-relation-matrix-result-v1",
  "input_shape": {
    "rows_m": 1,
    "columns_n": 2
  },
  "presentation": {
    "map": "A: Z^2 -> Z^1",
    "quotient": "coker(A)=Z^1/im(A)"
  },
  "smith_diagonal":,[3]
  "matrix_rank_over_Q": 1,
  "free_rank": 0,
  "torsion_invariant_factors":,[3]
  "canonical_structure": "Z/4Z",
  "finite": true,
  "quotient_order": 4,
  "projection": {
    "formula": "pi(x)=x+im(A)",
    "kernel": "im(A)",
    "identity_image": "pi(0)=im(A)",
    "surjective": true
  }
}
```

## Output field definitions

| Field | Meaning |
|---|---|
| `smith_diagonal` | Nonzero Smith diagonal entries, including any entries equal to \(1\) |
| `matrix_rank_over_Q` | Rank of \(A\) over \(\mathbb Q\) |
| `free_rank` | \(m-\operatorname{rank}_{\mathbb Q}(A)\) |
| `torsion_invariant_factors` | Smith factors greater than \(1\) |
| `canonical_structure` | Human-readable invariant-factor decomposition |
| `finite` | True exactly when free rank is zero |
| `quotient_order` | Product of torsion factors when finite; otherwise omitted or `null` |
| `projection` | Canonical quotient map and kernel summary |

## Zero-column example

```json
{
  "schema": "aqarion-relation-matrix-v1",
  "convention": "A: Z^0 -> Z^2; output group is coker(A)=Z^2",
  "matrix": [
    [],
    []
  ]
}
```

Expected output:

```json
{
  "smith_diagonal": [],
  "matrix_rank_over_Q": 0,
  "free_rank": 2,
  "torsion_invariant_factors": [],
  "canonical_structure": "Z^2",
  "finite": false,
  "quotient_order": null
}
```

## G/H conversion example

Suppose:

\[
G=
\mathbb Z
\oplus
\mathbb Z/4\mathbb Z
\oplus
\mathbb Z/12\mathbb Z,
\]

and:

\[
H=
\langle(2,1,3),(0,2,6)\rangle.
\]

The ambient free group has three generators. Add torsion columns:

\[
\begin{bmatrix}
0\\
4\\
0
\end{bmatrix},
\qquad
\begin{bmatrix}
0\\
0\\
12
\end{bmatrix},
\]

and subgroup columns:

\[
\begin{bmatrix}
2\\
1\\
3
\end{bmatrix},
\qquad
\begin{bmatrix}
0\\
2\\
6
\end{bmatrix}.
\]

The complete relation matrix is:

\[
A=
\begin{bmatrix}
0 & 0 & 2 & 0\\
4 & 0 & 1 & 2\\
0 & 12 & 3 & 6
\end{bmatrix}.
\]

The dashboard computes:

\[
\operatorname{coker}(A)\cong G/H.
\]

Do not claim a displayed quotient decomposition for this example without
executing the Smith normal form computation on the actual matrix.
```

***

# `relation-matrix-dashboard/TESTING.md`

```markdown
# Testing Guide

## Purpose

This document defines the minimum manual and automated checks for the AQARION
Relation Matrix Dashboard.

The dashboard is a static browser application. Its mathematical core is the
interpretation:

\[
A:\mathbb Z^n\to\mathbb Z^m,
\qquad
\operatorname{coker}(A)=\mathbb Z^m/\operatorname{im}(A).
\]

## Required static checks

From the repository root:

```bash
test -f relation-matrix-dashboard/index.html
test -f relation-matrix-dashboard/styles.css
test -f relation-matrix-dashboard/app.js
test -f relation-matrix-dashboard/README.md
test -f relation-matrix-dashboard/MATHEMATICAL_SPECIFICATION.md
test -f relation-matrix-dashboard/INPUT_OUTPUT_SCHEMA.md
test -f relation-matrix-dashboard/TESTING.md
node --check relation-matrix-dashboard/app.js
```

Validate JSON examples:

```bash
for file in relation-matrix-dashboard/examples/*.json; do
  python -m json.tool "$file" > /dev/null
done

python -m json.tool \
  relation-matrix-dashboard/fixtures/snf-fixtures.json \
  > /dev/null
```

## Required mathematical fixtures

| Fixture | Matrix | Expected quotient |
|---|---|---|
| Cyclic quotient | \([12\;\;4]\) | \(\mathbb Z/4\mathbb Z\) |
| Diagonal finite group | \(\operatorname{diag}(4,12)\) | \(\mathbb Z/4\mathbb Z\oplus\mathbb Z/12\mathbb Z\) |
| Free plus torsion | \(\begin{bmatrix}0\\6\end{bmatrix}\) | \(\mathbb Z\oplus\mathbb Z/6\mathbb Z\) |
| Free rank two | \(2\times0\) matrix | \(\mathbb Z^2\) |
| Non-cyclic finite | \(\operatorname{diag}(2,2)\) | \(\mathbb Z/2\mathbb Z\oplus\mathbb Z/2\mathbb Z\) |
| Trivial quotient | \([1]\) | \(0\) |
| Mixed relation | \(\begin{bmatrix}2&4\\0&6\end{bmatrix}\) | Verify against fixture result |

## Manual browser test

Start a local web server:

```bash
cd relation-matrix-dashboard
python -m http.server 8080
```

Open:

```text
http://localhost:8080
```

Then perform the following checks.

### Matrix editor

- [ ] Set rows to 1 and columns to 2.
- [ ] Enter `12` and `4`.
- [ ] Confirm matrix shape displays `1 × 2`.
- [ ] Click `Compute Smith normal form`.
- [ ] Confirm quotient displays `Z/4Z`.

### Diagonal finite group

- [ ] Load the `Z/4Z ⊕ Z/12Z` preset.
- [ ] Confirm the Smith diagonal displays `4, 12`.
- [ ] Confirm quotient order displays `48`.
- [ ] Confirm quotient displays two torsion factors.

### Free plus torsion

- [ ] Load the `Z ⊕ Z/6Z` preset.
- [ ] Confirm free rank is `1`.
- [ ] Confirm quotient order displays `infinite`.
- [ ] Confirm quotient displays `Z ⊕ Z/6Z`.

### Free group

- [ ] Load the free-group preset.
- [ ] Confirm the matrix editor accepts zero relation columns.
- [ ] Confirm quotient displays `Z^2`.
- [ ] Confirm Smith diagonal is empty.
- [ ] Confirm free rank is `2`.

### Non-cyclic quotient

- [ ] Load the `Z/2Z ⊕ Z/2Z` preset.
- [ ] Confirm quotient displays both factors.
- [ ] Confirm cyclic quotient field displays `no`.
- [ ] Confirm quotient order displays `4`.

### Projection display

For any nontrivial example:

- [ ] Confirm `pi(x)=x+im(A)` is shown.
- [ ] Confirm `ker(pi)=im(A)` is shown.
- [ ] Confirm `pi(0)=im(A)` is shown.
- [ ] Confirm projection is labelled a surjective homomorphism.

### Tooltip behavior

- [ ] Hover over each `?` button.
- [ ] Confirm explanatory text appears.
- [ ] Tab to a `?` button.
- [ ] Confirm tooltip appears on keyboard focus.
- [ ] Move focus away.
- [ ] Confirm tooltip disappears.

## Negative-input tests

| Input | Expected behavior |
|---|---|
| `1.5` | Reject as non-integer |
| `3/4` | Reject as non-integer |
| `abc` | Reject as non-integer |
| Empty matrix entry | Reject or treat only if deliberately normalized; current contract rejects |
| Unequal row length in imported JSON | Reject import |
| Matrix larger than UI limit | Reject or require source-code configuration change |
| Invalid dimension `m=0` | Reject in UI |
| Negative row or column count | Reject in UI |

## CI boundary

A successful static CI check means only:

```text
- Required files exist.
- JavaScript parses.
- JSON fixtures parse.
- Expected dashboard labels exist.
- Hash receipt was generated.
```

A successful static CI check does not itself prove the Smith normal form
algorithm correct for every integer matrix.

## Governance

```text
Finite fixture tests: required.
Browser manual test: required before release.
Formal proof: OPEN.
C4: BLOCKED.
Promotion: false.
```
```

***

# `relation-matrix-dashboard/.gitignore`

```gitignore
# Generated dashboard evidence
artifacts/*.json
artifacts/*.log
artifacts/*.sha256
artifacts/*.txt
artifacts/*.tmp

# Preserve the tracked directory marker
!artifacts/.gitkeep

# Editor and operating-system noise
.DS_Store
Thumbs.db
*.swp
*.swo
*~
```

***

# `relation-matrix-dashboard/examples/README.md`

```markdown
# Relation Matrix Examples

Each JSON file in this folder provides a reusable matrix example for the
AQARION Relation Matrix Dashboard.

## Convention

Every matrix is interpreted as:

\[
A:\mathbb Z^n\to\mathbb Z^m,
\]

with quotient:

\[
\operatorname{coker}(A)=\mathbb Z^m/\operatorname{im}(A).
\]

Columns are relation vectors.

## Included examples

| File | Relation matrix | Expected structure |
|---|---|---|
| `cyclic-z12-mod-4.json` | \([12\;\;4]\) | \(\mathbb Z/4\mathbb Z\) |
| `diagonal-z4-z12.json` | \(\operatorname{diag}(4,12)\) | \(\mathbb Z/4\mathbb Z\oplus\mathbb Z/12\mathbb Z\) |
| `free-plus-torsion.json` | \(\begin{bmatrix}0\\6\end{bmatrix}\) | \(\mathbb Z\oplus\mathbb Z/6\mathbb Z\) |
| `zero-matrix.json` | \(2\times0\) | \(\mathbb Z^2\) |
| `noncyclic-z2-z2.json` | \(\operatorname{diag}(2,2)\) | \(\mathbb Z/2\mathbb Z\oplus\mathbb Z/2\mathbb Z\) |
| `mixed-relation-example.json` | \(\begin{bmatrix}2&4\\0&6\end{bmatrix}\) | See fixture result |

## Import boundary

The present static dashboard does not require a file-import UI. These JSON files
serve as reproducible documented inputs and CI fixtures.

If file import is added later, validate:

```text
- schema name,
- rectangular matrix shape,
- integer-only entries,
- explicit cokernel convention.
```
```

***

# `relation-matrix-dashboard/examples/cyclic-z12-mod-4.json`

```json
{
  "schema": "aqarion-relation-matrix-v1",
  "name": "Cyclic quotient Z/12Z modulo <4>",
  "convention": "A: Z^n -> Z^m; output group is coker(A)=Z^m/im(A)",
  "matrix": [
    [12, 4]
  ],
  "expected": {
    "smith_diagonal": [4],
    "free_rank": 0,
    "torsion_invariant_factors": [4],
    "canonical_structure": "Z/4Z",
    "finite": true,
    "quotient_order": 4
  }
}
```

***

# `relation-matrix-dashboard/examples/diagonal-z4-z12.json`

```json
{
  "schema": "aqarion-relation-matrix-v1",
  "name": "Diagonal finite abelian group Z/4Z direct sum Z/12Z",
  "convention": "A: Z^n -> Z^m; output group is coker(A)=Z^m/im(A)",
  "matrix": [
    [4, 0],
    [0, 12]
  ],
  "expected": {
    "smith_diagonal": [4, 12],
    "free_rank": 0,
    "torsion_invariant_factors": [4, 12],
    "canonical_structure": "Z/4Z ⊕ Z/12Z",
    "finite": true,
    "quotient_order": 48
  }
}
```

***

# `relation-matrix-dashboard/examples/free-plus-torsion.json`

```json
{
  "schema": "aqarion-relation-matrix-v1",
  "name": "Free plus torsion group Z direct sum Z/6Z",
  "convention": "A: Z^n -> Z^m; output group is coker(A)=Z^m/im(A)",
  "matrix": [
    [0],
    [6]
  ],
  "expected": {
    "smith_diagonal": [6],
    "free_rank": 1,
    "torsion_invariant_factors": [6],
    "canonical_structure": "Z ⊕ Z/6Z",
    "finite": false,
    "quotient_order": null
  }
}
```

***

# `relation-matrix-dashboard/examples/zero-matrix.json`

```json
{
  "schema": "aqarion-relation-matrix-v1",
  "name": "Free rank two group",
  "convention": "A: Z^0 -> Z^2; output group is coker(A)=Z^2",
  "matrix": [
    [],
    []
  ],
  "expected": {
    "smith_diagonal": [],
    "free_rank": 2,
    "torsion_invariant_factors": [],
    "canonical_structure": "Z^2",
    "finite": false,
    "quotient_order": null
  }
}
```

***

# `relation-matrix-dashboard/examples/noncyclic-z2-z2.json`

```json
{
  "schema": "aqarion-relation-matrix-v1",
  "name": "Non-cyclic finite quotient Z/2Z direct sum Z/2Z",
  "convention": "A: Z^n -> Z^m; output group is coker(A)=Z^m/im(A)",
  "matrix": [
    [2, 0],
    [0, 2]
  ],
  "expected": {
    "smith_diagonal": [2, 2],
    "free_rank": 0,
    "torsion_invariant_factors": [2, 2],
    "canonical_structure": "Z/2Z ⊕ Z/2Z",
    "finite": true,
    "quotient_order": 4
  }
}
```

***

# `relation-matrix-dashboard/examples/mixed-relation-example.json`

```json
{
  "schema": "aqarion-relation-matrix-v1",
  "name": "Mixed two-generator relation example",
  "convention": "A: Z^n -> Z^m; output group is coker(A)=Z^m/im(A)",
  "matrix": [
    [2, 4],
    [0, 6]
  ],
  "expected": {
    "smith_diagonal": [2, 6],
    "free_rank": 0,
    "torsion_invariant_factors": [2, 6],
    "canonical_structure": "Z/2Z ⊕ Z/6Z",
    "finite": true,
    "quotient_order": 12
  }
}
```

***

# `relation-matrix-dashboard/fixtures/README.md`

```markdown
# Smith Normal Form Fixtures

The fixture file stores known input matrices and expected quotient invariants.

## Purpose

Fixtures are intended to detect regressions in:

```text
- Matrix orientation.
- Cokernel versus kernel confusion.
- Free-rank calculation.
- Omission of trivial Z/1Z factors.
- Torsion-factor ordering.
- Finite-order calculation.
- Non-cyclic quotient rendering.
```

## Mathematical convention

All fixtures use:

\[
A:\mathbb Z^n\to\mathbb Z^m,
\qquad
\operatorname{coker}(A)=\mathbb Z^m/\operatorname{im}(A).
\]

They do not use the transpose convention.

## Minimum fixture assertions

For each fixture:

```text
- Smith diagonal is divisibility ordered.
- Free rank is m minus the number of nonzero Smith factors.
- Torsion list omits only factors equal to 1.
- Finite order is the product of displayed torsion factors if free rank is zero.
- Infinite groups have quotient_order = null.
```
```

***

# `relation-matrix-dashboard/fixtures/snf-fixtures.json`

```json
{
  "schema": "aqarion-snf-fixtures-v1",
  "convention": "A: Z^n -> Z^m; output group is coker(A)=Z^m/im(A)",
  "fixtures": [
    {
      "id": "SNF-001",
      "name": "Cyclic quotient",
      "matrix": [
        [12, 4]
      ],
      "smith_diagonal": [4],
      "free_rank": 0,
      "torsion_invariant_factors": [4],
      "finite": true,
      "quotient_order": 4,
      "cyclic": true
    },
    {
      "id": "SNF-002",
      "name": "Diagonal finite quotient",
      "matrix": [
        [4, 0],
        [0, 12]
      ],
      "smith_diagonal": [4, 12],
      "free_rank": 0,
      "torsion_invariant_factors": [4, 12],
      "finite": true,
      "quotient_order": 48,
      "cyclic": false
    },
    {
      "id": "SNF-003",
      "name": "Free plus torsion",
      "matrix": [
        [0],
        [6]
      ],
      "smith_diagonal": [6],
      "free_rank": 1,
      "torsion_invariant_factors": [6],
      "finite": false,
      "quotient_order": null,
      "cyclic": false
    },
    {
      "id": "SNF-004",
      "name": "Free rank two",
      "matrix": [
        [],
        []
      ],
      "smith_diagonal": [],
      "free_rank": 2,
      "torsion_invariant_factors": [],
      "finite": false,
      "quotient_order": null,
      "cyclic": false
    },
    {
      "id": "SNF-005",
      "name": "Non-cyclic elementary 2-group",
      "matrix": [
        [2, 0],
        [0, 2]
      ],
      "smith_diagonal": [2, 2],
      "free_rank": 0,
      "torsion_invariant_factors": [2, 2],
      "finite": true,
      "quotient_order": 4,
      "cyclic": false
    },
    {
      "id": "SNF-006",
      "name": "Trivial quotient",
      "matrix": [
        [1]
      ],
      "smith_diagonal": [1],
      "free_rank": 0,
      "torsion_invariant_factors": [],
      "finite": true,
      "quotient_order": 1,
      "cyclic": true
    },
    {
      "id": "SNF-007",
      "name": "Mixed relation matrix",
      "matrix": [
        [2, 4],
        [0, 6]
      ],
      "smith_diagonal": [2, 6],
      "free_rank": 0,
      "torsion_invariant_factors": [2, 6],
      "finite": true,
      "quotient_order": 12,
      "cyclic": false
    }
  ]
}
```

***

# `relation-matrix-dashboard/artifacts/.gitkeep`

```text
Generated dashboard test reports, receipts, and local execution logs belong here.
```

## Recommended repository additions

Also add one file outside the dashboard folder:

```text
.github/workflows/relation-matrix-dashboard-check.yml
```

The workflow should validate:

```text
- Folder documentation exists.
- JavaScript parses with node --check.
- All example JSON files parse.
- Fixture JSON parses.
- Core labels exist.
- A SHA-256 receipt is created.
```

## Safe commit command

```bash
git add \
  relation-matrix-dashboard/README.md \
  relation-matrix-dashboard/MATHEMATICAL_SPECIFICATION.md \
  relation-matrix-dashboard/INPUT_OUTPUT_SCHEMA.md \
  relation-matrix-dashboard/TESTING.md \
  relation-matrix-dashboard/.gitignore \
  relation-matrix-dashboard/examples \
  relation-matrix-dashboard/fixtures \
  relation-matrix-dashboard/artifacts/.gitkeep

git commit -m "Document relation matrix Smith normal form dashboard"
```

## Important correction before committing

Your browser dashboard must be tested against the supplied fixtures before public use. In particular, it must correctly distinguish:

$$
\mathbb Z/2\mathbb Z\oplus\mathbb Z/2\mathbb Z
$$

from:

$$
\mathbb Z/4\mathbb Z.
$$

Both groups have order $$4$$, but only the latter is cyclic. That distinction is exactly why invariant factors—not only quotient order—must be displayed.

Citations:
[1] RES.18-012 (Spring 2022) Lecture 21: Smith Normal Form https://ocw.mit.edu/courses/res-18-012-algebra-ii-student-notes-spring-2022/mit18_702s22_lect21.pdf
[2] Introduction to Algebraic Number Theory https://wstein.org/129-05/notes/129.pdf
[3] https://en.wikipedia.org/wiki/Kaprekar's_routine
[4] https://huggingface.co/Quantarion9
[5] Smith normal form - Reed College https://people.reed.edu/~davidp/361/lectures/08wed.pdf
[6] https://github.com/JASKSG9/AQARION-ARITHMETIC-FDS-FINITE-DYNAMICAL-SYSTEMS-/blob/main/CHECKPOINT.MD
[7] https://math.nyu.edu/~tschinke/.manin/submitted/ConnesConsaniMarcolli.pdf
[8] https://alainconnes.org/publications/
[9] Lecture 10 : Smith normal form - Reed College https://people.reed.edu/~davidp/cameroon/lectures/10lecture.pdf
[10] Finitely generated abelian groups - Harvard University https://people.math.harvard.edu/archive/129_spring_04/ant/html/node9.html
[11] Math 129: Algebraic Number Theory Tuesdays and ... https://wstein.org/edu/Spring2004/129/lectures/day1/day1.pdf
[12] Smith normal form - Wikipedia https://en.wikipedia.org/wiki/Smith_normal_form
[13] Finitely generated abelian group - Wikipedia https://en.wikipedia.org/wiki/Finitely_generated_abelian_group
[14] [PDF] Structure theorem for finitely generated abelian groups https://people.reed.edu/~davidp/361/lectures/08fri.pdf
[15] Finitely Generated Abelian Groups - wstein https://wstein.org/books/ant/ant/node10.html
