#!/usr/bin/env python3

import numpy as np


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


def test_case(m, k, s):
    n = m * k

    T = [
        (i + s) % n
        for i in range(n)
    ]

    blocks = [
        [
            b * k + j
            for j in range(k)
        ]
        for b in range(m)
    ]

    P = build_P(
        blocks,
        n,
    )

    K = build_K(
        T,
        n,
    )

    D = (
        np.eye(n) - P
    ) @ K @ P

    r = s % k

    expected = (
        2
        * m
        * r
        * (k - r)
        / k**2
    )

    observed = (
        np.linalg.norm(
            D,
            "fro",
        )
        ** 2
    )

    return observed, expected


def main():
    failures = 0
    tested = 0

    for k in range(2, 6):
        for m in range(2, 5):
            for s in range(
                1,
                k * m,
            ):
                r = s % k

                if r == 0:
                    continue

                observed, expected = (
                    test_case(
                        m,
                        k,
                        s,
                    )
                )

                tested += 1

                if abs(
                    observed - expected
                ) > 1e-8:
                    failures += 1

                    print(
                        "FAIL:",
                        f"m={m}",
                        f"k={k}",
                        f"s={s}",
                        f"observed={observed}",
                        f"expected={expected}",
                    )

    print(
        "R4 ||D||_F²="
        "2mr(k-r)/k²: "
        f"{failures}/{tested} "
        f"fails "
        f"{'PASS' if failures == 0 else 'FAIL'}"
    )

    if failures:
        raise AssertionError(
            "Frobenius formula failed "
            f"{failures}/{tested} cases."
        )


if __name__ == "__main__":
    main()
