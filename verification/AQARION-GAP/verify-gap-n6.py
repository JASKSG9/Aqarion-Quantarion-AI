#!/usr/bin/env python3
"""
AQARION-Gap — independent stdlib verification of the gap identity for n=6.
No Lean, no Mathlib, no third-party packages.
Expect: B6=203, 20503 pairs, 0 mismatches on d_T and gap rule.
"""
from collections import defaultdict

def all_partitions(n):
    def helper(elems):
        if not elems:
            yield ()
            return
        first, rest = elems[0], elems[1:]
        for part in helper(rest):
            yield (frozenset([first]),) + part
            for i, block in enumerate(part):
                yield part[:i] + (block | {first},) + part[i + 1 :]
    seen = set()
    for p in helper(list(range(n))):
        can = tuple(sorted((tuple(sorted(b)) for b in p), key=lambda t: (t[0], len(t), t)))
        if can not in seen:
            seen.add(can)
            yield can

def meet(P, Q):
    blocks = []
    for b1 in P:
        s1 = set(b1)
        for b2 in Q:
            inter = s1 & set(b2)
            if inter:
                blocks.append(tuple(sorted(inter)))
    return tuple(sorted(blocks, key=lambda t: (t[0], len(t), t)))

def join(P, Q, n):
    parent = list(range(n))
    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x
    def union(a, b):
        ra, rb = find(a), find(b)
        if ra != rb:
            parent[ra] = rb
    for part in (P, Q):
        for block in part:
            block = list(block)
            for y in block[1:]:
                union(block[0], y)
    groups = defaultdict(list)
    for x in range(n):
        groups[find(x)].append(x)
    return tuple(sorted((tuple(sorted(g)) for g in groups.values()),
                        key=lambda t: (t[0], len(t), t)))

def apply_T(P, T):
    return tuple(sorted((tuple(sorted(T[x] for x in b)) for b in P),
                        key=lambda t: (t[0], len(t), t)))

def orbit_join(P, T, n):
    TP = apply_T(P, T)
    T2P = apply_T(TP, T)
    return join(join(P, TP, n), T2P, n)

def d_T(P, T, n):
    return len(P) - len(orbit_join(P, T, n))

def restr_class(P, S=(0, 1, 2)):
    blocks_for_s = []
    for s in S:
        for b in P:
            if s in b:
                blocks_for_s.append(b)
                break
    p0, p1, p2 = blocks_for_s
    if p0 == p1 == p2:
        return "ALL3"
    if p0 != p1 and p1 != p2 and p0 != p2:
        pure = p0 == (0,) and p1 == (1,) and p2 == (2,)
        return "SEP-pure" if pure else "SEP-ext"
    return "PAIR"

def cS_cG(P, Q, n, S=(0, 1, 2)):
    def tau_card(Pi):
        e2b = {}
        for b in Pi:
            local = frozenset(x for x in b if x in S)
            for x in b:
                if x in S:
                    e2b[x] = local
        return len({e2b[s] for s in S})
    U = join(P, Q, n)
    cG = tau_card(U)
    parent = {s: s for s in S}
    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x
    def union(a, b):
        ra, rb = find(a), find(b)
        if ra != rb:
            parent[ra] = rb
    for Pi in (P, Q):
        for b in Pi:
            members = [x for x in b if x in S]
            for i in range(1, len(members)):
                union(members[0], members[i])
    cS = len({find(s) for s in S})
    return cS, cG

def main():
    n = 6
    Tmap = {0: 1, 1: 2, 2: 0, 3: 3, 4: 4, 5: 5}
    parts = list(all_partitions(n))
    assert len(parts) == 203, f"B6 expected 203, got {len(parts)}"

    mism_d = 0
    for P in parts:
        cls = restr_class(P)
        d = d_T(P, Tmap, n)
        expected = {"ALL3": 0, "PAIR": 1, "SEP-pure": 0, "SEP-ext": 2}[cls]
        if d != expected:
            mism_d += 1
    assert mism_d == 0, f"d_T mismatches: {mism_d}"

    mismatches = 0
    checked = 0
    diff_hist = defaultdict(int)
    for i in range(len(parts)):
        for j in range(i + 1, len(parts)):
            P, Q = parts[i], parts[j]
            M = meet(P, Q)
            U = join(P, Q, n)
            dd = d_T(P, Tmap, n) + d_T(Q, Tmap, n) - d_T(M, Tmap, n) - d_T(U, Tmap, n)
            cS, cG = cS_cG(P, Q
... 
