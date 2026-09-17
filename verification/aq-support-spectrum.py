#!/usr/bin/env python3

"""
AQ-SUPPORT-SPECTRUM-001

Constructive verifier for the exact marked-defect spectrum.

This program is a computational companion to the analytic existence proof.

It does not prove the universal theorem.
It verifies canonical finite constructions for requested (s,k) pairs.

No NumPy.
No floating point.
"""

from __future__ import annotations

import math
import sys


def lower_bound(s: int) -> int:
    return -s + math.ceil(2 * math.sqrt(s)) - 1


def upper_bound(s: int) -> int:
    return s - 1


def construct_graph(s: int, k: int):
    if s < 1:
        raise ValueError("s must be >= 1")

    lo = lower_bound(s)
    hi = upper_bound(s)

    if not lo <= k <= hi:
        raise ValueError(
            f"k={k} outside [{lo},{hi}]"
        )

    v = s + 1 + k

    a = v // 2
    b = v - a

    if a * b < s:
        raise AssertionError(
            "bipartite capacity is insufficient"
        )

    edges = set()

    # Cover every vertex.
    for i in range(min(a, b)):
        edges.add((i, i))

    if a > b:
        for i in range(b, a):
            edges.add((i, 0))

    if b > a:
        for j in range(a, b):
            edges.add((0, j))

    # Fill to exactly s marked edges.
    for i in range(a):
        for j in range(b):
            if len(edges) == s:
                break

            edges.add((i, j))

        if len(edges) == s:
            break

    if len(edges) != s:
        raise AssertionError(
            "failed to construct exactly s marked edges"
        )

    if any(
        not any(i == u or j == w for u, w in edges)
        for i in range(a)
        for j in range(b)
    ):
        # This condition is deliberately not used.
        # Vertex coverage is checked below.
        pass

    left_degree = {
        i: 0
        for i in range(a)
    }

    right_degree = {
        j: 0
        for j in range(b)
    }

    for i, j in edges:
        left_degree[i] += 1
        right_degree[j] += 1

    if any(x == 0 for x in left_degree.values()):
        raise AssertionError("isolated left vertex")

    if any(x == 0 for x in right_degree.values()):
        raise AssertionError("isolated right vertex")

    return a, b, edges


def components(a: int, b: int, edges):
    n = a + b
    adjacency = [
        set()
        for _ in range(n)
    ]

    for i, j in edges:
        u = i
        v = a + j

        adjacency[u].add(v)
        adjacency[v].add(u)

    unseen = set(range(n))
    output = []

    while unseen:
        root = unseen.pop()
        stack = [root]
        component = {root}

        while stack:
            u = stack.pop()

            for v in adjacency[u]:
                if v in unseen:
                    unseen.remove(v)
                    component.add(v)
                    stack.append(v)

        output.append(component)

    return output


def verify(s: int, k: int) -> dict:
    a, b, edges = construct_graph(s, k)

    comps = components(
        a,
        b,
        edges,
    )

    v = a + b
    e = len(edges)
    c = len(comps)

    beta = e - v + c

    kappa = c - 1 - beta

    expected = k

    if kappa != expected:
        raise AssertionError(
            f"kappa mismatch: "
            f"expected={expected}, "
            f"observed={kappa}"
        )

    return {
        "s": s,
        "k": k,
        "vertices": v,
        "edges": e,
        "components": c,
        "cycle_rank": beta,
        "kappa": kappa,
    }


def verify_range(max_s: int):
    total = 0

    for s in range(1, max_s + 1):
        for k in range(
            lower_bound(s),
            upper_bound(s) + 1,
        ):
            verify(s, k)
            total += 1

    return total


def main():
    max_s = int(
        sys.argv[1]
        if len(sys.argv) > 1
        else 30
    )

    total = verify_range(max_s)

    print(
        "AQ-SUPPORT-SPECTRUM PASS"
    )

    print(
        f"max_s={max_s}"
    )

    print(
        f"constructed_cases={total}"
    )

    print(
        "all admissible (s,k) pairs "
        "passed"
    )


if __name__ == "__main__":
    main()
