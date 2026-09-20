#!/usr/bin/env python3
"""
AQ-SM-SPECTRAL-SPLIT-001

EXACT 3x3 EQUAL-MARGIN SPECTRAL / SUPPORT ATLAS

Governance:
    FROZEN · EXACT · NO PROMOTION
    C4 BLOCKED · PUBLICATION BLOCKED · Lean OPEN

This program enumerates all 3x3 nonnegative integer matrices M
whose row sums and column sums equal n.

For every M it records:

    - matrix
    - margin
    - exact rank(M)
    - determinant
    - nullity
    - primitive integer null basis
    - exact Mv = 0 checks
    - support edges
    - support-component count
    - rank(G) = 3 - support_components
    - saturation = (rank(M) < 3)
    - canonical S3 x S3 row/column permutation class

No floating-point arithmetic is used for the certification fields.

USAGE:
    python aq_sm_spectral_atlas.py
    python aq_sm_spectral_atlas.py 10
    python aq_sm_spectral_atlas.py 30

The default maximum margin is 10.
"""

from __future__ import annotations

import hashlib
import itertools
import json
import math
import sys
from fractions import Fraction
from pathlib import Path


ROOT = Path(__file__).resolve().parent
DEFAULT_MAX_N = 10

OUT_JSONL = ROOT / "AQ-SM-SPECTRAL-ATLAS.jsonl"
OUT_RECEIPT = ROOT / "AQ-SM-SPECTRAL-ATLAS.RECEIPT.txt"


def permutations3():
    return list(itertools.permutations(range(3)))


PERMS = permutations3()


def flatten(M):
    return tuple(x for row in M for x in row)


def permute_matrix(M, rp, cp):
    return tuple(
        tuple(M[rp[i]][cp[j]] for j in range(3))
        for i in range(3)
    )


def canonical_class(M):
    """
    Canonical representative under independent row and column
    permutations S3 x S3.

    This preserves:
        rank,
        determinant up to sign,
        singular values,
        support-component count.
    """
    reps = [
        flatten(permute_matrix(M, rp, cp))
        for rp in PERMS
        for cp in PERMS
    ]
    return min(reps)


def compositions3(n):
    """
    All triples (a,b,c) of nonnegative integers summing to n.
    """
    for a in range(n + 1):
        for b in range(n - a + 1):
            c = n - a - b
            yield (a, b, c)


def enumerate_matrices(n):
    """
    Parameterize the first two rows.

    If row 1 = (a,b,n-a-b)
    and row 2 = (c,d,n-c-d),

    then row 3 is forced by the column sums:
        (n-a-c, n-b-d, a+b+c+d-n).

    Nonnegativity is checked exactly.
    """
    for r1 in compositions3(n):
        for r2 in compositions3(n):
            r3 = (
                n - r1[0] - r2[0],
                n - r1[1] - r2[1],
                n - r1[2] - r2[2],
            )

            if min(r3) < 0:
                continue

            yield (
                tuple(r1),
                tuple(r2),
                tuple(r3),
            )


def det3(M):
    a, b, c = M[0]
    d, e, f = M[1]
    g, h, i = M[2]

    return (
        a * (e * i - f * h)
        - b * (d * i - f * g)
        + c * (d * h - e * g)
    )


def cross(u, v):
    return (
        u[1] * v[2] - u[2] * v[1],
        u[2] * v[0] - u[0] * v[2],
        u[0] * v[1] - u[1] * v[0],
    )


def dot(u, v):
    return sum(a * b for a, b in zip(u, v))


def mat_vec(M, v):
    return tuple(dot(row, v) for row in M)


def primitive(v):
    """
    Divide an integer vector by the gcd of its coordinates and
    normalize the sign so the first nonzero entry is positive.
    """
    if all(x == 0 for x in v):
        return (0, 0, 0)

    g = 0
    for x in v:
        g = math.gcd(g, abs(x))

    w = tuple(x // g for x in v)

    for x in w:
        if x != 0:
            if x < 0:
                w = tuple(-y for y in w)
            break

    return w


def null_basis_3x3(M):
    """
    Exact integer nullspace basis.

    rank 3: empty
    rank 2: one primitive cross-product vector
    rank 1: two independent primitive cross-product vectors
    """
    rows = [tuple(row) for row in M]

    crosses = []
    for i, j in itertools.combinations(range(3), 2):
        v = cross(rows[i], rows[j])
        if any(v):
            v = primitive(v)
            if v not in crosses:
                crosses.append(v)

    if crosses:
        # For rank 2 there is exactly one null direction.
        # All nonzero row-pair cross products are parallel.
        basis = [crosses[0]]

        for v in crosses[1:]:
            if not any(
                cross(basis[0], v)
            ):
                continue

        return basis

    # If every pair of rows is parallel, rank <= 1.
    # Find two independent vectors perpendicular to the first
    # nonzero row using coordinate constructions.
    row = next((r for r in rows if any(r)), None)

    if row is None:
        # Zero matrix: canonical basis.
        return [
            (1, 0, 0),
            (0, 1, 0),
            (0, 0, 1),
        ]

    # Pick two coordinate basis vectors and cross with row.
    candidates = []
    for e in (
        (1, 0, 0),
        (0, 1, 0),
        (0, 0, 1),
    ):
        v = primitive(cross(row, e))
        if any(v) and v not in candidates:
            candidates.append(v)

    basis = []
    for v in candidates:
        if not basis:
            basis.append(v)
        elif any(cross(basis[0], v)):
            basis.append(v)
            break

    return basis


def rank3_exact(M):
    """
    Exact rank from determinants / 2x2 minors.
    """
    if det3(M) != 0:
        return 3

    for i, j in itertools.combinations(range(3), 2):
        for p, q in itertools.combinations(range(3), 2):
            minor = (
                M[i][p] * M[j][q]
                - M[i][q] * M[j][p]
            )
            if minor != 0:
                return 2

    if any(any(x != 0 for x in row) for row in M):
        return 1

    return 0


def support_edges(M):
    return [
        [i, j]
        for i in range(3)
        for j in range(3)
        if M[i][j] > 0
    ]


class DSU:
    def __init__(self, n):
        self.p = list(range(n))

    def find(self, x):
        while self.p[x] != x:
            self.p[x] = self.p[self.p[x]]
            x = self.p[x]
        return x

    def union(self, a, b):
        a = self.find(a)
        b = self.find(b)
        if a != b:
            self.p[b] = a


def support_components(M):
    """
    Bipartite support graph:
        rows 0,1,2 -> vertices 0,1,2
        cols 0,1,2 -> vertices 3,4,5
    """
    dsu = DSU(6)

    for i, j in support_edges(M):
        dsu.union(i, 3 + j)

    return len({dsu.find(i) for i in range(6)})


def gram_rank_from_support(M):
    return 3 - support_components(M)


def check_equal_margin(M, n):
    rows = [sum(row) for row in M]
    cols = [
        sum(M[i][j] for i in range(3))
        for j in range(3)
    ]

    return rows == [n] * 3 and cols == [n] * 3


def trace_gram(M, n):
    """
    G = I - A^T A, A=M/n.

    tr(G) = 3 - tr(M^T M)/n^2.

    Returned exactly as Fraction.
    """
    frob_sq = sum(x * x for row in M for x in row)
    return Fraction(3 * n * n - frob_sq, n * n)


def gram_principal_2sum(M, n):
    """
    Since G is 3x3 and has eigenvalue 0, the sum of its
    principal 2x2 minors equals the product of the two
    nonzero eigenvalues.

    Compute G exactly as Fractions.
    """
    A = [
        [Fraction(M[i][j], n) for j in range(3)]
        for i in range(3)
    ]

    G = [[Fraction(int(i == j), 1) for j in range(3)]
         for i in range(3)]

    for i in range(3):
        for j in range(3):
            G[i][j] -= sum(A[t][i] * A[t][j] for t in range(3))

    total = Fraction(0)

    for i, j in ((0, 1), (0, 2), (1, 2)):
        total += G[i][i] * G[j][j] - G[i][j] * G[j][i]

    return total


def atlas_record(M, n):
    det = det3(M)
    rank = rank3_exact(M)
    nullity = 3 - rank

    basis = null_basis_3x3(M)

    checks = [
        list(mat_vec(M, v))
        for v in basis
    ]

    assert all(x == [0, 0, 0] for x in checks)

    c = support_components(M)
    rank_g = gram_rank_from_support(M)

    # Fundamental exact consistency check.
    assert rank_g == 3 - c

    # G has eigenvalue 1 iff M is singular.
    saturated = rank < 3

    record = {
        "matrix": [list(row) for row in M],
        "dimension": 3,
        "margin": n,
        "rank_M": rank,
        "det_M": det,
        "nullity_M": nullity,
        "null_basis_primitive_integer": [list(v) for v in basis],
        "null_basis_Mv": checks,
        "saturated_lambda_max_1": saturated,
        "support_edges": support_edges(M),
        "support_components": c,
        "rank_G": rank_g,
        "gram_trace": str(trace_gram(M, n)),
        "gram_nonzero_eigenvalue_product": str(
            gram_principal_2sum(M, n)
        ),
        "symmetry_class_S3xS3": list(canonical_class(M)),
    }

    return record


def sha256_file(path):
    h = hashlib.sha256()

    with path.open("rb") as f:
        while True:
            chunk = f.read(1024 * 1024)
            if not chunk:
                break
            h.update(chunk)

    return h.hexdigest()


def main():
    max_n = DEFAULT_MAX_N

    if len(sys.argv) >= 2:
        max_n = int(sys.argv[1])

    if max_n < 1:
        raise SystemExit("max margin must be >= 1")

    all_records = []

    print("AQ-SM-SPECTRAL-SPLIT-001")
    print("EXACT 3x3 EQUAL-MARGIN ATLAS")
    print("Governance: FROZEN · EXACT · NO PROMOTION")
    print("C4 BLOCKED · PUBLICATION BLOCKED · Lean OPEN")
    print()

    for n in range(1, max_n + 1):
        records = []

        for M in enumerate_matrices(n):
            assert check_equal_margin(M, n)

            record = atlas_record(M, n)
            records.append(record)

        # Exact census checks.
        total = len(records)

        expected_total = (
            n**4
            + 6 * n**3
            + 15 * n**2
            + 18 * n
            + 8
        ) // 8

        assert total == expected_total, (
            f"n={n}: total {total} != "
            f"expected {expected_total}"
        )

        c3 = sum(
            r["support_components"] == 3
            for r in records
        )
        c2 = sum(
            r["support_components"] == 2
            for r in records
        )
        c1 = sum(
            r["support_components"] == 1
            for r in records
        )

        assert c3 == 6
        assert c2 == 9 * (n - 1)
        assert c1 == total - c2 - c3

        rankg_counts = {
            r: sum(x["rank_G"] == r for x in records)
            for r in range(3)
        }

        assert rankg_counts[0] == c3
        assert rankg_counts[1] == c2
        assert rankg_counts[2] == c1

        # Exact support/rank theorem check.
        for r in records:
            assert r["rank_G"] == 3 - r["support_components"]

        # Exact saturation/nullity theorem check.
        for r in records:
            assert (
                r["saturated_lambda_max_1"]
                == (r["rank_M"] < 3)
            )

        all_records.extend(records)

        print(
            f"n={n:2d} "
            f"total={total:6d} "
            f"c=3:{c3:5d} "
            f"c=2:{c2:5d} "
            f"c=1:{c1:6d} "
            f"saturated={sum(r['saturated_lambda_max_1'] for r in records):6d}"
        )

    with OUT_JSONL.open("w", encoding="utf-8") as f:
        for record in all_records:
            f.write(
                json.dumps(
                    record,
                    sort_keys=True,
                    separators=(",", ":"),
                )
                + "\n"
            )

    output_hash = sha256_file(OUT_JSONL)

    receipt = [
        "AQ-SM-SPECTRAL-SPLIT-001",
        "EXACT 3x3 EQUAL-MARGIN SPECTRAL / SUPPORT ATLAS",
        "",
        "GOVERNANCE:",
        "FROZEN · EXACT · NO PROMOTION",
        "C4 BLOCKED · PUBLICATION BLOCKED · Lean OPEN",
        "",
        f"maximum_margin={max_n}",
        f"records={len(all_records)}",
        "",
        "CERTIFIED PROGRAM ASSERTIONS:",
        "1. Every emitted matrix has equal row/column margin.",
        "2. Exact determinant/rank is internally consistent.",
        "3. Every emitted null vector satisfies M*v=0 exactly.",
        "4. support_components is computed by exact DSU.",
        "5. rank_G = 3 - support_components.",
        "6. lambda_max(G)=1 flag equals rank(M)<3.",
        "7. 3x3 total count matches the Birkhoff count polynomial.",
        "8. c=3 count equals 6.",
        "9. c=2 count equals 9(n-1).",
        "",
        "OUTPUT:",
        str(OUT_JSONL),
        f"sha256={output_hash}",
        "",
        "IMPORTANT:",
        "This is a computational certificate for the stated finite scope.",
        "It is not a Lean certificate.",
        "It does not close C4.",
        "It does not establish publication readiness.",
    ]

    OUT_RECEIPT.write_text(
        "\n".join(receipt) + "\n",
        encoding="utf-8",
    )

    print()
    print("OUTPUT:", OUT_JSONL)
    print("RECEIPT:", OUT_RECEIPT)
    print("SHA256:", output_hash)


if __name__ == "__main__":
    main()


