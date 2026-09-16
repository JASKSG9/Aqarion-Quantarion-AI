#!/usr/bin/env python3
"""Placeholder registry gate: prevents silent substitution of legacy scripts.

This does not assert theorem equivalence. It only requires every registered
check to provide an exact source path and declared scope in manifest.json.
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
manifest = json.loads((ROOT / "verification/manifest.json").read_text())
errors = []
for check in manifest.get("checks", []):
    for key in ("check_id", "path", "command", "scope"):
        if key not in check: errors.append(f"{check.get('check_id','UNKNOWN')}:MISSING_{key}")
print("SEMANTIC_REGISTRY_PASS" if not errors else "SEMANTIC_REGISTRY_FAIL")
for error in errors: print(error)
raise SystemExit(0 if not errors else 1)
