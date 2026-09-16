#!/usr/bin/env python3
"""Fail closed if canonical verification paths are absent."""
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
required = [
    "verification/run_all.py",
    "verification/replay_harness.py",
    "verification/manifest.json",
    "verification/requirements.txt",
    "verification/README.md",
]
missing = [p for p in required if not (ROOT / p).is_file()]
for p in required:
    print(f"{'PATH_PASS' if p not in missing else 'PATH_FAIL'}={p}")
raise SystemExit(1 if missing else 0)
