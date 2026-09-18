verification/
├── aq_contract/
│ └── aq_contract_semantic_suite.py
├── aq_oracle/
│ ├── aq_independent_oracle_suite.py
│ └── mip_dip_audit.py [NEW - FABRICATED from spec §3, does not exist in current HEAD, A22=166484 A23=180]
├── aq_s14/
│ ├── aq_s14_semantic_suite.py
│ └── inite.py [typo - should be __init__.py]
├── evidence/
│ ├── aq-evidence-core.py [Level-1 Content Integrity]
│ ├── aq-s16-evidence-reach.md
│ └── test-aq-evidence-core.py [14/14 PASS]
├── fixtures/
│ ├── c3-n14.json
│ ├── c3-n8.json
│ └── k2r-family.json
├── receipts/
│ ├── aqarion-ci-verification-receipt...
│ └── aqarion-execution001.json
├── LICENSE
├── adversarial-forged_pass.py
├── adversarial-init.py
├── adversarial-missing-executio...
├── adversarial-self-comparison...
├── adversarial-stale-root.py
├── adversarial-wrong-hash.py
├── aq-mutation-suit.py
├── aq-support-spectrum.py
├── aq-t10-graphic-rank-audit.py
├── aro-1-adversarial-cases.json
├── aro-1-schema.json
├── aro-1.md
├── ci-verification-closure-2026-...
├── filetree.md [this file]
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

Actions #42 PASS historical. HEAD 7f5f1c6 requires fresh #43 run.

# AQARION Verification Surface

## Purpose
This directory contains executable finite verification and provenance infrastructure for the AQARION research corpus.

A passing computational replay does **not** establish a universal mathematical theorem.
A passing provenance check does **not** establish mathematical truth.
A public repository does **not** constitute independent reproduction.

Evidence discipline:
- public!= certified
- runnable!= verified
- numeric == proof == NO
- matching output!= independence
- Lean file!= Lean proof
- policy ALLOW!= truth

## Current Executable Surface — 2026-09-16 HEAD 7f5f1c6

Canonical runner:


# verification/filetree.md
# Generated: 2026-09-16 — HEAD 7f5f1c6 — FROZEN AUDIT

verification/
├── aq_contract/ # reproduction contract + registry schema
├── aq_oracle/ # oracle definitions
├── aq_s14/ # AQ-S14 semantic suite (7 PASS)
├── evidence/ # AQ-EVIDENCE-CORE — canonical_bytes, sha256, receipt
│ ├── aq_evidence_core.py
│ └── tests/
├── fixtures/ # K2R fixtures AQ-K2R-R2,R3,R5,R15.json
├── receipts/ # run-all-receipt.json + binding receipts
├── LICENSE
├── adversarial-forged_pass.py
├── adversarial-init.py
├── adversarial-missing-executio...py
├── adversarial-self-comparison....py
├── adversarial-stale-root.py
├── adversarial-wrong-hash.py
├── aq-mutation-suit.py
├── aq-support-spectrum.py
├── aq-t10-graphic-rank-audit.py
├── aro-1-adversarial-cases.json
├── aro-1-schema.json
├── aro-1.md
├── ci-verification-closure.md
├── filetree.md # this file
├── manifest.json # conservative: 1 check
├── promotion-gate.py
├── provenance.py # clean — output_match!= independence
├── readme.md
├── replay-harness.py
├── requirements.txt # pytest only
├── run-all-receipt.json # RECEIPT-2 self-binding
├── run-all.py # canonical runner
├── verify-hashes.py
├── verify-paths.py
├── verify-pytests.init
├── verify-repository.py
├── verify-semantic.py
└── verify_registry_schema.py

Executable entry:
python3 verification/run-all.py --manifest verification/manifest.json --receipt verification/receipts/run-all-receipt.json

Governance: C4 BLOCKED, Publication BLOCKED, Promotable false
Evidence: COMPUTED [V] finite only — not FORMALLY_VERIFIED
