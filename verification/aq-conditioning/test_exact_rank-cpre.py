#!/usr/bin/env python3
"""
Standalone tests for AQARION-CONDITIONING/exact_rank_core.py.

These tests intentionally do not import or touch the existing AQARION
verification directory.
"""

from exact_rank_core import (
    bareiss_determinant,
    cycle_laplacian,
    exact_rank_certificate,
    exhaustive_audit,
)


def test_cycle_laplacian_cofactors():
    for k in range(2, 25):
        L = cycle_laplacian(k)
        minor = [
            row[:-1]
            for row in L[:-1]
        ]

        determinant = bareiss_determinant(minor)

        assert determinant == k, (
            f"C_{k}: expected cofactor {k}, "
            f"got {determinant}"
        )


def test_zero_residue_rank():
    for m in range(2, 12):
        for k in range(2, 12):
            s = m

            result = exact_rank_certificate(
                m,
                k,
                s,
            )

            assert result["c"] == 0
            assert result["expected_rank"] == 0
            assert result["cofactor"] == 0


def test_nonzero_residue_rank():
    for m in range(2, 12):
        for k in range(2, 12):
            for c in range(1, m):
                s = c

                result = exact_rank_certificate(
                    m,
                    k,
                    s,
                )

                assert result["c"] == c
                assert result["expected_rank"] == k - 1
                assert result["cofactor"] != 0
                assert (
                    result["cofactor"]
                    == result["expected_cofactor"]
                )


def test_exhaustive_audit():
    result = exhaustive_audit(
        min_m=2,
        max_m=8,
        min_k=2,
        max_k=8,
    )

    assert result["status"] == "PASS"
    assert result["arithmetic"] == "exact_integer"
    assert result["floating_point_used"] is False

    expected_cases = sum(
        m * k
        for m in range(2, 9)
        for k in range(2, 9)
    )

    assert result["cases"] == expected_cases


if __name__ == "__main__":
    test_cycle_laplacian_cofactors()
    test_zero_residue_rank()
    test_nonzero_residue_rank()
    test_exhaustive_audit()

    print("AQARION-CONDITION8NG exact-rank tests: PASS")
