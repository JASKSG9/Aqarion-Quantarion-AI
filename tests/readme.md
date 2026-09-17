# tests/readme-filetree.md — 2026-09-16

tests/
├── aq-001.py # ARO-1
├── mutation-tests.py # evidence core mutations 14/14
├── test-brt-q54.py
├── test-depth-exact.py
├── test-frob-equal.py
└── test-reproduction-contract.py # contract TEMPLATE guard

Run: python3 -m pytest tests/ -v

# tests/ — AQARION Test Surface

## Purpose
Independent pytest-discoverable tests for saturation criterion, evidence core, and reproduction contract.

Previous failure: `QUICKSTART/AQARION-RIP/TESTS` collected 0 tests due to non-discoverable filenames and stale fixture paths. This directory fixes that.

## Files

- `aq-001.py` — 15 min ago — ARO-1 smoke test (Bell(8)=4140, 4138 nontrivial)
- `mutation-tests.py` — 17 min ago — 14/14 adversarial mutation tests for AQ-EVIDENCE-CORE (must PASS)
- `test-brt-q54.py` — 13 min ago — BRT Q54 depth/exact checks
- `test-depth-exact.py` — 14 min ago — depth exactness
- `test-frob-equal.py` — 12 min ago — Frobenius equality checks
- `test-reproduction-contract.py` — 11 min ago — contract registry + TEMPLATE vs EXECUTED semantics

## Execution

```bash
python3 -m pytest tests/ -v
# Expected: 6+ tests collected, all PASS, 0 collected is FAIL
