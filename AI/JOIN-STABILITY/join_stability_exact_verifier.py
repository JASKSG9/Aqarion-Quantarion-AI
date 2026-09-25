#!/usr/bin/env python3
"""
AQARION JOIN-STABILITY
Exact finite verifier for pullback-stable join closure.

Evidence target:
    [V] exhaustive finite verification over the requested domain.

Mathematical theorem checked:
    For finite X, if E and F are pullback-stable under T,
    then E join F is pullback-stable under T.

This program does NOT replace the mathematical proof.
It independently reconstructs:
    - all maps T,
    - all equivalence partitions,
    - stable E/F pairs,
    - E join F,
    - the incidence-graph permutation condition.

No floating point.
Standard library only.
"""

from __future__ import annotations

from itertools import product
from dataclasses import dataclass


@dataclass(frozen=True)
class RunSummary:
    n: int
    maps: int
    equivalence_relations: int
    stable_pairs: int
    join_failures: int
    incidence_failures: int


def canonical(labels: list[int] | tuple[int, ...]) -> tuple[int, ...]:
    names: dict[int, int] = {}
    out: list[int] = []

    for x in labels:
        if x not in names:
            names[x] = len(names)
        out.append(names[x])

    return tuple(out)


def partitions(n: int) -> list[tuple[int, ...]]:
    """Enumerate all set partitions as restricted-growth strings."""
    result: list[tuple[int, ...]] = []

    def extend(prefix: list[int], maximum: int) -> None:
        if len(prefix) == n:
            result.append(tuple(prefix))
            return

        for value in range(maximum + 2):
            extend(prefix + [value], max(maximum, value))

    if n == 0:
        return [()]

    extend([0], 0)
    return result


def pullback_stable(
    partition: tuple[int, ...],
    T: tuple[int, ...],
) -> bool:
    """
    Exact condition:

        T(x) ~ T(y) => x ~ y.

    Equivalently every target partition block has at most one
    source partition block mapping into it.
    """
    source_for_target: dict[int, int] = {}

    for x, tx in enumerate(T):
        target_block = partition[tx]
        source_block = partition[x]

        old = source_for_target.get(target_block)

        if old is None:
            source_for_target[target_block] = source_block
        elif old != source_block:
            return False

    return True


def induced_class_map(
    partition: tuple[int, ...],
    T: tuple[int, ...],
) -> tuple[int, ...]:
    """
    Return the target block reached by each source block.

    Pullback stability guarantees that this is well-defined.
    For finite X it is a permutation.
    """
    number_of_blocks = max(partition, default=-1) + 1
    result: list[int] = []

    for block in range(number_of_blocks):
        targets = {
            partition[T[x]]
            for x in range(len(T))
            if partition[x] == block
        }

        if len(targets) != 1:
            raise AssertionError(
                "Stable partition did not induce a single target block"
            )

        result.append(next(iter(targets)))

    return tuple(result)


def is_permutation(values: tuple[int, ...]) -> bool:
    return sorted(values) == list(range(len(values)))


def join(
    P: tuple[int, ...],
    Q: tuple[int, ...],
) -> tuple[int, ...]:
    """Equivalence-relation join via transitive closure."""
    n = len(P)
    parent = list(range(n))

    def find(x: int) -> int:
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def union(a: int, b: int) -> None:
        a = find(a)
        b = find(b)

        if a != b:
            parent[b] = a

    for i in range(n):
        for j in range(i):
            if P[i] == P[j] or Q[i] == Q[j]:
                union(i, j)

    return canonical([find(i) for i in range(n)])


def incidence_edges(
    E: tuple[int, ...],
    F: tuple[int, ...],
) -> set[tuple[int, int]]:
    """
    Bipartite incidence graph.

    One edge (E[x], F[x]) for each nonempty intersection cell.
    """
    return {(E[x], F[x]) for x in range(len(E))}


def incidence_automorphism_holds(
    E: tuple[int, ...],
    F: tuple[int, ...],
    sigma_E: tuple[int, ...],
    sigma_F: tuple[int, ...],
) -> bool:
    """
    Verify that the induced class permutation preserves the complete
    incidence-edge set.

    For finite stable E/F this is the structural core of the proof.
    """
    edges = incidence_edges(E, F)

    image = {
        (sigma_E[e], sigma_F[f])
        for e, f in edges
    }

    return image == edges


def verify_one_map(
    T: tuple[int, ...],
    all_partitions: list[tuple[int, ...]],
) -> tuple[int, int]:
    stable = [
        P for P in all_partitions
        if pullback_stable(P, T)
    ]

    stable_pairs = 0
    failures = 0
    incidence_failures = 0

    for i, E in enumerate(stable):
        sigma_E = induced_class_map(E, T)

        if not is_permutation(sigma_E):
            incidence_failures += 1

        for F in stable[i:]:
            stable_pairs += 1

            sigma_F = induced_class_map(F, T)

            if not is_permutation(sigma_F):
                incidence_failures += 1

            if not incidence_automorphism_holds(
                E, F, sigma_E, sigma_F
            ):
                incidence_failures += 1

            G = join(E, F)

            if not pullback_stable(G, T):
                failures += 1

    return stable_pairs, failures + incidence_failures


def exhaustive(n: int) -> RunSummary:
    all_partitions = partitions(n)

    maps = 0
    stable_pairs = 0
    join_failures = 0
    incidence_failures = 0

    for T in product(range(n), repeat=n):
        maps += 1

        stable = [
            P for P in all_partitions
            if pullback_stable(P, T)
        ]

        for i, E in enumerate(stable):
            sigma_E = induced_class_map(E, T)

            if not is_permutation(sigma_E):
                incidence_failures += 1

            for F in stable[i:]:
                stable_pairs += 1

                sigma_F = induced_class_map(F, T)

                if not is_permutation(sigma_F):
                    incidence_failures += 1

                if not incidence_automorphism_holds(
                    E, F, sigma_E, sigma_F
                ):
                    incidence_failures += 1

                G = join(E, F)

                if not pullback_stable(G, T):
                    join_failures += 1

    return RunSummary(
        n=n,
        maps=maps,
        equivalence_relations=len(all_partitions),
        stable_pairs=stable_pairs,
        join_failures=join_failures,
        incidence_failures=incidence_failures,
    )


def main() -> int:
    print("AQARION JOIN-STABILITY EXACT FINITE VERIFIER")
    print("Evidence: [V] finite exhaustive computation")
    print()

    expected = {
        1: (1, 1, 1, 0, 0),
        2: (4, 2, 8, 0, 0),
        3: (27, 5, 84, 0, 0),
        4: (256, 15, 1276, 0, 0),
        5: (3125, 52, 24475, 0, 0),
        6: (46656, 203, 582696, 0, 0),
    }

    overall_failures = 0

    for n in range(1, 7):
        summary = exhaustive(n)

        print(
            f"n={summary.n} "
            f"maps={summary.maps} "
            f"partitions={summary.equivalence_relations} "
            f"stable_pairs={summary.stable_pairs} "
            f"join_failures={summary.join_failures} "
            f"incidence_failures={summary.incidence_failures}"
        )

        exp_maps, exp_parts, exp_pairs, exp_join, exp_inc = expected[n]

        if (
            summary.maps != exp_maps
            or summary.equivalence_relations != exp_parts
            or summary.stable_pairs != exp_pairs
            or summary.join_failures != exp_join
            or summary.incidence_failures != exp_inc
        ):
            overall_failures += 1

    if overall_failures:
        print("RESULT=FAIL")
        return 1

    print()
    print("RESULT=PASS")
    print("DOMAIN=n=1..6")
    print("JOIN_THEOREM_FINITE_DOMAIN=EXHAUSTIVELY_VERIFIED")
    print("INCIDENCE_GRAPH_STRUCTURE=EXHAUSTIVELY_VERIFIED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())



