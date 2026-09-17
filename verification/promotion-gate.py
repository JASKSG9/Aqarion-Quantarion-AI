#!/usr/bin/env python3
"""
AQARION promotion gate.

Fails closed.

The gate checks repository state and provenance prerequisites.
It does not prove mathematical theorems; it prevents an execution
result from being presented as repository-certified when its binding
conditions are absent.
"""

from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent

MANIFEST = ROOT / "verification" / "manifest.json"
RECEIPT = ROOT / "verification" / "receipts" / "run_all_receipt.json"


def git(*args):
    p = subprocess.run(
        ["git", *args],
        cwd=ROOT,
        text=True,
        capture_output=True,
    )

    if p.returncode:
        raise RuntimeError(p.stderr.strip())

    return p.stdout.strip()


def sha256(path):
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(
            lambda: f.read(1024 * 1024),
            b"",
        ):
            h.update(chunk)
    return h.hexdigest()


def fail(message):
    print(f"PROMOTION BLOCKED: {message}")
    raise SystemExit(1)


def main():
    if not MANIFEST.is_file():
        fail("manifest missing")

    if not RECEIPT.is_file():
        fail("verification receipt missing")

    status = git("status", "--porcelain")
    if status:
        fail(
            "working tree is not clean; "
            "certification requires committed source"
        )

    commit = git("rev-parse", "HEAD")
    tree = git("rev-parse", "HEAD^{tree}")

    manifest = json.loads(
        MANIFEST.read_text(encoding="utf-8")
    )

    receipt = json.loads(
        RECEIPT.read_text(encoding="utf-8")
    )

    if receipt.get("schema") != "AQARION-RUN-RECEIPT-2":
        fail("wrong receipt schema")

    if receipt.get("status") != "PASS":
        fail("receipt status is not PASS")

    source = receipt.get("source", {})

    if source.get("commit") != commit:
        fail(
            "receipt commit does not equal current HEAD"
        )

    if source.get("tree") != tree:
        fail(
            "receipt tree does not equal current HEAD tree"
        )

    expected_manifest_sha = sha256(MANIFEST)

    actual_manifest_sha = (
        receipt.get("manifest", {})
        .get("sha256")
    )

    if actual_manifest_sha != expected_manifest_sha:
        fail("receipt manifest SHA256 mismatch")

    checks = receipt.get("checks", [])

    manifest_ids = {
        item["id"]
        for item in manifest.get("checks", [])
    }

    receipt_ids = {
        item["id"]
        for item in checks
    }

    if manifest_ids != receipt_ids:
        fail(
            "receipt check set differs from manifest"
        )

    if any(
        item.get("status") != "PASS"
        for item in checks
    ):
        fail("one or more registered checks failed")

    print("PROMOTION GATE PASS")
    print(f"commit={commit}")
    print(f"tree={tree}")
    print(f"manifest_sha256={expected_manifest_sha}")
    print(f"checks={len(checks)}")


if __name__ == "__main__":
    main()
