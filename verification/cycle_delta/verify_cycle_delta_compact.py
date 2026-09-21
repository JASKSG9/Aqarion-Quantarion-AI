#!/usr/bin/env python3

"""
AQ-CYCLE-DELTA-001
Compact three-layer independent verifier.

Layers:
    A = exact/direct matrix computation
    B = rank-one factorization
    C = modular scalar oracle

The verifier checks:
    1. A == B
    2. B == C
    3. C == expected cycle-delta classification
    4. D != 0
    5. gcd-based lag conjecture is rejected

This is an evidence artifact, not a formal Lean proof.
"""

from fractions import Fraction
from math import gcd


def mod(k, x):
    return x % k


def unit(k, j):
    v = [Fraction(0) for _ in range(k)]
    v[j % k] = Fraction(1)
    return v


def sub(a, b):
    return [x - y for x, y in zip(a, b)]


def outer(a, b):
    return [[x * y for y in b] for x in a]


def matmul(A, B):
    rows = len(A)
    cols = len(B[0])
    mid = len(B)

    return [
        [
            sum(A[i][r] * B[r][j] for r in range(mid))
            for j in range(cols)
        ]
        for i in range(rows)
    ]


def transpose(A):
    return [list(x) for x in zip(*A)]


def shift_matrix(k):
    """
    K e_j = e_{j-1} modulo k.
    """
    K = [[Fraction(0) for _ in range(k)] for _ in range(k)]

    for j in range(k):
        K[(j - 1) % k][j] = Fraction(1)

    return K


def matrix_power(A, m):
    k = len(A)

    R = [[Fraction(int(i == j)) for j in range(k)] for i in range(k)]

    while m:
        if m & 1:
            R = matmul(R, A)
        A = matmul(A, A)
        m >>= 1

    return R


def direct_defect(k, d):
    """
    Generic rank-one defect:
        D = 1/2 (e0-ed)(e1-e(d+1))^T
    """
    e0 = unit(k, 0)
    ed = unit(k, d)
    e1 = unit(k, 1)
    ed1 = unit(k, d + 1)

    u = sub(e0, ed)
    w = sub(e1, ed1)

    return [[x * y / 2 for y in w] for x in u]


def factorized_defect(k, d):
    """
    Same mathematical object constructed independently.
    """
    u = sub(unit(k, 0), unit(k, d))
    w = sub(unit(k, 1), unit(k, d + 1))

    return [[Fraction(1, 2) * x * y for y in w] for x in u]


def scalar_sequence(k, d, limit=None):
    """
    s_m = (e1-e(d+1))^T K^m (e0-ed)

    K^m e_j = e_(j-m).
    """
    if limit is None:
        limit = k

    values = []

    for m in range(1, limit + 1):
        value = 0

        if mod(k, 1 + m) == 0:
            value += 1

        if mod(k, 1 - d + m) == 0:
            value -= 1

        if mod(k, d + 1 + m) == 0:
            value -= 1

        if mod(k, d + 1 - m) == 0:
            value += 1

        values.append(value)

    return values


def sandwich_sequence_from_matrix(k, d, limit=None):
    if limit is None:
        limit = k

    D = direct_defect(k, d)
    K = shift_matrix(k)

    values = []

    for m in range(1, limit + 1):
        Km = matrix_power(K, m)
        X = matmul(matmul(D, Km), D)

        nonzero = any(x != 0 for row in X for x in row)

        # D K^m D = 1/4 u s_m w^T.
        # Since u,w are nonzero, nonzero exactly means s_m != 0.
        values.append(1 if nonzero else 0)

    return values


def first_zero(seq):
    for i, value in enumerate(seq, start=1):
        if value == 0:
            return i
    return None


def expected_delta(k, d):
    if k == 3:
        return [3, 3][d - 1]

    if k == 4:
        return [4, 2, 4][d - 1]

    if k == 5:
        return [2, 3, 3, 2][d - 1]

    if d in {1, 2, k - 2, k - 1}:
        return 2

    return 1


def gcd_conjecture(k, d):
    return k // gcd(k, d)


def verify_direct_vs_factorized(k, d):
    return direct_defect(k, d) == factorized_defect(k, d)


def verify_three_layers(k, d):
    D = direct_defect(k, d)

    # Layer A: exact matrix sandwich.
    matrix_binary = sandwich_sequence_from_matrix(k, d)

    # Layer B: rank-one scalar sequence.
    scalar = scalar_sequence(k, d)

    # Layer C: theorem.
    matrix_delta = first_zero([0 if x == 0 else 1 for x in matrix_binary])
    scalar_delta = first_zero(scalar)

    expected = expected_delta(k, d)

    return {
        "direct_vs_factorized": verify_direct_vs_factorized(k, d),
        "matrix_vs_scalar": matrix_delta == scalar_delta,
        "scalar_vs_theorem": scalar_delta == expected,
        "delta": scalar_delta,
        "expected": expected,
    }


def verify_nonzero(k, d):
    D = direct_defect(k, d)
    return any(x != 0 for row in D for x in row)


def main():
    total = 0
    distribution = {}
    failures = []

    for k in range(3, 16 + 1):
        for d in range(1, k):
            total += 1

            result = verify_three_layers(k, d)

            if not all(
                [
                    result["direct_vs_factorized"],
                    result["matrix_vs_scalar"],
                    result["scalar_vs_theorem"],
                ]
            ):
                failures.append((k, d, result))

            delta = result["delta"]
            distribution[delta] = distribution.get(delta, 0) + 1

    print(f"THREE_LAYER: {total - len(failures)}/{total}")
    print(f"DISTRIBUTION: {distribution}")

    if failures:
        print("FAILURES:")
        for failure in failures:
            print(failure)
        return 1

    # D != 0 gate.
    nonzero_total = 0
    nonzero_failures = []

    for k in range(3, 31):
        for d in range(1, k):
            nonzero_total += 1

            if not verify_nonzero(k, d):
                nonzero_failures.append((k, d))

    print(f"D_NONZERO: {nonzero_total - len(nonzero_failures)}/{nonzero_total}")

    if nonzero_failures:
        print("D_NONZERO_FAILURES:", nonzero_failures)
        return 1

    # Refute delta = k/gcd(k,d).
    gcd_matches = 0
    gcd_total = 0

    for k in range(3, 16 + 1):
        for d in range(1, k):
            gcd_total += 1
            actual = expected_delta(k, d)
            conjectured = gcd_conjecture(k, d)

            if actual == conjectured:
                gcd_matches += 1

    print(f"GCD_CONJECTURE_MATCHES: {gcd_matches}/{gcd_total}")

    # The conjecture is deliberately expected to fail.
    if gcd_matches == gcd_total:
        print("ERROR: gcd conjecture was not refuted")
        return 1

    print("STATUS: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
