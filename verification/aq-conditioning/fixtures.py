from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from pathlib import Path
from typing import Any

from .canonical import load_json, sha256_file


@dataclass(frozen=True)
class MatrixFixture:
    fixture_id: str
    description: str
    matrix: tuple[tuple[Fraction, ...], ...]
    expected: dict[str, Any]
    source_path: str
    source_sha256: str

    @property
    def nrows(self) -> int:
        return len(self.matrix)

    @property
    def ncols(self) -> int:
        return len(self.matrix[0]) if self.matrix else 0


def parse_fraction(value: int | float | str) -> Fraction:
    if isinstance(value, int):
        return Fraction(value, 1)
    if isinstance(value, str):
        return Fraction(value)
    raise TypeError(
        "Fixture entries must be integers or exact rational strings; "
        f"received {type(value).__name__}."
    )


def load_fixture(path: str | Path) -> MatrixFixture:
    path = Path(path)
    raw = load_json(path)

    rows = raw["matrix"]
    matrix = tuple(
        tuple(parse_fraction(entry) for entry in row)
        for row in rows
    )

    if not matrix:
        raise ValueError("Fixture matrix must be nonempty.")

    width = len(matrix[0])
    if width == 0 or any(len(row) != width for row in matrix):
        raise ValueError("Fixture matrix must be rectangular.")

    return MatrixFixture(
        fixture_id=raw["fixture_id"],
        description=raw["description"],
        matrix=matrix,
        expected=raw["expected"],
        source_path=str(path),
        source_sha256=sha256_file(path),
    )
