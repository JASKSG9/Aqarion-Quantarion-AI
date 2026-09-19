from __future__ import annotations

from fractions import Fraction
from typing import Any

from .fixtures import MatrixFixture
from .invariants import exact_matrix_summary, verify_zero_sum_kernel_witness
from .numerical_svd import compute_svd


def parse_vector(values: list[int | str]) -> list[Fraction]:
    parsed: list[Fraction] = []

    for value in values:
        if isinstance(value, int):
            parsed.append(Fraction(value, 1))
        elif isinstance(value, str):
            parsed.append(Fraction(value))
        else:
            raise TypeError("Kernel witness values must be integers or rational strings.")

    return parsed


def evaluate_fixture(
    fixture: MatrixFixture,
    rank_tolerance: float,
) -> dict[str, Any]:
    exact = exact_matrix_summary(fixture.matrix)
    numeric = compute_svd(fixture.matrix, rank_tolerance)

    report: dict[str, Any] = {
        "fixture_id": fixture.fixture_id,
        "description": fixture.description,
        "fixture_path": fixture.source_path,
        "fixture_sha256": fixture.source_sha256,
        "expected": fixture.expected,
        "exact": exact,
        "numerical": {
            "singular_values": list(numeric.singular_values),
            "sigma_min": numeric.sigma_min,
            "sigma_max": numeric.sigma_max,
            "condition_number": numeric.condition_number,
            "numerical_rank": numeric.numerical_rank,
            "rank_tolerance": numeric.rank_tolerance,
        },
        "checks": {},
    }

    expected_rank = fixture.expected.get("exact_rank")
    if expected_rank is not None:
        report["checks"]["exact_rank_matches_expected"] = (
            exact["exact_rank"] == expected_rank
        )

    expected_nullity = fixture.expected.get("exact_nullity")
    if expected_nullity is not None:
        report["checks"]["exact_nullity_matches_expected"] = (
            exact["exact_nullity"] == expected_nullity
        )

    expected_column_sum = fixture.expected.get("column_sum_invariant_holds")
    if expected_column_sum is not None:
        report["checks"]["column_sum_invariant_matches_expected"] = (
            exact["column_sum_invariant_holds"] == expected_column_sum
        )

    witness_raw = fixture.expected.get("kernel_witness")
    if witness_raw is not None:
        witness = parse_vector(witness_raw)
        witness_result = verify_zero_sum_kernel_witness(fixture.matrix, witness)
        report["kernel_witness"] = witness_result

        report["checks"]["kernel_witness_matches_expectation"] = (
            witness_result["is_exact_kernel_vector"]
            == fixture.expected.get("kernel_witness_is_exact", True)
        )

        report["checks"]["zero_sum_witness_matches_expectation"] = (
            witness_result["is_zero_sum"]
            == fixture.expected.get("kernel_witness_zero_sum", True)
        )

    report["all_declared_checks_pass"] = all(report["checks"].values())
    return report
