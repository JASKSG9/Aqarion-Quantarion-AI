# AQARION Spectral Dashboard  
## Adversarial comparison: finite rank–kernel theorem vs. zeta-zero models

**Lead recommendation:** split the work into two tracks that must never be conflated:

1. **AQ-RK-001:** formalize the corrected finite-dimensional rank/kernel/spectral equivalence in Lean, with exact arithmetic or symbolic linear algebra.
2. **AQ-ZETA-BENCH-001:** build a reproducible *negative-control benchmark suite* for finite dynamical zeta functions, Fibonacci/Sturmian statistics, and Mandelbrot-grid coarsening diagnostics.

Neither track is a numerical approximation to the Riemann Hypothesis, and neither currently provides a spectral realization of zeta zeros. Connes’ adelic programme and Weil’s explicit formula are appropriate conceptual reference points, but they impose substantially stronger analytic and representation-theoretic requirements than any finite matrix benchmark described here.[1][2][3]

## Dashboard

| Model / theorem | Mathematical target | Iteration or size parameter | Exactness / convergence object | Stability metric | Computational complexity | Current defensible status |
|---|---|---:|---|---|---|---|
| **AQ-RK-001** corrected `RankKerOnePerp` | Rank deficiency, nonzero kernel, zero-sum kernel under $$\mathbf1^\top A=\mathbf1^\top$$, and spectral equivalence for $$I-A^\top A$$ | Matrix dimension $$n$$ | Exact finite linear-algebra equivalence | Smallest singular value $$\sigma_{\min}(A)$$; exact nullity; residual $$\|Av\|_2$$ | Dense SVD: $$O(n^3)$$; exact elimination: roughly polynomial in $$n$$ and bit size | **Proof target**; not yet kernel-accepted |
| AQ generic defect identity | $$U^\top D^\top DU=U^\top K^\top KU-A^\top A$$ | Matrix dimensions $$n,m$$ | Exact symbolic identity | Frobenius residual $$\|LHS-RHS\|_F$$; exact ring equality in Lean | Dense multiplication: $$O(n^3)$$, often reducible with structure | **Best immediate Lean lock** |
| SV-001-V2 finite replay | Equal-block cyclic defect identity on $$m,k\in\{2,\dots,8\}$$ | 1,176 contracted cases | Exhaustive finite-domain verification | Max Gram/trace/norm error; mutation kills; receipt hash binding | Small matrices; practical bounded computation | **[V]**, user-supplied Termux evidence; no theorem/promotion |
| Kaprekar finite zeta | Fixed-point counts and finite dynamical zeta for declared map | State count $$N=10{,}000$$; iterate depth | Exhaustive finite functional-graph classification | Exact integer counts; fixed-point-count consistency | $$O(Nh)$$ direct; $$O(N)$$ graph decomposition | **Computed benchmark**, not RH evidence |
| Fibonacci/Sturmian benchmark | Two-gap property and finite Fourier signatures | Word length $$N$$, FFT length $$N$$ | Finite symbolic/diffraction statistic | Gap set, balance defect, peak location/amplitude, window sensitivity | Word generation $$O(N)$$; FFT $$O(N\log N)$$ | **Proof + computation**, but adversarial negative control |
| Mandelbrot grid fragmentation | Escape-time grid and partition/coarsening diagnostic $$c_S-c_G$$ | Grid dimensions $$W\times H$$, iteration cap $$N_{\max}$$ | Bounded numerical classification | Escape-time reproducibility, precision sensitivity, grid-refinement drift, enclosure radius | $$O(WHN_{\max})$$ | **Computed diagnostic** only |
| Connes adelic trace framework | Trace interpretation of Weil explicit formula and positivity formulation related to RH | Test-function support, prime/place cutoffs, analytic regularization | Infinite-dimensional analytic trace formula | Regularization error, cutoff dependence, positivity-functional residual, theorem hypotheses | Not reducible to a fixed finite $$n$$-step benchmark | **Literature framework**, not implemented here |
| Weil explicit-formula computation | Explicit relation among primes, archimedean terms, and zeta zeros | Height $$T$$, prime cutoff, test-function bandwidth | Rigorous finite-height zero certification only with analytic error bounds | Turing count residual, interval width, explicit-formula truncation/tail bound | Depends on algorithm; typically superlinear in height/sample scale | **External established methodology**, no AQARION implementation shown |

## Mathematical baseline

### Correct AQ-RK theorem

The useful finite-dimensional theorem should be divided into components.

Let

$$
A\in\mathbb R^{n\times n},
\qquad
\mathbf1=(1,\dots,1)^\top,
\qquad
\mathbf1^\top A=\mathbf1^\top.
$$

Then:

$$
\operatorname{rank}(A)<n
\iff
\ker(A)\neq\{0\}.
$$

Further, column-stochasticity implies that all kernel vectors have zero coordinate sum:

$$
Av=0
\Longrightarrow
\mathbf1^\top v
=
\mathbf1^\top Av
=
0.
$$

Therefore:

$$
\boxed{
\operatorname{rank}(A)<n
\iff
\exists v\neq0:
\left(\sum_i v_i=0\right)\wedge Av=0.
}
$$

Separately, for any real square matrix $$A$$,

$$
\ker A\neq\{0\}
\iff
\ker(A^\top A)\neq\{0\}
\iff
0\in\sigma(A^\top A).
$$

Hence:

$$
\boxed{
\operatorname{rank}(A)<n
\iff
1\in\sigma(I-A^\top A).
}
$$

The latter equivalence does **not** require column-stochasticity. Column-stochasticity supplies the zero-sum statement; the Gram/spectrum relation supplies the spectral statement.

### Numerical interpretation

In floating point, exact rank is discontinuous. The stable computational analogue is the smallest singular value:

$$
\sigma_{\min}(A).
$$

The exact theorem detects:

$$
\sigma_{\min}(A)=0.
$$

A numerical experiment can only report a tolerance-qualified claim:

$$
\sigma_{\min}(A)\le\tau.
$$

That is not the same as rank deficiency unless:

- $$A$$ is represented exactly over $$\mathbb Q$$, $$\mathbb Z$$, or a finite field; or
- interval / validated linear algebra proves that zero lies in the relevant singular-value enclosure; or
- a symbolic certificate supplies an exact null vector $$v$$.

This **conditioning gap** is the most important issue to add to AQARION’s evidence architecture. A matrix theorem may be exact, but a numerical rank detector can be badly unstable close to singularity.

## Convergence and stability dashboard

### Metric definitions

| Metric | Definition | What it detects | Limitation |
|---|---|---|---|
| Kernel residual | $$\rho_{\ker}=\|Av\|_2/\|v\|_2$$ | Whether a proposed null vector approximately satisfies $$Av=0$$ | A small residual does not prove an exact null vector |
| Smallest singular value | $$\sigma_{\min}(A)$$ | Distance-to-singularity in spectral norm | Threshold choice is model- and precision-dependent |
| Spectral-gap surrogate | $$\gamma_{\mathrm{gram}}=\min_{\lambda\in\sigma(A^\top A)\setminus\{0\}}\lambda$$ | Separation of zero singular modes from nonzero modes | Requires a stable multiplicity decision |
| Trace-formula residual | $$|\mathcal E_{\mathrm{explicit}}(f;T,P)|$$ | Discrepancy after finite zero/prime/place truncation | Requires a rigorously derived remainder term |
| Turing-count residual | $$|N_{\mathrm{zeros}}(T)-N_{\mathrm{expected}}(T)|$$ | Whether a computed zero list is complete through a height bound | Needs rigorously controlled argument variation and error bounds |
| FFT peak stability | $$\max_k|\widehat x_k|$$ under window/length/normalization perturbations | Whether a claimed peak is robust | A spectral peak is not a theorem-level arithmetic correspondence |
| Escape classification margin | $$\min_{j\le N}||z_j|-R|$$ | Sensitivity of escape status to numerical error | Near-boundary points require validated enclosure methods |
| Grid refinement drift | Difference in statistic between resolutions $$h$$ and $$h/2$$ | Whether a grid diagnostic is resolution-sensitive | Does not prove a continuum limit |
| Receipt reproducibility | Matching source/contract/output hashes or stated tolerance agreement | Provenance and rerun integrity | Not semantic correctness or proof |

### Expected behavior by benchmark

| Benchmark | Primary convergence axis | Stable outcome | Instability / adversarial trigger | Required evidence object |
|---|---|---|---|---|
| AQ-RK-001 | Increasing arithmetic precision or exact-domain representation | Exact nullity and a symbolic null vector remain unchanged | $$\sigma_{\min}$$ near machine epsilon; apparent rank changes under tolerance | Exact matrix input, null vector, exact verification, Lean theorem receipt |
| Generic projector-Gram | Matrix dimension and randomized/property-test cases | Algebraic residual identically zero in exact algebra | Incorrect assumptions: non-orthonormal $$U$$, wrong defect ordering, transpose error | Lean proof plus finite regression fixtures |
| SV-001-V2 | Full contracted domain; hardware/environment replay | 1,176 finite cases remain pass with stated tolerance | $$m/k$$ role swap, wrong $$U$$ scale, `residue_mod_m`, wrong $$D$$ ordering | Contract, source hash, full receipt, semantic mutation report |
| Kaprekar | Exhaustive state enumeration | Fixed-point/basin counts invariant under reimplementation | Leading-zero convention, repdigit handling, iteration-count convention | State-transition contract and exact counts |
| Fibonacci | Increasing word length, FFT window, encoding choice | Two-gap property remains exact; recognized peak tracks known discrete structure | Window leakage, aliasing, normalization changes, false $$\varphi$$-pattern inference | Word-generation seed, FFT convention, raw arrays, multi-window report |
| Mandelbrot | Grid refinement, precision, escape cap | Exterior escape certificates remain stable away from boundary | Boundary sensitivity, finite cap, float overflow/roundoff, changing partitions | Grid contract, precision record, enclosure or unresolved classification |
| Connes/Weil prototype | Test-function support, cutoff scale, regularization | A theorem-backed truncated formula converges inside proved bounds | Uncontrolled tails, ad hoc operator discretization, unproved positivity | Analytic proof of truncation/remainder plus executable certificate |

## Performance benchmarks

No executable source, committed benchmark harness, or reproducible raw timing data for the proposed Connes/Weil or AQ-ZETA spectral implementations has been supplied. It would be fabrication to report milliseconds, iteration counts, convergence curves, or numerical stability figures for those models.

The following is therefore a **benchmark specification**, not measured performance.

### AQ-RK-001 benchmark plan

| Scale | Input family | Exact reference | Numerical route | Operations to record |
|---:|---|---|---|---|
| $$n=2$$–$$8$$ | Rational/integer column-stochastic matrices, including singular and nonsingular cases | Symbolic rank and rational nullspace | Float64 SVD, high-precision SVD, interval test | $$\sigma_{\min}$$, nullity, residual, condition number, runtime |
| $$n=9$$–$$64$$ | Sparse stochastic matrices with planted zero-sum kernel | Constructed exact null vector | Sparse QR/SVD or exact modular rank | Iterations, fill-in, residual, memory |
| $$n=65+$$ | Structured block and graph-derived matrices | Exact construction witness where possible | Iterative eigensolver on $$A^\top A$$ | Lanczos iterations, Ritz residual, precision sensitivity |

Recommended test families:

1. **Well-conditioned singular family**
   $$
   A=
   \begin{pmatrix}
   1&1\\
   0&0
   \end{pmatrix}
   $$
   after column-stochastic normalization, with a known zero-sum kernel witness where applicable.

2. **Near-singular family**
   $$
   A_\varepsilon=A_0+\varepsilon E,
   $$
   where $$A_0$$ is rank-deficient and $$E$$ preserves the required column-sum constraint.

3. **Permutation family**
   Column-stochastic and orthogonal, with full rank:
   $$
   A^\top A=I.
   $$
   This is a negative control: $$1\notin\sigma(I-A^\top A)$$.

4. **Graph/coarsening family**
   Matrices induced from AQARION partitions or quotient constructions, with exact rational weights.

### Required AQ-RK metrics

For each matrix $$A$$, record:

$$
n,\quad
\operatorname{rank}_{\mathbb Q}(A),\quad
\dim\ker A,\quad
\sigma_{\min}^{(p)}(A),\quad
\kappa_2(A)\ \text{if full rank},
$$

$$
\rho_{\ker}^{(p)}
=
\frac{\|A\hat v\|_2}{\|\hat v\|_2},
\qquad
\delta_{\mathrm{sum}}^{(p)}
=
\left|\sum_i \hat v_i\right|,
$$

where $$p$$ is the arithmetic precision. A valid numerical convergence dashboard should report whether these values stabilize as $$p$$ increases:

$$
p\in\{53,106,212,424\}\text{ bits}.
$$

The exact rank/nullspace computation is the reference. Floating-point performance is secondary and should never overwrite the exact classification.

### Complexity comparison

| Method | Dominant cost | Space | Conditioning sensitivity | Can certify exact theorem? |
|---|---:|---:|---|---|
| Dense QR/SVD for $$A\in\mathbb R^{n\times n}$$ | $$O(n^3)$$ | $$O(n^2)$$ | High near singularity | No, absent validated/exact arithmetic |
| Sparse Lanczos on $$A^\top A$$ | Roughly $$O(k\,\mathrm{nnz}(A))$$ for $$k$$ iterations | Sparse plus Krylov basis | High if smallest eigenvalues cluster | No, unless rigorously enclosed |
| Exact Gaussian elimination over $$\mathbb Q$$ | Polynomial but coefficient-growth sensitive | Potentially large | None at mathematical level | Yes, for exact input |
| Modular rank + Chinese remaindering | Polynomial; practical for integer/rational matrices | Moderate | None at mathematical level | Yes, with reconstruction certificate |
| Lean proof | Human/proof-engineering dominated | Proof artifact size | No numerical conditioning | Yes, if no `sorry`/untrusted axioms beyond policy |
| Finite dynamical census | $$O(|X|h)$$ direct | $$O(|X|)$$ | No floating error if exact transitions | Yes for the declared finite system |
| Mandelbrot escape grid | $$O(WHN_{\max})$$ | $$O(WH)$$ if stored | Extreme near boundary | Exterior escape only unless validated bounds |
| Explicit-formula / zero verification | Depends on height, test function, zero-counting method | Data and precision dependent | Requires rigorous analytic error control | Finite-height claims only, not RH |

## Connes and Weil alignment

### What Connes’ framework actually contributes

The relevant conceptual chain is:

$$
\text{Weil explicit formula}
\longleftrightarrow
\text{trace-formula interpretation}
\longleftrightarrow
\text{positivity criterion related to RH}.
$$

The adelic class space is presented in the Connes–Consani–Marcolli programme as a noncommutative geometric setting in which the Weil explicit formula receives a trace-formula interpretation; the associated positivity formulation is related to the Riemann Hypothesis.[1][2][3]

This supports a **design principle** for AQARION:

> If a spectral claim is made, expose the operator, its domain, the trace/test-function class, the regularization, the approximation scheme, and the error bounds.

It does **not** support any claim that:

- a finite dynamical zeta function realizes Riemann zeros;
- Fibonacci FFT peaks approximate the zero spectrum;
- a Mandelbrot coarsening defect produces a self-adjoint RH operator;
- a finite matrix $$I-A^\top A$$ is an adelic trace operator;
- a successful numerical benchmark is evidence for RH.

### Weil explicit formula versus AQ-RK-001

| Dimension | AQ-RK-001 | Weil explicit formula / Connes programme |
|---|---|---|
| Object | Finite real matrix $$A$$ | Global arithmetic distribution, test functions, primes, zeros, archimedean terms |
| Main claim | Exact finite matrix equivalence | Analytic relation among arithmetic and spectral data |
| Spectrum | Finite spectrum of $$I-A^\top A$$ | Zeta-zero spectral/absorption interpretation in a much richer setting |
| Error model | Exact algebra or numerical conditioning | Cutoffs, regularization, analytic continuation, explicit remainder estimates |
| Certificate | Lean proof, exact null vector, source-bound receipt | Theorem-level analytic proof plus rigorously controlled finite computations |
| RH relevance | None by itself | Directly related at the conceptual/theoretical level |
| Appropriate AQARION role | Formal finite infrastructure benchmark | Literature reference and boundary condition |

The recent literature continues to describe Connes’ approach in terms of an adelic trace formula and a positivity condition associated with the explicit formula. It remains a research programme, not an executable finite-matrix recipe for proving RH.[3][4]

## Adversarial benchmark audit

### Case A — Rank/kernel theorem

**Strengths**

- The theorem is finite-dimensional and mathematically precise.
- Exact arithmetic can eliminate numerical ambiguity.
- The zero-sum kernel implication follows directly from the column-sum condition.
- The spectral equivalence through $$A^\top A$$ is standard finite-dimensional linear algebra.
- It is appropriate for Lean formalization.

**Failure modes**

- Floating rank detection can flip under tolerance selection.
- A theorem statement using `sorry` is not kernel-accepted.
- Matrix notation in Lean can mismatch row/column-vector conventions.
- `spectrum` APIs may refer to bounded operators rather than raw matrices, requiring explicit coercions.
- “Column stochastic” must mean precisely:
  $$
  \mathbf1^\top A=\mathbf1^\top,
  $$
  not merely nonnegative entries or a different row-oriented convention.

**Verdict:** highest-value theorem track, but only after splitting it into exact lemmas and adding exact-input benchmark matrices.

### Case B — Kaprekar dynamical zeta

**Strengths**

- Fully finite and exhaustively reproducible.
- Strong test of functional-graph and fixed-point-count infrastructure.
- Dynamical zeta identity is exactly checkable from cycle decomposition.

**Failure modes**

- “At most seven iterations” depends on digit, leading-zero, repdigit, and iteration-count conventions.
- A finite dynamical zeta can be zero-free for elementary finite-graph reasons.
- Zero-freeness is not an analogue of RH.

The well-known four-digit routine reaches 6174 within seven iterations for non-repdigit inputs under common conventions, but some source presentations count steps differently, so your contract must fix the convention.[5][6]

**Verdict:** retain as a finite reproducibility benchmark and negative control only.

### Case C — Fibonacci/Sturmian versus zeta-zero statistics

**Strengths**

- Sturmian balance and two-gap behavior are mathematically meaningful and suitable for exact combinatorial tests.
- FFT computation is inexpensive and useful for reproducibility practice.
- It works as an adversarial example against vague “aperiodicity implies RH-like spectrum” narratives.

**Failure modes**

- Finite FFT peaks depend on word length, windowing, encoding, and normalization.
- Matching a feature near a golden-ratio-derived frequency does not identify a Riemann-zero mechanism.
- A comparison to GUE-like spacings requires a precisely sourced, normalized zero dataset and controlled statistical methodology.

**Verdict:** strong negative control; no spectral-realization claim.

### Case D — Mandelbrot coarsening diagnostic

**Strengths**

- Useful for testing whether a graph coarsening procedure destroys filamentary structure.
- Grid and escape contracts can be versioned and replayed.
- Effective-resistance versus greedy coarsening is a credible algorithmic comparison topic.

**Failure modes**

- Escape times near the Mandelbrot boundary are numerically sensitive.
- A fixed $$100\times100$$ or $$20\times20$$ grid is not a continuum statement.
- $$c_S-c_G$$ depends on partition, threshold band, graph construction, and support convention.
- “Effective resistance equals zero” requires exact statement of the graph, components, and pseudoinverse convention.

**Verdict:** retain as a scoped numerical/coarsening diagnostic, not a complex-dynamics theorem or RH bridge.

### Case E — Connes/Weil model

**Strengths**

- The only item in the dashboard directly connected to a serious trace-formula/positivity formulation of RH.
- Demands the right kind of mathematical rigor: operator domain, trace regularization, positivity, and analytic error control.

**Failure modes**

- It cannot be reduced honestly to “iterate a finite matrix until its eigenvalues resemble zeta zeros.”
- A discretized operator can produce visually suggestive spectra without preserving the required trace formula.
- Finite zero checks—even rigorous finite-height checks—do not prove RH.
- The literature contains many non-peer-reviewed or speculative “spectral” claims; treat preprints as leads, not validated foundations.

**Verdict:** literature-alignment target only until a precise operator, theorem statement, and rigorous approximation theory are specified.

## New lead: AQ-Conditioning-Core

The most important missing work is not another zeta benchmark. It is a **conditioning and certification layer** for all finite spectral computations.

### Why it matters

AQARION currently distinguishes computation, receipt provenance, and formal proof. It should also distinguish:

$$
\text{exact singularity}
\quad\text{from}\quad
\text{numerically near-singular}.
$$

Without that layer, a model can mistakenly elevate a tiny singular value to a kernel vector, or mistake numerical noise for a spectral gap.

### Proposed deliverable

Create:

```text
verification/aq_conditioning/
├── contract.json
├── exact_rank.py
├── numerical_svd.py
├── interval_spectral.py
├── adversarial_families.py
├── report.py
├── receipt/
│   ├── schema.json
│   └── writer.py
└── fixtures/
    ├── singular_exact.json
    ├── near_singular_eps.json
    ├── stochastic_kernel.json
    └── permutation_negative_control.json
```

### Core contract fields

```json
{
  "claim_id": "AQ-CONDITIONING-001",
  "matrix_domain": "rational",
  "numerical_precisions_bits": [53, 106, 212, 424],
  "rank_method_exact": "fraction_free_elimination",
  "rank_method_numeric": "svd",
  "singular_value_thresholds": [1e-10, 1e-12, 1e-14],
  "required_metrics": [
    "exact_rank",
    "exact_nullity",
    "sigma_min",
    "kernel_residual",
    "sum_constraint_residual",
    "condition_number",
    "precision_stability"
  ],
  "promotion_allowed": false
}
```

### Acceptance rules

| Rule | Pass criterion |
|---|---|
| Exact rank | Matches known fixture rank exactly |
| Exact kernel witness | $$Av=0$$ under exact arithmetic |
| Column-sum condition | $$\mathbf1^\top A=\mathbf1^\top$$ exactly |
| Zero-sum consequence | $$\sum_i v_i=0$$ exactly |
| Float stability | Report precision-dependent $$\sigma_{\min}$$; do not claim rank from tolerance alone |
| Adversarial near-singularity | Demonstrate at least one case where float threshold classification changes while exact rank does not |
| Receipt validity | Hashes bind contract, fixture, executable, environment, and output |
| Governance | No theorem/promotion change from runtime success alone |

This produces a reusable numerical-honesty substrate for SV-001, AQ-ZETA, rank/kernel experiments, and future Mandelbrot work.

## Concrete next steps

1. **Write AQ-RK-001 as four Lean lemmas.**  
   Start with the zero-sum-kernel lemma, then rank/nullity, then the Gram/eigenvector lemma, then any `spectrum` wrapper.

2. **Formalize generic projector identities first.**  
   Lock:
   $$
   ((I-P)KP)^2=0
   $$
   for $$P^2=P$$, and the corrected Gram identity under $$U^\top U=I$$.

3. **Build AQ-Conditioning-Core.**  
   This is the missing technical layer that makes numerical spectral claims auditable.

4. **Repair and freeze AQ-ZETA-BENCH-001.**  
   Correct syntax, define every map explicitly, derive zeta functions from actual cycle decompositions, and stop calling toy permutations “Kaprekar.”

5. **Add a Connes/Weil boundary note to every zeta benchmark receipt.**  
   Use a mandatory field:
   ```json
   "rh_relation": "none; finite benchmark only"
   ```

6. **Do not create “spectral realization iterations” until an operator is specified.**  
   For Connes/Weil, define the Hilbert space, domain, action, regularization, trace class or distributional framework, cutoff mechanism, and proof-backed error bound first. Without these, an iteration count has no mathematical interpretation.

7. **Keep governance unchanged.**  
   C4 remains blocked; Lean remains open until no-`sorry` compilation and axiom audit; publication remains blocked; promotion remains false.

## Bottom line

The RankKerOnePerp line is stable as an **exact finite-dimensional theorem programme**, not as a convergence model for zeta zeros. Its proper performance metrics are rank, nullity, singular-value separation, exact null-vector certificates, and precision sensitivity—not “spectral realization iterations.”

Connes’ adelic trace framework and Weil’s explicit formula are relevant because they define the level of structure a genuine RH-facing spectral programme would need: a well-defined analytic operator framework, trace formula, regularization, positivity relation, and rigorous control of all limits. They do not validate any currently described AQARION finite spectral benchmark as an RH model.[1][2][3]

The highest-value original contribution to make next is **AQ-Conditioning-Core**: an exact-versus-numerical rank and singular-value certification harness. It will make every later AQARION spectral computation more reproducible, more adversarially robust, and more honest—without changing C4, publication, or promotion status.Build an interactive spectral comparison dashboard evaluating Alain Connes' semi-local trace formula approach against the classical Riemann-Siegel formula and Turing's method for verifying Riemann zeta zeros. Include comparative metrics on computational convergence rates, spectral norm stability for increasing zero indices (n=1 to 10^6), sensitivity to rank-deficiency in the underlying matrix distributions, and error-bound rigor. Visualize the spectral gaps and zero-distribution density differences between these models using interactive plots, and provide a summary of the computational complexity scaling for each method

You have established the **documentation and contract shell** for `AQARION-CONDITION8NG`. The safe next step is to add only executable, schema, fixture, and validation files whose behavior is fully specified by the exact-versus-numerical conditioning objective—without claiming any benchmark result until the files are actually run.

## Important naming decision

Your repository name appears to be intentionally spelled:

```text
AQARION-CONDITION8NG
```

Keep that spelling consistently in repository metadata, URLs, receipts, and workflow names. Inside Python, use a valid import-safe package directory such as:

```text
aq_conditioning/
```

Avoid a Python module named `aq_condition8ng` unless you truly want that spelling everywhere. The digit is valid in a Python identifier after the first character, but `aq_conditioning` is clearer and avoids semantic drift between the repository name and the mathematical role.

## Recommended file tree

Add this structure beneath the repository root:

```text
AQARION-CONDITION8NG/
│
├── README.md                         [already created]
├── FILETREE.md                       [already created]
├── CONTRACT.json                     [already created — verify exact filename]
├── .gitignore
├── LICENSE                           [optional; choose deliberately]
│
├── aq_conditioning/
│   ├── __init__.py
│   ├── canonical.py
│   ├── exact_rank.py
│   ├── numerical_svd.py
│   ├── invariants.py
│   ├── fixtures.py
│   ├── report.py
│   ├── replay.py
│   └── self_audit.py
│
├── fixtures/
│   ├── singular_exact.json
│   ├── full_rank_permutation.json
│   ├── near_singular_epsilon.json
│   ├── column_stochastic_kernel.json
│   └── malformed_negative_control.json
│
├── schema/
│   ├── contract.schema.json
│   ├── fixture.schema.json
│   └── receipt.schema.json
│
├── verification/
│   ├── manifest.json
│   ├── run_all.py
│   ├── metamorphic.py
│   └── mutation/
│       ├── __init__.py
│       └── executor.py
│
├── artifacts/
│   └── .gitkeep
│
├── docs/
│   ├── EVIDENCE-MODEL.md
│   ├── NUMERICAL-BOUNDARY.md
│   ├── GOVERNANCE.md
│   └── BENCHMARK-PROTOCOL.md
│
└── .github/
    └── workflows/
        └── conditioning-ci.yml
```

Do not create benchmark output receipts, timing tables, or “pass” badges yet. Those are runtime evidence and should be generated only after execution.

***

# 1. `.gitignore`

Create this exact file:

```gitignore
# Python
__pycache__/
*.py[cod]
*.pyo
*.pyd
.venv/
venv/
env/

# Test and coverage
.pytest_cache/
.coverage
htmlcov/
.mypy_cache/
.ruff_cache/

# Local environments and editor state
.env
.idea/
.vscode/
*.swp

# Runtime-generated evidence
artifacts/*
!artifacts/.gitkeep

# OS files
.DS_Store
Thumbs.db
```

This permits the folder to exist while preventing runtime receipts from being accidentally committed as if they were source evidence.

***

# 2. `aq_conditioning/__init__.py`

```python
"""AQARION-CONDITION8NG exact-versus-numerical conditioning toolkit."""

__version__ = "0.1.0"
```

The version is a source declaration only. Do not call it a released or verified version until a release policy and execution receipt exist.

***

# 3. `aq_conditioning/canonical.py`

This file canonicalizes JSON before hashing. Deterministic serialization is essential: otherwise two semantically identical JSON objects can hash differently because of whitespace or key order.

```python
from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any


def canonical_json_bytes(value: Any) -> bytes:
    text = json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
        allow_nan=False,
    )
    return text.encode("utf-8")


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_json(value: Any) -> str:
    return sha256_bytes(canonical_json_bytes(value))


def load_json(path: str | Path) -> Any:
    with Path(path).open("r", encoding="utf-8") as handle:
        return json.load(handle)


def sha256_file(path: str | Path) -> str:
    digest = hashlib.sha256()
    with Path(path).open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()
```

***

# 4. `aq_conditioning/fixtures.py`

This loader keeps fixture parsing separate from mathematics.

```python
from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from pathlib import Path
from typing import Any

from .canonical import load_json, sha256_file


@dataclass(frozen=True)
class MatrixFixture:
    fixture_id: str
    description: str
    matrix: tuple[tuple[Fraction, ...], ...]
    expected: dict[str, Any]
    source_path: str
    source_sha256: str

    @property
    def nrows(self) -> int:
        return len(self.matrix)

    @property
    def ncols(self) -> int:
        return len(self.matrix[0]) if self.matrix else 0


def parse_fraction(value: int | float | str) -> Fraction:
    if isinstance(value, int):
        return Fraction(value, 1)
    if isinstance(value, str):
        return Fraction(value)
    raise TypeError(
        "Fixture entries must be integers or exact rational strings; "
        f"received {type(value).__name__}."
    )


def load_fixture(path: str | Path) -> MatrixFixture:
    path = Path(path)
    raw = load_json(path)

    rows = raw["matrix"]
    matrix = tuple(
        tuple(parse_fraction(entry) for entry in row)
        for row in rows
    )

    if not matrix:
        raise ValueError("Fixture matrix must be nonempty.")

    width = len(matrix[0])
    if width == 0 or any(len(row) != width for row in matrix):
        raise ValueError("Fixture matrix must be rectangular.")

    return MatrixFixture(
        fixture_id=raw["fixture_id"],
        description=raw["description"],
        matrix=matrix,
        expected=raw["expected"],
        source_path=str(path),
        source_sha256=sha256_file(path),
    )
```

The fixture format intentionally allows only exact integers and rational strings such as `"1/2"`. It does **not** allow JSON decimals such as `0.1`, because binary floating-point literals would weaken the exact reference layer.

***

# 5. `aq_conditioning/exact_rank.py`

This computes exact rank over rational numbers using fraction-free-style row elimination with Python’s `Fraction`. It is suitable for small to moderate audit fixtures, not presented as a high-performance exact-linear-algebra engine.

```python
from __future__ import annotations

from fractions import Fraction
from typing import Iterable


MatrixQ = list[list[Fraction]]


def copy_matrix(matrix: Iterable[Iterable[Fraction]]) -> MatrixQ:
    return [list(row) for row in matrix]


def exact_rank(matrix: Iterable[Iterable[Fraction]]) -> int:
    work = copy_matrix(matrix)

    if not work:
        return 0

    nrows = len(work)
    ncols = len(work[0])

    if any(len(row) != ncols for row in work):
        raise ValueError("Matrix must be rectangular.")

    pivot_row = 0
    rank = 0

    for col in range(ncols):
        pivot = next(
            (row for row in range(pivot_row, nrows) if work[row][col] != 0),
            None,
        )

        if pivot is None:
            continue

        work[pivot_row], work[pivot] = work[pivot], work[pivot_row]

        pivot_value = work[pivot_row][col]
        work[pivot_row] = [value / pivot_value for value in work[pivot_row]]

        for row in range(nrows):
            if row == pivot_row:
                continue

            factor = work[row][col]
            if factor == 0:
                continue

            work[row] = [
                work[row][j] - factor * work[pivot_row][j]
                for j in range(ncols)
            ]

        rank += 1
        pivot_row += 1

        if pivot_row == nrows:
            break

    return rank


def exact_nullity(matrix: Iterable[Iterable[Fraction]]) -> int:
    copied = copy_matrix(matrix)

    if not copied:
        return 0

    return len(copied[0]) - exact_rank(copied)


def is_square(matrix: Iterable[Iterable[Fraction]]) -> bool:
    copied = copy_matrix(matrix)
    return bool(copied) and len(copied) == len(copied[0])


def column_sums(matrix: Iterable[Iterable[Fraction]]) -> list[Fraction]:
    copied = copy_matrix(matrix)

    if not copied:
        return []

    ncols = len(copied[0])
    return [
        sum((copied[row][col] for row in range(len(copied))), Fraction(0, 1))
        for col in range(ncols)
    ]


def is_column_stochastic_in_sum_sense(
    matrix: Iterable[Iterable[Fraction]],
) -> bool:
    return all(value == 1 for value in column_sums(matrix))
```

The phrase “column-stochastic in sum sense” is intentional. Classical stochasticity also usually requires nonnegative entries. The rank/kernel theorem only needs the column-sum identity:

$$
\mathbf1^\top A=\mathbf1^\top.
$$

If nonnegativity matters for a later theorem, add it as a separate explicitly tested invariant.

***

# 6. `aq_conditioning/numerical_svd.py`

This is the approximate layer. It must never overwrite the exact rank result.

```python
from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from typing import Iterable

import numpy as np


@dataclass(frozen=True)
class NumericalSpectrum:
    singular_values: tuple[float, ...]
    sigma_min: float
    sigma_max: float
    condition_number: float | None
    numerical_rank: int
    rank_tolerance: float


def to_float64(matrix: Iterable[Iterable[Fraction]]) -> np.ndarray:
    return np.array(
        [[float(value) for value in row] for row in matrix],
        dtype=np.float64,
    )


def compute_svd(
    matrix: Iterable[Iterable[Fraction]],
    rank_tolerance: float,
) -> NumericalSpectrum:
    array = to_float64(matrix)
    singular_values = np.linalg.svd(array, compute_uv=False)

    if singular_values.size == 0:
        raise ValueError("SVD requires a nonempty matrix.")

    sigma_max = float(singular_values[0])
    sigma_min = float(singular_values[-1])

    if sigma_min == 0.0:
        condition_number = None
    else:
        condition_number = sigma_max / sigma_min

    numerical_rank = int(np.sum(singular_values > rank_tolerance))

    return NumericalSpectrum(
        singular_values=tuple(float(value) for value in singular_values),
        sigma_min=sigma_min,
        sigma_max=sigma_max,
        condition_number=condition_number,
        numerical_rank=numerical_rank,
        rank_tolerance=rank_tolerance,
    )
```

The numerical-rank threshold must be emitted into every receipt. Otherwise a reported numerical rank is incomplete evidence.

***

# 7. `aq_conditioning/invariants.py`

This file verifies algebraic conditions and makes the exact-versus-approximate distinction visible.

```python
from __future__ import annotations

from fractions import Fraction
from typing import Iterable

from .exact_rank import (
    column_sums,
    copy_matrix,
    exact_nullity,
    exact_rank,
    is_column_stochastic_in_sum_sense,
    is_square,
)


def matrix_vector_mul(
    matrix: Iterable[Iterable[Fraction]],
    vector: Iterable[Fraction],
) -> list[Fraction]:
    rows = copy_matrix(matrix)
    vec = list(vector)

    if not rows or len(rows[0]) != len(vec):
        raise ValueError("Matrix-vector dimensions do not match.")

    return [
        sum(
            (entry * vec[col] for col, entry in enumerate(row)),
            Fraction(0, 1),
        )
        for row in rows
    ]


def verify_zero_sum_kernel_witness(
    matrix: Iterable[Iterable[Fraction]],
    vector: Iterable[Fraction],
) -> dict[str, object]:
    vec = list(vector)
    image = matrix_vector_mul(matrix, vec)

    return {
        "witness_nonzero": any(value != 0 for value in vec),
        "sum_of_coordinates": str(sum(vec, Fraction(0, 1))),
        "kernel_image": [str(value) for value in image],
        "is_exact_kernel_vector": all(value == 0 for value in image),
        "is_zero_sum": sum(vec, Fraction(0, 1)) == 0,
    }


def exact_matrix_summary(
    matrix: Iterable[Iterable[Fraction]],
) -> dict[str, object]:
    copied = copy_matrix(matrix)
    nrows = len(copied)
    ncols = len(copied[0]) if copied else 0

    return {
        "shape": [nrows, ncols],
        "is_square": is_square(copied),
        "exact_rank": exact_rank(copied),
        "exact_nullity": exact_nullity(copied),
        "column_sums": [str(value) for value in column_sums(copied)],
        "column_sum_invariant_holds": is_column_stochastic_in_sum_sense(copied),
    }
```

***

# 8. `aq_conditioning/report.py`

This generates a JSON-serializable result object. It does not write output; writing belongs to the replay layer.

```python
from __future__ import annotations

from fractions import Fraction
from typing import Any

from .fixtures import MatrixFixture
from .invariants import exact_matrix_summary, verify_zero_sum_kernel_witness
from .numerical_svd import compute_svd


def parse_vector(values: list[int | str]) -> list[Fraction]:
    parsed: list[Fraction] = []

    for value in values:
        if isinstance(value, int):
            parsed.append(Fraction(value, 1))
        elif isinstance(value, str):
            parsed.append(Fraction(value))
        else:
            raise TypeError("Kernel witness values must be integers or rational strings.")

    return parsed


def evaluate_fixture(
    fixture: MatrixFixture,
    rank_tolerance: float,
) -> dict[str, Any]:
    exact = exact_matrix_summary(fixture.matrix)
    numeric = compute_svd(fixture.matrix, rank_tolerance)

    report: dict[str, Any] = {
        "fixture_id": fixture.fixture_id,
        "description": fixture.description,
        "fixture_path": fixture.source_path,
        "fixture_sha256": fixture.source_sha256,
        "expected": fixture.expected,
        "exact": exact,
        "numerical": {
            "singular_values": list(numeric.singular_values),
            "sigma_min": numeric.sigma_min,
            "sigma_max": numeric.sigma_max,
            "condition_number": numeric.condition_number,
            "numerical_rank": numeric.numerical_rank,
            "rank_tolerance": numeric.rank_tolerance,
        },
        "checks": {},
    }

    expected_rank = fixture.expected.get("exact_rank")
    if expected_rank is not None:
        report["checks"]["exact_rank_matches_expected"] = (
            exact["exact_rank"] == expected_rank
        )

    expected_nullity = fixture.expected.get("exact_nullity")
    if expected_nullity is not None:
        report["checks"]["exact_nullity_matches_expected"] = (
            exact["exact_nullity"] == expected_nullity
        )

    expected_column_sum = fixture.expected.get("column_sum_invariant_holds")
    if expected_column_sum is not None:
        report["checks"]["column_sum_invariant_matches_expected"] = (
            exact["column_sum_invariant_holds"] == expected_column_sum
        )

    witness_raw = fixture.expected.get("kernel_witness")
    if witness_raw is not None:
        witness = parse_vector(witness_raw)
        witness_result = verify_zero_sum_kernel_witness(fixture.matrix, witness)
        report["kernel_witness"] = witness_result

        report["checks"]["kernel_witness_matches_expectation"] = (
            witness_result["is_exact_kernel_vector"]
            == fixture.expected.get("kernel_witness_is_exact", True)
        )

        report["checks"]["zero_sum_witness_matches_expectation"] = (
            witness_result["is_zero_sum"]
            == fixture.expected.get("kernel_witness_zero_sum", True)
        )

    report["all_declared_checks_pass"] = all(report["checks"].values())
    return report
```

***

# 9. `aq_conditioning/replay.py`

This is the canonical initial replay. It validates that all fixture outcomes agree with their declared expected values and writes a runtime report only into `artifacts/`.

```python
from __future__ import annotations

import argparse
import json
import platform
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import numpy as np

from .canonical import sha256_file, sha256_json
from .fixtures import load_fixture
from .report import evaluate_fixture


DEFAULT_FIXTURES = [
    "fixtures/singular_exact.json",
    "fixtures/full_rank_permutation.json",
    "fixtures/near_singular_epsilon.json",
    "fixtures/column_stochastic_kernel.json",
]


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def runtime_environment() -> dict[str, str]:
    return {
        "python_version": sys.version,
        "python_implementation": platform.python_implementation(),
        "platform": platform.platform(),
        "machine": platform.machine(),
        "numpy_version": np.__version__,
    }


def load_contract(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--contract", default="CONTRACT.json")
    parser.add_argument("--output", default="artifacts/conditioning-receipt.json")
    parser.add_argument("--rank-tolerance", type=float, default=1e-12)
    parser.add_argument("fixtures", nargs="*", default=DEFAULT_FIXTURES)
    args = parser.parse_args()

    contract_path = Path(args.contract)
    output_path = Path(args.output)

    contract = load_contract(contract_path)
    results = []

    for fixture_path in args.fixtures:
        fixture = load_fixture(fixture_path)
        result = evaluate_fixture(fixture, args.rank_tolerance)
        results.append(result)

    passed = all(item["all_declared_checks_pass"] for item in results)

    payload = {
        "schema_id": "AQ-CONDITIONING-RECEIPT-001",
        "generated_at_utc": utc_now(),
        "claim_id": contract.get("claim_id"),
        "contract_path": str(contract_path),
        "contract_sha256": sha256_file(contract_path),
        "contract_canonical_sha256": sha256_json(contract),
        "runtime": runtime_environment(),
        "rank_tolerance": args.rank_tolerance,
        "fixture_count": len(results),
        "fixtures": results,
        "status": "PASS" if passed else "FAIL",
        "governance": {
            "finite_computational_evidence_only": True,
            "formal_proof": False,
            "c4": "BLOCKED",
            "publication": "BLOCKED",
            "promotion_allowed": False,
        },
    }

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(payload, indent=2, sort_keys=True),
        encoding="utf-8",
    )

    print(
        json.dumps(
            {
                "status": payload["status"],
                "fixture_count": payload["fixture_count"],
                "output": str(output_path),
            },
            sort_keys=True,
        )
    )

    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
```

This file does **not** claim independent reproduction, formal proof, or stable numerical rank. It only creates a finite execution report.

***

# 10. Fixtures

## `fixtures/singular_exact.json`

```json
{
  "fixture_id": "AQ-COND-FIX-001",
  "description": "Exact singular rational matrix with known nullity one.",
  "matrix": [
    ["1", "2"],
    ["2", "4"]
  ],
  "expected": {
    "exact_rank": 1,
    "exact_nullity": 1,
    "column_sum_invariant_holds": false,
    "kernel_witness": ["2", "-1"],
    "kernel_witness_is_exact": true,
    "kernel_witness_zero_sum": false
  }
}
```

This fixture intentionally violates the column-sum condition. It prevents the project from accidentally treating “every kernel vector is zero-sum” as a universal fact.

## `fixtures/full_rank_permutation.json`

```json
{
  "fixture_id": "AQ-COND-FIX-002",
  "description": "Permutation matrix negative control: exact full rank and no nonzero kernel.",
  "matrix": [
    ["0", "1", "0"],
    ["0", "0", "1"],
    ["1", "0", "0"]
  ],
  "expected": {
    "exact_rank": 3,
    "exact_nullity": 0,
    "column_sum_invariant_holds": true
  }
}
```

This fixture is important because it is column-stochastic in the column-sum sense but nonsingular. It prevents a false inference that stochasticity itself implies a zero eigenvalue or rank deficiency.

## `fixtures/near_singular_epsilon.json`

```json
{
  "fixture_id": "AQ-COND-FIX-003",
  "description": "Full-rank but near-singular exact rational matrix for tolerance-sensitivity testing.",
  "matrix": [
    ["1", "1"],
    ["1", "1000000000001/1000000000000"]
  ],
  "expected": {
    "exact_rank": 2,
    "exact_nullity": 0,
    "column_sum_invariant_holds": false
  }
}
```

This is not a stochastic matrix. It is a conditioning adversarial fixture: exact rank is 2, while a float64 SVD may produce a smallest singular value near a practical threshold.

## `fixtures/column_stochastic_kernel.json`

```json
{
  "fixture_id": "AQ-COND-FIX-004",
  "description": "Column-stochastic singular matrix with an exact zero-sum kernel witness.",
  "matrix": [
    ["1", "1", "0"],
    ["0", "0", "1"],
    ["0", "0", "0"]
  ],
  "expected": {
    "exact_rank": 2,
    "exact_nullity": 1,
    "column_sum_invariant_holds": true,
    "kernel_witness": ["1", "-1", "0"],
    "kernel_witness_is_exact": true,
    "kernel_witness_zero_sum": true
  }
}
```

Check the column sums:

$$
\begin{pmatrix}
1\\0\\0
\end{pmatrix},
\quad
\begin{pmatrix}
1\\0\\0
\end{pmatrix},
\quad
\begin{pmatrix}
0\\1\\0
\end{pmatrix},
$$

so every column sum is $$1$$. The witness

$$
v=(1,-1,0)^\top
$$

satisfies

$$
Av=0,
\qquad
\mathbf1^\top v=0.
$$

This is the appropriate small finite fixture for the intended theorem.

## `fixtures/malformed_negative_control.json`

Do not include this file in the canonical replay fixture list. It is a parser-failure control:

```json
{
  "fixture_id": "AQ-COND-FIX-NEG-001",
  "description": "Negative control: non-rectangular matrix must be rejected.",
  "matrix": [
    ["1", "0"],
    ["0"]
  ],
  "expected": {
    "must_fail_fixture_validation": true
  }
}
```

The failure itself should be tested in a separate self-audit or negative-control runner; it should not be treated as a normal passing mathematical fixture.

***

# 11. `verification/manifest.json`

Use a conservative manifest that lists only executable checks that actually exist.

```json
{
  "schema_id": "AQ-CONDITIONING-MANIFEST-001",
  "version": "0.1.0",
  "project": "AQARION-CONDITION8NG",
  "checks": [
    {
      "id": "AQ-COND-SELF-AUDIT-001",
      "path": "aq_conditioning/self_audit.py",
      "command": "python -m aq_conditioning.self_audit",
      "required": true
    },
    {
      "id": "AQ-COND-REPLAY-001",
      "path": "aq_conditioning/replay.py",
      "command": "python -m aq_conditioning.replay",
      "required": true
    }
  ],
  "governance": {
    "c4": "BLOCKED",
    "publication": "BLOCKED",
    "promotion_allowed": false
  }
}
```

Do not register Lean, interval arithmetic, RO-Crate export, Mandelbrot analysis, or zeta-model checks until those executable artifacts exist.

***

# 12. `aq_conditioning/self_audit.py`

```python
from __future__ import annotations

import json
from pathlib import Path


REQUIRED_PATHS = [
    "CONTRACT.json",
    "README.md",
    "FILETREE.md",
    "aq_conditioning/__init__.py",
    "aq_conditioning/canonical.py",
    "aq_conditioning/exact_rank.py",
    "aq_conditioning/numerical_svd.py",
    "aq_conditioning/invariants.py",
    "aq_conditioning/fixtures.py",
    "aq_conditioning/report.py",
    "aq_conditioning/replay.py",
    "fixtures/singular_exact.json",
    "fixtures/full_rank_permutation.json",
    "fixtures/near_singular_epsilon.json",
    "fixtures/column_stochastic_kernel.json",
    "verification/manifest.json",
]


def is_valid_json(path: str) -> bool:
    try:
        with Path(path).open("r", encoding="utf-8") as handle:
            json.load(handle)
    except (OSError, json.JSONDecodeError):
        return False
    return True


def main() -> int:
    missing = [path for path in REQUIRED_PATHS if not Path(path).is_file()]

    json_files = [
        "CONTRACT.json",
        "fixtures/singular_exact.json",
        "fixtures/full_rank_permutation.json",
        "fixtures/near_singular_epsilon.json",
        "fixtures/column_stochastic_kernel.json",
        "verification/manifest.json",
    ]

    invalid_json = [path for path in json_files if not is_valid_json(path)]

    result = {
        "missing": missing,
        "invalid_json": invalid_json,
        "status": "PASS" if not missing and not invalid_json else "FAIL",
    }

    print(json.dumps(result, sort_keys=True))
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
```

This directly addresses the earlier observed risk of a JSON file containing concatenated objects: the check fails closed.

***

# 13. `verification/run_all.py`

```python
from __future__ import annotations

import subprocess
import sys


COMMANDS = [
    [sys.executable, "-m", "aq_conditioning.self_audit"],
    [sys.executable, "-m", "aq_conditioning.replay"],
]


def main() -> int:
    failures = 0

    for command in COMMANDS:
        completed = subprocess.run(command, check=False)
        failures += int(completed.returncode != 0)

    return 0 if failures == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
```

***

# 14. `verification/metamorphic.py`

For conditioning, the first meaningful metamorphic test is rank preservation under exact invertible row/column transformations. The test should not invent performance results; it checks an exact mathematical invariant.

```python
from __future__ import annotations

from fractions import Fraction

from aq_conditioning.exact_rank import exact_rank


def main() -> int:
    matrix = [
        [Fraction(1), Fraction(2)],
        [Fraction(2), Fraction(4)],
    ]

    transformed = [
        [matrix[0][0], matrix[0][1]],
        [matrix[1][0] - 2 * matrix[0][0], matrix[1][1] - 2 * matrix[0][1]],
    ]

    original_rank = exact_rank(matrix)
    transformed_rank = exact_rank(transformed)

    passed = original_rank == transformed_rank == 1

    print(
        {
            "test": "invertible_row_operation_preserves_exact_rank",
            "original_rank": original_rank,
            "transformed_rank": transformed_rank,
            "status": "PASS" if passed else "FAIL",
        }
    )

    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
```

Do not call this “proof of rank preservation.” It is an executable regression check of an already-known theorem.

***

# 15. `verification/mutation/__init__.py`

```python
"""Mutation tests for AQARION-CONDITION8NG."""
```

***

# 16. `verification/mutation/executor.py`

This is a minimal first mutation suite. It attacks the parser/verification route rather than pretending to establish broad mutation adequacy.

```python
from __future__ import annotations

from fractions import Fraction

from aq_conditioning.exact_rank import exact_rank


def wrong_rank_mutant(_: object) -> int:
    return 0


def main() -> int:
    matrix = [
        [Fraction(1), Fraction(2)],
        [Fraction(2), Fraction(4)],
    ]

    canonical_rank = exact_rank(matrix)
    mutant_rank = wrong_rank_mutant(matrix)

    killed = canonical_rank != mutant_rank

    print(
        {
            "mutant": "constant_zero_rank",
            "canonical_rank": canonical_rank,
            "mutant_rank": mutant_rank,
            "status": "KILLED" if killed else "SURVIVED",
        }
    )

    return 0 if killed else 1


if __name__ == "__main__":
    raise SystemExit(main())
```

This is intentionally weak. In the README or governance ledger, label it:

```text
Mutation adequacy: INITIAL / WEAK.
```

The next semantic mutants should include:

- Pivot-selection errors in exact elimination.
- Incorrect exact `Fraction` parsing.
- Transposed column-sum test.
- Incorrect singular-value threshold comparator.
- Corrupt kernel-witness verifier.
- Replacement of `AᵀA` with `AAᵀ` in a theorem-specific spectral test.

***

# 17. `schema/fixture.schema.json`

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "AQARION-CONDITION8NG Matrix Fixture",
  "type": "object",
  "required": [
    "fixture_id",
    "description",
    "matrix",
    "expected"
  ],
  "properties": {
    "fixture_id": {
      "type": "string",
      "minLength": 1
    },
    "description": {
      "type": "string",
      "minLength": 1
    },
    "matrix": {
      "type": "array",
      "minItems": 1,
      "items": {
        "type": "array",
        "minItems": 1,
        "items": {
          "anyOf": [
            { "type": "integer" },
            { "type": "string", "pattern": "^-?[0-9]+(/[1-9][0-9]*)?$" }
          ]
        }
      }
    },
    "expected": {
      "type": "object"
    }
  },
  "additionalProperties": false
}
```

This schema does not validate rectangularity; that semantic rule belongs in Python validation.

***

# 18. `schema/receipt.schema.json`

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "AQARION-CONDITION8NG Receipt",
  "type": "object",
  "required": [
    "schema_id",
    "generated_at_utc",
    "claim_id",
    "contract_sha256",
    "runtime",
    "fixture_count",
    "fixtures",
    "status",
    "governance"
  ],
  "properties": {
    "schema_id": {
      "const": "AQ-CONDITIONING-RECEIPT-001"
    },
    "generated_at_utc": {
      "type": "string"
    },
    "claim_id": {
      "type": ["string", "null"]
    },
    "contract_sha256": {
      "type": "string",
      "pattern": "^[a-f0-9]{64}$"
    },
    "runtime": {
      "type": "object"
    },
    "fixture_count": {
      "type": "integer",
      "minimum": 0
    },
    "fixtures": {
      "type": "array"
    },
    "status": {
      "enum": ["PASS", "FAIL"]
    },
    "governance": {
      "type": "object"
    }
  },
  "additionalProperties": true
}
```

***

# 19. `docs/EVIDENCE-MODEL.md`

```markdown
# AQARION-CONDITION8NG Evidence Model

## Scope

AQARION-CONDITION8NG distinguishes exact finite algebra, numerical approximation,
execution provenance, and formal proof.

## Evidence labels

| Label | Meaning |
|---|---|
| [D] | Defined contract, fixture, or theorem target |
| [V] | Finite computational verification completed under a declared contract |
| [P] | Mathematical theorem proved and accepted under the declared proof policy |
| [PV] | Both proved and computationally verified |
| [F] | Refuted, killed, or rejected by a counterexample |
| [Q] | Quarantined pending repair or review |

## Rules

- A floating-point SVD does not establish exact rank.
- A small singular value is not an exact kernel certificate.
- An exact rational null vector is stronger than a tolerance-qualified approximate null vector.
- A valid SHA-256 hash establishes artifact identity, not mathematical truth.
- A CI pass establishes execution of declared checks, not a theorem.
- A Lean file containing `sorry` is not a kernel-accepted proof.
- A receipt from one environment is not external independent reproduction.
- All generated runtime receipts remain finite computational evidence unless separately formalized.

## Governance

C4 is blocked.
Publication is blocked.
Promotion is false.
```

***

# 20. `docs/NUMERICAL-BOUNDARY.md`

```markdown
# Numerical Boundary

## Exact rank

For matrices with integer or rational entries, exact rank is computed over the rational field.
This is the reference classification for the included small fixtures.

## Numerical rank

A numerical singular-value decomposition reports singular values

\[
\sigma_1 \ge \cdots \ge \sigma_n \ge 0.
\]

A numerical rank requires a tolerance \(\tau\):

\[
\operatorname{rank}_{\tau}(A)
=
\#\{j:\sigma_j>\tau\}.
\]

Changing \(\tau\), arithmetic precision, BLAS implementation, or scaling may change this
numerical classification for a near-singular matrix.

## Required reporting

Every numerical-rank report must include:

- Arithmetic type and precision
- Singular values
- Rank tolerance
- Exact rank, when an exact rational fixture exists
- Condition number if finite
- Any proposed null-vector residual
- The explicit statement that numerical rank is not exact rank

## No overclaim

The project does not infer a kernel, theorem, spectral gap, or singularity solely from a
floating-point threshold.
```

***

# 21. `docs/GOVERNANCE.md`

```markdown
# Governance

## Current state

| Gate | Status |
|---|---|
| Finite contracts | Defined |
| Local execution | Pending first repository receipt |
| Independent reproduction | Not established |
| Formal Lean proof | Open |
| C4 | Blocked |
| Publication | Blocked |
| Promotion | False |

## Promotion restriction

No benchmark result, SVD output, receipt hash, or CI pass may be represented as:

- a formal theorem,
- a proof of the Riemann Hypothesis,
- a Connes trace-formula realization,
- a universal statement outside its declared finite domain,
- external independent reproduction,
- C4 clearance,
- publication authorization.

## Required language

Use:

> “The declared finite conditioning check passed under the recorded contract.”

Do not use:

> “The theorem is proved.”

unless a no-`sorry`, kernel-accepted proof receipt exists and the project’s proof policy has accepted it.
```

***

# 22. `docs/BENCHMARK-PROTOCOL.md`

```markdown
# Benchmark Protocol

## Objective

Measure the difference between exact algebraic classification and numerical
conditioning diagnostics.

## Required fixture classes

1. Exact singular matrix.
2. Exact full-rank matrix.
3. Near-singular full-rank matrix.
4. Column-sum-preserving singular matrix with a zero-sum kernel witness.
5. Negative malformed fixture rejected by validation.

## Reported values

For each valid fixture, record:

\[
n,\quad
\operatorname{rank}_{\mathbb Q}(A),\quad
\operatorname{nullity}_{\mathbb Q}(A),\quad
\sigma_{\min}(A),\quad
\sigma_{\max}(A).
\]

If a numerical rank is reported, also record the tolerance:

\[
\tau.
\]

For each declared kernel witness \(v\), record:

\[
Av,\qquad
\sum_i v_i.
\]

## Acceptance boundary

A result is a finite computational verification only if:

- The contract parses as strict JSON.
- All required fixtures parse and validate.
- Exact ranks equal their declared expected values.
- Declared exact kernel witnesses verify exactly.
- The runtime receipt is generated and validates against its schema.

No performance or stability conclusion is valid until the benchmark has been run and
the raw receipt is available.
```

***

# 23. `.github/workflows/conditioning-ci.yml`

Create this only if you want CI to execute the minimal runnable core. It intentionally performs no publication, release, or promotion action.

```yaml
name: AQARION-CONDITION8NG

on:
  push:
    branches: [main]
  pull_request:
  workflow_dispatch:

permissions:
  contents: read

jobs:
  verify:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout exact revision
        uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.11"

      - name: Install dependency
        run: python -m pip install --upgrade pip numpy

      - name: Verify required paths
        run: |
          test -f CONTRACT.json
          test -f aq_conditioning/replay.py
          test -f aq_conditioning/self_audit.py
          test -f fixtures/singular_exact.json
          test -f fixtures/full_rank_permutation.json
          test -f fixtures/near_singular_epsilon.json
          test -f fixtures/column_stochastic_kernel.json
          test -f verification/manifest.json

      - name: Run self audit
        run: python -m aq_conditioning.self_audit

      - name: Run conditioning replay
        run: python -m aq_conditioning.replay

      - name: Run exact-rank metamorphic test
        run: python verification/metamorphic.py

      - name: Run initial mutation test
        run: python verification/mutation/executor.py

      - name: Upload runtime receipt
        uses: actions/upload-artifact@v4
        with:
          name: aq-conditioning-receipt
          path: artifacts/conditioning-receipt.json
```

## Before your first run

There are two things you should check manually before adding these files:

1. **Exact existing filename:** You wrote `C0NTRACT.JSON` once with a zero and `CONTRACT.JSON` elsewhere. Pick exactly one filename. I recommend:

   ```text
   CONTRACT.json
   ```

   Then use it consistently in the tree, self-audit, replay, README, and workflow.

2. **Repository root:** Place `aq_conditioning/`, `fixtures/`, `schema/`, `verification/`, and `docs/` at the root of `AQARION-CONDITION8NG`, not nested under an accidental duplicate repository folder.

## Honest status after creating files

After you paste these files but **before executing them**, the honest state is:

| Item | Status |
|---|---|
| Repository skeleton | Defined |
| Exact-rank fixture protocol | Defined |
| Numerical SVD comparison layer | Defined |
| Conditioning evidence model | Defined |
| Runtime receipt schema | Defined |
| CI workflow | Defined, not yet executed |
| Fixture correctness | Requires execution |
| Exact rank results | Not yet generated in this repository |
| Numerical stability metrics | Not yet measured |
| Lean theorem | Open |
| C4 / publication / promotion | Blocked / blocked / false |

The next safe action is to create the files, run:

```text
python -m aq_conditioning.self_audit
python -m aq_conditioning.replay
python verification/metamorphic.py
python verification/mutation/executor.py
```

Then preserve the resulting `artifacts/conditioning-receipt.json` locally or as a CI artifact. Do not commit it as a “latest proof” unless you later establish a deliberate immutable evidence-release policy.

Citations:
[1] Quantarion9 (James Aaron) https://huggingface.co/Quantarion9

I can’t inspect all repository files yet because the GitHub connector is currently disconnected, and the public GitHub fetch route has not been returning the repository contents. **Do not push the new `verification/` files until you run a local collision audit** against your existing manifest, mutation package, and metamorphic files.

To let me inspect the actual repository directly, connect GitHub through the **Connectors** page in your settings, then tell me when it is connected. I can then compare the live tree before recommending any push.

## What can conflict

Because you already have a manifest, mutation files, and metamorphic files, the main risks are not mathematical—they are **namespace, path, command, and ownership collisions**.

| Collision type | Example | Risk |
|---|---|---|
| Path collision | Existing `verification/manifest.json` | Accidentally overwrite the project-wide registry |
| Module collision | Existing `mutation/__init__.py` | Python imports the wrong package |
| Command collision | Existing `run_all.py` / `run-all.py` | CI executes a different runner than expected |
| Fixture collision | Existing `fixtures/` at repo root | New files silently mix with unrelated fixtures |
| Receipt collision | Existing `artifacts/` or `receipts/` conventions | Runtime evidence goes to the wrong location |
| Workflow collision | Existing workflow uses `verification/manifest.json` | New registry alters unrelated CI behavior |
| Schema collision | Existing `schema.json` or receipt schema | A validator applies incompatible rules |
| Naming collision | `aq_conditioning` versus existing package | Imports resolve unpredictably |
| Policy collision | Existing manifest bans outputs or expects specific fields | New replay passes locally but fails central audit |

The most dangerous error would be creating:

```text
verification/manifest.json
verification/run_all.py
verification/metamorphic.py
verification/mutation/
```

at the repository root when those paths are already part of AQARION’s central verification system.

## Safe architecture

Because AQARION already has a shared verification surface, do **not** create a second top-level manifest or generic runner unless the existing one explicitly supports it.

Use a namespaced package instead:

```text
AQARION-CONDITION8NG/
│
├── CONTRACT.json
├── README.md
├── FILETREE.md
│
├── aq_conditioning/
│   ├── __init__.py
│   ├── canonical.py
│   ├── exact_rank.py
│   ├── numerical_svd.py
│   ├── invariants.py
│   ├── fixtures.py
│   ├── report.py
│   ├── replay.py
│   └── self_audit.py
│
├── fixtures/
│   └── conditioning/
│       ├── singular_exact.json
│       ├── full_rank_permutation.json
│       ├── near_singular_epsilon.json
│       └── column_stochastic_kernel.json
│
├── schema/
│   └── conditioning/
│       ├── fixture.schema.json
│       └── receipt.schema.json
│
├── verification/
│   └── aq_conditioning/
│       ├── manifest.json
│       ├── run.py
│       ├── metamorphic.py
│       └── mutation/
│           ├── __init__.py
│           └── executor.py
│
└── artifacts/
    └── aq_conditioning/
        └── .gitkeep
```

This avoids claiming ownership of generic global names such as:

```text
verification/manifest.json
verification/run_all.py
verification/metamorphic.py
verification/mutation/
fixtures/
schema/
artifacts/
```

### Namespacing rule

Use these names, not generic duplicates:

| Do not add | Add instead |
|---|---|
| `verification/manifest.json` | `verification/aq_conditioning/manifest.json` |
| `verification/run_all.py` | `verification/aq_conditioning/run.py` |
| `verification/metamorphic.py` | `verification/aq_conditioning/metamorphic.py` |
| `verification/mutation/executor.py` | `verification/aq_conditioning/mutation/executor.py` |
| `fixtures/singular_exact.json` | `fixtures/conditioning/singular_exact.json` |
| `schema/receipt.schema.json` | `schema/conditioning/receipt.schema.json` |
| `artifacts/conditioning-receipt.json` | `artifacts/aq_conditioning/receipt.json` |

## Local collision audit

Run this in Termux from the repository root **before copying any new verification files**:

```bash
pwd
git rev-parse --show-toplevel
git status --short
find . -maxdepth 4 -type f | sort > /tmp/aqarion-files-before.txt
cat /tmp/aqarion-files-before.txt
```

This gives you a frozen pre-change file inventory.

Then search specifically for the names that may conflict:

```bash
find . -type f \( \
  -name 'manifest.json' -o \
  -name 'run_all.py' -o \
  -name 'run-all.py' -o \
  -name 'metamorphic.py' -o \
  -name 'executor.py' -o \
  -name '__init__.py' -o \
  -name 'schema.json' -o \
  -name 'receipt.schema.json' \
\) | sort
```

Search for all existing conditioning-related content:

```bash
grep -RInE \
  'AQARION-CONDITION8NG|AQARION-CONDITIONING|aq_conditioning|conditioning-receipt|AQ-CONDITIONING' \
  . \
  --exclude-dir=.git \
  --exclude-dir=__pycache__
```

Search for existing central manifest references:

```bash
grep -RInE \
  'manifest\.json|run_all\.py|run-all\.py|metamorphic\.py|mutation|receipt' \
  .github verification aqarion.toml . \
  --exclude-dir=.git \
  --exclude-dir=__pycache__
```

If `aqarion.toml` exists, inspect it before adding any new package:

```bash
test -f aqarion.toml && cat aqarion.toml
```

Inspect every existing manifest before writing a new one:

```bash
find . -type f -name 'manifest.json' -print -exec sh -c '
  echo "============================================================"
  echo "FILE: $1"
  python3 -m json.tool "$1" 2>&1 || true
' sh {} \;
```

Strict JSON validation is mandatory. This catches the prior class of error where two JSON objects are concatenated in one file.

## Detect exact path collisions

Before writing any proposed file, test whether that path already exists:

```bash
for p in \
  "aq_conditioning/__init__.py" \
  "aq_conditioning/canonical.py" \
  "aq_conditioning/exact_rank.py" \
  "aq_conditioning/numerical_svd.py" \
  "aq_conditioning/invariants.py" \
  "aq_conditioning/fixtures.py" \
  "aq_conditioning/report.py" \
  "aq_conditioning/replay.py" \
  "aq_conditioning/self_audit.py" \
  "verification/aq_conditioning/manifest.json" \
  "verification/aq_conditioning/run.py" \
  "verification/aq_conditioning/metamorphic.py" \
  "verification/aq_conditioning/mutation/__init__.py" \
  "verification/aq_conditioning/mutation/executor.py" \
  "fixtures/conditioning/singular_exact.json" \
  "fixtures/conditioning/full_rank_permutation.json" \
  "fixtures/conditioning/near_singular_epsilon.json" \
  "fixtures/conditioning/column_stochastic_kernel.json" \
  "schema/conditioning/fixture.schema.json" \
  "schema/conditioning/receipt.schema.json"
do
  if [ -e "$p" ]; then
    echo "COLLISION: $p already exists"
  else
    echo "FREE:      $p"
  fi
done
```

Expected safe result:

```text
FREE: aq_conditioning/__init__.py
FREE: aq_conditioning/canonical.py
...
FREE: verification/aq_conditioning/manifest.json
...
```

If any output says `COLLISION`, do **not** overwrite it. Open that exact file first:

```bash
sed -n '1,240p' "THE-COLLIDING-PATH"
```

## Detect Python import collisions

A file can be absent while a package name is still already importable through your repository or Termux environment.

Run:

```bash
python3 - <<'PY'
import importlib.util

names = [
    "aq_conditioning",
    "verification",
    "mutation",
    "metamorphic",
    "fixtures",
]

for name in names:
    spec = importlib.util.find_spec(name)
    origin = None if spec is None else spec.origin
    locations = None if spec is None else spec.submodule_search_locations
    print({
        "module": name,
        "found": spec is not None,
        "origin": origin,
        "locations": None if locations is None else list(locations),
    })
PY
```

Interpretation:

- `aq_conditioning: found false` means the intended new package name is currently free.
- `aq_conditioning: found true` means you must inspect the existing package before adding another.
- Generic names such as `mutation` and `fixtures` may already resolve somewhere; do not import them as top-level project modules.
- Always use fully qualified imports such as:

```python
from aq_conditioning.exact_rank import exact_rank
```

not:

```python
from exact_rank import exact_rank
```

and not:

```python
from fixtures import load_fixture
```

## Detect CI workflow collisions

List existing workflows:

```bash
find .github/workflows -maxdepth 1 -type f \( -name '*.yml' -o -name '*.yaml' \) -print | sort
```

Then search their commands:

```bash
grep -RInE \
  'python|pytest|manifest|verification|mutation|metamorphic|receipt|artifacts' \
  .github/workflows \
  --include='*.yml' \
  --include='*.yaml'
```

Before adding a conditioning workflow, determine whether the repository already has:

- One canonical verification dispatcher.
- A workflow registry.
- A top-level `run-all.py` command.
- A manifest-based runner.
- Artifact directory rules.
- Existing package-install requirements.

If a central workflow already exists, the safe integration is usually:

```text
Existing workflow dispatcher
        │
        └── Add one namespaced AQ-CONDITION8NG check
              │
              ├── verification/aq_conditioning/manifest.json
              ├── python -m aq_conditioning.self_audit
              └── python -m aq_conditioning.replay
```

Do not create another independent top-level workflow until the central convention is understood.

## Verify before staging

After adding namespaced files, run these checks:

```bash
python3 -m json.tool CONTRACT.json > /dev/null
python3 -m json.tool verification/aq_conditioning/manifest.json > /dev/null

python3 -m compileall -q aq_conditioning verification/aq_conditioning

python3 -m aq_conditioning.self_audit
python3 -m aq_conditioning.replay
python3 verification/aq_conditioning/metamorphic.py
python3 verification/aq_conditioning/mutation/executor.py
```

Then inspect only the changes you intend to stage:

```bash
git status --short
git diff --check
git diff --name-status
git diff --stat
```

`git diff --check` is particularly important. It catches trailing whitespace and malformed patch spacing, but it does **not** validate JSON, imports, or mathematics—so keep the earlier checks.

Finally, inspect the staged set:

```bash
git add \
  aq_conditioning \
  fixtures/conditioning \
  schema/conditioning \
  verification/aq_conditioning \
  docs \
  .gitignore

git diff --cached --name-status
git diff --cached --check
```

Do **not** stage these unless you consciously intend to edit the repository-wide system:

```text
verification/manifest.json
verification/run-all.py
verification/run_all.py
verification/mutation/
verification/metamorphic.py
.github/workflows/verify.yml
aqarion.toml
```

## What I need from you

Run these three commands and paste the output here:

```bash
find verification -maxdepth 4 -type f | sort
```

```bash
find . -maxdepth 3 -type f -name 'manifest.json' -o -name 'aqarion.toml' -o -name 'run-all.py' -o -name 'run_all.py'
```

```bash
grep -RInE 'mutation|metamorphic|manifest|receipt|run-all|run_all' \
  verification .github aqarion.toml 2>/dev/null | head -250
```

With those real outputs, I can identify exact collision points and tell you precisely whether to:

- reuse an existing manifest;
- create only a namespaced sub-manifest;
- add one entry to an existing dispatcher;
- avoid a duplicate mutation package;
- or stop because an existing package already owns the same paths.

## Honest current status

| Item | Status |
|---|---|
| AQARION-CONDITION8NG documentation shell | Created, according to your report |
| Existing manifest/mutation/metamorphic compatibility | **Not yet inspected** |
| Proposed generic top-level verification files | **Do not add yet** |
| Namespaced layout | Recommended pending live tree audit |
| Runtime replay | Not yet established for this repository |
| CI execution | Not yet established |
| Lean / C4 / publication / promotion | Open / blocked / blocked / false |

The correct immediate action is an inventory audit—not a push.


No—it was **not** for nothing, and it does not have to mix with or break your existing AQARION verification system.

The mistake was presenting generic paths such as `verification/manifest.json`, `verification/mutation/`, and `verification/metamorphic.py` as if they should be added beside your existing shared files. **Do not do that.** Your current AQARION repository already owns those names and conventions.

## The safe interpretation

`AQARION-CONDITION8NG` should be a **separate repository / standalone research package**, not a replacement for or modification of:

```text
Aqarions-Quantarion-AI/
├── verification/
├── verification/manifest.json
├── verification/mutation/
├── verification/metamorphic.py
├── aqarion.toml
└── .github/workflows/
```

So nothing needs to be copied into your existing repository’s `verification/` folder.

Keep your established repository exactly as it is:

```text
Aqarions-Quantarion-AI/
    └── existing AQARION verification infrastructure
```

Keep the new work separately:

```text
AQARION-CONDITION8NG/
    ├── CONTRACT.json
    ├── README.md
    ├── FILETREE.md
    ├── aq_conditioning/
    ├── fixtures/
    ├── schema/
    └── local scripts
```

There is no collision if they are two separate Git repositories in two different folders.

## What you should do now

Do **not** add anything to the old repository’s `verification/` directory.

For `AQARION-CONDITION8NG`, you only need a small standalone core first:

```text
AQARION-CONDITION8NG/
├── CONTRACT.json
├── README.md
├── FILETREE.md
│
├── aq_conditioning/
│   ├── __init__.py
│   ├── canonical.py
│   ├── exact_rank.py
│   ├── numerical_svd.py
│   ├── invariants.py
│   ├── fixtures.py
│   ├── report.py
│   └── replay.py
│
├── fixtures/
│   ├── singular_exact.json
│   ├── full_rank_permutation.json
│   ├── near_singular_epsilon.json
│   └── column_stochastic_kernel.json
│
└── artifacts/
    └── .gitkeep
```

That is all. No top-level `verification/` folder is required. No shared manifest is required. No mutation or metamorphic files are required at this stage.

## What to skip

Do **not** create or copy these into either repository right now:

```text
verification/manifest.json
verification/run_all.py
verification/run-all.py
verification/metamorphic.py
verification/mutation/
.github/workflows/conditioning-ci.yml
aqarion.toml
```

Those were optional later-stage infrastructure suggestions, not requirements for the new project. Since you already have an established AQARION system, adding generic duplicates risks confusion and is not worth it now.

## Why the new repository still matters

`AQARION-CONDITION8NG` has one focused purpose:

$$
\text{exact rank/nullity}
\quad\text{versus}\quad
\text{numerical SVD-based rank classification}.
$$

It can hold:

- Exact rational matrix fixtures.
- Exact rank and nullity calculations.
- Numerical singular values and tolerance-qualified rank reports.
- Known singular, full-rank, and near-singular adversarial examples.
- A future Lean theorem target.
- Runtime JSON reports local to that repository.

It should **not** own or interfere with SV-001-V2, Kaprekar verification, Mandelbrot experiments, old manifests, or your existing CI architecture.

## Minimal next step

Since you already created:

```text
CONTRACT.json
FILETREE.md
README.md
```

the safest next file is only:

```text
aq_conditioning/__init__.py
```

with:

```python
"""AQARION-CONDITION8NG exact-versus-numerical conditioning toolkit."""

__version__ = "0.1.0"
```

Then stop and make sure the new repository root is correct.

In Termux:

```bash
pwd
git rev-parse --show-toplevel
git status --short
```

You want the result to point to something like:

```text
.../AQARION-CONDITION8NG
```

and **not**:

```text
.../Aqarions-Quantarion-AI
```

If the command says you are inside `Aqarions-Quantarion-AI`, stop—do not create any new files there.

## Honest boundary

| Question | Answer |
|---|---|
| Was the design work useless? | No. It defined a standalone conditioning project. |
| Must it alter existing AQARION verification? | No. |
| Should you put it in the old `verification/` folder? | No. |
| Does it need its own manifest, mutation suite, or CI today? | No. |
| Could duplicate generic paths break the old system? | Yes, which is why you should not add them. |
| Can the project remain completely separate? | Yes. |
| Does this change C4, Lean, publication, or promotion? | No. All remain open/blocked/blocked/false. |

The safe action is simple: **keep AQARION-CONDITION8NG separate, do not touch your existing verification folder, and build only the standalone exact-rank core.**

Citations:
[1] The Weil proof and the geometry of the adeles class space https://arxiv.org/abs/math/0703392
[2] the weil proof and the geometry of the adeles class space https://math.nyu.edu/~tschinke/.manin/submitted/ConnesConsaniMarcolli.pdf
[3] [PDF] Introduction to motives https://www.its.caltech.edu/~matilde/SujataPlazasMarcolliMotives.pdf
[4] The Riemann Hypothesis: A 2026 Status Report | MathLumen https://www.mathlumen.com/articles/riemann-hypothesis-2026-status-report
[5] Kaprekar's routine https://en.wikipedia.org/wiki/Kaprekar's_routine
[6] Kaprekar Routine -- from Wolfram MathWorld https://mathworld.wolfram.com/KaprekarRoutine.html
[7] Calculating the Singular Values and Pseudo-Inverse of a Matrix https://epubs.siam.org/doi/10.1137/0702016
[8] The numerical linear algebra of weights. Part I: from the spectral ... https://link.springer.com/article/10.1007/s10543-025-01088-3
[9] Numerical Behavior of the Riemann Zeta Function Using Real-to ... https://www.preprints.org/manuscript/202511.1070
[10] The Riemann Hypothesis: Past, Present and a Letter Through Time https://arxiv.org/html/2602.04022v1
[11] Normal matrix - Wikipedia https://en.wikipedia.org/wiki/Normal_matrix
[12] [PDF] Than Two Thirds of the Zeros of the Riemann Zeta Function Lie on ... https://www-cdn.anthropic.com/564f962e60643842f5fcb4a17c9dbc8f608f1c37.pdf
[13] Lower spectrum of financial correlation matrices: a new perspective ... https://arxiv.org/html/2608.09641v1
[14] [PDF] φ-Resonance in Riemann Zeros - PhilPapers https://philpapers.org/archive/NOWRZS.pdf
[15] [PDF] Higher Topos-Theoretic Closure of the Riemann Hypothesis https://philarchive.org/archive/BHAHTC
[16] Building the Riemann Tensor Sieve in Lean - Thinghood Limited https://thing.rodeo/tensor-sieve/
[17] Analysing the Riemann Hypothesis and the approach to solve it ... https://www.oneyoungindia.com/white-papers/analysing-the-riemann-hypothesis-and-the-approach-to-solve-it-through-zeta-function-analysis-and-quantum-inspired-random-matrix-theory
[18] Appendix C: Math review for the rusty - The Holy Grail https://www.kunwar.page/chapter/appendix-c-math-review-for-the-rusty
[19] R Baye - Harvard University - 50+ Papers - Academia.edu https://harvard.academia.edu/rbaye

https://www.its.caltech.edu/~matilde/SujataPlazasMarcolliMotives.pdf?utm_source=perplexity

https://math.nyu.edu/~tschinke/.manin/submitted/ConnesConsaniMarcolli.pdf?utm_source=perplexity

https://arxiv.org/abs/math/0703392?utm_source=perplexity

https://www.mathlumen.com/articles/riemann-hypothesis-2026-status-report?utm_source=perplexity
