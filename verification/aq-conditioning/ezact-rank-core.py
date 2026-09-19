#!/usr/bin/env python3
"""
AQARION-CONDITIONING
Exact-rank core for the cyclic block-shift Gram identity.

CONVENTION
----------
n = m * k
X is partitioned into k consecutive blocks of size m.
U is n x k.
c = s mod m.
S is the k x k cyclic shift.

The normalized Gram identity is

    G_orth = [c * (m - c) / m^2] * L(C_k)

where

    L(C_k) = 2 I - S - S^{-1}.

For exact rank certification we scale away the denominator:

    B = m^2 G_orth
      = c * (m - c) * L(C_k).

This file deliberately avoids floating-point arithmetic.

EXACT RANK THEOREM
------------------
If c = 0:
    B = 0
    rank(B) = 0.

If 1 <= c < m:
    every row of B sums to zero, hence rank(B) <= k - 1.

    The principal (k-1)x(k-1) cofactor of L(C_k) is k.
    Therefore the corresponding cofactor of B is

        k * [c * (m-c)]^(k-1),

    which is nonzero.

Thus

    rank(B) = k - 1

and therefore

    rank(G_orth) = k - 1.

The certificate consists of:
    - the exact matrix identity B = c(m-c)L(C_k),
    - the exact row-sum/null-vector condition,
    - one exact nonzero (k-1)x(k-1) minor.

No floating-point tolerance is used.
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict, dataclass
from typing import List


IntMatrix = List[List[int]]


def zero_matrix(rows: int, cols: int) -> IntMatrix:
    return [[0 for _ in range(cols)] for _ in range(rows)]


def identity_matrix(n: int) -> IntMatrix:
    out = zero_matrix(n, n)
    for i in range(n):
        out[i][i] = 1
    return out


def matrix_add(A: IntMatrix, B: IntMatrix) -> IntMatrix:
    rows = len(A)
    cols = len(A[0])
    return [
        [A[i][j] + B[i][j] for j in range(cols)]
        for i in range(rows)
    ]


def matrix_sub(A: IntMatrix, B: IntMatrix) -> IntMatrix:
    rows = len(A)
    cols = len(A[0])
    return [
        [A[i][j] - B[i][j] for j in range(cols)]
        for i in range(rows)
    ]


def scalar_mul(a: int, A: IntMatrix) -> IntMatrix:
    return [[a * x for x in row] for row in A]


def matrix_equal(A: IntMatrix, B: IntMatrix) -> bool:
    return A == B


def cyclic_shift(k: int) -> IntMatrix:
    """
    S e_j = e_{j+1 mod k}.

    The orientation is immaterial for the undirected cycle Laplacian
    because L = 2I - S - S^{-1}.
    """
    S = zero_matrix(k, k)
    for i in range(k):
        S[i][(i + 1) % k] = 1
    return S


def transpose(A: IntMatrix) -> IntMatrix:
    rows = len(A)
    cols = len(A[0])
    return [[A[i][j] for i in range(rows)] for j in range(cols)]


def matrix_mul(A: IntMatrix, B: IntMatrix) -> IntMatrix:
    rows = len(A)
    inner = len(B)
    cols = len(B[0])

    out = zero_matrix(rows, cols)

    for i in range(rows):
        for t in range(inner):
            a = A[i][t]
            if a == 0:
                continue
            for j in range(cols):
                out[i][j] += a * B[t][j]

    return out


def matrix_power(A: IntMatrix, exponent: int) -> IntMatrix:
    if exponent < 0:
        raise ValueError("matrix_power requires a nonnegative exponent")

    n = len(A)
    result = identity_matrix(n)
    base = A

    while exponent:
        if exponent & 1:
            result = matrix_mul(result, base)
        base = matrix_mul(base, base)
        exponent >>= 1

    return result


def cycle_laplacian(k: int) -> IntMatrix:
    S = cyclic_shift(k)
    return matrix_sub(
        matrix_sub(
            scalar_mul(2, identity_matrix(k)),
            S,
        ),
        transpose(S),
    )


def integer_gram_from_shift(
    m: int,
    k: int,
    s: int,
) -> tuple[int, int, IntMatrix]:
    """
    Construct the exact integer Gram matrix

        B = m^2 G_orth

    from the block-shift counting matrix

        A = (m-c) S^q + c S^(q+1),

    where s = q*m + c.

    The exact identity is

        B = m^2 I - A^T A
          = c(m-c)L(C_k).

    Returns:
        q, c, B.
    """
    if m < 1 or k < 1:
        raise ValueError("m and k must be positive")
    if s < 0:
        raise ValueError("s must be nonnegative")
    if s >= m * k:
        raise ValueError("s must satisfy 0 <= s < m*k")

    q, c = divmod(s, m)

    S = cyclic_shift(k)

    A = matrix_add(
        scalar_mul(m - c, matrix_power(S, q)),
        scalar_mul(c, matrix_power(S, q + 1)),
    )

    B = matrix_sub(
        scalar_mul(m * m, identity_matrix(k)),
        matrix_mul(transpose(A), A),
    )

    return q, c, B


def expected_integer_gram(m: int, k: int, s: int) -> IntMatrix:
    """
    Exact theorem-side construction:

        B_expected = c(m-c)L(C_k).
    """
    _, c = divmod(s, m)
    return scalar_mul(
        c * (m - c),
        cycle_laplacian(k),
    )


def delete_row_col(A: IntMatrix, index: int) -> IntMatrix:
    return [
        [
            A[i][j]
            for j in range(len(A))
            if j != index
        ]
        for i in range(len(A))
        if i != index
    ]


def bareiss_determinant(A: IntMatrix) -> int:
    """
    Exact determinant using fraction-free Bareiss elimination.

    Only integer arithmetic is used.
    """
    n = len(A)

    if n == 0:
        return 1

    if any(len(row) != n for row in A):
        raise ValueError("determinant requires a square matrix")

    M = [row[:] for row in A]

    if n == 1:
        return M[0][0]

    sign = 1
    previous_pivot = 1

    for pivot_index in range(n - 1):
        pivot_row = None

        for r in range(pivot_index, n):
            if M[r][pivot_index] != 0:
                pivot_row = r
                break

        if pivot_row is None:
            return 0

        if pivot_row != pivot_index:
            M[pivot_index], M[pivot_row] = (
                M[pivot_row],
                M[pivot_index],
            )
            sign = -sign

        pivot = M[pivot_index][pivot_index]

        for i in range(pivot_index + 1, n):
            for j in range(pivot_index + 1, n):
                numerator = (
                    M[i][j] * pivot
                    - M[i][pivot_index] * M[pivot_index][j]
                )

                if previous_pivot != 1:
                    if numerator % previous_pivot != 0:
                        raise ArithmeticError(
                            "Bareiss exact division failed"
                        )
                    numerator //= previous_pivot

                M[i][j] = numerator

        for i in range(pivot_index + 1, n):
            M[i][pivot_index] = 0

        previous_pivot = pivot

    return sign * M[n - 1][n - 1]


def row_sums(A: IntMatrix) -> List[int]:
    return [sum(row) for row in A]


def exact_rank_certificate(
    m: int,
    k: int,
    s: int,
) -> dict:
    """
    Produce a complete exact rank certificate for one (m,k,s).

    No numerical eigensolver and no floating-point rank routine appear
    anywhere in this certificate.
    """
    q, c, B = integer_gram_from_shift(m, k, s)
    expected = expected_integer_gram(m, k, s)

    identity_holds = matrix_equal(B, expected)

    if not identity_holds:
        raise AssertionError(
            "Exact Gram identity failed:\n"
            f"B={B}\nEXPECTED={expected}"
        )

    sums = row_sums(B)
    null_vector_condition = all(x == 0 for x in sums)

    if c == 0:
        expected_rank = 0
        cofactor = 0
        expected_cofactor = 0
    else:
        expected_rank = k - 1

        minor = delete_row_col(B, k - 1)
        cofactor = bareiss_determinant(minor)

        expected_cofactor = (
            k * (c * (m - c)) ** (k - 1)
        )

        if cofactor != expected_cofactor:
            raise AssertionError(
                "Exact cofactor certificate failed: "
                f"actual={cofactor}, "
                f"expected={expected_cofactor}"
            )

        if cofactor == 0:
            raise AssertionError(
                "Nonzero rank witness unexpectedly vanished"
            )

    if not null_vector_condition:
        raise AssertionError(
            f"Expected B*1=0, got row sums {sums}"
        )

    return {
        "m": m,
        "k": k,
        "n": m * k,
        "s": s,
        "q": q,
        "c": c,
        "identity_exact": True,
        "row_sum_zero": True,
        "expected_rank": expected_rank,
        "cofactor": cofactor,
        "expected_cofactor": expected_cofactor,
        "rank_certificate": (
            "zero_matrix"
            if c == 0
            else "nonzero_(k-1)x(k-1)_minor"
        ),
    }


def exhaustive_audit(
    min_m: int = 2,
    max_m: int = 8,
    min_k: int = 2,
    max_k: int = 8,
) -> dict:
    """
    Exhaustively audit the finite domain

        m,k in [2,8]
        s in [0,m*k-1].

    This is an exact-integer audit.
    """
    cases = 0
    nonzero_residue_cases = 0
    zero_residue_cases = 0

    for m in range(min_m, max_m + 1):
        for k in range(min_k, max_k + 1):
            for s in range(m * k):
                result = exact_rank_certificate(m, k, s)

                cases += 1

                if result["c"] == 0:
                    zero_residue_cases += 1
                else:
                    nonzero_residue_cases += 1

    return {
        "status": "PASS",
        "arithmetic": "exact_integer",
        "cases": cases,
        "m_range": [min_m, max_m],
        "k_range": [min_k, max_k],
        "zero_residue_cases": zero_residue_cases,
        "nonzero_residue_cases": nonzero_residue_cases,
        "floating_point_used": False,
        "rank_claim": (
            "rank=0 when c=0; rank=k-1 when 1<=c<m"
        ),
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description="AQARION-CONDITION8NG exact-rank core"
    )

    parser.add_argument("--m", type=int)
    parser.add_argument("--k", type=int)
    parser.add_argument("--s", type=int)

    parser.add_argument(
        "--exhaustive",
        action="store_true",
        help="run the default exact finite audit",
    )

    args = parser.parse_args()

    if args.exhaustive:
        result = exhaustive_audit()
        print(json.dumps(result, indent=2, sort_keys=True))
        return 0

    if args.m is None or args.k is None or args.s is None:
        parser.error(
            "provide --m, --k, --s, or use --exhaustive"
        )

    result = exact_rank_certificate(
        args.m,
        args.k,
        args.s,
    )

    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
