#!/usr/bin/env python3
"""
AQARION canonical verification runner.

Receipt schema:
    AQARION-RUN-RECEIPT-2

PASS means only that every registered manifest check executed
and returned exit code 0.

This runner does not establish mathematical truth.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import platform
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
    return datetime.now(timezone.utc).replace(
        microsecond=0
    ).isoformat()


def load_json(path: Path) -> dict[str, Any]:
    if not path.is_file():
        raise RuntimeError(f"missing JSON file: {path}")

    try:
        value = json.loads(
            path.read_text(encoding="utf-8")
        )
    except json.JSONDecodeError as exc:
        raise RuntimeError(
            f"invalid JSON: {path}: {exc}"
        ) from exc

    if not isinstance(value, dict):
        raise RuntimeError(
            f"JSON root must be an object: {path}"
        )

    return value


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()

    with path.open("rb") as handle:
        for chunk in iter(
            lambda: handle.read(1024 * 1024),
            b"",
        ):
            digest.update(chunk)

    return digest.hexdigest()


def git(*args: str) -> str:
    process = subprocess.run(
        ["git", *args],
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )

    if process.returncode != 0:
        raise RuntimeError(
            f"git {' '.join(args)} failed: "
            f"{process.stderr.strip()}"
        )

    return process.stdout.strip()


def validate_manifest(
    manifest: dict[str, Any],
) -> list[dict[str, Any]]:

    checks = manifest.get("checks")

    if not isinstance(checks, list) or not checks:
        raise RuntimeError(
            "manifest must contain a non-empty "
            "'checks' list"
        )

    seen: set[str] = set()
    normalized: list[dict[str, Any]] = []

    for index, check in enumerate(checks):

        if not isinstance(check, dict):
            raise RuntimeError(
                f"manifest check {index} "
                "is not an object"
            )

        check_id = check.get("id")
        command = check.get("command")

        if not isinstance(check_id, str) or not check_id:
            raise RuntimeError(
                f"manifest check {index} "
                "has invalid id"
            )

        if check_id in seen:
            raise RuntimeError(
                f"duplicate manifest check id: "
                f"{check_id}"
            )

        if (
            not isinstance(command, list)
            or not command
            or not all(
                isinstance(item, str) and item
                for item in command
            )
        ):
            raise RuntimeError(
                f"manifest check {check_id} "
                "has invalid command"
            )

        seen.add(check_id)
        normalized.append(check)

    return normalized


def run_check(
    check: dict[str, Any],
) -> dict[str, Any]:

    process = subprocess.run(
        check["command"],
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )

    return {
        "id": check["id"],
        "command": check["command"],
        "status": (
            "PASS"
            if process.returncode == 0
            else "FAIL"
        ),
        "returncode": process.returncode,
        "stdout": process.stdout,
        "stderr": process.stderr,
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

    manifest_path = Path(
        args.manifest
    ).resolve()

    receipt_path = Path(
        args.receipt
    ).resolve()

    try:
        manifest = load_json(manifest_path)
        checks = validate_manifest(manifest)

        commit = git(
            "rev-parse",
            "HEAD",
        )

        tree = git(
            "rev-parse",
            "HEAD^{tree}",
        )

    except RuntimeError as exc:
        print(
            f"SETUP FAIL: {exc}",
            file=sys.stderr,
        )
        return 2

    manifest_sha256 = sha256_file(
        manifest_path
    )

    print(
        f"Repository commit: {commit}"
    )

    print(
        f"Repository tree: {tree}"
    )

    print(
        f"Manifest SHA256: {manifest_sha256}"
    )

    print(
        f"Loaded manifest {len(checks)} checks"
    )

    results: list[dict[str, Any]] = []

    for check in checks:

        result = run_check(check)
        results.append(result)

        print(
            f"[{result['status']}] "
            f"{result['id']} "
            f"exit={result['returncode']}"
        )

        if result["stdout"]:
            print(
                result["stdout"],
                end="",
            )

        if result["stderr"]:
            print(
                result["stderr"],
                file=sys.stderr,
                end="",
            )

    failed = [
        result
        for result in results
        if result["status"] != "PASS"
    ]

    receipt = {
        "schema": (
            "AQARION-RUN-RECEIPT-2"
        ),
        "generated_at": utc_now(),
        "source": {
            "repository":
                "JASKSG9/Aqarions-Quantarion-AI",
            "commit": commit,
            "tree": tree,
        },
        "manifest": {
            "path": str(
                manifest_path.relative_to(ROOT)
            ),
            "sha256": manifest_sha256,
        },
        "runtime": {
            "python": platform.python_version(),
            "implementation":
                platform.python_implementation(),
            "platform": platform.platform(),
        },
        "status": (
            "FAIL"
            if failed
            else "PASS"
        ),
        "checks": [
            {
                "id": result["id"],
                "status": result["status"],
                "returncode":
                    result["returncode"],
            }
            for result in results
        ],
    }

    receipt_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    receipt_path.write_text(
        json.dumps(
            receipt,
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )

    if failed:

        print(
            "RUN-ALL FAIL: "
            f"{len(failed)} of "
            f"{len(results)} checks failed",
            file=sys.stderr,
        )

        return 1

    print(
        f"RUN-ALL PASS: "
        f"{len(results)} checks passed"
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
