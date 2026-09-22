AQARION Arithmetic — Research Checkpoint


Date: 2026-09-22

Repository: AQARION-ARITHMETIC

Scope: finite dynamical systems, partition refinement, Koopman defect, support-spectrum structure, reproducibility, and formalization

Checkpoint status: active research / certification preparation

Governance: C4 blocked; publication blocked; Lean open



1. Current research state


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



2. Evidence classes


The project distinguishes:




Class
Meaning




theorem
mathematically established result


verified
formally proved or mechanically checked under a defined proof system


empirical
computational observation


conjecture
proposed but unproved statement


refuted
contradicted by an exact counterexample


workload
computation executed as an exploratory workload but not sufficient for promotion




Computational receipts are not silently upgraded to mathematical proofs.



3. Canonical mathematical results


3.1 Partition refinement


For a finite map


[
T:X\to X
]


and partition \Pi_t,


[
\Pi_{t+1}


\Pi_t\wedge T^{-1}\Pi_t.
]


The refinement process terminates on finite X.


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


The deprecated legacy quantity s_t must not be reused in new certification material.



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



4. Bipartite support graph


For partition


[
\Pi={A_1,\ldots,A_m},
]


construct the bipartite support graph whose source vertices represent partition blocks and whose target vertices represent partition blocks.


An edge A_i\to A_j exists whenever


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



5. Weighted realization correction


For incidence matrix B and positive diagonal edge-weight matrix W,


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



6. Native operator bridge status


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





7. Forest skeleton target


For the target-support hypergraph


[
\mathcal H_\Pi=([m],{R_i}),
]


let H be its 2-section.


For a spanning forest F of H, the proposed structural target is


[
\ker D_\Pi=\ker B_F^T.
]


This would yield a noncanonical factorization


[
D_\Pi=A_FB_F^T.
]


The quotient images may then be canonically related even though the factorization itself depends on the selected forest.


This is currently a theorem target, not a closed Lean theorem.



8. Matroid result/status


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



9. Rank bound


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


Equality regimes have been identified separately for odd and even n.


The AQARION-specific sharpness/realizability argument must remain distinct from the abstract graph bound.



10. Support-spectrum theorem status


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



11. Exact finite baselines


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


g_1\ne r: 18,000;


depth-class counts:



\ell_0=39,300


\ell_1=96,080


\ell_2=24,720


\ell_3=2,400;






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



12. Domain lock


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



13. AQARION certification state


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



14. Governance


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



15. Reproducibility architecture


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



16. Repository boundary


The canonical mathematical source of truth is:


AQARION-ARITHMETIC/



The certification package is:


certification/



The actual GitHub Actions entry point is:


.github/workflows/aqarion-ci.yml



A YAML file merely placed under CI/ is not automatically a GitHub Actions workflow.



17. Known refuted or deprecated claims


The following must not be reintroduced:




universal g_1=r;


defect-norm monotonicity under refinement;


entropy monotonicity under refinement;


cross-base nilpotency invariance;


commutator necessity for D=0;


E_G=\ker D as the general matroid identification;


ordinary projection in place of the weighted projection;


vertex-space and edge-space kernels treated as the same typed object;


hash equality presented as semantic equivalence;


same-executable reruns presented as independent reproduction;


computational receipts presented as formal proofs;


AQARION-specific support-spectrum sharpness inferred solely from an abstract graph theorem.





18. Immediate checkpoint conclusion


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



The next work should therefore reduce unresolved theorem and provenance dependencies rather than generate additional redundant certificates.

Yes. For now, only create this one file in the canonical repo:


AQARION-ARITHMETIC/certification/file_tree.md


This is the complete certification subtree for the deliverables we just defined; it does not claim that unrelated files elsewhere in the repository already exist.


Create exactly that file for now: certification/file_tree.md. No other repo or directory needs to be touched yet.

AQARION Research File Tree


September 22, 2026


aqarion-arithmetic/
│
├── README.md
├── CHECKPOINT.md
├── CLAIMS.md
├── STATUS.md
├── FILE_TREE.md
│
├── governance/
│   ├── evidence-policy.md
│   ├── claim-status.md
│   ├── audit-policy.md
│   ├── promotion-policy.md
│   ├── no-computation-as-proof.md
│   └── reproducibility-policy.md
│
├── theory/
│   ├── definitions.md
│   ├── finite-dynamics.md
│   ├── partition-lattice.md
│   ├── equivalence-relations.md
│   ├── kernel-pairs.md
│   ├── congruences.md
│   ├── behavioral-refinement.md
│   ├── quotient-descent.md
│   ├── invariant-subspaces.md
│   ├── koopman-operator.md
│   ├── koopman-convention.md
│   ├── defect-operator.md
│   ├── defect-kernel.md
│   ├── incidence-graph.md
│   ├── marked-support.md
│   ├── support-curvature.md
│   ├── cycle-rank.md
│   ├── support-spectrum-theorem.md
│   ├── support-spectrum-constructions.md
│   └── backward-closure.md
│
├── theorems/
│   ├── t0-definitions.md
│   ├── t1-factor-map.md
│   ├── t2-invariant-subspace.md
│   ├── t3-defect-zero.md
│   ├── t4-transport-identity.md
│   ├── t5-closure-properties.md
│   ├── t6-meet-join-relation.md
│   ├── t7-closure-loss.md
│   ├── t8-support-graph-identity.md
│   ├── t9-support-curvature.md
│   ├── t10-c3-nonnegativity.md
│   ├── t11-c3-exact-spectrum.md
│   ├── t12-general-support-spectrum.md
│   ├── t13-first-negative-support.md
│   └── t14-finite-backward-closure.md
│
├── transport/
│   ├── transport-identity.md
│   ├── delta-definition.md
│   ├── mt-definition.md
│   ├── mt-zero-equivalence.md
│   ├── delta-equals-kappa.md
│   └── witnesses.md
│
├── witnesses/
│   ├── README.md
│   ├── n8/
│   │   ├── witness.json
│   │   └── receipt.md
│   ├── n14/
│   │   ├── witness.json
│   │   └── receipt.md
│   ├── p5/
│   │   └── receipt.md
│   └── k2_2/
│       ├── witness.json
│       └── receipt.md
│
├── kaprekar/
│   ├── definitions.md
│   ├── digit-map.md
│   ├── gap-projection.md
│   ├── semiconjugacy.md
│   ├── q54-quotient.md
│   ├── q55-null-inclusive.md
│   ├── image-chains.md
│   ├── spectrum.md
│   └── universal-bases.md
│
├── audits/
│   ├── audit-ledger.md
│   ├── adversarial-findings.md
│   ├── counterexamples.md
│   ├── claim-downgrades.md
│   ├── refuted-claims.md
│   └── open-claims.md
│
├── audits/
│   └── pullback/
│       ├── quotient-bijection-refuted.md
│       └── kernel-pair-correction.md
│
├── certification/
│   ├── aqarion-certificate.json
│   ├── layer-1-mutation-receipt.md
│   ├── layer-2-canonical-receipt.md
│   ├── layer-3-exploratory.md
│   ├── reproducibility-contract.md
│   └── hashes.md
│
├── tests/
│   ├── mutation_test.py
│   ├── test_brt_q54.py
│   ├── test_aq001.py
│   ├── test_depth_exact.py
│   ├── test_frob_equal.py
│   ├── support_spectrum.py
│   └── test_t10.py
│
├── lean/
│   ├── README.md
│   ├── SupportSpectrum.lean
│   ├── Transport.lean
│   ├── Defect.lean
│   └── BackwardClosure.lean
│
├── literature/
│   └── source-matrix.md
│
├── open-problems/
│   ├── pullback-join-stability.md
│   ├── lean-support-spectrum.md
│   └── general-quotient-theory.md
│
├── archive/
│   ├── disproved/
│   │   ├── quotient-bijection.md
│   │   ├── submodularity-route.md
│   │   ├── commutator-shortcut.md
│   │   └── invariant-kernel-assumption.md
│   └── superseded/
│       ├── old-c3-bound.md
│       ├── old-support-counts.md
│       └── old-quotient-model.md
│
└── .github/
    └── workflows/
        └── aqarion-ci.yml



Execution rule


.github/workflows/aqarion-ci.yml is the executable GitHub Actions workflow.


A copy under ci/ is documentation only and must not be treated as an active workflow.


Naming rule


All newly introduced paths use lowercase names.


Existing legacy paths are not silently renamed by this specification.


A capitalization migration is a separate repository operation.


Physical-existence rule


This file describes the target research organization.


It does not assert that every listed artifact currently exists.


The current repository must be reconciled against this tree before any commit.


Promotion rule


Only artifacts with an explicit evidence class and claim status may enter the active theorem/certification spine.

https://github.com/JASKSG9/Aqarion-Quantarion-AI/tree/main/certification
https://huggingface.co/Quantarion9
~/AQARION-ARITHMETIC-FDS-FINITE-DYNAMICAL-SYSTEMS- $  ~/AQARION-ARITHMETIC-FDS-FINITE-DYNAMICAL-SYSTEMS- $ ```bash
> sha256sum \
>   AI/verification/pullback_join/verify_preimage_join.py \
>   AI/verification/pullback_join/artifacts/aq-dyn-pull-preimage-join-report.json \
>   AI/verification/pullback_join/NEGATIVE_CONTROL_PREIMAGE_JOIN.md \
>   > AI/verification/pullback_join/artifacts/aq-dyn-pull-preimage-join-receipt.sha256
> cat AI/verification/pullback_join/artifacts/aq-dyn-pull-preimage-join-receipt.sha256
> ^C
~/AQARION-ARITHMETIC-FDS-FINITE-DYNAMICAL-SYSTEMS- $ cat AI/verification/pullback_join/artifacts/aq-dyn-pull-preimage-join-receipt.sha256                         1d0dc898cc73a177dd7d8155348b0d7ba39e526107afcd45a6561bd0ee1ab5eb  AI/verification/pullback_join/verify_preimage_join.py
a6e3f55c776a0832de3aca7db8429c5e99bd4a011fb8750b648ede222ff4d9c0  AI/verification/pullback_join/artifacts/aq-dyn-pull-preimage-join-report.json
~/AQARION-ARITHMETIC-FDS-FINITE-DYNAMICAL-SYSTEMS- $ sha256sum \
AI/verification/pullback_join/artifacts/aq-dyn-pull-join-report.json \
  > AI/verification/pullback_join/artifacts/aq-dyn-pull-join-n5-receipt.sha256>   AI/verification/pullback_join/verify_pullback_join.py \                         >   AI/verification/pullback_join/verify_pullback_join_n5.py \
>   AI/verification/pullback_join/artifacts/aq-dyn-pull-join-report.json \
>   > AI/verification/pullback_join/artifacts/aq-dyn-pull-join-n5-receipt.sha256
~/AQARION-ARITHMETIC-FDS-FINITE-DYNAMICAL-SYSTEMS- $  ~/AQARION-ARITHMETIC-FDS-FINITE-DYNAMICAL-SYSTEMS- $ cat AI/verification/pullback_join/artifacts/aq-dyn-pull-join-n5-receipt.sha256
61cbb20be89c1126b85c74b253e2452fdb2f5904131b40f39b5c071e3604e83b  AI/verification/pullback_join/verify_pullback_join.py
65c6a6fa3a60bebbb25dfd5993507ed0866036105da61f3bcbad7ac753c31c75  AI/verification/pullback_join/verify_pullback_join_n5.py
2f050f2a032a28dd00a5b549e4764a37bf3c8c3ecced5a33c68c6d04c0cac97c  AI/verification/pullback_join/artifacts/aq-dyn-pull-join-report.json                            ~/AQARION-ARITHMETIC-FDS-FINITE-DYNAMICAL-SYSTEMS- $ ls -lh AI/verification/pullback_join/NEGATIVE_CONTROL_PREIMAGE_JOIN.md 2>&1
ls: cannot access 'AI/verification/pullback_join/NEGATIVE_CONTROL_PREIMAGE_JOIN.md': No such file or directory
~/AQARION-ARITHMETIC-FDS-FINITE-DYNAMICAL-SYSTEMS- $ sha256sum AI/verification/pullback_join/verify_preimage_join.py AI/verification/pullback_join/artifacts/aq-dyn-pull-preimage-join-report.json AI/verification/pullback_join/NEGATIVE_CONTROL_PREIMAGE_JOIN.md > AI/verification/pullback_join/artifacts/aq-dyn-pull-preimage-join-receipt.sha256                                     sha256sum: AI/verification/pullback_join/NEGATIVE_CONTROL_PREIMAGE_JOIN.md: No such file or directory
~/AQARION-ARITHMETIC-FDS-FINITE-DYNAMICAL-SYSTEMS- $ cat AI/verification/pullback_join/artifacts/aq-dyn-pull-preimage-join-receipt.sha256
1d0dc898cc73a177dd7d8155348b0d7ba39e526107afcd45a6561bd0ee1ab5eb  AI/verification/pullback_join/verify_preimage_join.py
a6e3f55c776a0832de3aca7db8429c5e99bd4a011fb8750b648ede222ff4d9c0  AI/verification/pullback_join/artifacts/aq-dyn-pull-preimage-join-report.json
~/AQARION-ARITHMETIC-FDS-FINITE-DYNAMICAL-SYSTEMS- $ cat AI/verification/pullback_join/artifacts/aq-dyn-pull-preimage-join-receipt.sha256```bash
> command here
> ^C
~/AQARION-ARITHMETIC-FDS-FINITE-DYNAMICAL-SYSTEMS- $
~/AQARION-ARITHMETIC-FDS-FINITE-DYNAMICAL-SYSTEMS- $ sha256sum \
>   AI/verification/pullback_join/verify_preimage_join.py \
>   AI/verification/pullback_join/artifacts/aq-dyn-pull-preimage-join-report.json \
>   > AI/verification/pullback_join/artifacts/aq-dyn-pull-preimage-join-receipt.sha256
~/AQARION-ARITHMETIC-FDS-FINITE-DYNAMICAL-SYSTEMS- $ sha256sum -c \
>   AI/verification/pullback_join/artifacts/aq-dyn-pull-preimage-join-receipt.sha256                        AI/verification/pullback_join/verify_preimage_join.py: OK
AI/verification/pullback_join/artifacts/aq-dyn-pull-preimage-join-report.json: OK
~/AQARION-ARITHMETIC-FDS-FINITE-DYNAMICAL-SYSTEMS- $ 0~/AQARION-ARITHMETIC-FDS-FINITE-DYNAMICAL-SYSTEMS- $  ~/AQARION-ARITHMETIC-FDS-FINITE-DYNAMICAL-SYSTEMS- $ ```bash
> sha256sum \
>   AI/verification/pullback_join/verify_preimage_join.py \
>   AI/verification/pullback_join/artifacts/aq-dyn-pull-preimage-join-report.json \
>   AI/verification/pullback_join/NEGATIVE_CONTROL_PREIMAGE_JOIN.md \
>   > AI/verification/pullback_join/artifacts/aq-dyn-pull-preimage-join-receipt.sha256
> cat AI/verification/pullback_join/artifacts/aq-dyn-pull-preimage-join-receipt.sha256
> ^C
~/AQARION-ARITHMETIC-FDS-FINITE-DYNAMICAL-SYSTEMS- $ cat AI/verification/pullback_join/artifacts/aq-dyn-pull-preimage-join-receipt.sha256                         1d0dc898cc73a177dd7d8155348b0d7ba39e526107afcd45a6561bd0ee1ab5eb  AI/verification/pullback_join/verify_preimage_join.py
a6e3f55c776a0832de3aca7db8429c5e99bd4a011fb8750b648ede222ff4d9c0  AI/verification/pullback_join/artifacts/aq-dyn-pull-preimage-join-report.json
~/AQARION-ARITHMETIC-FDS-FINITE-DYNAMICAL-SYSTEMS- $ sha256sum \
AI/verification/pullback_join/artifacts/aq-dyn-pull-join-report.json \
  > AI/verification/pullback_join/artifacts/aq-dyn-pull-join-n5-receipt.sha256>   AI/verification/pullback_join/verify_pullback_join.py \                         >   AI/verification/pullback_join/verify_pullback_join_n5.py \
>   AI/verification/pullback_join/artifacts/aq-dyn-pull-join-report.json \
>   > AI/verification/pullback_join/artifacts/aq-dyn-pull-join-n5-receipt.sha256
~/AQARION-ARITHMETIC-FDS-FINITE-DYNAMICAL-SYSTEMS- $  ~/AQARION-ARITHMETIC-FDS-FINITE-DYNAMICAL-SYSTEMS- $ cat AI/verification/pullback_join/artifacts/aq-dyn-pull-join-n5-receipt.sha256
61cbb20be89c1126b85c74b253e2452fdb2f5904131b40f39b5c071e3604e83b  AI/verification/pullback_join/verify_pullback_join.py
65c6a6fa3a60bebbb25dfd5993507ed0866036105da61f3bcbad7ac753c31c75  AI/verification/pullback_join/verify_pullback_join_n5.py
2f050f2a032a28dd00a5b549e4764a37bf3c8c3ecced5a33c68c6d04c0cac97c  AI/verification/pullback_join/artifacts/aq-dyn-pull-join-report.json                            ~/AQARION-ARITHMETIC-FDS-FINITE-DYNAMICAL-SYSTEMS- $ ls -lh AI/verification/pullback_join/NEGATIVE_CONTROL_PREIMAGE_JOIN.md 2>&1
ls: cannot access 'AI/verification/pullback_join/NEGATIVE_CONTROL_PREIMAGE_JOIN.md': No such file or directory
~/AQARION-ARITHMETIC-FDS-FINITE-DYNAMICAL-SYSTEMS- $ sha256sum AI/verification/pullback_join/verify_preimage_join.py AI/verification/pullback_join/artifacts/aq-dyn-pull-preimage-join-report.json AI/verification/pullback_join/NEGATIVE_CONTROL_PREIMAGE_JOIN.md > AI/verification/pullback_join/artifacts/aq-dyn-pull-preimage-join-receipt.sha256                                     sha256sum: AI/verification/pullback_join/NEGATIVE_CONTROL_PREIMAGE_JOIN.md: No such file or directory
~/AQARION-ARITHMETIC-FDS-FINITE-DYNAMICAL-SYSTEMS- $ cat AI/verification/pullback_join/artifacts/aq-dyn-pull-preimage-join-receipt.sha256
1d0dc898cc73a177dd7d8155348b0d7ba39e526107afcd45a6561bd0ee1ab5eb  AI/verification/pullback_join/verify_preimage_join.py
a6e3f55c776a0832de3aca7db8429c5e99bd4a011fb8750b648ede222ff4d9c0  AI/verification/pullback_join/artifacts/aq-dyn-pull-preimage-join-report.json
~/AQARION-ARITHMETIC-FDS-FINITE-DYNAMICAL-SYSTEMS- $ cat AI/verification/pullback_join/artifacts/aq-dyn-pull-preimage-join-receipt.sha256```bash
> command here
> ^C
~/AQARION-ARITHMETIC-FDS-FINITE-DYNAMICAL-SYSTEMS- $
~/AQARION-ARITHMETIC-FDS-FINITE-DYNAMICAL-SYSTEMS- $ sha256sum \
>   AI/verification/pullback_join/verify_preimage_join.py \
>   AI/verification/pullback_join/artifacts/aq-dyn-pull-preimage-join-report.json \
>   > AI/verification/pullback_join/artifacts/aq-dyn-pull-preimage-join-receipt.sha256
~/AQARION-~/AQARION-ARITHMETIC-FDS-FINITE-DYNAMICAL-SYSTEMS- $  ~/AQARION-ARITHMETIC-FDS-FINITE-DYNAMICAL-SYSTEMS- $ ```bash
> sha256sum \
>   AI/verification/pullback_join/verify_preimage_join.py \
>   AI/verification/pullback_join/artifacts/aq-dyn-pull-preimage-join-report.json \
>   AI/verification/pullback_join/NEGATIVE_CONTROL_PREIMAGE_JOIN.md \
>   > AI/verification/pullback_join/artifacts/aq-dyn-pull-preimage-join-receipt.sha256
> cat AI/verification/pullback_join/artifacts/aq-dyn-pull-preimage-join-receipt.sha256
> ^C
~/AQARION-ARITHMETIC-FDS-FINITE-DYNAMICAL-SYSTEMS- $ cat AI/verification/pullback_join/artifacts/aq-dyn-pull-preimage-join-receipt.sha256                         1d0dc898cc73a177dd7d8155348b0d7ba39e526107afcd45a6561bd0ee1ab5eb  AI/verification/pullback_join/verify_preimage_join.py
a6e3f55c776a0832de3aca7db8429c5e99bd4a011fb8750b648ede222ff4d9c0  AI/verification/pullback_join/artifacts/aq-dyn-pull-preimage-join-report.json
~/AQARION-ARITHMETIC-FDS-FINITE-DYNAMICAL-SYSTEMS- $ sha256sum \
AI/verification/pullback_join/artifacts/aq-dyn-pull-join-report.json \
  > AI/verification/pullback_join/artifacts/aq-dyn-pull-join-n5-receipt.sha256>   AI/verification/pullback_join/verify_pullback_join.py \                         >   AI/verification/pullback_join/verify_pullback_join_n5.py \
>   AI/verification/pullback_join/artifacts/aq-dyn-pull-join-report.json \
>   > AI/verification/pullback_join/artifacts/aq-dyn-pull-join-n5-receipt.sha256
~/AQARION-ARITHMETIC-FDS-FINITE-DYNAMICAL-SYSTEMS- $  ~/AQARION-ARITHMETIC-FDS-FINITE-DYNAMICAL-SYSTEMS- $ cat AI/verification/pullback_join/artifacts/aq-dyn-pull-join-n5-receipt.sha256
61cbb20be89c1126b85c74b253e2452fdb2f5904131b40f39b5c071e3604e83b  AI/verification/pullback_join/verify_pullback_join.py
65c6a6fa3a60bebbb25dfd5993507ed0866036105da61f3bcbad7ac753c31c75  AI/verification/pullback_join/verify_pullback_join_n5.py
2f050f2a032a28dd00a5b549e4764a37bf3c8c3ecced5a33c68c6d04c0cac97c  AI/verification/pullback_join/artifacts/aq-dyn-pull-join-report.json                            ~/AQARION-ARITHMETIC-FDS-FINITE-DYNAMICAL-SYSTEMS- $ ls -lh AI/verification/pullback_join/NEGATIVE_CONTROL_PREIMAGE_JOIN.md 2>&1
ls: cannot access 'AI/verification/pullback_join/NEGATIVE_CONTROL_PREIMAGE_JOIN.md': No such file or directory
~/AQARION-ARITHMETIC-FDS-FINITE-DYNAMICAL-SYSTEMS- $ sha256sum AI/verification/pullback_join/verify_preimage_join.py AI/verification/pullback_join/artifacts/aq-dyn-pull-preimage-join-report.json AI/verification/pullback_join/NEGATIVE_CONTROL_PREIMAGE_JOIN.md > AI/verification/pullback_join/artifacts/aq-dyn-pull-preimage-join-receipt.sha256                                     sha256sum: AI/verification/pullback_join/NEGATIVE_CONTROL_PREIMAGE_JOIN.md: No such file or directory
~/AQARION-ARITHMETIC-FDS-FINITE-DYNAMICAL-SYSTEMS- $ cat AI/verification/pullback_join/artifacts/aq-dyn-pull-preimage-join-receipt.sha256
1d0dc898cc73a177dd7d8155348b0d7ba39e526107afcd45a6561bd0ee1ab5eb  AI/verification/pullback_join/verify_preimage_join.py
a6e3f55c776a0832de3aca7db8429c5e99bd4a011fb8750b648ede222ff4d9c0  AI/verification/pullback_join/artifacts/aq-dyn-pull-preimage-join-report.json
~/AQARION-ARITHMETIC-FDS-FINITE-DYNAMICAL-SYSTEMS- $ cat AI/verification/pullback_join/artifacts/aq-dyn-pull-preimage-join-receipt.sha256```bash
> command here
> ^C
~/AQARION-ARITHMETIC-FDS-FINITE-DYNAMICAL-SYSTEMS- $
~/AQARION-ARITHMETIC-FDS-FINITE-DYNAMICAL-SYSTEMS- $ sha256sum \
>   AI/verification/pullback_join/verify_preimage_join.py \
>   AI/verification/pullback_join/artifacts/aq-dyn-pull-preimage-join-report.json \
>   > AI/verification/pullback_join/artifacts/aq-dyn-pull-preimage-join-receipt.sha256
~/AQARION-ARITHMETIC-FDS-FINITE-DYNAMICAL-SYSTEMS- $ sha256sum -c \
>   AI/verification/pullback_join/artifacts/aq-dyn-pull-preimage-join-receipt.sha256                        AI/verification/pullback_join/verify_preimage_join.py: OK
AI/verification/pullback_join/artifacts/aq-dyn-pull-preimage-join-report.json: OK
~/AQARION-ARITHMETIC-FDS-FINITE-DYNAMICAL-SYSTEMS- $ 0-FDS-FINITE-DYNAMICAL-SYSTEMS- $ sha256sum -c \
>   AI/verification/pullback_join/artifacts/aq-dyn-pull-preimage-join-receipt.sha256                        AI/verification/pullback_join/verify_preimage_join.py: OK
AI/verification/pullback_join/artifacts/aq-dyn-pull-preimage-join-report.json: OK
~/AQARION-ARITHMETIC-FDS-FINITE-DYNAMICAL-SYSTEMS- $ 0
