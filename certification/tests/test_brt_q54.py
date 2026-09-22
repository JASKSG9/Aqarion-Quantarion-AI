#!/usr/bin/env python3


import numpy as np


def kaprekar_t(n_digits=4, base=10):
def gap(x):
digits = [(x // (base ** i)) % base for i in range(n_digits)]
s = sorted(digits)
return (s[-1] - s[0], s[-2] - s[1])


states = [
    (g1, g2)
    for g1 in range(1, base)
    for g2 in range(0, g1 + 1)
]

index = {state: i for i, state in enumerate(states)}

transition = [
    index[gap(999 * g1 + 90 * g2)]
    for g1, g2 in states
]

return transition, len(states)



def build_koopman(transition, n):
matrix = np.zeros((n, n))


for i, target in enumerate(transition):
    matrix[i, target] = 1.0

return matrix



def build_projection(blocks, n):
projection = np.zeros((n, n))


for block in blocks:
    size = len(block)

    if size == 0:
        raise ValueError("empty partition block")

    for i in block:
        for j in block:
            projection[i, j] = 1.0 / size

return projection



def rank_defect(blocks, transition, n):
koopman = build_koopman(transition, n)
projection = build_projection(blocks, n)


defect = (
    np.eye(n) - projection
) @ koopman @ projection

return int(np.linalg.matrix_rank(defect, tol=1e-9))



def bipartite_components(blocks, transition):
block_count = len(blocks)


label = {
    element: block_index
    for block_index, block in enumerate(blocks)
    for element in block
}

parent = list(range(2 * block_count))

def find(x):
    while parent[x] != x:
        parent[x] = parent[parent[x]]
        x = parent[x]
    return x

def union(a, b):
    a = find(a)
    b = find(b)

    if a != b:
        parent[a] = b

for source_index, block in enumerate(blocks):
    for target_index in {
        label[transition[x]]
        for x in block
    }:
        union(source_index, block_count + target_index)

return len({find(v) for v in range(2 * block_count)})



def main():
transition, n = kaprekar_t()


rng = np.random.default_rng(42)

trials = 200
passed = 0

for _ in range(trials):
    block_size = int(rng.integers(1, n))

    permutation = rng.permutation(n)

    blocks = [
        list(permutation[:block_size]),
        list(permutation[block_size:]),
    ]

    expected = (
        2 - bipartite_components(
            blocks,
            transition,
        )
    )

    observed = rank_defect(
        blocks,
        transition,
        n,
    )

    if observed != expected:
        raise AssertionError(
            "BRT failure: "
            f"observed={observed}, "
            f"expected={expected}"
        )

    passed += 1

print(
    f"R1 BRT rank=m-c_bip: "
    f"{passed}/{trials} PASS"
)



if name == "main":
main()

