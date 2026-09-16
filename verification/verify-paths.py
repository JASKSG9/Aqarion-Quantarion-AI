#!/usr/bin/env python3
"""Verify that the declared verification surface actually exists."""

from pathlib import Path
import json
import sys


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "verification" / "manifest.json"


def fail(message: str) -> None:
    print(f"FAIL: {message}")
    raise SystemExit(1)


def main() -> int:
    if not MANIFEST.is_file():
        fail("verification/manifest.json is missing")

    try:
        data = json.loads(MANIFEST.read_text(encoding="utf-8"))
    except Exception as exc:
        fail(f"manifest is not valid JSON: {exc}")

    checks = data.get("checks")

    if not isinstance(checks, list):
        fail("manifest.checks is not a list")

    missing = []

    for item in checks:
        path = item.get("path")
        if not isinstance(path, str):
            fail("manifest check has no string path")

        if not (ROOT / path).exists():
            missing.append(path)

    if missing:
        print("FAIL: missing declared paths:")
        for path in missing:
            print(f"  {path}")
        return 1

    workflow_dir = ROOT / ".github" / "workflows"

    if not workflow_dir.is_dir():
        fail(".github/workflows is missing")

    workflows = list(workflow_dir.glob("*.y*ml"))

    if not workflows:
        fail(".github/workflows contains no workflow")

    print("PATH-CLOSURE=PASS")
    print(f"manifest={MANIFEST.relative_to(ROOT)}")
    print(f"workflows={len(workflows)}")
    print(f"registered_checks={len(checks)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
