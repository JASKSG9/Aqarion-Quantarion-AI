#!/usr/bin/env python3


from collections import defaultdict, deque


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

return [
    index[gap(999 * g1 + 90 * g2)]
    for g1, g2 in states
], len(states)



def build_koopman(transition, n):
matrix = np.zeros((n, n))


for i, target in enumerate(transition):
    matrix[i, target] = 1.0

return matrix



def build_projection(blocks, n):
projection = np.zeros((n, n))


for block in blocks:
    size = len(block)

    for i in block:
        for j in block:
            projection[i, j] = 1.0 / size

return projection



def rank_defect(blocks, transition, n):
defect = (
np.eye(n) - build_projection(blocks, n)
) @ build_koopman(transition, n) @ build_projection(
blocks,
n,
)


return int(np.linalg.matrix_rank(defect, tol=1e-9))



def is_congruence(blocks, transition):
label = {
element: block_index
for block_index, block in enumerate(blocks)
for element in block
}


return all(
    len({
        label[transition[x]]
        for x in block
    }) == 1
    for block in blocks
)



def depth_partition(transition, n):
fixed = next(
i
for i, target in enumerate(transition)
if target == i
)


reverse = defaultdict(list)

for source, target in enumerate(transition):
    reverse[target].append(source)

depth = {fixed: 0}
queue = deque([fixed])

while queue:
    vertex = queue.popleft()

    for predecessor in reverse[vertex]:
        if predecessor not in depth:
            depth[predecessor] = depth[vertex] + 1
            queue.append(predecessor)

by_depth = defaultdict(list)

for vertex in range(n):
    by_depth[depth[vertex]].append(vertex)

return [
    by_depth[d]
    for d in sorted(by_depth)
]



def main():
transition, n = kaprekar_t()


tested_partitions = [
    depth_partition(transition, n),
    [[i] for i in range(n)],
]

violations = 0

for blocks in tested_partitions:
    congruent = is_congruence(
        blocks,
        transition,
    )

    zero_defect = (
        rank_defect(
            blocks,
            transition,
            n,
        )
        == 0
    )

    if zero_defect != congruent:
        violations += 1

print(
    "R2 AQ-001 D=0<->congruence: "
    f"{violations} violations "
    f"{'PASS' if violations == 0 else 'FAIL'}"
)

if violations:
    raise AssertionError(
        "AQ-001 receipt failed."
    )



if name == "main":
main()

