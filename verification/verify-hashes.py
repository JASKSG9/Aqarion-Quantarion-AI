#!/usr/bin/env python3
"""Verify a standard sha256sum manifest."""
import argparse, subprocess
from pathlib import Path

p = argparse.ArgumentParser()
p.add_argument("manifest", type=Path)
a = p.parse_args()
r = subprocess.run(["sha256sum", "-c", str(a.manifest)])
raise SystemExit(r.returncode)
