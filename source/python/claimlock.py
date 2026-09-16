#!/usr/bin/env python3
"""
AQARION × QUANTARION AI — CLAIMLOCK minimal kernel.

Purpose:
    Derive whether a requested promotion is authorized by evidence scope
    and explicit policy requirements.

Non-goals:
    - It does not decide whether a mathematical statement is true.
    - It does not validate a SHA-256 digest against real artifact bytes.
    - It does not perform Lean compilation.
    - It does not clear SDS-002, C4, or publication.

Core rule:
    Claims do not promote themselves.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import platform
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        payload = json.load(handle)

    if not isinstance(payload, dict):
        raise ValueError(f"Expected JSON object: {path}")

    return payload


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()

    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)

    return "sha256:" + digest.hexdigest()


def scope_rank(scope: str, policy: dict[str, Any]) -> int:
    order = policy["scope_order"]

    if scope not in order:
        raise ValueError(f"Unknown evidence scope: {scope}")

    return order[scope]


def highest_evidence_scope(claim: dict[str, Any], policy: dict[str, Any]) -> str | None:
    evidence = claim.get("evidence", [])

    if not evidence:
        return None

    scopes = []

    for item in evidence:
        established = item.get("established_scope", {})
        scope = established.get("kind")

        if isinstance(scope, str):
            scopes.append(scope)

    if not scopes:
        return None

    return max(scopes, key=lambda value: scope_rank(value, policy))


def has_exact_computation(claim: dict[str, Any]) -> bool:
    accepted = {
        "EXACT_COMPUTATION",
        "EXACT_RATIONAL_COMPUTATION",
        "REPLAY"
    }

    return any(
        item.get("kind") in accepted and item.get("result") == "PASS"
        for item in claim.get("evidence", [])
    )


def has_independent_check(claim: dict[str, Any]) -> bool:
    return any(
        item.get("kind") == "INDEPENDENT_REPLAY"
        and item.get("result") == "PASS"
        for item in claim.get("evidence", [])
    )


def formalization_ready(claim: dict[str, Any]) -> bool:
    status = claim.get("formalization", {}).get("status")

    return status in {
        "KERNEL_ACCEPTED",
        "INDEPENDENTLY_CHECKED",
        "CERTIFIED"
    }


def evaluate_claim(
    claim: dict[str, Any],
    policy: dict[str, Any]
) -> dict[str, Any]:
    requested = claim.get("requested_promotion")

    requirements = policy["promotion_requirements"].get(requested)

    if requirements is None:
        return {
            "outcome": policy["failure_policy"]["unknown_promotion"],
            "reason_codes": ["CL_UNKNOWN_PROMOTION"],
            "reasons": [f"No policy requirements exist for: {requested}"],
            "effective_evidence_scope": None,
            "promotion_allowed": False
        }

    established_scope = highest_evidence_scope(claim, policy)

    if established_scope is None:
        return {
            "outcome": policy["failure_policy"]["missing_evidence"],
            "reason_codes": ["CL_MISSING_EVIDENCE"],
            "reasons": ["No evidence item declares an established scope."],
            "effective_evidence_scope": None,
            "promotion_allowed": False
        }

    required_scope = requirements["minimum_scope"]

    if scope_rank(established_scope, policy) < scope_rank(required_scope, policy):
        return {
            "outcome": policy["failure_policy"]["scope_insufficient"],
            "reason_codes": ["CL_SCOPE_INSUFFICIENT"],
            "reasons": [
                f"Evidence establishes {established_scope}, "
                f"but {requested} requires {required_scope}."
            ],
            "effective_evidence_scope": established_scope,
            "promotion_allowed": False
        }

    if requirements["require_exact_computation"] and not has_exact_computation(claim):
        return {
            "outcome": policy["failure_policy"]["missing_evidence"],
            "reason_codes": ["CL_EXACT_COMPUTATION_MISSING"],
            "reasons": ["Required exact computation evidence is absent."],
            "effective_evidence_scope": established_scope,
            "promotion_allowed": False
        }

    if requirements["require_formalization"] and not formalization_ready(claim):
        return {
            "outcome": policy["failure_policy"]["formalization_missing"],
            "reason_codes": ["CL_FORMALIZATION_MISSING"],
            "reasons": [
                "Requested promotion requires a kernel-accepted "
                "or independently checked formalization."
            ],
            "effective_evidence_scope": established_scope,
            "promotion_allowed": False
        }

    if requirements["require_independent_check"] and not has_independent_check(claim):
        return {
            "outcome": policy["failure_policy"]["independent_check_missing"],
            "reason_codes": ["CL_INDEPENDENT_CHECK_MISSING"],
            "reasons": [
                "Requested promotion requires an independent replay "
                "or checker receipt."
            ],
            "effective_evidence_scope": established_scope,
            "promotion_allowed": False
        }

    return {
        "outcome": "ALLOW",
        "reason_codes": [],
        "reasons": ["All currently modeled policy obligations passed."],
        "effective_evidence_scope": established_scope,
        "promotion_allowed": True
    }


def write_receipt(
    receipt_path: Path,
    claim_path: Path,
    policy_path: Path,
    decision: dict[str, Any],
    claim: dict[str, Any],
    policy: dict[str, Any]
) -> None:
    receipt = {
        "receipt_schema": "aqarion.claimlock.receipt.v1",
        "created_utc": datetime.now(timezone.utc).isoformat(),

        "claim": {
            "claim_id": claim.get("claim_id"),
            "requested_promotion": claim.get("requested_promotion"),
            "declared_scope": claim.get("declared_scope"),
            "sha256": sha256_file(claim_path)
        },

        "policy": {
            "policy_id": policy.get("policy_id"),
            "policy_version": policy.get("policy_version"),
            "sha256": sha256_file(policy_path)
        },

        "decision": decision,

        "environment": {
            "python_executable": sys.executable,
            "python_version": sys.version,
            "platform": platform.platform(),
            "machine": platform.machine()
        },

        "governance": policy.get("governance", {}),

        "limitations": [
            "This receipt is a local policy-evaluation artifact.",
            "Artifact digest strings inside claim evidence are not independently validated by this prototype.",
            "The decision is limited to modeled policy obligations.",
            "A policy ALLOW result does not prove universal mathematical truth.",
            "SDS-002, C4, Lean certification, and publication remain independently governed."
        ]
    }

    receipt_path.parent.mkdir(parents=True, exist_ok=True)

    receipt_path.write_text(
        json.dumps(receipt, indent=2, sort_keys=True) + "
",
        encoding="utf-8"
    )


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Evaluate an AQARION × QUANTARION AI claim under CLAIMLOCK policy."
    )

    parser.add_argument(
        "--claim",
        required=True,
        type=Path,
        help="Path to a claim JSON record."
    )

    parser.add_argument(
        "--policy",
        required=True,
        type=Path,
        help="Path to a policy JSON record."
    )

    parser.add_argument(
        "--receipt",
        required=True,
        type=Path,
        help="Output path for a machine-readable decision receipt."
    )

    args = parser.parse_args()

    try:
        claim = load_json(args.claim)
        policy = load_json(args.policy)
        decision = evaluate_claim(claim, policy)

        write_receipt(
            args.receipt,
            args.claim,
            args.policy,
            decision,
            claim,
            policy
        )

        print(f"CLAIM_ID={claim.get('claim_id')}")
        print(f"REQUESTED_PROMOTION={claim.get('requested_promotion')}")
        print(f"EVIDENCE_SCOPE={decision.get('effective_evidence_scope')}")
        print(f"OUTCOME={decision['outcome']}")
        print(f"PROMOTION_ALLOWED={decision['promotion_allowed']}")
        print(f"RECEIPT={args.receipt}")

        for reason_code in decision["reason_codes"]:
            print(f"REASON_CODE={reason_code}")

        for reason in decision["reasons"]:
            print(f"REASON={reason}")

        return 0 if decision["outcome"] == "ALLOW" else 1

    except Exception as error:
        print("OUTCOME=INDETERMINATE")
        print("PROMOTION_ALLOWED=False")
        print(f"ERROR={type(error).__name__}:{error}")
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
