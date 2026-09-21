#!/usr/bin/env python3
"""
AQ-CYCLE-DELTA-BRT pair-merge exact verifier.

Convention:
  X = Z/kZ
  T(i) = i + 1 mod k
  K[i, T(i)] = 1, hence (Kf)(i) = f(T(i))
  Pi_(0,d) = {{0,d}} plus singleton blocks
  P = uniform block-average projection
  D = (I-P)KP

Finite verification domain:
  3 <= k <= 16
  1 <= d < k

Governance:
  Exact finite arithmetic only.
  Lean: OPEN.
  C4: BLOCKED.
  Promotion: FALSE.
"""

from collections import Counter
from fractions import Fraction as F
from itertools import combinations
from math import gcd
import sys


def eye(n):
    return [[F(int(i == j)) for j in range(n)] for i in range(n)]


def mat_mul(left, right):
    rows = len(left)
    inner = len(right)
    cols = len(right[0])

    result = [[F(0) for _ in range(cols)] for _ in range(rows)]

    for i in range(rows):
        for t in range(inner):
            coefficient = left[i][t]
            if coefficient == 0:
                continue
            for j in range(cols):
                if right[t][j] != 0:
                    result[i][j] += coefficient * right[t][j]

    return result


def mat_sub(left, right):
    return [
        [left[i][j] - right[i][j] for j in range(len(left[0]))]
        for i in range(len(left))
    ]


def is_zero(matrix):
    return all(value == 0 for row in matrix for value in row)


def build_K(k):
    matrix = [[F(0) for _ in range(k)] for _ in range(k)]

    for i in range(k):
        matrix[i][(i + 1) % k] = F(1)

    return matrix


def build_P(k, d):
    pair_block = {0, d % k}
    matrix = [[F(0) for _ in range(k)] for _ in range(k)]

    for i in range(k):
        if i in pair_block:
            for j in pair_block:
                matrix[i][j] = F(1, 2)
        else:
            matrix[i][i] = F(1)

    return matrix


def defect_D(k, d):
    projection = build_P(k, d)
    return mat_mul(
        mat_sub(eye(k), projection),
        mat_mul(build_K(k), projection),
    )


def lag(D, k):
    if is_zero(D):
        return 0

    K = build_K(k)
    K_power = eye(k)

    for exponent in range(1, 3 * k + 2):
        K_power = mat_mul(K_power, K)

        if is_zero(mat_mul(mat_mul(D, K_power), D)):
            return exponent

    return None


def rank_exact(matrix):
    work = [row[:] for row in matrix]
    rows = len(work)
    cols = len(work[0])
    rank = 0
    pivot_row = 0

    for pivot_col in range(cols):
        candidate = next(
            (
                row
                for row in range(pivot_row, rows)
                if work[row][pivot_col] != 0
            ),
            None,
        )

        if candidate is None:
            continue

        work[pivot_row], work[candidate] = (
            work[candidate],
            work[pivot_row],
        )

        pivot = work[pivot_row][pivot_col]

        for col in range(pivot_col, cols):
            work[pivot_row][col] /= pivot

        for row in range(rows):
            if row == pivot_row:
                continue

            scale = work[row][pivot_col]

            if scale == 0:
                continue

            for col in range(pivot_col, cols):
                work[row][col] -= scale * work[pivot_row][col]

        rank += 1
        pivot_row += 1

        if pivot_row == rows:
            break

    return rank


def d_generic(k, d):
    matrix = [[F(0) for _ in range(k)] for _ in range(k)]

    for i in range(k):
        u_i = F(1 if i == 0 else (-1 if i == d else 0))

        for j in range(k):
            w_j = F(
                1 if j == 1 else (
                    -1 if j == (d + 1) % k else 0
                )
            )
            matrix[i][j] = F(1, 2) * u_i * w_j

    return matrix


def d_adjacent_left(k):
    matrix = [[F(0) for _ in range(k)] for _ in range(k)]

    for i in range(k):
        u_i = F(1 if i == 0 else (-1 if i == 1 else 0))

        for j in range(k):
            w_j = F(
                1 if j == 0 else (
                    1 if j == 1 else (
                        -2 if j == 2 else 0
                    )
                )
            )
            matrix[i][j] = F(1, 4) * u_i * w_j

    return matrix


def d_adjacent_wrap(k):
    matrix = [[F(0) for _ in range(k)] for _ in range(k)]

    for i in range(k):
        u_i = F(-1 if i == 0 else (1 if i == k - 1 else 0))

        for j in range(k):
            w_j = F(
                1 if j == 0 else (
                    -2 if j == 1 else (
                        1 if j == k - 1 else 0
                    )
                )
            )
            matrix[i][j] = F(1, 4) * u_i * w_j

    return matrix


def erroneous_old_wrap_factor(k):
    matrix = [[F(0) for _ in range(k)] for _ in range(k)]

    for i in range(k):
        u_i = F(-1 if i == 0 else (1 if i == k - 1 else 0))

        for j in range(k):
            w_j = F(
                1 if j == 0 else (
                    -2 if j == 1 else (
                        1 if j == k - 2 else 0
                    )
                )
            )
            matrix[i][j] = F(1, 4) * u_i * w_j

    return matrix


def expected_lag(k, d):
    if k == 3:
        return 3

    if k == 4:
        return 4 if d in (1, 3) else 2

    if k == 5:
        return 3 if d in (2, 3) else 2

    if d in (1, 2, k - 2, k - 1):
        return 2

    return 1


def partition_blocks(k, d):
    pair = frozenset((0, d % k))
    blocks = [pair]

    for i in range(k):
        if i not in pair:
            blocks.append(frozenset((i,)))

    return blocks


def gamma_components(k, d):
    blocks = partition_blocks(k, d)
    block_count = len(blocks)
    label = {}

    for block_index, block in enumerate(blocks):
        for state in block:
            label[state] = block_index

    parent = list(range(block_count))

    def find(vertex):
        while parent[vertex] != vertex:
            parent[vertex] = parent[parent[vertex]]
            vertex = parent[vertex]
        return vertex

    def union(left, right):
        left_root = find(left)
        right_root = find(right)

        if left_root != right_root:
            parent[right_root] = left_root

    for source_block in blocks:
        target_labels = sorted(
            {
                label[(state + 1) % k]
                for state in source_block
            }
        )

        for left, right in combinations(target_labels, 2):
            union(left, right)

    component_count = len({find(vertex) for vertex in range(block_count)})
    return component_count, block_count


def same_matrix(left, right):
    return all(
        left[i][j] == right[i][j]
        for i in range(len(left))
        for j in range(len(left[0]))
    )


def main():
    total_cases = 0
    direct_factorization_cases = 0
    factorization_matches = 0
    lag_matches = 0
    brt_matches = 0
    wrap_regression_matches = 0

    lag_distribution = Counter()
    rank_distribution = Counter()
    graph_rank_distribution = Counter()
    failures = []

    for k in range(3, 17):
        for d in range(1, k):
            total_cases += 1

            direct = defect_D(k, d)
            actual_lag = lag(direct, k)
            actual_rank = rank_exact(direct)

            lag_distribution[actual_lag] += 1
            rank_distribution[actual_rank] += 1

            expected = expected_lag(k, d)

            if actual_lag == expected:
                lag_matches += 1
            else:
                failures.append(
                    ("lag", k, d, actual_lag, expected)
                )

            expected_factor = None

            if k >= 5 and d == 1:
                expected_factor = d_adjacent_left(k)
            elif k >= 5 and d == k - 1:
                expected_factor = d_adjacent_wrap(k)
            elif 2 <= d <= k - 2:
                expected_factor = d_generic(k, d)

            if expected_factor is not None:
                direct_factorization_cases += 1

                if same_matrix(direct, expected_factor):
                    factorization_matches += 1
                else:
                    failures.append(("factorization", k, d))

            if k >= 5 and d == k - 1:
                if not same_matrix(
                    direct,
                    erroneous_old_wrap_factor(k),
                ):
                    wrap_regression_matches += 1
                else:
                    failures.append(("old_wrap_mutant_survived", k, d))

            components, block_count = gamma_components(k, d)
            predicted_rank = block_count - components
            graph_rank_distribution[predicted_rank] += 1

            if actual_rank == predicted_rank:
                brt_matches += 1
            else:
                failures.append(
                    (
                        "brt",
                        k,
                        d,
                        actual_rank,
                        predicted_rank,
                        components,
                        block_count,
                    )
                )

    expected_total = 119
    expected_lag_distribution = {1: 66, 2: 47, 3: 4, 4: 2}
    expected_rank_distribution = {1: 119}
    expected_graph_rank_distribution = {1: 119}
    expected_factorization_cases = 115
    expected_wrap_regression_cases = 12

    assert total_cases == expected_total
    assert direct_factorization_cases == expected_factorization_cases
    assert factorization_matches == expected_factorization_cases
    assert lag_matches == expected_total
    assert brt_matches == expected_total
    assert dict(sorted(lag_distribution.items())) == expected_lag_distribution
    assert dict(sorted(rank_distribution.items())) == expected_rank_distribution
    assert (
        dict(sorted(graph_rank_distribution.items()))
        == expected_graph_rank_distribution
    )
    assert wrap_regression_matches == expected_wrap_regression_cases
    assert not failures

    print("AQ-CYCLE-DELTA-BRT: PASS")
    print("DOMAIN: k=3..16, d=1..k-1")
    print("ARITHMETIC: exact Fraction")
    print(f"CASES: {total_cases}")
    print(
        "APPLICABLE_FACTORIZATION_CASES: "
        f"{factorization_matches}/{direct_factorization_cases}"
    )
    print(f"LAG_TABLE: {lag_matches}/{total_cases}")
    print(f"BRT_RANK: {brt_matches}/{total_cases}")
    print(f"LAG_DISTRIBUTION: {dict(sorted(lag_distribution.items()))}")
    print(f"RANK_DISTRIBUTION: {dict(sorted(rank_distribution.items()))}")
    print(
        "GRAPH_RANK_DISTRIBUTION: "
        f"{dict(sorted(graph_rank_distribution.items()))}"
    )
    print(
        "WRAP_MUTANT_REJECTED: "
        f"{wrap_regression_matches}/{expected_wrap_regression_cases}"
    )
    print("PROMOTION: FALSE")
    print("C4: BLOCKED")
    return 0


if __name__ == "__main__":
    sys.exit(main())
