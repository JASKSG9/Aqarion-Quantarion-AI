# ARO-1 — AQARION Reproduction Object

Status: PROPOSED
Date: 2026-09-17

## Purpose

ARO-1 defines the evidence object required to distinguish:

- a rerun;
- an independent reproduction;
- a reproduction failure;
- input drift;
- stale receipts;
- false independence.

ARO-1 is a reproducibility contract.

It is not a mathematical proof system.

## Core principle

Output equality is evidence of agreement.

Output equality is not evidence of independence.

Output inequality is evidence of reproduction failure.

Output inequality is not evidence of independence.

## Execution pair

Every reproduction comparison contains two execution records.

### Reference execution

Required:

- source digest;
- executable digest;
- input digest;
- environment digest;
- output digest;
- commit.

### Reproduction execution

Required:

- source digest;
- executable digest;
- input digest;
- environment digest;
- output digest;
- commit.

## Relation

The comparison records:

- specification_same;
- inputs_same;
- implementation_independent;
- environment_independent;
- outputs_equal.

## Classification

### RERUN

The reproduction uses the same implementation and agrees with
the reference output.

This is reproducibility by rerun.

It is not independent reproduction.

### INDEPENDENTLY_REPRODUCED

The implementation is independently separated according to the
declared independence boundary, the specification and inputs agree,
and the output agrees.

This is an evidence classification.

It is not a mathematical proof.

### REPRODUCTION_FAILURE

The specification/inputs are aligned but the output differs.

### INPUT_DRIFT

The input identity differs.

Matching output does not repair this failure.

### STALE_RECEIPT

The execution is not bound to the expected source revision.

### FALSE_INDEPENDENCE

The execution is claimed to be independent while the source and
executable are identical to the reference implementation.

## Independence limitation

A cryptographic digest proves byte equality or inequality.

It does not prove:

- authorship;
- intellectual independence;
- absence of shared source ancestry;
- absence of copied algorithms;
- absence of shared hidden dependencies.

Therefore ARO-1 uses:

    implementation_independent

as an evidence relation whose supporting evidence must itself be
represented.

The boolean is not treated as a self-authenticating fact.

## Governance

ARO-1 does not promote:

- computation to theorem;
- replay to proof;
- hash equality to semantic equality;
- different executables to mathematical truth.

Promotion remains subject to AQARION governance.
