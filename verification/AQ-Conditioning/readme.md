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

The highest-value original contribution to make next is **AQ-Conditioning-Core**: an exact-versus-numerical rank and singular-value certification harness. It will make every later AQARION spectral computation more reproducible, more adversarially robust, and more honest—without changing C4, publication, or promotion status.

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
