#!/usr/bin/env python3
"""
AQARION JOIN-STABILITY semantic oracle.


Purpose:
Small standard-library-only checks for the mathematical boundary
of the JOIN-STABILITY claim.


This file is NOT a theorem prover.
This file is NOT a Lean certificate.
This file is NOT a numerical-rank oracle.


It checks:




the explicit infinite counterexample;


the finite theorem on small exhaustive instances;


the basic surjective finite boundary.




No NumPy or external dependency is used.
"""


from future import annotations


from itertools import product


def canonical(labels):
"""Canonicalize a partition represented by integer labels."""
names = {}
result = []


for value in labels:
    if value not in names:
        names[value] = len(names)
    result.append(names[value])

return tuple(result)



def partitions(n):
"""Enumerate all set partitions as restricted-growth strings."""
if n == 0:
return [()]


result = []

def extend(prefix, maximum):
    if len(prefix) == n:
        result.append(tuple(prefix))
        return

    for value in range(maximum + 2):
        extend(prefix + [value], max(maximum, value))

extend([0], 0)
return result



def related(P, a, b):
return P[a] == P[b]


def pullback_stable(T, P):
"""Check T(a) P T(b) => a P b."""
n = len(T)


for a in range(n):
    for b in range(n):
        if related(P, T[a], T[b]) and not related(P, a, b):
            return False

return True



def join(P, Q):
"""Equivalence closure of P union Q."""
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

for a in range(n):
    for b in range(a):
        if related(P, a, b) or related(Q, a, b):
            union(a, b)

return canonical([find(i) for i in range(n)])



def join_stable(T, E, F):
return pullback_stable(T, join(E, F))


def explicit_infinite_counterexample():
"""
Check the canonical infinite witness on a finite prefix.


Points:
    x = 0,1,2,3,...

T(n) = n+1

E has class {0,2}.
F has class {0,3}.

The actual mathematical construction is infinite.
This finite-prefix check verifies the concrete witness equations
needed for the construction.
"""

def E(a, b):
    return (a == b) or ({a, b} == {0, 2})

def F(a, b):
    return (a == b) or ({a, b} == {0, 3})

def G(a, b):
    # The only nontrivial G component is {0,2,3}.
    return a == b or a in {0, 2, 3} and b in {0, 2, 3}

# E and F stability under T(n)=n+1.
for a in range(20):
    for b in range(20):
        if E(a + 1, b + 1) and not E(a, b):
            return False

        if F(a + 1, b + 1) and not F(a, b):
            return False

# Join failure:
# T(1)=2 and T(2)=3 are G-related,
# but 1 and 2 are not G-related.
if not G(2, 3):
    return False

if G(1, 2):
    return False

return True



def finite_exhaustive(max_n=4):
"""
Exhaustively test the finite theorem for n <= max_n.


This is a small semantic oracle, not the primary exhaustive
verifier.
"""

for n in range(1, max_n + 1):
    Ps = partitions(n)

    for T in product(range(n), repeat=n):
        stable = [P for P in Ps if pullback_stable(T, P)]

        for i, E in enumerate(stable):
            for F in stable[i:]:
                if not join_stable(T, E, F):
                    return False, {
                        "n": n,
                        "T": T,
                        "E": E,
                        "F": F,
                        "join": join(E, F),
                    }

return True, None



def main():
if not explicit_infinite_counterexample():
print("INFINITE_COUNTEREXAMPLE=FAIL")
return 1


print("INFINITE_COUNTEREXAMPLE=PASS")

ok, witness = finite_exhaustive(max_n=4)

if not ok:
    print("FINITE_THEOREM_SMOKE=FAIL")
    print(witness)
    return 1

print("FINITE_THEOREM_SMOKE=PASS")
print("DOMAIN=n=1..4")
print("STATUS=PASS")
return 0



if name == "main":
raise SystemExit(main())


