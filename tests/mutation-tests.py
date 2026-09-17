#!/usr/bin/env python3

"""
AQARION Layer 1 — operator-convention mutation test.

Canonical convention:

    K[i, T(i)] = 1

Deliberate mutant:

    K[T(i), i] = 1

This is a CI regression/self-refutation test.

It must:
  1. accept the canonical convention on every trial;
  2. reject the index-swapped mutant;
  3. exit nonzero if either condition fails.

This is not a theorem proof.
"""

import sys

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

    state_index = {
        g: i
        for i, g in enumerate(G)
    }

    T = [
        state_index[
            gap(999 * g1 + 90 * g2)
        ]
        for g1, g2 in G
    ]

    return T, len(G)


def build_K(T, n):
    """Canonical Koopman convention."""
    K = np.zeros((n, n))

    for i, ti in enumerate(T):
        K[i, ti] = 1.0

    return K


def build_K_mutant(T, n):
    """Deliberate index-swapped mutant."""
    K = np.zeros((n, n))

    for i, ti in enumerate(T):
        K[ti, i] = 1.0

    return K


def build_P(blocks, n):
    P = np.zeros((n, n))

    for block in blocks:
        k = len(block)

        for i in block:
            for j in block:
                P[i, j] = 1.0 / k

    return P


def rank_D(blocks, T, n, mutant=False):
    K = (
        build_K_mutant(T, n)
        if mutant
        else build_K(T, n)
    )

    P = build_P(blocks, n)

    D = (np.eye(n) - P) @ K @ P

    return int(
        np.linalg.matrix_rank(D, tol=1e-9)
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
        find(v)
        for v in range(2 * m)
    })


def main():
    T, n = kaprekar_T()

    rng = np.random.default_rng(42)

    total = 5000

    correct_pass = 0
    mutant_pass = 0

    for _ in range(total):
        k = int(
            rng.integers(
                2,
                min(n, 8)
            )
        )

        permutation = rng.permutation(n)

        blocks = [
            list(permutation[:k]),
            list(permutation[k:]),
        ]

        expected = 2 - c_bip(blocks, T)

        correct_rank = rank_D(
            blocks,
            T,
            n,
            mutant=False,
        )

        mutant_rank = rank_D(
            blocks,
            T,
            n,
            mutant=True,
        )

        if correct_rank == expected:
            correct_pass += 1

        if mutant_rank == expected:
            mutant_pass += 1

    mutation_detected = mutant_pass == 0

    print()
    print("CI LAYER 1 -- MUTATION TEST")
    print(
        f"  Correct Koopman: "
        f"{correct_pass}/{total} PASS"
    )
    print(
        f"  Mutant Transfer: "
        f"{mutant_pass}/{total} PASS"
    )
    print(
        f"  Mutation DETECTED: "
        f"{mutation_detected}"
    )

    if correct_pass != total:
        print(
            "FAIL: canonical Koopman operator "
            "does not reproduce the receipt."
        )
        return 1

    if not mutation_detected:
        print(
            "FAIL: operator mutation survived."
        )
        return 1

    print(
        "  PASS: CI catches the "
        "operator-index mutation."
    )

    return 0


if __name__ == "__main__":
    sys.exit(main())
