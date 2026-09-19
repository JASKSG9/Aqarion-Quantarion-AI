from __future__ import annotations

from fractions import Fraction
from typing import Iterable


MatrixQ = list[list[Fraction]]


def copy_matrix(matrix: Iterable[Iterable[Fraction]]) -> MatrixQ:
    return [list(row) for row in matrix]


def exact_rank(matrix: Iterable[Iterable[Fraction]]) -> int:
    work = copy_matrix(matrix)

    if not work:
        return 0

    nrows = len(work)
    ncols = len(work[0])

    if any(len(row) != ncols for row in work):
        raise ValueError("Matrix must be rectangular.")

    pivot_row = 0
    rank = 0

    for col in range(ncols):
        pivot = next(
            (row for row in range(pivot_row, nrows) if work[row][col] != 0),
            None,
        )

        if pivot is None:
            continue

        work[pivot_row], work[pivot] = work[pivot], work[pivot_row]

        pivot_value = work[pivot_row][col]
        work[pivot_row] = [value / pivot_value for value in work[pivot_row]]

        for row in range(nrows):
            if row == pivot_row:
                continue

            factor = work[row][col]
            if factor == 0:
                continue

            work[row] = [
                work[row][j] - factor * work[pivot_row][j]
                for j in range(ncols)
            ]

        rank += 1
        pivot_row += 1

        if pivot_row == nrows:
            break

    return rank


def exact_nullity(matrix: Iterable[Iterable[Fraction]]) -> int:
    copied = copy_matrix(matrix)

    if not copied:
        return 0

    return len(copied[0]) - exact_rank(copied)


def is_square(matrix: Iterable[Iterable[Fraction]]) -> bool:
    copied = copy_matrix(matrix)
    return bool(copied) and len(copied) == len(copied[0])


def column_sums(matrix: Iterable[Iterable[Fraction]]) -> list[Fraction]:
    copied = copy_matrix(matrix)

    if not copied:
        return []

    ncols = len(copied[0])
    return [
        sum((copied[row][col] for row in range(len(copied))), Fraction(0, 1))
        for col in range(ncols)
    ]


def is_column_stochastic_in_sum_sense(
    matrix: Iterable[Iterable[Fraction]],
) -> bool:
    return all(value == 1 for value in column_sums(matrix))
