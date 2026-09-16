#!/usr/bin/env python3
"""
AQ-S14 semantic and forest-kernel verification suite.

FILE:
    verification/aq_s14/aq_s14_semantic_suite.py

TYPE:
    PYTHON SCRIPT

Scope:
    K3 forest/incidence semantics and adversarial object identity.

Evidence:
    Exact finite computation only.

This script does NOT prove the universal forest theorem.
"""

from __future__ import annotations

from fractions import Fraction
from itertools import combinations
import sys


VERTICES = (0, 1, 2)
EDGES = (
    (0, 1),
    (0, 2),
    (1, 2),
)


def normalize_edges(edges):
    return frozenset(
        tuple(sorted(edge))
        for edge in edges
    )


def find(parent, x):
    while parent[x] != x:
        parent[x] = parent[parent[x]]
        x = parent[x]
    return x


def union(parent, a, b):
    ra = find(parent, a)
    rb = find(parent, b)

    if ra == rb:
        return False

    parent[rb] = ra
    return True


def is_forest(vertices, edges):
    parent = {v: v for v in vertices}

    for u, v in normalize_edges(edges):
        if not union(parent, u, v):
            return False

    return True


def component_count(vertices, edges):
    parent = {v: v for v in vertices}

    for u, v in normalize_edges(edges):
        union(parent, u, v)

    return len({
        find(parent, v)
        for v in vertices
    })


def is_spanning(vertices, edges):
    return component_count(vertices, edges) == 1


def rank(matrix):
    matrix = [
        [Fraction(value) for value in row]
        for row in matrix
    ]

    if not matrix:
        return 0

    rows = len(matrix)
    cols = len(matrix[0])

    pivot_row = 0

    for column in range(cols):
        pivot = None

        for row in range(pivot_row, rows):
            if matrix[row][column] != 0:
                pivot = row
                break

        if pivot is None:
            continue

        matrix[pivot_row], matrix[pivot] = (
            matrix[pivot],
            matrix[pivot_row],
        )

        pivot_value = matrix[pivot_row][column]

        matrix[pivot_row] = [
            value / pivot_value
            for value in matrix[pivot_row]
        ]

        for row in range(rows):
            if row == pivot_row:
                continue

            factor = matrix[row][column]

            if factor == 0:
                continue

            matrix[row] = [
                a - factor * b
                for a, b in zip(
                    matrix[row],
                    matrix[pivot_row],
                )
            ]

        pivot_row += 1

        if pivot_row == rows:
            break

    return pivot_row


def oriented_incidence(vertices, edges, signs=None):
    vertices = tuple(vertices)
    edges = tuple(normalize_edges(edges))

    position = {
        vertex: index
        for index, vertex in enumerate(vertices)
    }

    matrix = [
        [Fraction(0) for _ in edges]
        for _ in vertices
    ]

    for j, (u, v) in enumerate(edges):
        sign = 1

        if signs is not None:
            sign = signs[j]

        matrix[position[u]][j] += sign
        matrix[position[v]][j] -= sign

    return matrix


def unsigned_incidence(vertices, edges):
    vertices = tuple(vertices)
    edges = tuple(normalize_edges(edges))

    position = {
        vertex: index
        for index, vertex in enumerate(vertices)
    }

    matrix = [
        [Fraction(0) for _ in edges]
        for _ in vertices
    ]

    for j, (u, v) in enumerate(edges):
        matrix[position[u]][j] = 1
        matrix[position[v]][j] = 1

    return matrix


def assert_equal(label, actual, expected):
    if actual != expected:
        raise AssertionError(
            f"{label}: actual={actual!r}, expected={expected!r}"
        )


def test_spanning_trees():
    trees = []

    for edges in combinations(EDGES, 2):
        if is_forest(VERTICES, edges):
            trees.append(normalize_edges(edges))

    assert_equal(
        "K3 spanning tree count",
        len(trees),
        3,
    )

    for tree in trees:
        assert is_forest(VERTICES, tree)
        assert is_spanning(VERTICES, tree)

    return trees


def test_all_orientations(trees):
    cases = 0

    for tree in trees:
        tree_edges = tuple(sorted(tree))

        for mask in range(2 ** len(tree_edges)):
            signs = [
                1 if ((mask >> index) & 1) else -1
                for index in range(len(tree_edges))
            ]

            matrix = oriented_incidence(
                VERTICES,
                tree_edges,
                signs,
            )

            assert_equal(
                "oriented incidence rank",
                rank(matrix),
                2,
            )

            cases += 1

    assert_equal(
        "oriented incidence case count",
        cases,
        12,
    )


def test_all_edge_subsets():
    counts = {
        "forest_spanning": 0,
        "forest_nonspanning": 0,
        "cyclic_spanning": 0,
        "cyclic_nonspanning": 0,
    }

    for mask in range(2 ** len(EDGES)):
        subset = [
            EDGES[index]
            for index in range(len(EDGES))
            if (mask >> index) & 1
        ]

        forest = is_forest(VERTICES, subset)
        spanning = is_spanning(VERTICES, subset)

        if forest and spanning:
            counts["forest_spanning"] += 1
        elif forest and not spanning:
            counts["forest_nonspanning"] += 1
        elif not forest and spanning:
            counts["cyclic_spanning"] += 1
        else:
            counts["cyclic_nonspanning"] += 1

    assert_equal(
        "K3 forest/spanning classification",
        counts,
        {
            "forest_spanning": 3,
            "forest_nonspanning": 4,
            "cyclic_spanning": 1,
            "cyclic_nonspanning": 0,
        },
    )


def test_unsigned_negative_control():
    tree = ((0, 2), (1, 2))

    oriented = oriented_incidence(
        VERTICES,
        tree,
        [1, 1],
    )

    unsigned = unsigned_incidence(
        VERTICES,
        tree,
    )

    assert rank(oriented) == 2
    assert rank(unsigned) == 2

    # Equal rank is deliberately insufficient.
    assert oriented != unsigned


def test_two_edge_case_is_spanning():
    tree = ((0, 1), (1, 2))

    assert is_forest(VERTICES, tree)
    assert is_spanning(VERTICES, tree)

    # This is the corrected AQ-S14 control:
    # a two-edge forest on K3 is spanning.


def test_triangle_is_not_forest():
    triangle = EDGES

    assert not is_forest(VERTICES, triangle)
    assert is_spanning(VERTICES, triangle)


def test_semantic_mutation_partition():
    partition_a = (
        frozenset({0, 1}),
        frozenset({2}),
    )

    partition_b = (
        frozenset({0}),
        frozenset({1, 2}),
    )

    assert partition_a != partition_b


def test_semantic_mutation_graph():
    graph_a = normalize_edges(
        ((0, 1), (0, 2))
    )

    graph_b = normalize_edges(
        ((0, 1), (1, 2))
    )

    assert graph_a != graph_b

    # Both are connected and have two edges.
    assert component_count(VERTICES, graph_a) == 1
    assert component_count(VERTICES, graph_b) == 1


def main():
    trees = test_spanning_trees()
    test_all_orientations(trees)
    test_all_edge_subsets()
    test_unsigned_negative_control()
    test_two_edge_case_is_spanning()
    test_triangle_is_not_forest()
    test_semantic_mutation_partition()
    test_semantic_mutation_graph()

    print("AQ-S14-001 PASS: K3 spanning-tree enumeration = 3")
    print("AQ-S14-002 PASS: oriented incidence = 12/12")
    print("AQ-S14-003 PASS: all 8 edge subsets classified")
    print("AQ-S14-004 PASS: unsigned incidence rejected semantically")
    print("AQ-S14-005 PASS: two-edge K3 forest classified as spanning")
    print("AQ-S14-006 PASS: triangle classified as cyclic, not forest")
    print("AQ-S14-007 PASS: graph mutation detected despite equal coarse invariants")
    print("AQ-S14 SEMANTIC SUITE PASS")

    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except AssertionError as exc:
        print(f"AQ-S14 FAIL: {exc}", file=sys.stderr)
        raise SystemExit(1)
