# AQARION CI Verification Policy

Every verification workflow must execute the actual artifact.

A workflow MUST NOT replace an executable verification step with:

- a prose assertion;
- a hard-coded expected PASS;
- a grep against a fabricated output;
- a second implementation copied directly from the first;
- an unexecuted placeholder.

The CI result is evidence of execution only.

---

## Reference pattern

```yaml
name: AQ-ARTIFACT Verification

on:
  push:
  pull_request:
  workflow_dispatch:

jobs:
  verify:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"

      - name: Execute artifact
        run: python3 PATH/TO/ACTUAL_ARTIFACT.py

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

# .github/workflows

Workflow registry for Aqarions-Quantarion-AI.

## Files

| File | Purpose |
|------|---------|
| `aqarion-ci.yml` | Core AQARION CI pipeline. |
| `verify.yml` | General verification dispatcher. |
| `sv-001-v2.yaml` | SV-001-V2 claim replay (1176 canonical cases). |
| `readme.md` | This file. |

## Naming convention

- `sv-001-v2.yaml` uses the `.yaml` extension. This is intentional and must
  match the self-audit and `aqarion.toml` declarations exactly.
- `.yml` and `.yaml` are **not** interchangeable in this repository.

## SV-001-V2 workflow

Triggered on push to `main`, pull request to `main`, and manual dispatch.

Steps:

1. Checkout at the exact revision.
2. Python 3.11 setup.
3. `numpy` install.
4. Verify all declared SV-001-V2 package files exist.
5. Repository self-audit (`verification/repo_self_audit.py`).
6. Reject the deprecated `5720` execution domain.
7. Run oracle census.
8. Run matrix verifier.
9. Run metamorphic tests.
10. Run mutation tests.
11. Generate runtime receipt (not committed).
12. Validate receipt schema.
13. Bind receipt to the executing commit (`GITHUB_SHA`).
14. Upload the receipt as a build artifact.

## Governance

A green run of `sv-001-v2.yaml` establishes **finite computational evidence**
only. It does not establish a Lean theorem, C4 certification, or external
independent reproduction.

C4: BLOCKED
Publication: BLOCKED
Promotion: false
