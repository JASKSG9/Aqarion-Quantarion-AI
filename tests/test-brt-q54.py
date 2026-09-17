#!/usr/bin/env python3

import numpy as np


def kaprekar_T(n_digits=4, base=10):
    def gap(x):
        digits = [
            (x // (base ** i)) % base
            for i in range(n_digits)
        ]

        s = sorted(digits)

        return (
            s[-1] - s[0],
            s[-2] - s[1],
        )

    G = [
        (g1, g2)
        for g1 in range(1, base)
        for g2 in range(0, g1 + 1)
    ]

    index = {
        g: i
        for i, g in enumerate(G)
    }

    return [
        index[
            gap(999 * g1 + 90 * g2)
        ]
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
    K = build_K(T, n)
    P = build_P(blocks, n)

    D = (
        np.eye(n) - P
    ) @ K @ P

    return int(
        np.linalg.matrix_rank(
            D,
            tol=1e-9,
        )
    )


def c_bip(blocks, T):
    m = len(blocks)

    label = {
        x: i
        for i, block in enumerate(blocks)
        for x in block
    }

    parent = list(range(2 * m))

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]

        return x

    def union(a, b):
        a = find(a)
        b = find(b)

        if a != b:
            parent[a] = b

    for i, block in enumerate(blocks):
        targets = {
            label[T[x]]
            for x in block
        }

        for j in targets:
            union(i, m + j)

    return len({
        find(x)
        for x in range(2 * m)
    })


def main():
    T, n = kaprekar_T()

    rng = np.random.default_rng(42)

    trials = 200
    passed = 0

    for _ in range(trials):
        k = int(
            rng.integers(1, n)
        )

        permutation = rng.permutation(n)

        blocks = [
            list(permutation[:k]),
            list(permutation[k:]),
        ]

        expected = (
            2 - c_bip(blocks, T)
        )

        observed = rank_D(
            blocks,
            T,
            n,
        )

        if observed != expected:
            raise AssertionError(
                "BRT failure: "
                f"observed={observed}, "
                f"expected={expected}"
            )

        passed += 1

    print(
        f"R1 BRT rank=m-c_bip: "
        f"{passed}/{trials} PASS"
    )


if __name__ == "__main__":
    main()    main()
