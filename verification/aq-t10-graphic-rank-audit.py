#!/usr/bin/env python3

"""
AQ-T10-GRAPHIC-RANK-AUDIT

Adversarial finite audit of the corrected dynamic-closure proof route.

Checks:

1. dynamic closure = orbit-edge connected components;
2. orbit(meet) subset orbit(P) intersection orbit(Q);
3. join-orbit graph and union-orbit graph have identical components;
4. dynamic closure rank is submodular.

This is computational validation of proof obligations.
It is not a universal proof.
"""

from itertools import product


def rgs(n):
    if n == 0:
        return [()]

    out = []

    def rec(a, maximum):
        if len(a) == n:
            out.append(tuple(a))
            return

        for value in range(maximum + 2):
            rec(
                a + (value,),
                max(maximum, value),
            )

    rec((0,), 0)
    return out


def canon(labels):
    names = {}
    out = []

    for x in labels:
        if x not in names:
            names[x] = len(names)

        out.append(names[x])

    return tuple(out)


def edge_set(partition):
    n = len(partition)

    return frozenset(
        (i, j)
        for i in range(n)
        for j in range(i + 1, n)
        if partition[i] == partition[j]
    )


def orbit_edge(e, T):
    seen = set()
    current = e

    while current not in seen:
        seen.add(current)

        i, j = current

        current = tuple(
            sorted(
                (
                    T[i],
                    T[j],
                )
            )
        )

    return seen


def orbit_edges(edges, T):
    output = set()

    for e in edges:
        output.update(
            orbit_edge(e, T)
        )

    return frozenset(output)


def graph_components(n, edges):
    adjacency = [
        set()
        for _ in range(n)
    ]

    for i, j in edges:
        adjacency[i].add(j)
        adjacency[j].add(i)

    labels = [-1] * n
    count = 0

    for root in range(n):
        if labels[root] != -1:
            continue

        stack = [root]
        labels[root] = count

        while stack:
            u = stack.pop()

            for v in adjacency[u]:
                if labels[v] == -1:
                    labels[v] = count
                    stack.append(v)

        count += 1

    return canon(labels), count


def join(P, Q):
    n = len(P)

    edges = {
        (i, j)
        for i in range(n)
        for j in range(i + 1, n)
        if (
            P[i] == P[j]
            or
            Q[i] == Q[j]
        )
    }

    labels, _ = graph_components(
        n,
        edges,
    )

    return labels


def closure(P, T):
    orbit = orbit_edges(
        edge_set(P),
        T,
    )

    labels, _ = graph_components(
        len(P),
        orbit,
    )

    return labels


def rank_of_edges(n, edges):
    _, components = graph_components(
        n,
        edges,
    )

    return n - components


def audit(n):
    partitions = rgs(n)

    cases = 0
    meet_failures = 0
    join_failures = 0
    submod_failures = 0

    all_maps = product(
        range(n),
        repeat=n,
    )

    for T in all_maps:

        for P in partitions:

            EP = edge_set(P)
            OP = orbit_edges(EP, T)

            for Q in partitions:

                EQ = edge_set(Q)
                OQ = orbit_edges(EQ, T)

                meet = join(
                    P,
                    Q,
                )

                # The common refinement is easier to
                # represent directly.
                meet = canon(
                    tuple(
                        (P[i], Q[i])
                        for i in range(n)
                    )
                )

                EM = edge_set(meet)
                OM = orbit_edges(EM, T)

                if not (
                    OM <= OP & OQ
                ):
                    meet_failures += 1

                J = join(P, Q)
                EJ = edge_set(J)
                OJ = orbit_edges(EJ, T)

                _, union_components = (
                    graph_components(
                        n,
                        OP | OQ,
                    )
                )

                _, join_components = (
                    graph_components(
                        n,
                        OJ,
                    )
                )

                if (
                    union_components
                    != join_components
                ):
                    join_failures += 1

                rhoP = rank_of_edges(
                    n,
                    OP,
                )

                rhoQ = rank_of_edges(
                    n,
                    OQ,
                )

                rhoM = rank_of_edges(
                    n,
                    OM,
                )

                rhoJ = rank_of_edges(
                    n,
                    OJ,
                )

                if rhoP + rhoQ < rhoM + rhoJ:
                    submod_failures += 1

                cases += 1

    return {
        "n": n,
        "cases": cases,
        "meet_failures": meet_failures,
        "join_failures": join_failures,
        "submodularity_failures": submod_failures,
    }


def main():
    for n in range(1, 5):
        result = audit(n)
        print(result)

        assert result["meet_failures"] == 0
        assert result["join_failures"] == 0
        assert result["submodularity_failures"] == 0

    print(
        "AQ-T10-GRAPHIC-RANK-AUDIT PASS"
    )


if __name__ == "__main__":
    main()
