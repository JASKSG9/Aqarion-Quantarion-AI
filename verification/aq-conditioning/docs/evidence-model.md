# AQARION-CONDITION8NG Evidence Model

## Scope

AQARION-CONDITION8NG distinguishes exact finite algebra, numerical approximation,
execution provenance, and formal proof.

## Evidence labels

| Label | Meaning |
|---|---|
| [D] | Defined contract, fixture, or theorem target |
| [V] | Finite computational verification completed under a declared contract |
| [P] | Mathematical theorem proved and accepted under the declared proof policy |
| [PV] | Both proved and computationally verified |
| [F] | Refuted, killed, or rejected by a counterexample |
| [Q] | Quarantined pending repair or review |

## Rules

- A floating-point SVD does not establish exact rank.
- A small singular value is not an exact kernel certificate.
- An exact rational null vector is stronger than a tolerance-qualified approximate null vector.
- A valid SHA-256 hash establishes artifact identity, not mathematical truth.
- A CI pass establishes execution of declared checks, not a theorem.
- A Lean file containing `sorry` is not a kernel-accepted proof.
- A receipt from one environment is not external independent reproduction.
- All generated runtime receipts remain finite computational evidence unless separately formalized.

## Governance

C4 is blocked.
Publication is blocked.
Promotion is false.
