#!/usr/bin/env python3
"""
AQARION independent finite reference/oracle suite.

Purpose
-------
This module is intentionally implemented independently from
verification/aq_contract/aq_contract_semantic_suite.py.

It does NOT reuse the production algorithms for:
    * Koopman construction
    * raw image-block construction
    * T_* transport
    * equivalence-class generation

Instead it computes an independent reference result and compares
that result against the repository's current object/operator
implementation.

Scope
-----
Finite exhaustive verification for |X| <= 4.

For each n in {1,2,3,4}:
    * enumerate every function T : X -> X
    * enumerate every partition Pi of X
    * compare production results against independent results

This is still finite computation.
It is NOT a proof of a universal theorem.

Evidence class:
    INDEPENDENT FINITE ORACLE [IO]

No NumPy.
No floating point.
No external dependencies.
"""

from __future__ import annotations

from itertools import product
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[2]

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


from verification.aq_contract import aq_contract_semantic_suite as production


def canonical(blocks):
    """Canonical representation independent of production canonicalizer."""
    normalized = [frozenset(block) for block in blocks]
    return tuple(
        sorted(
            normalized,
            key=lambda block: (min(block), len(block), tuple(sorted(block))),
        )
    )


def reference_koopman(T):
    """
    Independent direct construction of K_T.

    Convention:
        K[x,y] = 1 iff y = T(x)
    """
    n = len(T)

    return tuple(
        tuple(
            1 if y == T[x] else 0
            for y in range(n)
        )
        for x in range(n)
    )


def reference_raw_image_blocks(T, partition):
    """
    Direct set-image construction.

    This deliberately does not call production.raw_image_blocks().
    """
    return canonical(
        {
            T[x]
            for x in block
        }
        for block in partition
    )


def reference_t_star(T, partition):
    """
    Independent graph-connectivity implementation of T_*.

    For every source block B in Pi, all states in T(B) are placed
    in the same connected component.

    Unlike the production implementation, this uses explicit
    adjacency + graph traversal rather than union-find.
    """
    n = len(T)

    adjacency = [
        set()
        for _ in range(n)
    ]

    for block in partition:
        images = sorted({T[x] for x in block})

        for left in images:
            for right in images:
                if left != right:
                    adjacency[left].add(right)
                    adjacency[right].add(left)

    components = []
    unseen = set(range(n))

    while unseen:
        start = min(unseen)
        stack = [start]
        component = set()

        while stack:
            current = stack.pop()

            if current not in unseen:
                continue

            unseen.remove(current)
            component.add(current)

            for neighbor in sorted(adjacency[current], reverse=True):
                if neighbor in unseen:
                    stack.append(neighbor)

        components.append(frozenset(component))

    return canonical(components)


def restricted_growth_strings(n):
    """
    Generate restricted-growth strings representing all set partitions.

    Example for n=3:
        000
        001
        010
        011
        012

    Each string corresponds to exactly one set partition.
    """
    if n == 0:
        yield ()
        return

    values = [0] * n

    def extend(position):
        if position == n:
            yield tuple(values)
            return

        max_value = max(values[:position])

        for value in range(max_value + 2):
            values[position] = value
            yield from extend(position + 1)

    yield from extend(1)


def all_partitions(n):
    """
    Enumerate every partition of {0,...,n-1}.
    """
    for encoding in restricted_growth_strings(n):
        blocks = []

        for label in range(max(encoding) + 1):
            block = {
                index
                for index, value in enumerate(encoding)
                if value == label
            }
            blocks.append(frozenset(block))

        yield tuple(blocks)


def relabel_map(T, permutation):
    """
    Conjugate T by a relabeling p:

        T' = p o T o p^{-1}
    """
    n = len(T)

    inverse = [0] * n

    for old, new in enumerate(permutation):
        inverse[new] = old

    return tuple(
        permutation[T[inverse[x]]]
        for x in range(n)
    )


def relabel_partition(partition, permutation):
    return tuple(
        frozenset(
            permutation[x]
            for x in block
        )
        for block in partition
    )


def relabel_blocks(blocks, permutation):
    return canonical(
        {
            permutation[x]
            for x in block
        }
        for block in blocks
    )


def assert_equal(label, actual, expected):
    if actual != expected:
        raise AssertionError(
            f"{label}\n"
            f"actual  = {actual!r}\n"
            f"expected= {expected!r}"
        )


def check_koopman(n):
    """
    Exhaustive Koopman-orientation check for every map X -> X.
    """
    count = 0

    for T in product(range(n), repeat=n):
        actual = production.koopman_matrix(T)
        expected = reference_koopman(T)

        assert_equal(
            f"Koopman mismatch n={n}, T={T}",
            actual,
            expected,
        )

        count += 1

    return count


def check_raw_images_and_transport(n):
    """
    Exhaustively compare production and independent results for
    every map and every partition.
    """
    map_count = 0
    case_count = 0

    partitions = tuple(all_partitions(n))

    for T in product(range(n), repeat=n):
        map_count += 1

        for partition_blocks in partitions:
            production_partition = production.Partition(
                tuple(partition_blocks)
            )

            actual_raw = production.raw_image_blocks(
                T,
                production_partition,
            )

            expected_raw = reference_raw_image_blocks(
                T,
                partition_blocks,
            )

            assert_equal(
                (
                    "raw image mismatch "
                    f"n={n}, T={T}, Pi={partition_blocks}"
                ),
                actual_raw,
                expected_raw,
            )

            actual_transport = production.t_star(
                T,
                production_partition,
            )

            expected_transport = reference_t_star(
                T,
                partition_blocks,
            )

            assert_equal(
                (
                    "T_* mismatch "
                    f"n={n}, T={T}, Pi={partition_blocks}"
                ),
                actual_transport,
                expected_transport,
            )

            case_count += 1

    return map_count, case_count


def check_relabeling_invariance(n):
    """
    Metamorphic test.

    Relabeling the finite state space must relabel the resulting
    semantic objects correspondingly.
    """
    partitions = tuple(all_partitions(n))

    # Deterministic cyclic relabeling is sufficient here because
    # exhaustive map/partition enumeration already supplies broad
    # finite coverage.
    permutation = tuple(
        (x + 1) % n
        for x in range(n)
    )

    for T in product(range(n), repeat=n):
        conjugated = relabel_map(T, permutation)

        for partition_blocks in partitions:
            conjugated_partition = relabel_partition(
                partition_blocks,
                permutation,
            )

            original_partition = production.Partition(
                tuple(partition_blocks)
            )

            conjugated_production_partition = production.Partition(
                tuple(conjugated_partition)
            )

            original_transport = production.t_star(
                T,
                original_partition,
            )

            conjugated_transport = production.t_star(
                conjugated,
                conjugated_production_partition,
            )

            expected_transport = relabel_blocks(
                original_transport,
                permutation,
            )

            assert_equal(
                (
                    "relabeling invariance failure "
                    f"n={n}, T={T}, Pi={partition_blocks}"
                ),
                conjugated_transport,
                expected_transport,
            )


def check_boundary_maps(n):
    """
    Explicit adversarial fixtures.

    These are supplementary to exhaustive enumeration.
    """
    maps = (
        ("identity", tuple(range(n))),
        ("constant_zero", tuple(0 for _ in range(n))),
        ("successor_mod_n", tuple((x + 1) % n for x in range(n))),
    )

    partitions = tuple(all_partitions(n))

    for name, T in maps:
        for partition_blocks in partitions:
            production_partition = production.Partition(
                tuple(partition_blocks)
            )

            actual = production.t_star(
                T,
                production_partition,
            )

            expected = reference_t_star(
                T,
                partition_blocks,
            )

            assert_equal(
                (
                    f"boundary-map failure {name} "
                    f"n={n}, Pi={partition_blocks}"
                ),
                actual,
                expected,
            )


def main():
    total_maps = 0
    total_cases = 0

    for n in range(1, 5):
        koopman_maps = check_koopman(n)
        maps, cases = check_raw_images_and_transport(n)

        check_relabeling_invariance(n)
        check_boundary_maps(n)

        assert_equal(
            f"map-count mismatch n={n}",
            maps,
            koopman_maps,
        )

        total_maps += maps
        total_cases += cases

        print(
            f"IO-N={n} PASS: "
            f"{maps} maps, "
            f"{cases} map/partition cases"
        )

    print(
        f"IO-KOOPMAN PASS: "
        f"{total_maps} finite maps checked"
    )

    print(
        f"IO-SEMANTICS PASS: "
        f"{total_cases} map/partition cases checked"
    )

    print(
        "IO-METAMORPHIC PASS: "
        "state-space relabeling invariance"
    )

    print(
        "IO-BOUNDARY PASS: "
        "identity/constant/cyclic adversarial maps"
    )

    print(
        "AQARION INDEPENDENT FINITE ORACLE SUITE PASS"
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())


