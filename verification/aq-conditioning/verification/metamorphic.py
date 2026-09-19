from __future__ import annotations

from fractions import Fraction

from aq_conditioning.exact_rank import exact_rank


def main() -> int:
    matrix = [
        [Fraction(1), Fraction(2)],
        [Fraction(2), Fraction(4)],
    ]

    transformed = [
        [matrix[0][0], matrix[0][1]],
        [matrix[1][0] - 2 * matrix[0][0], matrix[1][1] - 2 * matrix[0][1]],
    ]

    original_rank = exact_rank(matrix)
    transformed_rank = exact_rank(transformed)

    passed = original_rank == transformed_rank == 1

    print(
        {
            "test": "invertible_row_operation_preserves_exact_rank",
            "original_rank": original_rank,
            "transformed_rank": transformed_rank,
            "status": "PASS" if passed else "FAIL",
        }
    )

    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
