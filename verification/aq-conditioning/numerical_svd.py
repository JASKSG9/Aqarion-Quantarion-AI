from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from typing import Iterable

import numpy as np


@dataclass(frozen=True)
class NumericalSpectrum:
    singular_values: tuple[float, ...]
    sigma_min: float
    sigma_max: float
    condition_number: float | None
    numerical_rank: int
    rank_tolerance: float


def to_float64(matrix: Iterable[Iterable[Fraction]]) -> np.ndarray:
    return np.array(
        [[float(value) for value in row] for row in matrix],
        dtype=np.float64,
    )


def compute_svd(
    matrix: Iterable[Iterable[Fraction]],
    rank_tolerance: float,
) -> NumericalSpectrum:
    array = to_float64(matrix)
    singular_values = np.linalg.svd(array, compute_uv=False)

    if singular_values.size == 0:
        raise ValueError("SVD requires a nonempty matrix.")

    sigma_max = float(singular_values[0])
    sigma_min = float(singular_values[-1])

    if sigma_min == 0.0:
        condition_number = None
    else:
        condition_number = sigma_max / sigma_min

    numerical_rank = int(np.sum(singular_values > rank_tolerance))

    return NumericalSpectrum(
        singular_values=tuple(float(value) for value in singular_values),
        sigma_min=sigma_min,
        sigma_max=sigma_max,
        condition_number=condition_number,
        numerical_rank=numerical_rank,
        rank_tolerance=rank_tolerance,
    )
