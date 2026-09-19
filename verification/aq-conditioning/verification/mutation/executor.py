from __future__ import annotations

from fractions import Fraction

from aq_conditioning.exact_rank import exact_rank


def wrong_rank_mutant(_: object) -> int:
    return 0


def main() -> int:
    matrix = [
        [Fraction(1), Fraction(2)],
        [Fraction(2), Fraction(4)],
    ]

    canonical_rank = exact_rank(matrix)
    mutant_rank = wrong_rank_mutant(matrix)

    killed = canonical_rank != mutant_rank

    print(
        {
            "mutant": "constant_zero_rank",
            "canonical_rank": canonical_rank,
            "mutant_rank": mutant_rank,
            "status": "KILLED" if killed else "SURVIVED",
        }
    )

    return 0 if killed else 1


if __name__ == "__main__":
    raise SystemExit(main())
