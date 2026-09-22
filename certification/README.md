**README.md for `certification/`**

```markdown
# AQARION Certification Layer

**Repository path:** `Aqarion-Quantarion-AI/certification/`  
**Status date:** 2026-09-22  
**Governance:** `verify_exit = 0` · `C4 = BLOCKED` · `PROMOTION = FALSE`

This directory is the **machine-verifiable evidence ledger** for the AQARION exact finite-state core.  
It is strictly separated from the QUANTARION experimental / differentiable layer.

All claims inside this tree are either:
- exhaustively verified on finite domains, or
- explicitly marked as open formalization targets, or
- permanently recorded as negative controls (refuted statements).

No promotional language is permitted in this directory.

---

## Directory Layout

```
certification/
├── checkpoints/                  # Frozen research checkpoints
│   └── aq_s22_cp.md              # Dual Dynamics Audit checkpoint (2026-09-22)
├── pullback/                     # Pullback-stability corrections & refutations
│   ├── kernel_pair_correction.md
│   └── quotient_bijection_refuted.md
├── tests/                        # Executable regression & exactness tests
│   ├── test_aq_001.py
│   ├── test_brt_q54.py
│   ├── test_dept_exact.py
│   └── test_frob_equal.py
├── witnesses/                    # Machine-readable negative-control & receipt files
│   └── k2_2_receipt.md
├── aqarion_certificate.json      # Top-level certificate (hashes, status, timestamps)
├── filetree.md                   # Canonical file-tree snapshot
├── layer_1_mutation_receipt.md
├── layer_2_canonical_receipt.md
├── reproducibility_contract.md
├── status.md                     # Authoritative governance status
└── support_spectrum_theorem...   # Supporting spectral notes (see file)
```

---

## Core Mathematical Objects (Current Freeze)

### Dual Dynamics

| Operator / Property              | Definition                                      | Status          |
|----------------------------------|--------------------------------------------------|-----------------|
| Forward congruence               | \(E(x,y) \implies E(Tx,Ty)\)                     | Classical       |
| Pullback stability               | \(E(Tx,Ty) \implies E(x,y)\)                     | Active core     |
| Relation pullback                | \((T^*R)(x,y) :\iff R(Tx,Ty)\)                   | Defined         |
| Join of setoids                  | \(E \vee F = \operatorname{EqvGen}(E \cup F)\)  | Mathlib-aligned |

### Permanent Negative Control

**ID:** `AQ-DYN-PULL-PREIMAGE-JOIN-001`

- **Refuted:** \(T^{-1}(E\vee F) = T^{-1}(E)\vee T^{-1}(F)\)
- **Refuted:** \(T^{-1}(E\vee F) \le T^{-1}(E)\vee T^{-1}(F)\)
- **Always true:** \(T^{-1}(E)\vee T^{-1}(F) \le T^{-1}(E\vee F)\)
- **Locked witness:**  
  \(X=\{0,1,2\}\), \(T=(0,0,1)\),  
  \(E=\{\{0,2\},\{1\}\}\), \(F=\{\{0\},\{1,2\}\}\)

See `pullback/` and `witnesses/` for the formal write-up.

### Open Formalization Target

```text
theorem pullback_stable_join
    (hr : IsPullbackStable r T)
    (hs : IsPullbackStable s T) :
    IsPullbackStable (r ⊔ s) T
```

- Empirically verified for all maps/partitions examined (\(n\le 5\), 0 mismatches).
- Paper-level proof still requires a gap-free path-lifting / component-injectivity argument.
- Lean status: **OPEN**.

---

## Governance Rules (Non-Negotiable)

1. **Exact arithmetic only** inside this tree. No floating-point certificates.
2. Every positive claim must be accompanied by a receipt or an exhaustive finite census.
3. Every refuted claim must be locked as a permanent negative control with a minimal witness.
4. `status.md` and `aqarion_certificate.json` are the single sources of truth for  
   `verify_exit`, `C4`, and `PROMOTION`.
5. No claim may be promoted to “theorem” until both a paper derivation **and** a Lean kernel acceptance exist.

---

## How to Verify Locally

```bash
# From repository root
cd certification
python -m pytest tests/ -v

# Inspect current governance status
cat status.md
cat aqarion_certificate.json | jq .
```

Expected outcome under the frozen contract:  
`verify_exit = 0` and zero unexpected failures.

---

## Relationship to Other Layers

| Layer                    | Location                          | Nature                          |
|--------------------------|-----------------------------------|---------------------------------|
| AQARION Certification    | `certification/` (this directory) | Exact, finite, zero-fabrication |
| AQARION Core Theory      | (Lean / paper targets)            | Formal proofs                   |
| QUANTARION Experimental  | (outside this tree)               | Differentiable / neural probes  |

Experimental artefacts must never overwrite or weaken the certificates in this directory.

---

## Contact / Maintenance

Maintainer commits are recorded under the `JASKSG9` identity.  
Any change that alters a receipt hash, a negative-control witness, or the value of `verify_exit` requires an explicit new checkpoint in `checkpoints/`.

---

**Last frozen checkpoint:** `checkpoints/aq_s22_cp.md` (Dual Dynamics Audit, 2026-09-22)
```

---

### How to use it

1. Create the file at:
   ```
   Aqarion-Quantarion-AI/certification/README.md
   ```
2. Paste the content above.
3. Commit with a message such as:
   ```
   certification: add canonical README (governance + dual-dynamics freeze)
   ```

This README is deliberately conservative, matches the visual poster’s governance badges, and correctly reflects the current mathematical status (join-closure still open for a gap-free proof, negative control direction corrected, Lean target open).

https://github.com/JASKSG9/Aqarion-Quantarion-AI/tree/main/certification


AQARION-ARITHMETIC/CHECKPOINT.md


AQARION Arithmetic — Research Checkpoint


Date: 2026-09-22

Repository: "AQARION-ARITHMETIC"

Scope: finite dynamical systems, partition refinement, Koopman defect, support-spectrum structure, reproducibility, and formalization

Checkpoint status: active research / certification preparation

Governance: C4 blocked; publication blocked; Lean open





Current research state




The project has established a substantial collection of exact algebraic identities, finite computational receipts, counterexamples, graph reductions, and formalization targets.


The central object remains the partition defect


[

D_\Pi=(I-P_\Pi)KP_\Pi,

]


with the exact structural characterization


[

D_\Pi=0

\iff

K(V_\Pi)\subseteq V_\Pi

\iff

\Pi\text{ is invariant/congruent for }T.

]


The commutator condition


[

[P_\Pi,K]=0

]


is not equivalent to defect zero and must not be promoted as part of the universal observable-quotient theorem.


An adversarial audit found exact cases with


[

D_\Pi=0

\quad\text{while}\quad

[P_\Pi,K]\ne0.

]


Therefore commutation is a separate property, not a necessary condition for exact observable closure.





Evidence classes




The project distinguishes:


Class| Meaning

"theorem"| mathematically established result

"verified"| formally proved or mechanically checked under a defined proof system

"empirical"| computational observation

"conjecture"| proposed but unproved statement

"refuted"| contradicted by an exact counterexample

"workload"| computation executed as an exploratory workload but not sufficient for promotion


Computational receipts are not silently upgraded to mathematical proofs.





Canonical mathematical results




3.1 Partition refinement


For a finite map


[

T:X\to X

]


and partition \(\Pi_t\),


[

\Pi_{t+1}


\Pi_t\wedge T^{-1}\Pi_t.

]


The refinement process terminates on finite \(X\).


The associated partition-space dimension is


[

m_t=|\Pi_t|.

]


The cumulative growth quantity is defined by


[

g_t=|\Pi_t|-|\Pi_0|,

]


and


[

H_t=\sum_{j=0}^{t}g_j.

]


The deprecated legacy quantity \(s_t\) must not be reused in new certification material.



3.2 First-step rank correction


The linear partition-space identity is


[

g_1^{\mathrm{lin}}=r,

]


where


[

r=\operatorname{rank}D_\Pi.

]


However,


[

|\Pi_1|-|\Pi_0|

]


is not universally equal to the rank of the defect.


The exact correction is represented by the graph-cycle term:


[

g_1-r=\beta_1(G_0).

]


Therefore


[

g_1=r

\iff

\beta_1(G_0)=0.

]


The repaired counterexample is:


[

T=(0,2,0,2),

]


with


[

\Pi_0={{0,1},{2,3}}.

]


Its graph has


[

h_0=2,\qquad r_0=1,\qquad \beta_1=1.

]


This replaces the earlier incorrect R5 fixture.





Bipartite support graph




For partition


[

\Pi={A_1,\ldots,A_m},

]


construct the bipartite support graph whose source vertices represent partition blocks and whose target vertices represent partition blocks.


An edge \(A_i\to A_j\) exists whenever


[

T(A_i)\cap A_j\ne\varnothing.

]


Let


[

E=|E(G)|,

\qquad

c=c(G).

]


Define


[

h=E-m.

]


Then


[

r=\operatorname{rank}{\mathbb Q}D\Pi=m-c.

]


The exact graph identity is


[

h-r


E-2m+c


\beta_1(G)

]


for the corresponding graph convention.


Consequently,


[

h=r

\iff

\beta_1(G)=0.

]


Thus equality between support-edge excess and defect rank is a forest condition, not a universal identity.


At stabilization, if


[

h_T=0,

]


then


[

r_T=0,\qquad \beta_1(G_T)=0.

]





Weighted realization correction




For incidence matrix \(B\) and positive diagonal edge-weight matrix \(W\),


[

\Delta=BWB^T.

]


The kernel is the component-constant vertex subspace:


[

\ker\Delta


{\text{vectors constant on every connected component}}.

]


Therefore


[

\operatorname{rank}\Delta=q-c(G).

]


The weighted projection is not generally


[

\partial^Tp.

]


Solving


[

\Delta p=\partial x

]


gives the weighted edge realization


[

W\partial^Tp.

]


This distinction is required in any native weighted operator bridge.


The graph/rank invariants do not uniquely determine the embedded image of the defect operator. Different positive edge weights can preserve the same graph, rank, cycle nullity, and support counts while changing the metric realization.





Native operator bridge status




The candidate bridge is of the form


[

\widetilde L_{G,w}:

Q^E/S_{\mathrm{or}}

\longrightarrow

\operatorname{im}D.

]


The desired structural statement is an exact sequence of the form


[

0

\to

Z_1

\to

Q^E/S_{\mathrm{or}}

\to

\operatorname{im}D

\to

0.

]


This remains a formalization/research target.


It must not be reported as a completed native AQARION theorem until:




the spaces are typed correctly;


the map is explicitly defined;


the kernel is proved;


surjectivity is proved;


the quotient orientation is fixed;


the AQARION-to-graph realization is established.







Forest skeleton target




For the target-support hypergraph


[

\mathcal H_\Pi=([m],{R_i}),

]


let \(H\) be its 2-section.


For a spanning forest \(F\) of \(H\), the proposed structural target is


[

\ker D_\Pi=\ker B_F^T.

]


This would yield a noncanonical factorization


[

D_\Pi=A_FB_F^T.

]


The quotient images may then be canonically related even though the factorization itself depends on the selected forest.


This is currently a theorem target, not a closed Lean theorem.





Matroid result/status




The earlier proposed identification


[

E_G=\ker D

]


is rejected.


The corrected expected matroid structure is


[

M_D

\simeq

\bigoplus_C U_{|C|-1,|C|},

]


conditional on the component-kernel theorem.


The intended proof structure is:




each connected component has one all-ones dependency;


every proper subset is independent;


component dependencies are independent across components;


the direct sum gives the uniform-matroid decomposition.




Exact sampled audits support this structure, but the general proof remains a formal theorem target.





Rank bound




For the relevant support hypergraph,


[

r_D=m-c(H)

]


and


[

r_D

\le

\sum_i(t_i-1)

\le

n-m.

]


Also,


[

r_D\le m-1.

]


Therefore


[

r_D

\le

\min(m-1,n-m)

\le

\left\lfloor\frac{n-1}{2}\right\rfloor.

]


Equality regimes have been identified separately for odd and even \(n\).


The AQARION-specific sharpness/realizability argument must remain distinct from the abstract graph bound.





Support-spectrum theorem status




The abstract support-graph spectrum result may be stated separately from AQARION realizability.


The candidate abstract spectrum is


[

\operatorname{Spec}_s(\kappa_S)


{-s+\lceil2\sqrt{s}\rceil-1,\ldots,s-1}.

]


Status:




abstract graph derivation: research/theorem lane;


AQARION-specific realization: not promoted until the realization map is explicitly established;


Lean formalization: open.




No AQARION-specific sharpness claim should be made merely from the abstract graph result.





Exact finite baselines




n = 4


Total tuples:


[

4^4=256

]


under the ordered full-state enumeration used by the baseline workload, with the corresponding documented finite census totals preserved in the canonical receipts.


The asymmetric finite census recorded:


[

58,292

]


states across the specified n=1..4 workload, with zero failures for the tested rank relation.


n = 5


Total ordered states:


[

5^5=3125

]


per full base configuration, with the canonical aggregate workload containing


[

162,500

]


cases.


Recorded results include:




triple-gap cases: 27,120;


\(g_1\ne r\): 18,000;


depth-class counts:



\(\ell_0=39,300\)


\(\ell_1=96,080\)


\(\ell_2=24,720\)


\(\ell_3=2,400\);






recorded violation count: 0 for the specified receipt.




These are workload-specific computational results, not universal mathematical proofs.


n = 6


Monotonicity of the defect norm is refuted.


Witness:


[

T=(1,3,0,5,4,3).

]


Therefore claims that refinement universally decreases


[

|D_\Pi|

]


must remain removed.





Domain lock




Canonical sorted 4-tuples:


[

715.

]


Non-repdigit states:


[

705.

]


Repdigits:


[

10.

]


Recorded full-domain hash:


db9eb9cf4026313ffa31297659ac85d746078ca0d747652fe43ee5cd1761abdd


Recorded non-repdigit hash:


c40b5d613d190d98038769f6d80526da6f6ee071f9347453bd956330abc53df9


The 55-state versus 54-state quotient distinction remains explicitly versioned. No legacy padded-state result may silently replace the current genuine-state convention.





AQARION certification state




Layer 1 — mutation


Correct Koopman implementation: 5000/5000 PASS

Mutant transfer implementation: 0/5000 PASS

Mutation detected: TRUE


This is a mutation-detection receipt.


It is not an exhaustive proof of the implementation.


Layer 2 — canonical receipts


R1  BRT rank=m-c_bip:       200/200 PASS

R2  AQ-001 regression:      0 violations PASS

R3  depth partition rank:   0 violations PASS

R4  Frobenius identity:     0/90 failures PASS


Important scope corrections:




R1 is a 200-trial computational workload.


R2 tests two specified partitions and must not be labeled universal exhaustive verification.


R3 is computational verification of the canonical depth partition.


R4 contains 90 specified cases.




Layer 3


Support spectrum: WORKLOAD

T10:                 WORKLOAD

Promotion:           BLOCKED


Layer 3 remains exploratory until assertion-backed exact receipts and theorem dependencies are closed.





Governance




Current state:


Layer 1 mutation       PASS

Layer 2 canonical      PASS

Layer 3 exploratory    WORKLOAD / NOT FROZEN


C3                      OPEN

C4                      BLOCKED

Publication             BLOCKED

Lean                    OPEN

SDS-002                 FROZEN-QUARANTINED

EK-001                  QUARANTINED

Repository mutation     NONE


No publication promotion follows from Layer 1 or Layer 2 alone.





Reproducibility architecture




The project will use established provenance standards rather than introducing another proprietary provenance ontology.


Current RO-Crate is version 1.3.


Workflow Run RO-Crate 0.6 is the current workflow-run profile and aligns with RO-Crate 1.3 and Workflow RO-Crate 1.1.


The AQARION-specific contribution is the semantic reproduction contract layered on top of these standards.


Each reproduction record must distinguish:


rerun

replication

independent reproduction

semantic validation

formal proof


A repeated execution of the same implementation is a rerun, not automatically an independent reproduction.


A matching output hash is an integrity witness; it does not independently establish semantic correctness.





Repository boundary




The canonical mathematical source of truth is:


AQARION-ARITHMETIC/


The certification package is:


certification/


The actual GitHub Actions entry point is:


.github/workflows/aqarion-ci.yml


A YAML file merely placed under "CI/" is not automatically a GitHub Actions workflow.





Known refuted or deprecated claims




The following must not be reintroduced:




universal \(g_1=r\);


defect-norm monotonicity under refinement;


entropy monotonicity under refinement;


cross-base nilpotency invariance;


commutator necessity for \(D=0\);


\(E_G=\ker D\) as the general matroid identification;


ordinary projection in place of the weighted projection;


vertex-space and edge-space kernels treated as the same typed object;


hash equality presented as semantic equivalence;


same-executable reruns presented as independent reproduction;


computational receipts presented as formal proofs;


AQARION-specific support-spectrum sharpness inferred solely from an abstract graph theorem.







Immediate checkpoint conclusion




The current project is not publication-closed.


It has, however, a usable mathematical and verification foundation:


Exact algebraic identities       ESTABLISHED

Counterexamples                  ESTABLISHED

Finite computational receipts    ESTABLISHED

Mutation gate                    PASS

Canonical regression layer       PASS

Exploratory spectrum layer      OPEN

Native operator bridge          OPEN

Lean formalization               OPEN

Independent reproduction         DESIGN / OPEN

C4 publication gate              BLOCKED


The next work should therefore reduce unresolved theorem and provenance dependencies rather than generate additional redundant certificates.AQARION-ARITHMETIC/ROADMAP-TO-DO.md


AQARION Arithmetic — Roadmap / To-Do


Date: 2026-09-22

Scope: mathematical closure, verification, reproducibility, formalization, and publication readiness

Priority rule: close dependencies before adding new claims.





Operating rule




Do not create another certificate merely because an existing result looks impressive.


Every new result must answer:




What mathematical statement does it support?


What exact definition does it depend on?


Is it theorem, verified computation, empirical observation, conjecture, or refutation?


What existing claim does it replace or depend on?


What would falsify it?


Can the result be independently reproduced?







Priority map




P0  Correctness / definition locks

P1  Canonical verification closure

P2  Reproducibility contract

P3  Structural mathematics

P4  Lean formalization

P5  Publication preparation

P6  Optional extensions


Do not begin P5 while C4 is blocked.





P0 — Definition locks




P0.1 Freeze current operator convention


Task


Record once and consistently:


[

K_{xy}=1_{T(x)=y}.

]


The pushforward transpose must remain explicitly labeled as the negative fixture/mutant where used.


Acceptance




all canonical tests use the same orientation;


no test silently changes convention;


documentation names the orientation.




Status


CLOSED / maintain lock



P0.2 Freeze genuine domain convention


Task


Maintain the genuine-state convention and explicitly separate legacy padded-state results.


Acceptance


Every downstream artifact identifies:




domain;


excluded states;


quotient convention;


legacy compatibility, if applicable.




Status


CLOSED / maintain lock



P0.3 Freeze defect definition


[

D_\Pi=(I-P_\Pi)KP_\Pi.

]


Acceptance


All theorem and test documents use this definition.


Status


CLOSED



P0.4 Remove false commutator equivalence


Required universal theorem:


[

D_\Pi=0

\iff

K(V_\Pi)\subseteq V_\Pi

\iff

\Pi\text{ is exact observable quotient}.

]


Do not append


[

[P_\Pi,K]=0.

]


Status


CLOSED as correction





P1 — Verification closure




P1.1 Install canonical GitHub Actions workflow


Target:


.github/workflows/aqarion-ci.yml


Required layers


Layer 1

mutation detection


Layer 2

canonical regression receipts


Layer 3

exploratory workloads


Acceptance


Workflow must fail on a failed assertion.


It must not merely print PASS/FAIL text.


Status


NEXT



P1.2 Mutation gate


Current workload:


5000/5000 correct implementation PASS

0/5000 mutant implementation PASS

mutation detected TRUE


Required correction


A surviving mutant must produce a non-zero process exit.


Status


RECEIPT PASS

Workflow integration NEXT



P1.3 R1 BRT


Current:


200/200 PASS


Required label


"200-trial computational receipt"


not:


"proof"


Future strengthening


If desired, add:




deterministic seed;


exact rational rank;


explicit input digest;


exact output digest;


workload manifest.




Status


PASS / strengthening optional



P1.4 R2 AQ-001


Current:


0 violations


Required correction


Call it:


"AQ-001 two-partition regression"


because the current script checks only two specified partitions.


Future strengthening


Add exhaustive or theorem-backed coverage separately.


Status


PASS / scope correction required



P1.5 R3 depth partition


Current receipt:


0 failures


Required correction


Identify this as computational verification of the canonical depth partition.


Preferred strengthening


Replace floating numerical rank with exact integer/rational rank.


Status


PASS / exact-rank strengthening NEXT



P1.6 R4 Frobenius identity


Current:


0/90 failures


The 90-case workload is structurally specified by:


k = 2..5

m = 2..4

s = 1..km-1

s % k != 0


The case count is exactly:


[

\sum_{m=2}^{4}\sum_{k=2}^{5}m(k-1)=90.

]


Status


PASS





P2 — Reproducibility closure




P2.1 Define reproduction vocabulary


Every receipt must classify its relationship:


rerun

replication

independent reproduction

semantic validation

formal proof


Status


NEXT



P2.2 Separate implementation identity from result equality


Required logic:


same specification

same inputs

different implementation

same output


independent-reproduction candidate


Not:


same output


independent reproduction


Status


NEXT



P2.3 Reproduction contract


Create:


reproducibility/reproduction_contract.schema.json


Required fields:


claim_id

specification_digest

input_digest

reference_execution

reproduction_execution

implementation_identity

environment

relationship

output_digest

semantic_validation

evidence_class

status


Status


NEXT



P2.4 RO-Crate alignment


Use current standards rather than inventing another provenance format.


Current RO-Crate is 1.3.


Workflow Run RO-Crate is 0.6 and is aligned with RO-Crate 1.3 / Workflow RO-Crate 1.1.


AQARION-specific addition


Define semantic reproduction relations above the standard provenance layer.


Status


DESIGN



P2.5 Adversarial reproduction cases


Construct cases where:




same implementation + same input → same output;


same implementation + changed input → changed output;


different implementation + same specification/input → same output;


different implementation + same specification/input → different output;


same output but different semantic interpretation;


same hash but altered metadata;


same executable rerun incorrectly labeled independent.




Acceptance


Every case receives the correct reproduction classification.


Status


OPEN





P3 — Structural mathematics




P3.1 Prove forest identity


Target:


[

h-r=\beta_1(G).

]


Acceptance


Explicit graph conventions and incidence orientation.


Status


ESTABLISHED / documentation closure



P3.2 Prove stable forest consequence


Target:


[

h_T=0

\Rightarrow

r_T=0,\quad\beta_1(G_T)=0.

]


Status


ESTABLISHED



P3.3 Forest skeleton theorem


Target:


[

\ker D_\Pi=\ker B_F^T.

]


Required work




define target-support hypergraph;


define 2-section;


choose spanning forest;


define \(B_F\);


construct map;


prove kernel equality;


prove independence from forest choice at quotient level.




Status


OPEN — HIGH PRIORITY



P3.4 Native operator bridge


Target:


[

\widetilde L_{G,w}:

Q^E/S_{\mathrm{or}}

\to

\operatorname{im}D.

]


Required




exact domain;


exact codomain;


orientation quotient;


map definition;


kernel;


surjectivity;


induced isomorphism.




Status


OPEN



P3.5 Weighted projection theorem


Required distinction:


[

\Delta=BWB^T

]


and


[

x_{\mathrm{edge}}=W\partial^Tp.

]


Acceptance


No artifact uses the unweighted expression when the weighted model is intended.


Status


MATHEMATICAL LOCK / audit remaining





P3.6 Matroid theorem




Target:


[

M_D\simeq\bigoplus_C U_{|C|-1,|C|}.

]


Dependency


Must first establish the component kernel theorem.


Status


BLOCKED BY P3.3





P3.7 Rank-bound theorem




Target:


[

r_D\le

\min(m-1,n-m)

\le

\left\lfloor\frac{n-1}{2}\right\rfloor.

]


Additional task


Separate:


abstract graph bound


from:


AQARION realizability/sharpness


Status


ABSTRACT RESULT ESTABLISHED / AQARION SHARPNESS OPEN





P3.8 Support-spectrum theorem




Abstract lane


Establish the spectrum formula under the precise abstract graph definition.


AQARION lane


Prove that the required support graphs are realizable by the specified AQARION partition construction.


Status


Abstract theorem       OPEN/CLOSURE

AQARION realization    OPEN

Lean                   OPEN


No combined claim until both lanes close.





P3.9 Energy extremum




Current n=54 observations include the seven-singleton family and random search.


The observed value


[

\frac{1892}{47}\approx40.2553

]


is not a global maximum.


Random 20,000-sample result:


[

\frac{49526}{2209}\approx22.42009959.

]


Required work


Do not promote either as a global extremum.


Required:




exact optimization formulation;


combinatorial upper bound;


branch-and-bound or exhaustive reduction where feasible;


exact witness if a maximum is claimed.




Status


OPEN





P4 — Lean




P4.1 Kernel characterization


Current infrastructure includes completed components around:


defect_zero_iff_invariant_subspace

defect_zero_iff_quotient_exists


Status


Existing proof lane — maintain



P4.2 Replace incorrect kernel lemma


Close or replace the kernel characterization with the correctly typed block-constancy / zero-average statement.


Status


NEXT



P4.3 Projection imports


Integrate the required projection-operator definitions.


Status


OPEN



P4.4 Kaprekar semiconjugacy


Target:


[

\pi\circ K=T_G\circ\pi.

]


Status


OPEN / formalization



P4.5 Nilpotent index


Target the correct quotient nilpotent-index statement.


Status


OPEN



P4.6 Forest skeleton in Lean


Formalize:




finite graph;


incidence matrix;


forest;


component kernel;


defect map;


induced quotient.




Status


BLOCKED BY P3.3



P4.7 No fake Lean closure


Do not use:


sorry

axiom

opaque theorem stand-in


to turn an open mathematical result into a nominally completed certificate.


An explicitly marked formalization skeleton is preferable to an unproved theorem.





P5 — Witness package




Required witness families:


witnesses/

├── n8/

├── n14/

└── k2_2/


Each witness should contain:


claim_id

definition_version

input

partition

support_graph

invariants

exact_result

expected_relation

verification_method

digest

status


Do not invent missing raw witness data.


Known witness constraints


N8:


m_T = 0

Δ = 1

κ = 1


N14:


S = {0,1,2}

s0 = 1

m_T = 0

κ = 2

Δ = 2

s_T = 3


K2_2:


s = 4

κ = -1


These values must not be expanded into fabricated partitions or graph structures without source data.


Status


OPEN





P5 — Audit closure




Create/maintain:


audits/refuted_claims.md


Every refutation must include:




claim;


exact definition;


counterexample;


computed result;


corrected statement;


affected files;


migration status.




Status


NEXT





P5 — Certification package




Required:


certification/

├── file_tree.md

├── layer_1_mutation_receipt.txt

├── layer_2_canonical_receipt.txt

├── layer_3_exploratory.md

└── aqarion_certificate.json


Status


file tree        CREATED/DESIGNED

Layer 1          PASS

Layer 2          PASS

Layer 3          WORKLOAD

certificate      NEXT





P5 — Governance




Maintain:


governance/reproducibility_policy.md


It must prohibit:




hash-as-proof;


rerun-as-independent-reproduction;


workload-as-theorem;


exploratory output as certification;


unsupported publication promotion;


fabricated provenance.




Status


NEXT





P6 — Literature integration




Literature work should support actual unresolved mathematical questions rather than become another bibliography dump.


Priority areas:


finite dynamical systems

graph incidence rank

hypergraph 2-sections

weighted Laplacians

Koopman invariant subspaces

observable quotients

provenance/reproducibility

formal verification


RO-Crate workflow provenance should track the current 1.3/0.6 standards rather than the older 1.1/0.5 assumptions.


RO-Crate's workflow specification explicitly supports describing scripts as "SoftwareSourceCode", with runtime information, inputs, and outputs.


Status


ACTIVE / targeted





Publication gate




Publication remains blocked until all required gates are satisfied.


Minimum closure:


Definitions frozen

↓

Canonical tests passing

↓

Mutation gate passing

↓

Exact receipts inspected

↓

Exploratory claims separated

↓

Structural theorem dependencies closed

↓

Lean status accurately represented

↓

Independent reproduction contract exercised

↓

Evidence ledger reconciled

↓

C4 review

↓

Publication decision


No step may be skipped because a computational result is numerically convincing.





Dependency graph




P0 definition locks

│

├──────────────┐

↓              ↓

P1 verification     P2 provenance

│              │

└──────┬───────┘

↓

P3 structural math

│

┌──────┴─────────┐

↓                ↓

P4 Lean          P5 witnesses

│                │

└──────┬─────────┘

↓

certification

│

↓

C4

│

↓

publication




Immediate execution order




The next work sequence is:




Correct/finish root checkpoint and roadmap


Finish certification/file_tree.md


Create certification/aqarion_certificate.json


Create exact Layer 1 receipt


Create exact Layer 2 receipt


Create Layer 3 exploratory status


Install actual .github/workflows/aqarion-ci.yml


Correct R1/R2/R3 scope labels


Replace floating rank where practical with exact rank


Create reproducibility contract


Create adversarial reproduction cases


Close forest-skeleton theorem


Revisit native operator bridge


Formalize the closed structural theorem in Lean


Reconcile witness package


Re-run only after mutations/definitions are reconciled


Update certification state


Reassess C4







Explicit do-not-do list




Do not:


DO NOT duplicate certification packages across repos.

DO NOT create another generic certificate format.

DO NOT call a rerun an independent reproduction.

DO NOT treat SHA256 equality as semantic proof.

DO NOT turn 200 random trials into an exhaustive theorem.

DO NOT call two AQ-001 test cases universal verification.

DO NOT promote Layer 3 exploratory workloads.

DO NOT claim AQARION support-spectrum realizability from an abstract graph result.

DO NOT fabricate witness contents.

DO NOT add Lean sorry/axiom placeholders and call the theorem proved.

DO NOT create publication artifacts while C4 is blocked.

DO NOT move canonical mathematics into dashboard/UI repositories.

DO NOT create inert GitHub workflow YAML outside .github/workflows/.





Definition of done




The current research package is ready for C4 review only when:


[ ] all active definitions are version-locked

[ ] all refuted claims are migrated

[ ] Layer 1 mutation gate passes

[ ] Layer 2 receipts pass

[ ] Layer 2 scope labels are correct

[ ] Layer 3 remains explicitly exploratory

[ ] exact-rank requirements are satisfied where claimed

[ ] provenance contract is exercised

[ ] independent reproduction is demonstrated where claimed

[ ] forest-skeleton dependency is resolved

[ ] support-spectrum AQARION realization is resolved

[ ] native operator bridge is resolved or explicitly withdrawn

[ ] Lean status matches actual proofs

[ ] witnesses contain source-backed raw data

[ ] certificate metadata matches receipts

[ ] certification tree reconciles with actual files

[ ] no repository mutation is falsely reported

[ ] C4 governance review is performed


Until those conditions are met:


C4 = BLOCKED

Publication = BLOCKED


That is a governance state, not a failure of the mathematical research.Placement is therefore:


AQARION-ARITHMETIC/

├── CHECKPOINT.md

├── ROADMAP-TO-DO.md

└── certification/

└── file_tree.md


The important correction is that the roadmap now makes the forest-kernel theorem → native bridge → Lean → certification dependency explicit instead of letting another round of computational receipts obscure the unresolved mathematics.


JASKSG9/Aqarion-Quantarion-AI/certification/


I attempted to open that exact GitHub path, but GitHub's page fetch was blocked in this environment, so I cannot honestly inspect the live contents of that folder. Search does independently surface your AQARION GitHub ecosystem, including the AQARION/FDS and RO-Crate repositories, but it does not give me the contents of this exact path.


Therefore: keep it ALL under certification/


Do not move CHECKPOINT.md or ROADMAP-TO-DO.md to the repository root.


Your structure should be:


Aqarion-Quantarion-AI/

└── certification/

├── file_tree.md

├── CHECKPOINT.md

├── ROADMAP-TO-DO.md

│

├── layer_1_mutation_receipt.txt

├── layer_2_canonical_receipt.txt

├── layer_3_exploratory.md

├── aqarion_certificate.json

│

├── governance/

│   └── reproducibility_policy.md

│

├── reproducibility/

│   └── reproduction_contract.schema.json

│

├── theory/

│   └── support_spectrum_theorem.md

│

├── audits/

│   └── refuted_claims.md

│

├── witnesses/

│   ├── n8/

│   ├── n14/

│   └── k2_2/

│

└── lean/

└── support_spectrum.md


One important correction to my previous answer


I was reasoning from the mathematical canonical repo (AQARION-ARITHMETIC) rather than from the certification package you've actually established in Aqarion-Quantarion-AI.


Those are different roles.


For this package, the correct boundary is:


Aqarion-Quantarion-AI/certification/ = the certification/reconciliation package.


The mathematical source material can remain elsewhere. This certification directory can reference those sources rather than duplicating their entire contents.


https://huggingface.co/Quantarion9/AQARION-DEFECT
