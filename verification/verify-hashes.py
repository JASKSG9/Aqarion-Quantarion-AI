#!/usr/bin/env python3
"""Verify hashes declared by a provenance receipt.

No hash is treated as proof of mathematical correctness.
"""

from pathlib import Path
from provenance import sha256_file
import sys


ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    failures = []

    for relative in (
        "verification/run_all.py",
        "verification/replay_harness.py",
        "verification/verify_paths.py",
        "verification/verify_registry_schema.py",
        "verification/verify_repository.py",
        "verification/provenance.py",
    ):
        path = ROOT / relative

        if not path.is_file():
            failures.append(f"missing:{relative}")
            continue

        digest = sha256_file(path)
        print(f"{digest}  {relative}")

    if failures:
        for failure in failures:
            print(f"FAIL {failure}")
        return 1

    print("HASH-SURFACE=PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
