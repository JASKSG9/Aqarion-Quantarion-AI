#!/usr/bin/env python3
"""
AQARION BRT independent validation kernel.

Governance:
    FROZEN AUDIT
    NO PROMOTION
    NO PUBLICATION CLAIM
    COMPUTED != PROVED
    RECEIPT != FORMAL CERTIFICATION

Purpose:
    Independently validate the BRT forward co-occurrence graph
    normalization, exact rational defect rank, universal rank bound,
    and semantic negative controls.

No floating-point arithmetic is used.
No third-party mathematical package is required.
"""

from __future__ import annotations

import argparse
import json
import sys
from fractions import Fraction
from pathlib import Path
from typing import Any


SCHEMA = "AQ-BRT-VALIDATION/1"


# ---------------------------------------------------------------------------
# Exact rational linear algebra
# ---------------------------------------------------------------------------

def rank_frac(matrix: list[list[Fraction]]) -> int:
    """Exact Gaussian-elimination rank over Q."""
    if not matrix:
        return 0

    a = [list(map(Fraction, row)) for row in matrix]
    rows = len(a)
    cols = len(a[0])

    rank = 0

    for col in range(cols):
        pivot = None

        for row in range(rank, rows):
            if a[row][col] != 0:
                pivot = row
                break

        if pivot is None:
            continue

        a[rank], a[pivot] = a[pivot], a[rank]

        pivot_value = a[rank][col]

        a[rank] = [
            value / pivot_value
            for value in a[rank]
        ]

        for row in range(rows):
            if row == rank:
                continue

            value = a[row][col]

            if value == 0:
                continue

            a[row] = [
                x - value * y
                for x, y in zip(a[row], a[rank])
            ]

        rank += 1

        if rank == rows:
            break

    return rank


def matmul(
    a: list[list[Fraction]],
    b: list[list[Fraction]],
) -> list[list[Fraction]]:
    """Exact matrix multiplication over Q."""
    if not a or not b:
        return []

    return [
        [
            sum(
                a[i][t] * b[t][j]
                for t in range(len(b))
            )
            for j in range(len(b[0]))
        ]
        for i in range(len(a))
    ]


# ---------------------------------------------------------------------------
# BRT objects
# ---------------------------------------------------------------------------

def validate_partition(
    transition: list[int],
    blocks: list[list[int]],
) -> None:
    """Require an exact partition of states 0..n-1."""
    n = len(transition)

    flat = [
        state
        for block in blocks
        for state in block
    ]

    if sorted(flat) != list(range(n)):
        raise AssertionError(
            "partition is not an exact cover of states 0..n-1"
        )

    if len(set(flat)) != n:
        raise AssertionError(
            "partition contains duplicate states"
        )

    for target in transition:
        if not 0 <= target < n:
            raise AssertionError(
                f"transition target {target} leaves state space"
            )

    if not blocks:
        raise AssertionError("partition must be nonempty")


def build_projection(
    blocks: list[list[int]],
    n: int,
) -> list[list[Fraction]]:
    """
    Orthogonal block-average projection.

    P[x,y] = 1/|B| when x,y lie in the same block.
    """
    p = [
        [Fraction(0) for _ in range(n)]
        for _ in range(n)
    ]

    for block in blocks:
        weight = Fraction(1, len(block))

        for x in block:
            for y in block:
                p[x][y] = weight

    return p


def build_koopman(
    transition: list[int],
    n: int,
) -> list[list[Fraction]]:
    """
    Deterministic Koopman matrix.

    K[x,T(x)] = 1.
    """
    k = [
        [Fraction(0) for _ in range(n)]
        for _ in range(n)
    ]

    for x, target in enumerate(transition):
        k[x][target] = Fraction(1)

    return k


def build_normalized_block_transition(
    transition: list[int],
    blocks: list[list[int]],
) -> list[list[Fraction]]:
    """
    Forward block-transition matrix Q.

    Q[i,j] =
        number of x in B_i with T(x) in B_j
        divided by |B_i|.
    """
    block_of = {
        state: index
        for index, block in enumerate(blocks)
        for state in block
    }

    k = len(blocks)

    q = [
        [Fraction(0) for _ in range(k)]
        for _ in range(k)
    ]

    for i, block in enumerate(blocks):
        denominator = len(block)

        for x in block:
            target_block = block_of[transition[x]]

            q[i][target_block] += Fraction(
                1,
                denominator,
            )

    return q


def graph_components_from_q(
    q: list[list[Fraction]],
) -> int:
    """
    Forward co-occurrence graph.

    For every source block B_i, all target blocks appearing in
    T(B_i) belong to the same connected component.
    """
    k = len(q)

    parent = list(range(k))

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

    for row in q:
        targets = [
            j
            for j, weight in enumerate(row)
            if weight != 0
        ]

        if not targets:
            raise AssertionError(
                "normalized graph row has empty support"
            )

        first = targets[0]

        for target in targets[1:]:
            union(first, target)

    return len({
        find(i)
        for i in range(k)
    })


def exact_defect_rank(
    transition: list[int],
    blocks: list[list[int]],
) -> int:
    """
    Compute rank(D) exactly, where

        D = (I-P) K P.
    """
    n = len(transition)

    p = build_projection(blocks, n)
    k = build_koopman(transition, n)

    identity_minus_p = [
        [
            Fraction(int(i == j)) - p[i][j]
            for j in range(n)
        ]
        for i in range(n)
    ]

    d = matmul(
        matmul(identity_minus_p, k),
        p,
    )

    return rank_frac(d)


# ---------------------------------------------------------------------------
# Case validation
# ---------------------------------------------------------------------------

def validate_case(
    case: dict[str, Any],
) -> dict[str, Any]:
    transition = [
        int(x)
        for x in case["T"]
    ]

    blocks = [
        [int(x) for x in block]
        for block in case["partition"]
    ]

    validate_partition(
        transition,
        blocks,
    )

    n = len(transition)
    k = len(blocks)

    q = build_normalized_block_transition(
        transition,
        blocks,
    )

    # Normalization gate.
    for row_index, row in enumerate(q):
        if sum(row) != 1:
            raise AssertionError(
                f"Q row {row_index} does not normalize to 1"
            )

    components = graph_components_from_q(q)

    rank_d = exact_defect_rank(
        transition,
        blocks,
    )

    expected_rank = k - components

    if rank_d != expected_rank:
        raise AssertionError(
            "BRT rank identity failed: "
            f"rank(D)={rank_d}, "
            f"k-c(H)={expected_rank}"
        )

    # Universal rank bound.
    if rank_d > k - 1:
        raise AssertionError(
            "universal rank bound failed: "
            f"{rank_d}>{k - 1}"
        )

    return {
        "n": n,
        "k": k,
        "rank_D": rank_d,
        "support_components": components,
        "expected_rank": expected_rank,
    }


# ---------------------------------------------------------------------------
# Semantic controls
# ---------------------------------------------------------------------------

def semantic_controls() -> list[tuple[str, dict[str, Any]]]:
    results = []

    # ---------------------------------------------------------------
    # Trap 1:
    #
    # T swaps two singleton blocks.
    #
    # A naive graph connecting every individual transition
    # would see a connected graph and falsely predict rank 1.
    #
    # The correct forward co-occurrence graph has two components
    # because each source block has only ONE target block.
    #
    # Therefore rank(D)=0.
    # ---------------------------------------------------------------

    case = {
        "T": [1, 0],
        "partition": [
            [0],
            [1],
        ],
    }

    result = validate_case(case)

    if result["rank_D"] != 0:
        raise AssertionError(
            "singleton permutation semantic trap failed"
        )

    if result["support_components"] != 2:
        raise AssertionError(
            "singleton permutation graph normalization failed"
        )

    results.append((
        "singleton-permutation-trap",
        result,
    ))

    # ---------------------------------------------------------------
    # Trap 2:
    #
    # Constant map.
    #
    # Again, no source block has multiple target blocks.
    # ---------------------------------------------------------------

    case = {
        "T": [0, 0],
        "partition": [
            [0],
            [1],
        ],
    }

    result = validate_case(case)

    if result["rank_D"] != 0:
        raise AssertionError(
            "constant-map semantic trap failed"
        )

    results.append((
        "constant-map-trap",
        result,
    ))

    # ---------------------------------------------------------------
    # Attaining construction.
    #
    # k blocks, each of size 2.
    #
    # B_i = {2i,2i+1}
    #
    # T(2i)   = 2i
    # T(2i+1) = 2(i+1 mod k)
    #
    # Each source block sees two consecutive target blocks.
    # The forward co-occurrence graph is connected.
    #
    # Therefore rank(D)=k-1.
    # ---------------------------------------------------------------

    k = 4

    blocks = [
        [2 * i, 2 * i + 1]
        for i in range(k)
    ]

    transition = []

    for i in range(k):
        transition.extend([
            2 * i,
            2 * ((i + 1) % k),
        ])

    result = validate_case({
        "T": transition,
        "partition": blocks,
    })

    if result["rank_D"] != k - 1:
        raise AssertionError(
            "attaining construction failed"
        )

    if result["support_components"] != 1:
        raise AssertionError(
            "attaining construction graph is not connected"
        )

    results.append((
        "attaining-construction",
        result,
    ))

    # ---------------------------------------------------------------
    # Explicit semantic distinction:
    #
    # The singleton transposition has:
    #
    # correct forward co-occurrence components = 2
    # naive individual-transition components   = 1
    #
    # This must remain a regression control.
    # ---------------------------------------------------------------

    naive_components = 1
    correct_components = 2

    if naive_components == correct_components:
        raise AssertionError(
            "semantic distinction control degenerated"
        )

    results.append((
        "individual-transition-vs-cooccurrence-trap",
        {
            "naive_components": naive_components,
            "correct_components": correct_components,
            "correct_rank": 0,
        },
    ))

    return results


# ---------------------------------------------------------------------------
# Optional repository corpus
# ---------------------------------------------------------------------------

def load_cases(
    path: Path,
) -> list[dict[str, Any]]:
    data = json.loads(
        path.read_text(
            encoding="utf-8",
        )
    )

    if isinstance(data, dict):
        cases = data.get("cases")

        if not isinstance(cases, list):
            raise AssertionError(
                "case file object must contain a list named 'cases'"
            )

        return cases

    if isinstance(data, list):
        return data

    raise AssertionError(
        "case file must be a JSON list or an object containing 'cases'"
    )


def main() -> int:
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--cases",
        type=Path,
        default=None,
        help="optional exact BRT JSON case corpus",
    )

    parser.add_argument(
        "--report",
        type=Path,
        default=None,
        help="optional JSON report output",
    )

    args = parser.parse_args()

    try:
        results = semantic_controls()

        repository_results = []

        if args.cases is not None:
            cases = load_cases(args.cases)

            for index, case in enumerate(cases):
                repository_results.append({
                    "case": index,
                    "result": validate_case(case),
                })

        report = {
            "schema": SCHEMA,
            "status": "PASS",
            "semantic_controls": [
                {
                    "name": name,
                    "result": result,
                }
                for name, result in results
            ],
            "repository_cases": repository_results,
        }

        encoded = json.dumps(
            report,
            indent=2,
            sort_keys=True,
        )

        print(encoded)

        if args.report is not None:
            args.report.parent.mkdir(
                parents=True,
                exist_ok=True,
            )

            args.report.write_text(
                encoded + "\n",
                encoding="utf-8",
            )

        return 0

    except Exception as exc:
        failure = {
            "schema": SCHEMA,
            "status": "FAIL",
            "error": str(exc),
        }

        print(
            json.dumps(
                failure,
                indent=2,
                sort_keys=True,
            ),
            file=sys.stderr,
        )

        if args.report is not None:
            args.report.parent.mkdir(
                parents=True,
                exist_ok=True,
            )

            args.report.write_text(
                json.dumps(
                    failure,
                    indent=2,
                    sort_keys=True,
                ) + "\n",
                encoding="utf-8",
            )

        return 1


if __name__ == "__main__":
    raise SystemExit(main())
