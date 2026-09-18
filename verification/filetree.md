# verification/filetree.md

Generated: 2026-09-18
HEAD audited: 7f5f1c6
Status: FROZEN AUDIT — repository closure in progress

---

## Purpose

This directory contains the executable finite verification and provenance
infrastructure for the AQARION research corpus.

A passing computational replay does **not** establish a universal
mathematical theorem.
A passing provenance check does **not** establish mathematical truth.
A public repository does **not** constitute independent reproduction.

### Evidence discipline

- public      ≠ certified
- runnable    ≠ verified
- numeric     ≠ proof
- matching output ≠ independence
- Lean file   ≠ Lean proof
- policy ALLOW ≠ mathematical truth
- repository existence ≠ reproduction

---

## Current executable surface

```text
verification/
├── aq_contract/
│   └── aq_contract_semantic_suite.py
│
├── aq_oracle/
│   └── aq_independent_oracle_suite.py
│
├── aq_s14/
│   ├── __init__.py                       [PENDING: rename from inite.py]
│   └── aq_s14_semantic_suite.py
│
├── evidence/
│   ├── aq-evidence-core.py
│   ├── aq-s16-evidence-reach.md
│   └── test-aq-evidence-core.py
│
├── fixtures/
│   ├── c3-n14.json
│   ├── c3-n8.json
│   └── k2r-family.json
│
├── receipts/
│   ├── aqarion-ci-verification-receipt.json
│   └── aqarion-execution-001.json
│
├── sv-001-v2/
│   ├── mutation/
│   │   ├── __init__.py
│   │   ├── executor.py
│   │   └── metamorphic.py
│   │
│   ├── receipt/
│   │   ├── __init__.py
│   │   ├── schema.json
│   │   └── writer.py
│   │
│   ├── __init__.py
│   ├── contract.json
│   ├── oracle.py
│   ├── replay.py
│   └── verifier.py
│
├── LICENSE
├── adversarial-forged_pass.py
├── adversarial-init.py
├── adversarial-missing-execution.py
├── adversarial-self-comparison.py
├── adversarial-stale-root.py
├── adversarial-wrong-hash.py
├── aq-mutation-suit.py
├── aq-support-spectrum.py
├── aq-t10-graphic-rank-audit.py
├── aro-1-adversarial-cases.json
├── aro-1-schema.json
├── aro-1.md
├── ci-verification-closure-2026-09-16.md
├── filetree.md
├── manifest.json
├── promotion-gate.py
├── provenance.py
├── readme.md
├── replay-harness.py
├── reproducibility-policy.md
├── requirements.txt
├── run-all-receipt.json
├── run-all.py
├── verify-hashes.py
├── verify-paths.py
├── verify-pytests.init
├── verify-repository.py
├── verify-semantic.py
└── verify_registry_schema.py
