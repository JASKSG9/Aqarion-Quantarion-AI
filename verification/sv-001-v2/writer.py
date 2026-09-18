#!/usr/bin/env python3
from __future__ import annotations
import argparse, json
from pathlib import Path

REQUIRED = {"receipt_version","contract_id","status","evidence_class","domain","verification","binding","runtime","independence","notes"}

def validate(receipt: dict) -> list[str]:
    errors = []
    missing = REQUIRED - set(receipt)
    if missing:
        errors.append("missing fields: " + ", ".join(sorted(missing)))
    if receipt.get("contract_id") != "SV-001-V2":
        errors.append("wrong contract_id")
    if receipt.get("evidence_class") != "[V]":
        errors.append("wrong evidence class")
    domain = receipt.get("domain", {})
    if domain.get("cases") != 1176:
        errors.append("domain cases != 1176")
    if domain.get("zero_r") != 196:
        errors.append("domain zero_r != 196")
    if domain.get("nonzero_r") != 980:
        errors.append("domain nonzero_r != 980")
    verification = receipt.get("verification", {})
    if verification.get("cases") != 1176:
        errors.append("verification cases != 1176")
    if verification.get("failures") != 0:
        errors.append("verification failures != 0")
    if verification.get("status") != "PASS":
        errors.append("verification status != PASS")
    binding = receipt.get("binding", {})
    for key in ("git_commit","contract_sha256","manifest_sha256"):
        if not binding.get(key):
            errors.append(f"missing binding field: {key}")
    independence = receipt.get("independence", {})
    if independence.get("same_algorithm") is not False:
        errors.append("oracle/verifier independence declaration invalid")
    if independence.get("external_independent_reproduction") is not False:
        errors.append("external reproduction must not be falsely claimed")
    return errors

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("receipt", type=Path)
    args = parser.parse_args()
    receipt = json.loads(args.receipt.read_text(encoding="utf-8"))
    errors = validate(receipt)
    if errors:
        print("RECEIPT_STATUS=FAIL")
        for e in errors:
            print(f"ERROR: {e}")
        raise SystemExit(1)
    print("RECEIPT_STATUS=PASS")

if __name__ == "__main__":
    main()
    #!/usr/bin/env python3
"""SV-001-V2 receipt validator."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


REQUIRED = {
    "receipt_version",
    "contract_id",
    "status",
    "evidence_class",
    "domain",
    "verification",
    "binding",
    "runtime",
    "independence",
    "notes",
}


def validate(receipt: dict) -> list[str]:
    errors = []

    missing = REQUIRED - set(receipt)
    if missing:
        errors.append("missing fields: " + ", ".join(sorted(missing)))

    if receipt.get("contract_id") != "SV-001-V2":
        errors.append("wrong contract_id")
    if receipt.get("evidence_class") != "[V]":
        errors.append("wrong evidence class")

    domain = receipt.get("domain", {})
    if domain.get("cases") != 1176:
        errors.append("domain cases != 1176")
    if domain.get("zero_r") != 196:
        errors.append("domain zero_r != 196")
    if domain.get("nonzero_r") != 980:
        errors.append("domain nonzero_r != 980")

    verification = receipt.get("verification", {})
    if verification.get("cases") != 1176:
        errors.append("verification cases != 1176")
    if verification.get("failures") != 0:
        errors.append("verification failures != 0")
    if verification.get("status") != "PASS":
        errors.append("verification status != PASS")

    binding = receipt.get("binding", {})
    for key in ("git_commit", "contract_sha256", "manifest_sha256"):
        if not binding.get(key):
            errors.append(f"missing binding field: {key}")

    independence = receipt.get("independence", {})
    if independence.get("same_algorithm") is not False:
        errors.append("oracle/verifier independence declaration invalid")
    if independence.get("external_independent_reproduction") is not False:
        errors.append("external reproduction must not be falsely claimed")

    return errors


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("receipt", type=Path)
    args = parser.parse_args()

    receipt = json.loads(args.receipt.read_text(encoding="utf-8"))
    errors = validate(receipt)

    if errors:
        print("RECEIPT_STATUS=FAIL")
        for e in errors:
            print(f"ERROR: {e}")
        raise SystemExit(1)

    print("RECEIPT_STATUS=PASS")


if __name__ == "__main__":
    main()
