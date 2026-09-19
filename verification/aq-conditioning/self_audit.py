from __future__ import annotations

import json
from pathlib import Path


REQUIRED_PATHS = [
    "CONTRACT.json",
    "README.md",
    "FILETREE.md",
    "aq_conditioning/__init__.py",
    "aq_conditioning/canonical.py",
    "aq_conditioning/exact_rank.py",
    "aq_conditioning/numerical_svd.py",
    "aq_conditioning/invariants.py",
    "aq_conditioning/fixtures.py",
    "aq_conditioning/report.py",
    "aq_conditioning/replay.py",
    "fixtures/singular_exact.json",
    "fixtures/full_rank_permutation.json",
    "fixtures/near_singular_epsilon.json",
    "fixtures/column_stochastic_kernel.json",
    "verification/manifest.json",
]


def is_valid_json(path: str) -> bool:
    try:
        with Path(path).open("r", encoding="utf-8") as handle:
            json.load(handle)
    except (OSError, json.JSONDecodeError):
        return False
    return True


def main() -> int:
    missing = [path for path in REQUIRED_PATHS if not Path(path).is_file()]

    json_files = [
        "CONTRACT.json",
        "fixtures/singular_exact.json",
        "fixtures/full_rank_permutation.json",
        "fixtures/near_singular_epsilon.json",
        "fixtures/column_stochastic_kernel.json",
        "verification/manifest.json",
    ]

    invalid_json = [path for path in json_files if not is_valid_json(path)]

    result = {
        "missing": missing,
        "invalid_json": invalid_json,
        "status": "PASS" if not missing and not invalid_json else "FAIL",
    }

    print(json.dumps(result, sort_keys=True))
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
