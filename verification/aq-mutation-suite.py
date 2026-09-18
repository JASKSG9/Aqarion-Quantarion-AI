#!/usr/bin/env python3
"""
AQARION semantic mutation suite.

Purpose
-------
Deliberately mutate frozen semantic definitions and require
the independent oracle/specification to detect each mutation.

Registered mutations:
    NC-01  transposed Koopman orientation
    WRONG-SPEC  D = K P (I-P) instead of D = (I-P) K P
    NC-02  vertical incidence construction instead of horizontal

This is an adversarial regression test, not a mathematical
proof.
"""

from __future__ import annotations

from fractions import Fraction
from itertools import product


def partitions_of_set(n: int):
    if n == 0:
        yield ()
        return

    blocks: list[list[int]] = [[0]]

    def rec(x: int):
        if x == n:
            yield tuple(tuple(block) for block in blocks)
            return

        for i in range(len(blocks)):
            blocks[i].append(x)
            yield from rec(x + 1)
            blocks[i].pop()

        blocks.append([x])
        yield from rec(x + 1)
        blocks.pop()

    yield from rec(1)


def projection_matrix(n: int, partition):
    P = [
        [Fraction(0) for _ in range(n)]
        for _ in range(n)
    ]

    for block in partition:
        value = Fraction(1, len(block))

        for i in block:
            for j in block:
                P[i][j] = value

    return P


def identity(n: int):
    return [
        [
            Fraction(int(i == j))
            for j in range(n)
        ]
        for i in range(n)
    ]


def matsub(A, B):
    return [
        [
            A[i][j] - B[i][j]
            for j in range(len(A[0]))
        ]
        for i in range(len(A))
    ]


def matmul(A, B):
    rows = len(A)
    inner = len(B)
    cols = len(B[0])

    return [
        [
            sum(
                A[i][k] * B[k][j]
                for k in range(inner)
            )
            for j in range(cols)
        ]
        for i in range(rows)
    ]


def gaussian_rank(A):
    if not A:
        return 0

    A = [row[:] for row in A]

    rows = len(A)
    cols = len(A[0])
    rank = 0

    for col in range(cols):
        pivot = None

        for r in range(rank, rows):
            if A[r][col] != 0:
                pivot = r
                break

        if pivot is None:
            continue

        A[rank], A[pivot] = (
            A[pivot],
            A[rank],
        )

        pivot_value = A[rank][col]

        A[rank] = [
            value / pivot_value
            for value in A[rank]
        ]

        for r in range(rows):
            if r == rank:
                continue

            factor = A[r][col]

            if factor == 0:
                continue

            A[r] = [
                A[r][c]
                - factor * A[rank][c]
                for c in range(cols)
            ]

        rank += 1

        if rank == rows:
            break

    return rank


def koopman(T):
    n = len(T)

    K = [
        [Fraction(0) for _ in range(n)]
        for _ in range(n)
    ]

    for x, y in enumerate(T):
        K[x][y] = Fraction(1)

    return K


def transposed_koopman(T):
    K = koopman(T)

    return [
        [
            K[j][i]
            for j in range(len(K))
        ]
        for i in range(len(K))
    ]


def production_rank(T, partition):
    n = len(T)

    P = projection_matrix(
        n,
        partition,
    )

    Q = matsub(
        identity(n),
        P,
    )

    K = koopman(T)

    D = matmul(
        matmul(Q, K),
        P,
    )

    return gaussian_rank(D)


def mutant_transposed_koopman_rank(
    T,
    partition,
):
    n = len(T)

    P = projection_matrix(
        n,
        partition,
    )

    Q = matsub(
        identity(n),
        P,
    )

    K = transposed_koopman(T)

    D = matmul(
        matmul(Q, K),
        P,
    )

    return gaussian_rank(D)


def mutant_wrong_spec_rank(
    T,
    partition,
):
    n = len(T)

    P = projection_matrix(
        n,
        partition,
    )

    Q = matsub(
        identity(n),
        P,
    )

    K = koopman(T)

    D = matmul(
        matmul(K, P),
        Q,
    )

    return gaussian_rank(D)


def incidence_edges(
    T,
    partition,
):
    owner = {}

    for i, block in enumerate(partition):
        for x in block:
            owner[x] = i

    edges = set()

    for x, y in enumerate(T):
        edges.add(
            (
                owner[x],
                owner[y],
            )
        )

    return edges


def horizontal_incidence_matrix(
    T,
    partition,
):
    m = len(partition)

    edges = incidence_edges(
        T,
        partition,
    )

    A = [
        [Fraction(0) for _ in range(m)]
        for _ in range(m)
    ]

    for source, target in edges:
        A[source][target] = Fraction(1)

    return A


def vertical_incidence_matrix(
    T,
    partition,
):
    m = len(partition)

    edges = incidence_edges(
        T,
        partition,
    )

    A = [
        [Fraction(0) for _ in range(m)]
        for _ in range(m)
    ]

    for source, target in edges:
        A[target][source] = Fraction(1)

    return A


def horizontal_rank(
    T,
    partition,
):
    return gaussian_rank(
        horizontal_incidence_matrix(
            T,
            partition,
        )
    )


def vertical_rank(
    T,
    partition,
):
    return gaussian_rank(
        vertical_incidence_matrix(
            T,
            partition,
        )
    )


def require_killed(
    name,
    T,
    partition,
    oracle,
    mutant,
):
    if oracle == mutant:
        raise AssertionError(
            f"MUTATION SURVIVED: {name}\n"
            f"n={len(T)} "
            f"T={T} "
            f"part={partition} "
            f"oracle={oracle} "
            f"mutant={mutant}"
        )

    print(
        f"KILLED: {name} -> "
        f"n={len(T)} "
        f"T={T} "
        f"part={partition} "
        f"oracle={oracle} "
        f"mutant={mutant}"
    )


def run():
    require_killed(
        "NC-01 transposed Koopman",
        (0, 0),
        ((0, 1),),
        production_rank(
            (0, 0),
            ((0, 1),),
        ),
        mutant_transposed_koopman_rank(
            (0, 0),
            ((0, 1),),
        ),
    )

    require_killed(
        "WRONG-SPEC D=KP(I-P)",
        (0, 0, 1),
        ((0, 2), (1,)),
        production_rank(
            (0, 0, 1),
            ((0, 2), (1,)),
        ),
        mutant_wrong_spec_rank(
            (0, 0, 1),
            ((0, 2), (1,)),
        ),
    )

    found = False

    for n in range(2, 5):
        for T in product(range(n), repeat=n):
            for partition in partitions_of_set(n):
                oracle = horizontal_rank(
                    T,
                    partition,
                )

                mutant = vertical_rank(
                    T,
                    partition,
                )

                if oracle != mutant:
                    print(
                        "KILLED: "
                        "NC-02 vertical stack substituted "
                        "for horizontal -> "
                        f"n={n} "
                        f"T={T} "
                        f"part={partition} "
                        f"oracle={oracle} "
                        f"mutant={mutant}"
                    )
                    found = True
                    break

            if found:
                break

        if found:
            break

    if not found:
        raise AssertionError(
            "MUTATION SURVIVED: "
            "NC-02 vertical stack substituted "
            "for horizontal"
        )

    print(
        "AQARION MUTATION SUITE PASS: "
        "all registered semantic mutations killed"
    )


if __name__ == "__main__":
    run()
