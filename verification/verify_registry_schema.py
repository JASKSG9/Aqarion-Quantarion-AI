#!/usr/bin/env python3
"""Validate the verification registry schema.

This is a schema check.
It is NOT a theorem-equivalence or semantic-equivalence proof.
"""

from pathlib import Path
import json
import sys


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "verification" / "manifest.json"

REQUIRED = {
    "check_id",
    "kind",
    "path",
    "command",
    "scope",
}


def main() -> int:
    data = json.loads(MANIFEST.read_text(encoding="utf-8"))

    if data.get("schema") != "AQARION-VERIFICATION-MANIFEST-1":
        print("FAIL: unsupported manifest schema")
        return 1

    checks = data.get("checks")

    if not isinstance(checks, list) or not checks:
        print("FAIL: checks must be a non-empty list")
        return 1

    ids = set()

    for index, item in enumerate(checks):
        if not isinstance(item, dict):
            print(f"FAIL: check {index} is not an object")
            return 1

        missing = REQUIRED - item.keys()
        if missing:
            print(
                f"FAIL: check {index} missing "
                f"{sorted(missing)}"
            )
            return 1

        check_id = item["check_id"]

        if check_id in ids:
            print(f"FAIL: duplicate check_id={check_id}")
            return 1

        ids.add(check_id)

    print("REGISTRY-SCHEMA=PASS")
    print(f"checks={len(checks)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
