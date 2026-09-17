#!/usr/bin/env python3

from collections import defaultdict, deque

import numpy as np


def kaprekar_T(n_digits=4, base=10):
    def gap(x):
        digits = [(x // (base ** i)) % base for i in range(n_digits)]
        s = sorted(digits)
        return (s[-1] - s[0], s[-2] - s[1])

    G = [
        (g1, g2)
        for g1 in range(1, base)
        for g2 in range(0, g1 + 1)
    ]

    index = {g: i for i, g in enumerate(G)}

    return [
        index[gap(999 * g1 + 90 * g2)]
        for g1, g2 in G
    ], len(G)


def build_K(T, n):
    K = np.zeros((n, n))
    for i, t in enumerate(T):
        K[i, t] = 1.0
    return K


def build_P(blocks, n):
    P = np.zeros((n, n))

    for block in blocks:
        k = len(block)
        for i in block:
            for j in block:
                P[i, j] = 1.0 / k

    return P


def rank_D(blocks, T, n):
    D = (
        np.eye(n) - build_P(blocks, n)
    ) @ build_K(T, n) @ build_P(blocks, n)

    return int(np.linalg.matrix_rank(D, tol=1e-9))


def make_depth_partition(T, n):
    fixed = next(
        i for i, t in enumerate(T)
        if t == i
    )

    reverse = defaultdict(list)

    for i, t in enumerate(T):
        reverse[t].append(i)

    depth = {fixed: 0}
    queue = deque([fixed])

    while queue:
        v = queue.popleft()

        for u in reverse[v]:
            if u not in depth:
                depth[u] = depth[v] + 1
                queue.append(u)

    by_depth = defaultdict(list)

    for i in range(n):
        by_depth[depth[i]].append(i)

    return [
        by_depth[d]
        for d in sorted(by_depth)
    ]


def main():
    T, n = kaprekar_T()

    blocks = make_depth_partition(T, n)
    rank = rank_D(blocks, T, n)

    print(
        f"R3 depth partition rank: {rank} "
        f"{'PASS' if rank == 0 else 'FAIL'}"
    )

    if rank != 0:
        raise AssertionError(
            f"Depth quotient is not exact: rank={rank}"
        )


if __name__ == "__main__":
    main()
