# source/data

## Purpose
Source-adjacent data and Python surfaces for CLAIMLOCK evaluation and future CL-1 binding.

## Current State — Live now
- `source/` contains Python package for legacy claimlock.py — Scope, Evidence, Claim, Policy, evaluate()
- `source/data/` reserved for data artifacts

## Current Limitation — Honest
Current claimlock.py is legacy evaluator, not CL-1 kernel. It does NOT yet cryptographically bind:
- claim_digest
- evidence_manifest_digest
- policy_digest
- verifier.id / version / artifact_digest
- execution.input_digest / output_digest / network_mode

CL-1 remains OPEN until predicate-report architecture implemented and adversarially tested. No promotion based on current evaluator.
