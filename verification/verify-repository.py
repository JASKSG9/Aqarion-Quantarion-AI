#!/usr/bin/env python3
"""Minimal repository hygiene checks for the canonical verification surface."""
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
checks = {
    "manifest_parseable": False,
    "no_uppercase_verification_dir": not (ROOT / "VERIFICATION").exists(),
}
try:
    json.loads((ROOT / "verification/manifest.json").read_text(encoding="utf-8"))
    checks["manifest_parseable"] = True
except Exception:
    pass
for k, v in checks.items(): print(f"{k}={'PASS' if v else 'FAIL'}")
raise SystemExit(0 if all(checks.values()) else 1)
