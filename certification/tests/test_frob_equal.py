#!/usr/bin/env python3


import numpy as np


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



def test_case(m, k, shift):
n = m * k


transition = [
    (i + shift) % n
    for i in range(n)
]

blocks = [
    [
        block * k + j
        for j in range(k)
    ]
    for block in range(m)
]

projection = build_projection(blocks, n)
koopman = build_koopman(transition, n)

defect = (
    np.eye(n) - projection
) @ koopman @ projection

residue = shift % k

expected = (
    2 * m * residue * (k - residue)
    / k**2
)

observed = np.linalg.norm(
    defect,
    "fro",
) ** 2

return observed, expected



def main():
failures = 0
tested = 0


for k in range(2, 6):
    for m in range(2, 5):
        for shift in range(1, k * m):
            residue = shift % k

            if residue == 0:
                continue

            observed, expected = test_case(
                m,
                k,
                shift,
            )

            tested += 1

            if abs(observed - expected) > 1e-8:
                failures += 1
                print(
                    "FAIL:",
                    f"m={m}",
                    f"k={k}",
                    f"shift={shift}",
                    f"observed={observed}",
                    f"expected={expected}",
                )

print(
    f"R4 ||D||_F^2=2mr(k-r)/k^2: "
    f"{failures}/{tested} failures "
    f"{'PASS' if failures == 0 else 'FAIL'}"
)

if failures:
    raise AssertionError(
        f"Frobenius formula failed "
        f"{failures}/{tested} cases."
    )



if name == "main":
main()

