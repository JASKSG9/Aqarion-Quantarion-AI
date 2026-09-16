#!/usr/bin/env python3
"""Repository hygiene and canonical-surface verification."""

from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]


REQUIRED = [
    ".github/workflows/verify.yml",
    "verification/manifest.json",
    "verification/run_all.py",
    "verification/replay_harness.py",
    "verification/verify_paths.py",
    "verification/verify_registry_schema.py",
    "verification/verify_hashes.py",
    "verification/verify_repository.py",
    "verification/provenance.py",
    "source/python/claimlock.py",
]


FORBIDDEN_CANONICAL_DRIFT = [
    ".github/workflow",
    "verification/mainfest.json",
    "verification/run-all.py",
    "verification/replay-harness.py",
    "verification/verify-paths.py",
    "verification/verify-semantic.py",
    "verification/verify-hashes.py",
    "verification/verify-repository.py",
]


def main() -> int:
    failed = False

    for relative in REQUIRED:
        if (ROOT / relative).exists():
            print(f"PASS required {relative}")
        else:
            print(f"FAIL required {relative}")
            failed = True

    for relative in FORBIDDEN_CANONICAL_DRIFT:
        if (ROOT / relative).exists():
            print(f"FAIL stale-name {relative}")
            failed = True

    if failed:
        return 1

    print("REPOSITORY-HYGIENE=PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
