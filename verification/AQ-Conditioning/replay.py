from __future__ import annotations

import argparse
import json
import platform
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import numpy as np

from .canonical import sha256_file, sha256_json
from .fixtures import load_fixture
from .report import evaluate_fixture


DEFAULT_FIXTURES = [
    "fixtures/singular_exact.json",
    "fixtures/full_rank_permutation.json",
    "fixtures/near_singular_epsilon.json",
    "fixtures/column_stochastic_kernel.json",
]


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def runtime_environment() -> dict[str, str]:
    return {
        "python_version": sys.version,
        "python_implementation": platform.python_implementation(),
        "platform": platform.platform(),
        "machine": platform.machine(),
        "numpy_version": np.__version__,
    }


def load_contract(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--contract", default="CONTRACT.json")
    parser.add_argument("--output", default="artifacts/conditioning-receipt.json")
    parser.add_argument("--rank-tolerance", type=float, default=1e-12)
    parser.add_argument("fixtures", nargs="*", default=DEFAULT_FIXTURES)
    args = parser.parse_args()

    contract_path = Path(args.contract)
    output_path = Path(args.output)

    contract = load_contract(contract_path)
    results = []

    for fixture_path in args.fixtures:
        fixture = load_fixture(fixture_path)
        result = evaluate_fixture(fixture, args.rank_tolerance)
        results.append(result)

    passed = all(item["all_declared_checks_pass"] for item in results)

    payload = {
        "schema_id": "AQ-CONDITIONING-RECEIPT-001",
        "generated_at_utc": utc_now(),
        "claim_id": contract.get("claim_id"),
        "contract_path": str(contract_path),
        "contract_sha256": sha256_file(contract_path),
        "contract_canonical_sha256": sha256_json(contract),
        "runtime": runtime_environment(),
        "rank_tolerance": args.rank_tolerance,
        "fixture_count": len(results),
        "fixtures": results,
        "status": "PASS" if passed else "FAIL",
        "governance": {
            "finite_computational_evidence_only": True,
            "formal_proof": False,
            "c4": "BLOCKED",
            "publication": "BLOCKED",
            "promotion_allowed": False,
        },
    }

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(payload, indent=2, sort_keys=True),
        encoding="utf-8",
    )

    print(
        json.dumps(
            {
                "status": payload["status"],
                "fixture_count": payload["fixture_count"],
                "output": str(output_path),
            },
            sort_keys=True,
        )
    )

    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
