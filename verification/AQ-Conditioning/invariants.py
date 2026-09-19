from __future__ import annotations

from fractions import Fraction
from typing import Iterable

from .exact_rank import (
    column_sums,
    copy_matrix,
    exact_nullity,
    exact_rank,
    is_column_stochastic_in_sum_sense,
    is_square,
)


def matrix_vector_mul(
    matrix: Iterable[Iterable[Fraction]],
    vector: Iterable[Fraction],
) -> list[Fraction]:
    rows = copy_matrix(matrix)
    vec = list(vector)

    if not rows or len(rows[0]) != len(vec):
        raise ValueError("Matrix-vector dimensions do not match.")

    return [
        sum(
            (entry * vec[col] for col, entry in enumerate(row)),
            Fraction(0, 1),
        )
        for row in rows
    ]


def verify_zero_sum_kernel_witness(
    matrix: Iterable[Iterable[Fraction]],
    vector: Iterable[Fraction],
) -> dict[str, object]:
    vec = list(vector)
    image = matrix_vector_mul(matrix, vec)

    return {
        "witness_nonzero": any(value != 0 for value in vec),
        "sum_of_coordinates": str(sum(vec, Fraction(0, 1))),
        "kernel_image": [str(value) for value in image],
        "is_exact_kernel_vector": all(value == 0 for value in image),
        "is_zero_sum": sum(vec, Fraction(0, 1)) == 0,
    }


def exact_matrix_summary(
    matrix: Iterable[Iterable[Fraction]],
) -> dict[str, object]:
    copied = copy_matrix(matrix)
    nrows = len(copied)
    ncols = len(copied[0]) if copied else 0

    return {
        "shape": [nrows, ncols],
        "is_square": is_square(copied),
        "exact_rank": exact_rank(copied),
        "exact_nullity": exact_nullity(copied),
        "column_sums": [str(value) for value in column_sums(copied)],
        "column_sum_invariant_holds": is_column_stochastic_in_sum_sense(copied),
    }
