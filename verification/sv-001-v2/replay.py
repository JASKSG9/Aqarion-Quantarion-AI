#!/usr/bin/env python3
"""SV-001-V2 canonical replay. Writes a bound receipt."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import platform
import subprocess
from pathlib import Path

from verifier import run_all
from oracle import enumerate_cases


ROOT = Path(__file__).resolve().parents[2]
PACKAGE = Path(__file__).resolve().parent
CONTRACT = PACKAGE / "contract.json"
MANIFEST = ROOT / "verification" / "manifest.json"


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def git_revision() -> str:
    env_sha = os.environ.get("GITHUB_SHA")
    if env_sha:
        return env_sha
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"],
            cwd=ROOT,
            text=True,
        ).strip()
    except Exception:
        return "UNKNOWN"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--receipt", required=True, type=Path)
    args = parser.parse_args()

    if not CONTRACT.is_file():
        raise SystemExit("FAIL: contract.json missing")
    if not MANIFEST.is_file():
        raise SystemExit("FAIL: verification/manifest.json missing")

    cases = list(enumerate_cases())
    if len(cases) != 1176:
        raise SystemExit("FAIL: canonical domain is not 1176 cases")

    zero_r = sum(s % k == 0 for m, k, s in cases)
    if zero_r != 196:
        raise SystemExit("FAIL: zero-r count is not 196")

    result = run_all()
    status = result["status"]

    receipt = {
        "receipt_version": "SV-001-V2-RECEIPT-1",
        "contract_id": "SV-001-V2",
        "status": status,
        "evidence_class": "[V]",
        "governance": {
            "c4": "BLOCKED",
            "promotion": False,
            "formal_status": "LEAN_OPEN",
            "public_certification": False,
        },
        "domain": {
            "cases": len(cases),
            "zero_r": zero_r,
            "nonzero_r": len(cases) - zero_r,
        },
        "verification": result,
        "binding": {
            "git_commit": git_revision(),
            "contract_sha256": sha256_file(CONTRACT),
            "manifest_sha256": sha256_file(MANIFEST),
        },
        "runtime": {
            "python": platform.python_version(),
            "implementation": platform.python_implementation(),
            "system": platform.system(),
            "release": platform.release(),
            "machine": platform.machine(),
        },
        "independence": {
            "oracle": "closed_form_contract",
            "verifier": "direct_matrix_construction",
            "same_algorithm": False,
            "external_independent_reproduction": False,
        },
        "notes": [
            "This receipt records finite computational evidence only.",
            "It is not a formal proof.",
            "It is not C4 certification.",
            "Hash binding does not establish semantic correctness by itself.",
        ],
    }

    args.receipt.parent.mkdir(parents=True, exist_ok=True)
    args.receipt.write_text(
        json.dumps(receipt, sort_keys=True, separators=(",", ":")) + "\n"
    )
    print(json.dumps(receipt, indent=2))
    raise SystemExit(0 if status == "PASS" else 1)


if __name__ == "__main__":
    main()
