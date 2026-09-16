#!/usr/bin/env python3
"""Canonical verification orchestrator."""

from __future__ import annotations

from pathlib import Path
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[1]

CHECKS = [
    ["python", "verification/verify_paths.py"],
    ["python", "verification/verify_registry_schema.py"],
    ["python", "verification/verify_hashes.py"],
    ["python", "verification/verify_repository.py"],
]


def run(command: list[str]) -> int:
    print(f"\n$ {' '.join(command)}")
    proc = subprocess.run(
        command,
        cwd=ROOT,
        check=False,
    )
    return proc.returncode


def main() -> int:
    failures = 0

    for command in CHECKS:
        code = run(command)
        if code != 0:
            failures += 1

    print()
    print(f"VERIFICATION-CHECKS={len(CHECKS)}")
    print(f"VERIFICATION-FAILURES={failures}")

    if failures:
        print("VERIFICATION=FAIL")
        return 1

    print("VERIFICATION=PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
