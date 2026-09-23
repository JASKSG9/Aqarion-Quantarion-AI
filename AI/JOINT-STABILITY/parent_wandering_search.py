from __future__ import annotations

import argparse
import json
import random
import time

SEED = 22092026


def canon(labels):
    out = []
    names = {}

    for x in labels:
        if x not in names:
            names[x] = len(names)
        out.append(names[x])

    return tuple(out)


def random_partition(n, rng):
    return tuple(rng.randrange(n) for _ in range(n))


def is_pullback_stable(P, T):
    """
    Exact condition:

        T^{-1}(P) <= P

    Equivalently, whenever T(x) and T(y) lie in the same
    P-class, x and y must already lie in the same P-class.
    """
    parents = {}

    for x, tx in enumerate(T):
        parents.setdefault(P[tx], set()).add(P[x])

    return all(len(source_classes) == 1
               for source_classes in parents.values())


def stable_closure(P, T):
    """
    Compute the least coarsening obtained by repeatedly enforcing

        T^{-1}(P) <= P.

    This is used only to generate stable test partitions.
    """
    P = list(P)
    n = len(T)

    while True:
        merge = None

        for x in range(n):
            for y in range(x):
                if P[T[x]] == P[T[y]] and P[x] != P[y]:
                    merge = (P[x], P[y])
                    break

            if merge is not None:
                break

        if merge is None:
            return canon(P)

        a, b = merge

        for i in range(n):
            if P[i] == b:
                P[i] = a


def join(P, Q):
    """
    Exact equivalence-relation join.

    The join is the transitive closure of the union of P and Q.
    """
    n = len(P)
    parent = list(range(n))

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def union(a, b):
        a = find(a)
        b = find(b)

        if a != b:
            parent[b] = a

    for i in range(n):
        for j in range(i):
            if P[i] == P[j] or Q[i] == Q[j]:
                union(i, j)

    labels = {}

    return tuple(
        labels.setdefault(find(i), len(labels))
        for i in range(n)
    )


def range_gap_witness(T, E, F):
    """
    Find the necessary obstruction from Lemma E.

    Let G = E join F.

    For each G-component, restrict G to im(T).
    If the range points belonging to that G-component split into
    multiple connected components, a range-gap exists.

    Such a range-gap is necessary for an actual join-stability
    counterexample, but is not itself a counterexample.
    """
    n = len(T)
    image = set(T)
    G = join(E, F)

    adjacency = {
        vertex: set()
        for vertex in image
    }

    for i in image:
        for j in image:
            if i < j and (E[i] == E[j] or F[i] == F[j]):
                adjacency[i].add(j)
                adjacency[j].add(i)

    witnesses = []

    for g_class in sorted(set(G)):
        vertices = [
            v for v in image
            if G[v] == g_class
        ]

        seen = set()
        components = []

        for v in vertices:
            if v in seen:
                continue

            stack = [v]
            seen.add(v)
            component = []

            while stack:
                u = stack.pop()
                component.append(u)

                for w in adjacency[u]:
                    if w in vertices and w not in seen:
                        seen.add(w)
                        stack.append(w)

            components.append(sorted(component))

        if len(components) > 1:
            witnesses.append(
                {
                    "g_class": g_class,
                    "range_components": components,
                }
            )

    return witnesses


def search(n, maps, seeds_per_map, seed=SEED):
    rng = random.Random(seed)

    total_pairs = 0
    range_gap_pairs = 0
    max_stable_partitions = 0

    started = time.time()

    for map_index in range(maps):
        T = tuple(
            rng.randrange(n)
            for _ in range(n)
        )

        stable_partitions = {(0,) * n}

        for _ in range(seeds_per_map):
            P = random_partition(n, rng)
            stable_partitions.add(
                stable_closure(P, T)
            )

        stable_partitions = list(stable_partitions)

        max_stable_partitions = max(
            max_stable_partitions,
            len(stable_partitions),
        )

        for i, E in enumerate(stable_partitions):
            for F in stable_partitions[i:]:
                total_pairs += 1

                witnesses = range_gap_witness(
                    T,
                    E,
                    F,
                )

                if not witnesses:
                    continue

                range_gap_pairs += 1

                G = join(E, F)

                # A genuine join counterexample must also fail stability.
                if not is_pullback_stable(G, T):
                    return {
                        "status": "COUNTEREXAMPLE",
                        "n": n,
                        "seed": seed,
                        "map_index": map_index,
                        "T": T,
                        "E": E,
                        "F": F,
                        "G": G,
                        "range_gap": witnesses,
                        "stable_pair_samples": total_pairs,
                        "range_gap_candidates": range_gap_pairs,
                        "max_stable_partitions_seen":
                            max_stable_partitions,
                        "seconds":
                            round(time.time() - started, 3),
                    }

    return {
        "status": "NO_COUNTEREXAMPLE",
        "n": n,
        "maps": maps,
        "seeds_per_map": seeds_per_map,
        "seed": seed,
        "stable_pair_samples": total_pairs,
        "range_gap_candidates": range_gap_pairs,
        "max_stable_partitions_seen":
            max_stable_partitions,
        "seconds":
            round(time.time() - started, 3),
    }


def main():
    parser = argparse.ArgumentParser(
        description=(
            "AQARION join-stability range-gap "
            "obstruction census"
        )
    )

    parser.add_argument(
        "--n",
        type=int,
        required=True,
    )

    parser.add_argument(
        "--maps",
        type=int,
        required=True,
    )

    parser.add_argument(
        "--seeds-per-map",
        type=int,
        required=True,
    )

    parser.add_argument(
        "--seed",
        type=int,
        default=SEED,
    )

    args = parser.parse_args()

    result = search(
        args.n,
        args.maps,
        args.seeds_per_map,
        args.seed,
    )

    print(
        json.dumps(
            result,
            indent=2,
            sort_keys=True,
        )
    )

    return (
        0
        if result["status"] == "NO_COUNTEREXAMPLE"
        else 1
    )


if __name__ == "__main__":
    raise SystemExit(main())
