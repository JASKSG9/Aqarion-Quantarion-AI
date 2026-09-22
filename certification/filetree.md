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

Yes. For now, only create this one file in the canonical repo:


AQARION-ARITHMETIC/certification/file_tree.md


This is the complete certification subtree for the deliverables we just defined; it does not claim that unrelated files elsewhere in the repository already exist.


Create exactly that file for now: certification/file_tree.md. No other repo or directory needs to be touched yet.

