# Exact Support Spectrum for the Marked Defect

Date: 2026-09-17

## Claim identity

AQ-SUPPORT-SPECTRUM-001

## Statement

For every integer s >= 1, the set of realizable marked defects is

Spec_s(kappa_S)
=
{
  -s + ceil(2 sqrt(s)) - 1,
  ...,
  s - 1
}.

Equivalently, every integer k satisfying

-s + ceil(2 sqrt(s)) - 1 <= k <= s - 1

is realized by some finite partition pair (P,Q) and support
S with |S| = s.

## Analytic status

ANALYTICALLY DERIVED

The proof constructs a simple bipartite marked incidence graph with

v = s + 1 + k

vertices and s marked edges, followed by unmarked connector edges
joining all marked-incidence components.

The resulting defect is

kappa_S = c(H_S) - 1 - beta(H_S) = v - s - 1 = k.

## Computational support

INDEPENDENTLY COMPUTED

The constructive realization was independently checked for every
admissible (s,k) pair through s = 30.

This computation is regression evidence only.
It is not the proof of the universal statement.

## Corollaries

For s = 3,

Spec_3(kappa_S) = {0,1,2}.

Therefore universal nonnegativity holds for support size at most 3.

For s = 4,

Spec_4(kappa_S) = {-1,0,1,2,3}.

The first negative defect is therefore realizable at support size 4.

## Transport consequence

Under the separately established hypotheses

m_T = 0

and

kappa_S(JP,JQ) = 0,

together with the exact transport identity

Delta = s_T - s_0 = kappa_S(P,Q),

the C3 support spectrum implies

Delta in {0,1,2}.

This transport conclusion is conditional on those hypotheses.

## Evidence boundary

This record does not claim:

- Lean verification;
- formal proof;
- publication readiness;
- correctness of unrelated C3 claims;
- correctness of an unrestricted K_2,r extremal conjecture.

## Disposition

SUPPORTED

Analytic proof: present.

Independent computational construction check: present.

Formal receipt: absent.

Universal theorem status: analytic proof supplied; formalization optional.
