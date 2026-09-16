# schemas

## Purpose
JSON schemas defining claim records, verification manifests, receipts, and reproduction objects.

## Current Schemas
- AQARION-CLAIM-RECORD-1 — used by claims/sv-001-v2.json
- AQARION-VERIFICATION-MANIFEST-1 — used by verification/manifest.json
- AQARION-RUN-RECEIPT-1 / RECEIPT-2 — used by verification/receipts/run_all_receipt.json
- REPRODUCTION-OBJECT-SCHEMA — template in objects/

## Fail-Closed Requirements
- pass_requires_all_registered_checks: true
- not_implemented_is_failure: true
- missing_artifact_is_failure: true
- external_fallback_paths_forbidden: true

No schema may promote NOT_IMPLEMENTED to PASS.
