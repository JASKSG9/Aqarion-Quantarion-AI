#!/usr/bin/env python3
"""
AQARION-GAP lattice join simulator.

Computes the join P ∨ Q of two partitions of a finite set.

Convention:
  P ∨ Q is the coarsest partition coarser than both P and Q.
  Equivalently, it is the connected-component partition of the graph
  whose edges connect points that lie together in a block of P or Q.

No third-party dependencies required.

Examples:
  python3 lattice_join_simulator.py demo
  python3 lattice_join_simulator.py join "0,1|2,3|4" "0|1,2|3,4"
  python3 lattice_join_simulator.py benchmark
"""

from __future__ import annotations

import argparse
import random
import time
from dataclasses import dataclass
from typing import Iterable


Block = tuple[int, ...]
Partition = tuple[Block, ...]


@dataclass
class UnionStep:
    source: str
    anchor: int
    element: int
    merged: bool
    components_after: tuple[Block, ...]


class DisjointSetUnion:
    """Union-Find with path compression and union by size."""

    def __init__(self, n: int) -> None:
        self.parent = list(range(n))
        self.size = [1] * n
        self.component_count = n

    def find(self, x: int) -> int:
        while self.parent[x] != x:
            self.parent[x] = self.parent[self.parent[x]]
            x = self.parent[x]
        return x

    def union(self, a: int, b: int) -> bool:
        root_a = self.find(a)
        root_b = self.find(b)

        if root_a == root_b:
            return False

        if self.size[root_a] < self.size[root_b]:
            root_a, root_b = root_b, root_a

        self.parent[root_b] = root_a
        self.size[root_a] += self.size[root_b]
        self.component_count -= 1
        return True

    def components(self) -> Partition:
        groups: dict[int, list[int]] = {}

        for x in range(len(self.parent)):
            root = self.find(x)
            groups.setdefault(root, []).append(x)

        return canonical_partition(groups.values())


def canonical_partition(blocks: Iterable[Iterable[int]]) -> Partition:
    normalized = [tuple(sorted(block)) for block in blocks]
    return tuple(sorted(normalized, key=lambda block: (block[0], len(block), block)))


def format_partition(partition: Partition) -> str:
    return " | ".join("{" + ",".join(str(x) for x in block) + "}" for block in partition)


def validate_partition(partition: Partition, n: int, label: str) -> None:
    seen: set[int] = set()

    for block in partition:
        if not block:
            raise ValueError(f"{label} contains an empty block.")

        for x in block:
            if not isinstance(x, int):
                raise ValueError(f"{label} contains non-integer element: {x!r}.")

            if x < 0 or x >= n:
                raise ValueError(
                    f"{label} contains {x}, outside the declared universe 0..{n - 1}."
                )

            if x in seen:
                raise ValueError(f"{label} contains {x} in more than one block.")

            seen.add(x)

    expected = set(range(n))
    if seen != expected:
        missing = sorted(expected - seen)
        extra = sorted(seen - expected)
        raise ValueError(
            f"{label} must partition 0..{n - 1}; missing={missing}, extra={extra}."
        )


def parse_partition(text: str) -> Partition:
    """
    Parse:
      0,1|2,3|4

    into:
      ((0,1),(2,3),(4,))
    """
    if not text.strip():
        raise ValueError("Partition text is empty.")

    blocks: list[Block] = []

    for raw_block in text.split("|"):
        raw_block = raw_block.strip()

        if not raw_block:
            raise ValueError("Empty block syntax found. Use forms such as 0,1|2|3,4.")

        entries = [entry.strip() for entry in raw_block.split(",")]

        if any(not entry for entry in entries):
            raise ValueError("Empty element syntax found in a block.")

        blocks.append(tuple(int(entry) for entry in entries))

    return canonical_partition(blocks)


def join_partitions(
    left: Partition,
    right: Partition,
    n: int,
    record_steps: bool = False,
) -> tuple[Partition, list[UnionStep]]:
    """
    Compute P ∨ Q by DSU.

    Each block contributes edges from its first member to every remaining
    member. The resulting DSU components are the transitive closure of the
    union of P- and Q-block relations.
    """
    validate_partition(left, n, "Left partition")
    validate_partition(right, n, "Right partition")

    dsu = DisjointSetUnion(n)
    steps: list[UnionStep] = []

    for source, partition in (("P", left), ("Q", right)):
        for block in partition:
            anchor = block[0]

            for element in block[1:]:
                merged = dsu.union(anchor, element)

                if record_steps:
                    steps.append(
                        UnionStep(
                            source=source,
                            anchor=anchor,
                            element=element,
                            merged=merged,
                            components_after=dsu.components(),
                        )
                    )

    return dsu.components(), steps


def print_closure_trace(
    left: Partition,
    right: Partition,
    n: int,
) -> Partition:
    result, steps = join_partitions(left, right, n, record_steps=True)

    print("=== INPUT PARTITIONS ===")
    print(f"Universe: {{0,...,{n - 1}}}")
    print(f"P = {format_partition(left)}")
    print(f"Q = {format_partition(right)}")
    print()

    print("=== RELATION UNION / DSU CLOSURE STEPS ===")
    print("Start components:")
    print(format_partition(tuple((x,) for x in range(n))))
    print()

    for index, step in enumerate(steps, start=1):
        relation = f"{step.anchor} ~ {step.element}"

        if step.merged:
            action = "MERGED"
        else:
            action = "ALREADY CONNECTED"

        print(
            f"Step {index:02d}: [{step.source}] add relation {relation:<8} "
            f"-> {action}"
        )
        print(f"          components: {format_partition(step.components_after)}")

    print()
    print("=== FINAL JOIN ===")
    print(f"P ∨ Q = {format_partition(result)}")
    print(f"Block count: {len(result)}")

    return result


def graph_edges(partition: Partition) -> list[tuple[int, int]]:
    """
    Produce a sparse spanning-edge representation of a partition relation.

    For each block (b0,b1,...), emit (b0,b1), (b0,b2), ...
    This is enough to generate the same connected components as a clique.
    """
    edges: list[tuple[int, int]] = []

    for block in partition:
        anchor = block[0]
        edges.extend((anchor, element) for element in block[1:])

    return edges


def print_graph_view(left: Partition, right: Partition) -> None:
    print("=== SPARSE RELATION GRAPH ===")
    print(f"P edges: {graph_edges(left)}")
    print(f"Q edges: {graph_edges(right)}")
    print(
        "The join is the connected-component partition of the graph "
        "formed by the union of these edges."
    )


def random_partition(n: int, rng: random.Random) -> Partition:
    """
    Generate a random partition by assigning each next element to a
    current block or a new block.
    """
    if n <= 0:
        raise ValueError("n must be positive.")

    blocks: list[list[int]] = [[0]]

    for x in range(1, n):
        target = rng.randrange(len(blocks) + 1)

        if target == len(blocks):
            blocks.append([x])
        else:
            blocks[target].append(x)

    return canonical_partition(blocks)


def benchmark_join(
    n: int,
    trials: int,
    seed: int,
) -> dict[str, float | int]:
    rng = random.Random(seed + n)
    elapsed_values: list[float] = []
    edge_counts: list[int] = []

    for _ in range(trials):
        left = random_partition(n, rng)
        right = random_partition(n, rng)

        edge_count = len(graph_edges(left)) + len(graph_edges(right))
        edge_counts.append(edge_count)

        start = time.perf_counter()
        join_partitions(left, right, n, record_steps=False)
        elapsed_values.append(time.perf_counter() - start)

    return {
        "n": n,
        "trials": trials,
        "mean_seconds": sum(elapsed_values) / trials,
        "min_seconds": min(elapsed_values),
        "max_seconds": max(elapsed_values),
        "mean_sparse_relation_edges": sum(edge_counts) / trials,
    }


def run_benchmark() -> None:
    print("=== DSU JOIN COMPLEXITY BENCHMARK ===")
    print(
        "Theoretical cost for one join: "
        "O(E α(n)), where E is the number of sparse relation edges and "
        "α is the inverse-Ackermann function."
    )
    print(
        "For two partitions of n points, the sparse representation uses "
        "at most 2(n-1) union attempts."
    )
    print()

    plan = [
        (10, 2000),
        (100, 500),
        (1000, 100),
    ]

    print(
        f"{'n':>6} {'trials':>8} {'mean ms':>12} "
        f"{'min ms':>12} {'max ms':>12} {'mean edges':>14}"
    )
    print("-" * 72)

    for n, trials in plan:
        result = benchmark_join(n=n, trials=trials, seed=20260919)

        print(
            f"{result['n']:>6} "
            f"{result['trials']:>8} "
            f"{1000 * result['mean_seconds']:>12.4f} "
            f"{1000 * result['min_seconds']:>12.4f} "
            f"{1000 * result['max_seconds']:>12.4f} "
            f"{result['mean_sparse_relation_edges']:>14.1f}"
        )

    print()
    print(
        "Timing is device-, Python-version-, thermal-state-, and "
        "background-load-dependent. Treat it as a local performance receipt, "
        "not a universal benchmark."
    )


def demo() -> None:
    """
    Example chosen to show transitive closure:

      P = {0,1} | {2,3} | {4} | {5}
      Q = {0} | {1,2} | {3,4} | {5}

    P links 0~1 and 2~3.
    Q links 1~2 and 3~4.
    Together, transitive closure yields {0,1,2,3,4} | {5}.
    """
    n = 6
    left = parse_partition("0,1|2,3|4|5")
    right = parse_partition("0|1,2|3,4|5")

    print_graph_view(left, right)
    print()
    print_closure_trace(left, right, n)


def determine_n(left: Partition, right: Partition) -> int:
    values = [x for block in left + right for x in block]

    if not values:
        raise ValueError("Partitions contain no elements.")

    return max(values) + 1


def main() -> int:
    parser = argparse.ArgumentParser(
        description="AQARION partition-lattice join simulator."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser(
        "demo",
        help="Run a transitive-closure demonstration.",
    )

    join_parser = subparsers.add_parser(
        "join",
        help="Compute a join from partition strings.",
    )
    join_parser.add_argument(
        "left",
        help='Left partition, such as "0,1|2,3|4".',
    )
    join_parser.add_argument(
        "right",
        help='Right partition, such as "0|1,2|3,4".',
    )
    join_parser.add_argument(
        "--n",
        type=int,
        default=None,
        help="Universe size; default is one plus the largest stated element.",
    )

    subparsers.add_parser(
        "benchmark",
        help="Benchmark DSU join operations for n=10, 100, 1000.",
    )

    args = parser.parse_args()

    if args.command == "demo":
        demo()
        return 0

    if args.command == "join":
        left = parse_partition(args.left)
        right = parse_partition(args.right)
        n = args.n if args.n is not None else determine_n(left, right)

        print_graph_view(left, right)
        print()
        print_closure_trace(left, right, n)
        return 0

    if args.command == "benchmark":
        run_benchmark()
        return 0

    raise RuntimeError(f"Unhandled command: {args.command!r}")


if __name__ == "__main__":
    raise SystemExit(main())
