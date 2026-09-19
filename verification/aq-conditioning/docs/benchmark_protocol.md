# Benchmark Protocol

## Objective

Measure the difference between exact algebraic classification and numerical
conditioning diagnostics.

## Required fixture classes

1. Exact singular matrix.
2. Exact full-rank matrix.
3. Near-singular full-rank matrix.
4. Column-sum-preserving singular matrix with a zero-sum kernel witness.
5. Negative malformed fixture rejected by validation.

## Reported values

For each valid fixture, record:

[
n,quad
operatorname{rank}_{mathbb Q}(A),quad
operatorname{nullity}_{mathbb Q}(A),quad
sigma_{min}(A),quad
sigma_{max}(A).
]

If a numerical rank is reported, also record the tolerance:

[
\tau.
]

For each declared kernel witness (v), record:

[
Av,qquad
sum_i v_i.
]

## Acceptance boundary

A result is a finite computational verification only if:

- The contract parses as strict JSON.
- All required fixtures parse and validate.
- Exact ranks equal their declared expected values.
- Declared exact kernel witnesses verify exactly.
- The runtime receipt is generated and validates against its schema.

No performance or stability conclusion is valid until the benchmark has been run and
the raw receipt is available.
