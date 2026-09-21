# AQ-EVIDENCE-CORE v1

## Core principle

A successful execution is evidence of execution.

It is not automatically a proof of the mathematical claim.

---

## Evidence chain

CLAIM
  |
  v
SPECIFICATION
  |
  v
DERIVATION
  |
  +--> EXACT IMPLEMENTATION A
  |
  +--> INDEPENDENT IMPLEMENTATION B
  |
  +--> REDUCED ORACLE C
  |
  v
CROSSCHECK
  |
  v
ADVERSARIAL MUTATIONS
  |
  v
RECEIPT
  |
  v
PROVENANCE
  |
  v
FORMAL STATUS
  |
  v
GOVERNANCE

---

## Required separations

### Execution

PASS
FAIL
NOT_RUN
BLOCKED
UNKNOWN

### Artifact

PRESENT
MISSING
MISMATCH

### Reproduction

MATCH
MISMATCH
NOT_RUN

### Formal

PROVED
OPEN
FAILED

### Semantic

ALIGNED
MISALIGNED
UNREVIEWED

### Governance

PROMOTABLE
BLOCKED

These dimensions MUST NOT be collapsed into a single trust score.

---

## Promotion rule

Execution PASS does not imply:

FORMALLY_PROVED

SEMANTICALLY_ALIGNED

PUBLICATION_READY

PROMOTABLE

A claim is promotable only when every required governance gate
explicitly permits promotion.

---

## Reference specimen

AQ-CYCLE-DELTA-001 is the reference specimen for v1.

It exists to test the Evidence-Core mechanism itself.

The specimen must remain small enough that another researcher can:

1. inspect the claim;
2. inspect the derivation;
3. run the exact computation;
4. inspect independent routes;
5. run the mutation suite;
6. inspect the receipt;
7. identify what remains formally open.

---

## Trust boundary

The receipt describes evidence.

The receipt does not become the theorem.

A hash proves identity of bytes.

A successful execution proves execution.

A formal checker can establish formal validity.

None of those alone establishes semantic fidelity to the intended
research question.

---

## Current AQARION governance

C4: BLOCKED

Publication: BLOCKED

Lean: OPEN

Dashboard: UNVERIFIED

Promotion: NO
