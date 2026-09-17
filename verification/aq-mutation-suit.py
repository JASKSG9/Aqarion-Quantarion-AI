#!/usr/bin/env python3
"""
AQARION semantic mutation suite.

The purpose is not merely to show that the reference implementation
passes. It asks whether deliberate semantic errors are detectable.

Registered mutations
--------------------
NC-01:
    Transpose the Koopman matrix.

WRONG-SPEC:
    Use D = K P (I-P) instead of D = (I-P) K P.

NC-02:
    Replace the horizontal incidence construction with the
    deliberately wrong vertical-stack construction.

A mutation is "killed" only when the independent oracle produces
a different result from the mutated computation.

No probabilistic tolerance.
No floating point.
"""

from __future__ import annotations

from fractions import Fraction
from itertools import product


def partitions_of_set(n):
    if n == 0:
        yield ()
        return

    blocks = [[0]]

    def rec(x):
        if x == n:
            yield tuple(tuple(b) for b in blocks)
            return

        for i in range(len(blocks)):
            blocks[i].append(x)
            yield from rec(x + 1)
            blocks[i].pop()

        blocks.append([x])
        yield from rec(x + 1)
        blocks.pop()

    yield from rec(1)


def pidx(partition):
    result = {}
    for i, block in enumerate(partition):
        for x in block:
            result[x] = i
    return result


def identity(n):
    return [
        [Fraction(int(i == j)) for j in range(n)]
        for i in range(n)
    ]


def sub(A, B):
    return [
        [A[i][j] - B[i][j] for j in range(len(A[0]))]
        for i in range(len(A))
    ]


def mul(A, B):
    return [
        [
            sum(A[i][k] * B[k][j] for k in range(len(B)))
            for j in range(len(B[0]))
        ]
        for i in range(len(A))
    ]


def rank(A):
    A = [row[:] for row in A]

    if not A:
        return 0

    rows = len(A)
    cols = len(A[0])
    r = 0

    for c in range(cols):
        pivot = next(
            (
                i for i in range(r, rows)
                if A[i][c] != 0
            ),
            None,
        )

        if pivot is None:
            continue

        A[r], A[pivot] = A[pivot], A[r]

        q = A[r][c]
        A[r] = [x / q for x in A[r]]

        for i in range(rows):
            if i == r:
                continue

            q = A[i][c]

            if q:
                A[i] = [
                    A[i][j] - q * A[r][j]
                    for j in range(cols)
                ]

        r += 1

    return r


def P_matrix(n, partition):
    P = [
        [Fraction(0) for _ in range(n)]
        for _ in range(n)
    ]

    for block in partition:
        q = Fraction(1, len(block))
        for i in block:
            for j in block:
                P[i][j] = q

    return P


def K_matrix(T):
    n = len(T)

    K = [
        [Fraction(0) for _ in range(n)]
        for _ in range(n)
    ]

    for x, y in enumerate(T):
        K[x][y] = Fraction(1)

    return K


def production_rank(T, partition):
    n = len(T)

    P = P_matrix(n, partition)
    Q = sub(identity(n), P)
    K = K_matrix(T)

    D = mul(mul(Q, K), P)

    return rank(D)


def mutant_transposed_koopman_rank(T, partition):
    n = len(T)

    P = P_matrix(n, partition)
    Q = sub(identity(n), P)
    K = K_matrix(T)

    K = [
        list(row)
        for row in zip(*K)
    ]

    D = mul(mul(Q, K), P)

    return rank(D)


def mutant_wrong_spec_rank(T, partition):
    n = len(T)

    P = P_matrix(n, partition)
    Q = sub(identity(n), P)
    K = K_matrix(T)

    D = mul(mul(K, P), Q)

    return rank(D)


def mutant_vertical_stack_rank(T, partition):
    """
    Deliberately wrong incidence representation.

    This mutation is intentionally not algebraically equivalent
    to the production horizontal construction.
    """
    n = len(T)
    m = len(partition)
    idx = pidx(partition)

    rows = []

    for x, y in enumerate(T):
        source = idx[x]
        target = idx[y]

        row = [
            Fraction(int(j == source))
            for j in range(m)
        ]

        row += [
            Fraction(int(j == target))
            for j in range(m)
        ]

        rows.append(row)

    # Wrong vertical-stack semantics:
    # transpose before rank calculation.
    A = [
        list(row)
        for row in zip(*rows)
    ]

    return rank(A)


MUTATIONS = [
    (
        "NC-01 transposed Koopman",
        mutant_transposed_koopman_rank,
    ),
    (
        "WRONG-SPEC D=KP(I-P)",
        mutant_wrong_spec_rank,
    ),
    (
        "NC-02 vertical stack substituted for horizontal",
        mutant_vertical_stack_rank,
    ),
]


def find_counterexample(mutant):
    for n in range(1, 5):
        partitions = list(partitions_of_set(n))

        for T in product(range(n), repeat=n):
            for partition in partitions:
                oracle = production_rank(
                    T,
                    partition,
                )

                mutated = mutant(
                    T,
                    partition,
                )

                if oracle != mutated:
                    return (
                        n,
                        T,
                        partition,
                        oracle,
                        mutated,
                    )

    return None


def run():
    for name, mutant in MUTATIONS:
        witness = find_counterexample(mutant)

        if witness is None:
            raise AssertionError(
                f"MUTATION SURVIVED: {name}"
            )

        n, T, partition, oracle, mutated = witness

        print(
            f"KILLED: {name} -> "
            f"n={n} T={T} part={partition} "
            f"oracle={oracle} mutant={mutated}"
        )

    print(
        "AQARION MUTATION SUITE PASS: "
        "all registered semantic mutations killed"
    )


if __name__ == "__main__":
    run()
