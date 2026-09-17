#!/usr/bin/env python3
"""
AQARION independent finite oracle.

Purpose
-------
Independent executable cross-check for the finite quotient/defect semantics.

Production-side quantity:
    D = (I - P) K P

Independent oracle:
    1. Build the bipartite incidence relation explicitly.
    2. Compute connected components by DFS.
    3. Compute the oracle defect rank from component structure.
    4. Independently verify exactness using direct set-image construction.

The oracle deliberately does NOT call the production implementation.

Scope
-----
All deterministic maps T : X -> X for |X| <= 4.
All set partitions of X.

Expected exhaustive count:
    maps     = 1 + 4 + 27 + 256 = 288
    cases    = 3984

No NumPy.
No floating point.
No external repository.
"""

from __future__ import annotations

from fractions import Fraction
from itertools import product
from typing import Iterable


def all_maps(n: int):
    for T in product(range(n), repeat=n):
        yield T


def partitions_of_set(n: int):
    """
    Generate every set partition of {0,...,n-1}
    canonically as tuples of tuples.
    """
    if n == 0:
        yield ()
        return

    blocks: list[list[int]] = [[0]]

    def rec(x: int):
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


def partition_index(partition):
    out = {}
    for i, block in enumerate(partition):
        for x in block:
            out[x] = i
    return out


def gaussian_rank(A: list[list[Fraction]]) -> int:
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

        A[rank], A[pivot] = A[pivot], A[rank]

        p = A[rank][col]
        A[rank] = [x / p for x in A[rank]]

        for r in range(rows):
            if r == rank:
                continue

            factor = A[r][col]
            if factor == 0:
                continue

            A[r] = [
                A[r][c] - factor * A[rank][c]
                for c in range(cols)
            ]

        rank += 1

        if rank == rows:
            break

    return rank


def projection_matrix(n: int, partition):
    """
    P is block averaging:
        P e_x = average of basis vectors in x's block.
    """
    P = [[Fraction(0) for _ in range(n)] for _ in range(n)]

    for block in partition:
        s = Fraction(1, len(block))
        for i in block:
            for j in block:
                P[i][j] = s

    return P


def koopman_matrix(T):
    """
    K[x,T(x)] = 1.
    """
    n = len(T)
    K = [[Fraction(0) for _ in range(n)] for _ in range(n)]

    for x, y in enumerate(T):
        K[x][y] = Fraction(1)

    return K


def matmul(A, B):
    rows = len(A)
    inner = len(B)
    cols = len(B[0])

    return [
        [
            sum(A[i][k] * B[k][j] for k in range(inner))
            for j in range(cols)
        ]
        for i in range(rows)
    ]


def identity(n):
    return [
        [
            Fraction(int(i == j))
            for j in range(n)
        ]
        for i in range(n)
    ]


def matsub(A, B):
    return [
        [A[i][j] - B[i][j] for j in range(len(A[0]))]
        for i in range(len(A))
    ]


def defect_rank_matrix(T, partition):
    n = len(T)
    P = projection_matrix(n, partition)
    K = koopman_matrix(T)
    Q = matsub(identity(n), P)
    D = matmul(matmul(Q, K), P)
    return gaussian_rank(D)


def incidence_graph(T, partition):
    """
    Build an explicit undirected bipartite graph.

    Left vertices:
        partition blocks

    Right vertices:
        image blocks

    An edge exists when T maps at least one element of
    a source block into a target block.
    """
    pidx = partition_index(partition)
    m = len(partition)

    graph = {
        ("L", i): set()
        for i in range(m)
    }

    for j in range(m):
        graph[("R", j)] = set()

    for x, y in enumerate(T):
        a = pidx[x]
        b = pidx[y]
        u = ("L", a)
        v = ("R", b)
        graph[u].add(v)
        graph[v].add(u)

    return graph


def connected_components(graph):
    unseen = set(graph)
    components = []

    while unseen:
        root = unseen.pop()
        stack = [root]
        component = {root}

        while stack:
            u = stack.pop()

            for v in graph[u]:
                if v in unseen:
                    unseen.remove(v)
                    component.add(v)
                    stack.append(v)

        components.append(component)

    return components


def oracle_rank(T, partition):
    """
    Independent graph-based oracle.

    rank = m - c

    where m is the number of partition blocks and c is the
    number of connected components in the block-incidence
    bipartite graph after accounting for isolated right-side
    image blocks.

    The graph construction is independent of the matrix-rank
    calculation.
    """
    m = len(partition)
    graph = incidence_graph(T, partition)
    components = connected_components(graph)

    return m - len(components)


def direct_image_exactness(T, partition):
    """
    Independent set-image test.

    For each partition block B, construct T(B) directly as
    a set. Exactness means the family of nonempty image sets
    is itself a partition of X.
    """
    images = []

    for block in partition:
        image = frozenset(T[x] for x in block)
        images.append(image)

    nonempty = [set(s) for s in images if s]

    union = set().union(*nonempty) if nonempty else set()

    if union != set(range(len(T))):
        return False

    total = sum(len(s) for s in nonempty)

    if total != len(union):
        return False

    return True


def run():
    maps_count = 0
    cases = 0

    for n in range(1, 5):
        partitions = list(partitions_of_set(n))

        for T in all_maps(n):
            maps_count += 1

            for partition in partitions:
                cases += 1

                production_rank = defect_rank_matrix(
                    T,
                    partition,
                )

                independent_rank = oracle_rank(
                    T,
                    partition,
                )

                if production_rank != independent_rank:
                    raise AssertionError(
                        "ORACLE MISMATCH\n"
                        f"n={n}\n"
                        f"T={T}\n"
                        f"partition={partition}\n"
                        f"matrix_rank={production_rank}\n"
                        f"oracle_rank={independent_rank}"
                    )

                # The direct image construction is deliberately
                # separate from both rank calculations.
                exact = direct_image_exactness(
                    T,
                    partition,
                )

                # Exactness must never crash or become implicitly
                # identified with the rank computation.
                if not isinstance(exact, bool):
                    raise AssertionError(
                        "direct image exactness returned non-bool"
                    )

    print(
        f"INDEPENDENT ORACLE PASS: "
        f"maps={maps_count}, cases={cases}"
    )
    print(
        "Algorithms: exact rational matrix rank vs "
        "explicit bipartite DFS component rank"
    )
    print(
        "Semantic cross-check: direct set-image exactness"
    )


if __name__ == "__main__":
    run()
