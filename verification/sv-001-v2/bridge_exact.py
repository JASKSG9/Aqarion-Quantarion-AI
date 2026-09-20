#!/usr/bin/env python3
"""
AQ-SIDE-PIVOT-002
SV-001-V2 EXACT ACTUAL-BRIDGE VERIFIER

Governance:
FROZEN AUDIT · NO PROMOTION · C4 BLOCKED · PUBLICATION BLOCKED

Target:

    A_actual = U^T K U

versus

    A_model = q S^b + p S^(b+1)

where

    s = b*k + r
    0 < r < k
    p = r/k
    q = (k-r)/k

and the finite space consists of m blocks of size k.

The verifier then checks:

    A^T A = I - p*q*L_m

and independently constructs

    D = (I-Q) K Q

to check:

    U^T D^T D U = p*q*L_m.

All arithmetic is exact Fraction arithmetic.

No floating point is used.

This is finite computational evidence, NOT a universal theorem proof.

Exit:
    0 = all tests pass
    1 = mathematical verification failure
"""

from __future__ import annotations

from fractions import Fraction
from dataclasses import dataclass
import hashlib
import json
import sys
from typing import Iterable


@dataclass(frozen=True)
class Case:
    m: int
    k: int
    b: int
    r: int


def zero_matrix(rows: int, cols: int) -> list[list[Fraction]]:
    return [
        [Fraction(0) for _ in range(cols)]
        for _ in range(rows)
    ]


def identity(n: int) -> list[list[Fraction]]:
    out = zero_matrix(n, n)

    for i in range(n):
        out[i][i] = Fraction(1)

    return out


def transpose(A: list[list[Fraction]]) -> list[list[Fraction]]:
    if not A:
        return []

    return [list(row) for row in zip(*A)]


def matmul(
    A: list[list[Fraction]],
    B: list[list[Fraction]],
) -> list[list[Fraction]]:
    if not A or not B:
        return []

    rows = len(A)
    inner = len(B)
    cols = len(B[0])

    if len(A[0]) != inner:
        raise ValueError("matrix dimension mismatch")

    out = zero_matrix(rows, cols)

    for i in range(rows):
        for k in range(inner):
            aik = A[i][k]

            if aik == 0:
                continue

            for j in range(cols):
                out[i][j] += aik * B[k][j]

    return out


def matsub(
    A: list[list[Fraction]],
    B: list[list[Fraction]],
) -> list[list[Fraction]]:
    if len(A) != len(B):
        raise ValueError("row mismatch")

    if A and B and len(A[0]) != len(B[0]):
        raise ValueError("column mismatch")

    return [
        [
            A[i][j] - B[i][j]
            for j in range(len(A[0]))
        ]
        for i in range(len(A))
    ]


def matadd(
    A: list[list[Fraction]],
    B: list[list[Fraction]],
) -> list[list[Fraction]]:
    if len(A) != len(B):
        raise ValueError("row mismatch")

    if A and B and len(A[0]) != len(B[0]):
        raise ValueError("column mismatch")

    return [
        [
            A[i][j] + B[i][j]
            for j in range(len(A[0]))
        ]
        for i in range(len(A))
    ]


def scalar_mul(
    c: Fraction,
    A: list[list[Fraction]],
) -> list[list[Fraction]]:
    return [
        [c * x for x in row]
        for row in A
    ]


def matrix_equal(
    A: list[list[Fraction]],
    B: list[list[Fraction]],
) -> bool:
    return A == B


def shift_matrix(m: int, d: int) -> list[list[Fraction]]:
    """
    S[e_j] = e_{j+d mod m}.

    Thus S[i][j] = 1 iff i = j+d mod m.
    """
    S = zero_matrix(m, m)

    d %= m

    for j in range(m):
        S[(j + d) % m][j] = Fraction(1)

    return S


def permutation_map(n: int, s: int) -> list[int]:
    return [(x + s) % n for x in range(n)]


def koopman_matrix(n: int, s: int) -> list[list[Fraction]]:
    """
    Pullback convention:

        (Kf)(x) = f(T(x))

    for T(x)=x+s.

    Therefore K has one 1 in row x, column T(x).
    """
    T = permutation_map(n, s)

    K = zero_matrix(n, n)

    for x in range(n):
        K[x][T[x]] = Fraction(1)

    return K


def block_indicator_matrix(m: int, k: int) -> list[list[Fraction]]:
    """
    U has n=m*k rows and m columns.

    Column j is the normalized indicator of block j:

        U[x,j] = 1/sqrt(k)

    would introduce irrational arithmetic.

    Instead we use the unnormalized block-incidence matrix W,
    and separately use the rational normalized Gram scaling.

    For the exact bridge A = U^T K U, the sqrt(k) factors
    cancel and the resulting entries are counts/k.
    """
    n = m * k

    W = zero_matrix(n, m)

    for x in range(n):
        j = x // k
        W[x][j] = Fraction(1)

    return W


def compressed_K_exact(
    m: int,
    k: int,
    s: int,
) -> list[list[Fraction]]:
    """
    A = (1/k) W^T K W.

    This equals U^T K U for normalized block indicators,
    because U = W/sqrt(k).

    The computation remains exactly rational.
    """
    n = m * k

    W = block_indicator_matrix(m, k)
    K = koopman_matrix(n, s)

    WT = transpose(W)

    return scalar_mul(
        Fraction(1, k),
        matmul(matmul(WT, K), W),
    )


def model_A(
    m: int,
    k: int,
    b: int,
    r: int,
) -> list[list[Fraction]]:
    p = Fraction(r, k)
    q = Fraction(k - r, k)

    S_b = shift_matrix(m, b)
    S_br1 = shift_matrix(m, b + 1)

    return matadd(
        scalar_mul(q, S_b),
        scalar_mul(p, S_br1),
    )


def cycle_laplacian(m: int) -> list[list[Fraction]]:
    """
    L = 2I - S - S^T
    using unit cyclic shift.
    """
    I = identity(m)
    S = shift_matrix(m, 1)

    return matsub(
        scalar_mul(Fraction(2), I),
        matadd(S, transpose(S)),
    )


def defect_projector_Q(m: int, k: int) -> list[list[Fraction]]:
    """
    Q = W W^T / k.
    """
    W = block_indicator_matrix(m, k)

    return scalar_mul(
        Fraction(1, k),
        matmul(W, transpose(W)),
    )


def defect_matrix(
    m: int,
    k: int,
    s: int,
) -> list[list[Fraction]]:
    """
    D = (I-Q) K Q.
    """
    n = m * k

    I = identity(n)
    Q = defect_projector_Q(m, k)
    K = koopman_matrix(n, s)

    return matmul(
        matsub(I, Q),
        matmul(K, Q),
    )


def projected_defect_gram(
    m: int,
    k: int,
    s: int,
) -> list[list[Fraction]]:
    """
    U^T D^T D U.

    Again we use W/sqrt(k) representation:

        U^T D^T D U
        = (1/k) W^T D^T D W.
    """
    W = block_indicator_matrix(m, k)
    D = defect_matrix(m, k, s)

    DT = transpose(D)

    return scalar_mul(
        Fraction(1, k),
        matmul(
            matmul(transpose(W), DT),
            matmul(D, W),
        ),
    )


def expected_gram(
    m: int,
    k: int,
    r: int,
) -> list[list[Fraction]]:
    p = Fraction(r, k)
    q = Fraction(k - r, k)

    return scalar_mul(
        p * q,
        cycle_laplacian(m),
    )


def expected_ata(
    m: int,
    k: int,
    r: int,
) -> list[list[Fraction]]:
    p = Fraction(r, k)
    q = Fraction(k - r, k)

    return matsub(
        identity(m),
        scalar_mul(
            p * q,
            cycle_laplacian(m),
        ),
    )


def entry_formula_check(
    actual: list[list[Fraction]],
    model: list[list[Fraction]],
) -> bool:
    return matrix_equal(actual, model)


def case_digest(cases: Iterable[Case]) -> str:
    payload = "\n".join(
        f"{c.m},{c.k},{c.b},{c.r}"
        for c in cases
    ).encode("utf-8")

    return hashlib.sha256(payload).hexdigest()


def run_case(case: Case) -> dict:
    m, k, b, r = case

    s = b * k + r

    actual_A = compressed_K_exact(m, k, s)
    model = model_A(m, k, b, r)

    bridge_ok = entry_formula_check(actual_A, model)

    ata = matmul(transpose(actual_A), actual_A)
    ata_expected = expected_ata(m, k, r)

    ata_ok = matrix_equal(ata, ata_expected)

    actual_gram = projected_defect_gram(m, k, s)
    gram_expected = expected_gram(m, k, r)

    gram_ok = matrix_equal(actual_gram, gram_expected)

    return {
        "m": m,
        "k": k,
        "b": b,
        "r": r,
        "s": s,
        "bridge_A_actual_eq_model": bridge_ok,
        "A_transpose_A_eq_I_minus_pqL": ata_ok,
        "full_projected_defect_gram": gram_ok,
    }


def generate_cases() -> list[Case]:
    cases: list[Case] = []

    # Exact deterministic finite suite.
    #
    # m = 2..20
    # k = 2..12
    # b = 0..m-1
    # r = 1..k-1
    #
    # This deliberately covers the m=2 multigraph boundary as well.
    for m in range(2, 21):
        for k in range(2, 13):
            for b in range(m):
                for r in range(1, k):
                    cases.append(Case(m, k, b, r))

    return cases


def main() -> int:
    print("AQ-SIDE-PIVOT-002 / SV-001-V2 EXACT BRIDGE")
    print("Governance: FROZEN AUDIT · NO PROMOTION · C4 BLOCKED · PUBLICATION BLOCKED")
    print("Arithmetic: exact Fraction")
    print()

    cases = generate_cases()

    print(f"CASES={len(cases)}")
    print(f"CASE_SHA256={case_digest(cases)}")
    print()

    bridge_failures = []
    ata_failures = []
    gram_failures = []

    for index, case in enumerate(cases, start=1):
        result = run_case(case)

        if not result["bridge_A_actual_eq_model"]:
            bridge_failures.append(result)

        if not result["A_transpose_A_eq_I_minus_pqL"]:
            ata_failures.append(result)

        if not result["full_projected_defect_gram"]:
            gram_failures.append(result)

        if index % 500 == 0:
            print(f"PROGRESS={index}/{len(cases)}")

    print()
    print(f"BRIDGE_FAILURES={len(bridge_failures)}")
    print(f"ATA_FAILURES={len(ata_failures)}")
    print(f"GRAM_FAILURES={len(gram_failures)}")

    if bridge_failures:
        print()
        print("FIRST_BRIDGE_FAILURE:")
        print(json.dumps(bridge_failures[0], sort_keys=True))

    if ata_failures:
        print()
        print("FIRST_ATA_FAILURE:")
        print(json.dumps(ata_failures[0], sort_keys=True))

    if gram_failures:
        print()
        print("FIRST_GRAM_FAILURE:")
        print(json.dumps(gram_failures[0], sort_keys=True))

    if bridge_failures or ata_failures or gram_failures:
        print()
        print("RESULT=FAIL")
        return 1

    print()
    print("RESULT=PASS")
    print("CLASSIFICATION=EXACT_FINITE_REPLAY")
    print("CLAIM_BOUNDARY=NOT_A_UNIVERSAL_PROOF")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
