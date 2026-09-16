#.github/workflows

## Purpose
Executable CI surface for AQARION / QUANTARION-AI hub.

## Current File
- `verify.yml` — AQARION Replay workflow
    - Checkout exact HEAD
    - Setup Python 3.11.16
    - `git rev-parse HEAD`
    - `python3 -m compileall -q verification`
    - `python3 verification/aq_s14/aq_s14_semantic_suite.py`
    - `python3 verification/run-all.py --manifest verification/manifest.json --receipt verification/receipts/run_all_receipt.json`
    - Validates receipt exists

## Current Status — Live
Run #42 on 5922c96dae992b7544b188d78fbe6934e2171be4: PASS

All steps success. No external dependencies installed. NumPy deliberately removed — AQ-S14 uses exact rational arithmetic from stdlib.

## Fail-Closed Rule
Workflow fails if any step returns non-zero. No NOT_IMPLEMENTED→PASS.

## Maintenance Note
Actions show Node 20→24 warning for checkout@v4 / setup-python@v5. Not a failure, track separately.
