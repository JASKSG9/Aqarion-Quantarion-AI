Certification file tree


Repository: AQARION-ARITHMETIC

Certification scope: verification, receipts, governance status, and certification metadata

Status: working deliverable tree

Authority: this file describes the intended certification package; it is not itself a certification result.


certification/
├── file_tree.md
│
├── layer_1_mutation_receipt.txt
│   └── Correct Koopman operator vs mutated transfer operator
│       ├── correct implementation: 5000/5000 pass
│       ├── mutant implementation: 0/5000 pass
│       └── mutation detected: true
│
├── layer_2_canonical_receipt.txt
│   ├── R1: BRT rank = m - c_bip
│   │   └── 200-trial computational receipt
│   ├── R2: AQ-001 D = 0 ↔ congruence
│   │   └── 2-partition regression receipt
│   ├── R3: depth partition rank
│   │   └── computational receipt for the canonical depth partition
│   └── R4: Frobenius identity
│       └── 90-case exact regression receipt
│
├── layer_3_exploratory.md
│   ├── support-spectrum workload
│   ├── T10 workload
│   ├── exploratory results
│   └── explicit non-promotion status
│
└── aqarion_certificate.json
    ├── certification layers
    ├── governance state
    ├── reproducibility state
    ├── formalization state
    └── publication state



Certification boundary


The certification/ directory contains receipts and certification metadata.


It does not contain:




canonical theorem definitions;


research proofs;


experimental source code;


Lean proofs;


literature reviews;


raw witness construction;


publication manuscripts.




Those belong to their respective repository directories.


Evidence classification




Artifact
Evidence type
Certification role




layer_1_mutation_receipt.txt
computational verification
mutation gate


layer_2_canonical_receipt.txt
computational verification
canonical regression gate


layer_3_exploratory.md
exploratory computation
non-promotion evidence


aqarion_certificate.json
governance metadata
machine-readable status


file_tree.md
documentation
package structure only




Layer 1 — mutation gate


layer_1_mutation_receipt.txt



Records whether the test suite distinguishes the canonical Koopman implementation from the intentionally mutated implementation.


A passing mutation gate demonstrates mutation detection for the specified test workload. It does not constitute a mathematical proof of the underlying Koopman theorem.


Layer 2 — canonical receipts


layer_2_canonical_receipt.txt



Contains the four canonical regression receipts:


R1  BRT rank = m - c_bip
R2  AQ-001 D = 0 ↔ congruence
R3  depth-partition rank
R4  Frobenius identity



The receipt must preserve the actual workload size and method.


In particular:




R1 is a 200-trial computational receipt, not an exhaustive proof.


R2 is a two-partition regression, not a universal exhaustive test.


R3 is a computational verification of the canonical depth partition.


R4 contains the 90 specified cases.




Layer 3 — exploratory workload


layer_3_exploratory.md



Contains support-spectrum and T10 exploratory computations.


Layer 3 is explicitly not promotion-grade certification until the associated assertions, exact definitions, and realization conditions are closed.


Machine-readable certification state


aqarion_certificate.json



The certificate records status rather than asserting unsupported mathematical conclusions.


It must distinguish at minimum:


PASS
WORKLOAD
OPEN
BLOCKED
QUARANTINED



It must not encode:


PROVED
CERTIFIED
PUBLISHED



unless the corresponding governance and evidence conditions have actually been satisfied.


Certification exclusions


The following are intentionally outside this directory:


tests/
theory/
audits/
witnesses/
lean/
literature/
open_problems/
governance/
reproducibility/



Those directories contain the evidence or definitions consumed by certification; they are not themselves certification receipts.


Current governance boundary


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



These statuses describe the certification package state and must be updated only when new evidence changes the corresponding gate.


Reproducibility requirement


Every future certification receipt should identify:




specification or claim identifier;


specification digest where applicable;


exact input/workload;


implementation identifier;


execution environment;


reference execution;


reproduction execution;


reproduction relationship;


output digest;


evidence classification;


governance disposition.




A matching output is evidence of reproducibility only when the executions satisfy the stated independence/reproduction contract.


A rerun of the same implementation is not an independent reproduction.


File-tree rule


This tree is authoritative only for the certification package.


It does not imply that every referenced file currently exists.


A file becomes a certification artifact only when its contents have been created, executed where required, inspected, and assigned an evidence status.

