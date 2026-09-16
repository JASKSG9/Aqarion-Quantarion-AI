#!/usr/bin/env python3
"""
AQARION canonical verification runner.

FILE:
    verification/run_all.py

TYPE:
    PYTHON SCRIPT

RULE:
    PASS is possible only when every manifest check actually executes
    and returns exit code 0.

NOT_IMPLEMENTED, SKIPPED, MISSING, MALFORMED, or BLOCKED are failures.

This runner does not establish mathematical truth.
It establishes only the execution result of the registered verification
checks.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent.parent
VERIFICATION = ROOT / "verification"
DEFAULT_MANIFEST = VERIFICATION / "manifest.json"
DEFAULT_RECEIPT = VERIFICATION / "receipts" / "run_all_receipt.json"


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def load_json(path: Path) -> dict[str, Any]:
    if not path.is_file():
        raise RuntimeError(f"missing JSON file: {path}")

    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise RuntimeError(f"invalid JSON: {path}: {exc}") from exc

    if not isinstance(value, dict):
        raise RuntimeError(f"JSON root must be an object: {path}")

    return value


def validate_manifest(manifest: dict[str, Any]) -> list[dict[str, Any]]:
    checks = manifest.get("checks")

    if not isinstance(checks, list) or not checks:
        raise RuntimeError("manifest must contain a non-empty 'checks' list")

    seen: set[str] = set()
    normalized: list[dict[str, Any]] = []

    for index, check in enumerate(checks):
        if not isinstance(check, dict):
            raise RuntimeError(f"manifest check {index} is not an object")

        check_id = check.get("id")
        command = check.get("command")

        if not isinstance(check_id, str) or not check_id:
            raise RuntimeError(f"manifest check {index} has invalid id")

        if check_id in seen:
            raise RuntimeError(f"duplicate manifest check id: {check_id}")

        seen.add(check_id)

        if (
            not isinstance(command, list)
            or not command
            or not all(isinstance(x, str) and x for x in command)
        ):
            raise RuntimeError(
                f"manifest check {check_id} has invalid command"
            )

        normalized.append(check)

    return normalized


def run_check(check: dict[str, Any]) -> dict[str, Any]:
    check_id = check["id"]
    command = check["command"]

    proc = subprocess.run(
        command,
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )

    status = "PASS" if proc.returncode == 0 else "FAIL"

    return {
        "id": check_id,
        "command": command,
        "status": status,
        "returncode": proc.returncode,
        "stdout": proc.stdout,
        "stderr": proc.stderr,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--manifest",
        default=str(DEFAULT_MANIFEST),
    )
    parser.add_argument(
        "--receipt",
        default=str(DEFAULT_RECEIPT),
    )
    args = parser.parse_args()

    manifest_path = Path(args.manifest).resolve()
    receipt_path = Path(args.receipt).resolve()

    try:
        manifest = load_json(manifest_path)
        checks = validate_manifest(manifest)
    except RuntimeError as exc:
        print(f"MANIFEST FAIL: {exc}", file=sys.stderr)
        return 2

    results: list[dict[str, Any]] = []

    print(f"Loaded manifest {len(checks)} checks")

    for check in checks:
        result = run_check(check)
        results.append(result)

        print(
            f"[{result['status']}] "
            f"{result['id']} "
            f"exit={result['returncode']}"
        )

        if result["stdout"]:
            print(result["stdout"], end="")

        if result["stderr"]:
            print(result["stderr"], file=sys.stderr, end="")

    failed = [
        result
        for result in results
        if result["status"] != "PASS"
    ]

    receipt = {
        "schema": "AQARION-RUN-RECEIPT-1",
        "generated_at": utc_now(),
        "repository_root": str(ROOT),
        "manifest": str(manifest_path.relative_to(ROOT)),
        "status": "FAIL" if failed else "PASS",
        "checks": [
            {
                "id": result["id"],
                "status": result["status"],
                "returncode": result["returncode"],
            }
            for result in results
        ],
    }

    receipt_path.parent.mkdir(parents=True, exist_ok=True)
    receipt_path.write_text(
        json.dumps(receipt, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )

    if failed:
        print(
            f"RUN-ALL FAIL: {len(failed)} of {len(results)} checks failed",
            file=sys.stderr,
        )
        return 1

    print(f"RUN-ALL PASS: {len(results)} checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
