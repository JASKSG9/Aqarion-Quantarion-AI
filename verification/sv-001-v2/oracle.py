#!/usr/bin/env python3
"""
SV-001-V2 independent closed-form oracle.

The oracle does NOT construct the n x n Koopman/shift matrix.
It evaluates the mathematical contract directly from (m, k, s).
"""

from __future__ import annotations

import math
from dataclasses import dataclass


TOL = 1e-12


@dataclass(frozen=True)
class OracleResult:
    m: int
    k: int
    s: int
    r: int
    alpha_squared: float
    trace: float
    norm: float


def validate_case(m: int, k: int, s: int) -> None:
    if not (2 <= m <= 8):
        raise ValueError(f"m outside canonical domain: {m}")
    if not (2 <= k <= 8):
        raise ValueError(f"k outside canonical domain: {k}")
    n = m * k
    if not (1 <= s <= n - 1):
        raise ValueError(f"s outside canonical domain: {s}")


def oracle(m: int, k: int, s: int) -> OracleResult:
    validate_case(m, k, s)
    r = s % k
    alpha_squared = (r * (k - r)) / (k * k)
    trace = 2.0 * m * alpha_squared
    if r == 0:
        norm = 0.0
    else:
        factor = 1.0 if m % 2 == 0 else math.cos(math.pi / (2.0 * m))
        norm = 2.0 * math.sqrt(alpha_squared) * factor
    return OracleResult(
        m=m, k=k, s=s, r=r,
        alpha_squared=alpha_squared,
        trace=trace,
        norm=norm,
    )


def enumerate_cases():
    for m in range(2, 9):
        for k in range(2, 9):
            for s in range(1, m * k):
                yield m, k, s


def expected_case_count() -> int:
    return sum(m * k - 1 for m in range(2, 9) for k in range(2, 9))


def expected_zero_r_count() -> int:
    return sum(m - 1 for m in range(2, 9) for _k in range(2, 9))


if __name__ == "__main__":
    cases = list(enumerate_cases())
    assert len(cases) == 1176
    assert expected_case_count() == 1176
    assert expected_zero_r_count() == 196
    zero_r = sum(oracle(*case).r == 0 for case in cases)
    print(f"SV-001-V2 oracle cases={len(cases)} zero_r={zero_r} nonzero_r={len(cases)-zero_r}")
    print("status=PASS")
