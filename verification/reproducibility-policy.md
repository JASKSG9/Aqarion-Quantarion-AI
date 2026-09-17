# AQARION Reproducibility Policy

Version: 1.0-proposed
Date: 2026-09-17

## 1. Status vocabulary

AQARION distinguishes:

    DEFINED
    COMPUTED
    REPLAYED
    VERIFIED
    INDEPENDENTLY_REPRODUCED
    PROVED
    FORMALLY_VERIFIED

These labels are not interchangeable.

## 2. Rerun

A rerun repeats an execution using the same implementation.

A successful rerun demonstrates execution repeatability.

It does not establish independent reproduction.

## 3. Independent reproduction

Independent reproduction requires:

    same specification
    same inputs
    independent implementation evidence
    output agreement

Environment separation may provide additional evidence but does
not by itself establish implementation independence.

## 4. Exact reproduction

For deterministic exact claims:

    output equality is required.

Output inequality is a reproduction failure.

## 5. Hash semantics

SHA-256 equality establishes byte equality of the hashed objects.

SHA-256 does not establish:

    mathematical equivalence
    semantic equivalence
    authorship
    intellectual independence
    correctness

## 6. Input integrity

A reproduction comparison with changed inputs is not an exact
reproduction comparison.

This remains true even when the output happens to match.

## 7. Receipt freshness

A receipt must identify the source revision from which the execution
was produced.

A receipt detached from the claimed revision is stale.

## 8. Independence evidence

The field:

    implementation_independent

is a relation requiring supporting evidence.

It must not be treated as a magical self-certifying boolean.

Possible supporting evidence includes:

- independently developed implementation;
- separately maintained source tree;
- independently generated executable;
- separate execution environment;
- separate provenance chain;
- external attestation where available.

AQARION does not claim that any single item proves intellectual
independence.

## 9. Adversarial requirements

Any implementation claiming ARO-1 support must reject:

    same implementation + independent=true

and must classify:

    different implementation + same output

as a possible independent reproduction rather than a theorem proof.

It must classify:

    different implementation + different output

as reproduction failure.

It must reject:

    changed inputs + same output

as exact reproduction.

It must reject stale source bindings.

## 10. Governance

Reproducibility status never automatically promotes mathematical
status.

A result can be:

    independently reproduced
    but not proved.

A result can be:

    formally proved
    but not independently reproduced computationally.

AQARION therefore maintains separate evidence axes.
