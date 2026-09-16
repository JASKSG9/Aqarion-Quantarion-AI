AQARION Verification Surface
Purpose
This directory is the canonical Python replay surface for AQARION. It replaces case-sensitive mixed names such as VERIFICATION/PROJECTION.PY only after an explicit Git migration.
Governance
A passing replay establishes only its declared finite scope.
Replay does not establish a general theorem or Lean certification.
Every run emits a JSON receipt.
Missing checks, mismatched expected paths, and malformed manifests fail closed.
Canonical entry point
python3 verification/run_all.py --manifest verification/manifest.json --receipt AQ-S16-CI-RECEIPT.json
Before migration
Do not delete or overwrite legacy VERIFICATION/ files. First map and rename them with git mv, update imports, run the harness locally, then update CI.
