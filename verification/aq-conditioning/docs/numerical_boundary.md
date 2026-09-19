# Numerical Boundary

## Exact rank

For matrices with integer or rational entries, exact rank is computed over the rational field.
This is the reference classification for the included small fixtures.

## Numerical rank

A numerical singular-value decomposition reports singular values

[
sigma_1 ge cdots ge sigma_n ge 0.
]

A numerical rank requires a tolerance (\tau):

[
operatorname{rank}_{\tau}(A)
=
#{j:sigma_j>\tau}.
]

Changing (\tau), arithmetic precision, BLAS implementation, or scaling may change this
numerical classification for a near-singular matrix.

## Required reporting

Every numerical-rank report must include:

- Arithmetic type and precision
- Singular values
- Rank tolerance
- Exact rank, when an exact rational fixture exists
- Condition number if finite
- Any proposed null-vector residual
- The explicit statement that numerical rank is not exact rank

## No overclaim

The project does not infer a kernel, theorem, spectral gap, or singularity solely from a
floating-point threshold.
