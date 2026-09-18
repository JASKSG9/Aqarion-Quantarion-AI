#!/usr/bin/env python3
"""
SV-001-V2 independent matrix verifier.

Constructs U, Q, K, D directly. Does NOT use oracle formulas.
Supports AQ_SV001_MUTANT environment variable for mutation testing.
"""

from __future__ import annotations

import argparse
import math
import os
from dataclasses import dataclass

import numpy as np

from oracle import oracle, enumerate_cases, validate_case


TOL = 1e-12


@dataclass(frozen=True)
class VerificationResult:
    m: int
    k: int
    s: int
    r: int
    gram_error: float
    trace_error: float
    norm_error: float
    gram_pass: bool
    trace_pass: bool
    norm_pass: bool

    @property
    def passed(self) -> bool:
        return self.gram_pass and self.trace_pass and self.norm_pass


def build_U(m: int, k: int) -> np.ndarray:
    n = m * k
    U = np.zeros((n, m), dtype=float)
    scale = 1.0 / math.sqrt(k)
    for x in range(n):
        U[x, x // k] = scale
    return U


def build_K(m: int, k: int, s: int) -> np.ndarray:
    n = m * k
    K = np.zeros((n, n), dtype=float)
    for x in range(n):
        K[x, (x + s) % n] = 1.0
    return K


def build_S(m: int) -> np.ndarray:
    S = np.zeros((m, m), dtype=float)
    for i in range(m):
        S[i, (i + 1) % m] = 1.0
    return S


def matrix_verification(m: int, k: int, s: int) -> VerificationResult:
    validate_case(m, k, s)
    expected = oracle(m, k, s)

    mutant = os.environ.get("AQ_SV001_MUTANT")
    if mutant == "wrong_trace":
        expected = type(expected)(
            m=expected.m, k=expected.k, s=expected.s, r=expected.r,
            alpha_squared=expected.alpha_squared,
            trace=expected.trace + 1.0,
            norm=expected.norm,
        )
    elif mutant == "wrong_norm":
        expected = type(expected)(
            m=expected.m, k=expected.k, s=expected.s, r=expected.r,
            alpha_squared=expected.alpha_squared,
            trace=expected.trace,
            norm=expected.norm + 1.0,
        )
    elif mutant == "wrong_gram":
        expected = type(expected)(
            m=expected.m, k=expected.k, s=expected.s, r=expected.r,
            alpha_squared=expected.alpha_squared * 2.0,
            trace=expected.trace,
            norm=expected.norm,
        )
    elif mutant == "nan_error":
        expected = type(expected)(
            m=expected.m, k=expected.k, s=expected.s, r=expected.r,
            alpha_squared=expected.alpha_squared,
            trace=float("nan"),
            norm=expected.norm,
        )

    U = build_U(m, k)
    Q = U @ U.T
    K = build_K(m, k, s)
    n = m * k
    D = (np.eye(n) - Q) @ K @ Q
    G = U.T @ D.T @ D @ U
    S = build_S(m)
    expected_G = expected.alpha_squared * (2.0 * np.eye(m) - S - S.T)

    actual_trace = float(np.trace(G))
    singular_values = np.linalg.svd(D, compute_uv=False)
    actual_norm = float(singular_values[0])

    gram_error = float(np.max(np.abs(G - expected_G)))
    trace_error = abs(actual_trace - expected.trace)
    norm_error = abs(actual_norm - expected.norm)

    finite = all(
        math.isfinite(v) for v in (gram_error, trace_error, norm_error)
    )

    return VerificationResult(
        m=m, k=k, s=s, r=expected.r,
        gram_error=gram_error,
        trace_error=trace_error,
        norm_error=norm_error,
        gram_pass=finite and gram_error <= TOL,
        trace_pass=finite and trace_error <= TOL,
        norm_pass=finite and norm_error <= TOL,
    )


def run_all():
    failures = []
    max_gram = 0.0
    max_trace = 0.0
    max_norm = 0.0
    cases = list(enumerate_cases())
    for case in cases:
        result = matrix_verification(*case)
        max_gram = max(max_gram, result.gram_error)
        max_trace = max(max_trace, result.trace_error)
        max_norm = max(max_norm, result.norm_error)
        if not result.passed:
            failures.append(result)
    return {
        "cases": len(cases),
        "failures": len(failures),
        "max_gram_error": max_gram,
        "max_trace_error": max_trace,
        "max_norm_error": max_norm,
        "status": "PASS" if not failures else "FAIL",
        "failure_cases": [
            {
                "m": x.m, "k": x.k, "s": x.s, "r": x.r,
                "gram_error": x.gram_error,
                "trace_error": x.trace_error,
                "norm_error": x.norm_error,
            }
            for x in failures[:20]
        ],
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--case", nargs=3, type=int)
    args = parser.parse_args()

    if args.case:
        result = matrix_verification(*args.case)
        print(result)
        raise SystemExit(0 if result.passed else 1)

    result = run_all()
    print(
        f"SV-001-V2 matrix verifier "
        f"cases={result['cases']} "
        f"failures={result['failures']}"
    )
    print(f"max_gram_error={result['max_gram_error']:.17g}")
    print(f"max_trace_error={result['max_trace_error']:.17g}")
    print(f"max_norm_error={result['max_norm_error']:.17g}")
    print(f"status={result['status']}")
    raise SystemExit(0 if result["status"] == "PASS" else 1)


if __name__ == "__main__":
    main()
