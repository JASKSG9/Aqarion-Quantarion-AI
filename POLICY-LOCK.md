# AQARION POLICY LOCK

**Policy ID:** AQ-POLICY-001  
**Effective:** 2026-09-17  
**Status:** ACTIVE

---

# 1. LEAN IS OPTIONAL

Lean is an optional formalization layer.

Lean does not automatically block:

- research;
- computation;
- experiments;
- literature synthesis;
- collaboration;
- computational releases;
- analytic derivations;
- evidence records;
- publication drafts.

A claim may be computationally or analytically established without a Lean
receipt when the applicable evidence standard is satisfied.

---

# 2. FORMAL STATUS MUST REMAIN HONEST

Lean source without a successful checker receipt is not:

`FORMALLY VERIFIED`

A successful formal checker receipt establishes formal verification only
for the exact proposition and environment actually checked.

---

# 3. CLAIM-TYPE-SPECIFIC EVIDENCE

Promotion is determined by the evidence required by the claim type.

### Analytic claim

Required:

- complete derivation;
- adversarial validation;
- appropriate independent review.

### Computational claim

Required:

- deterministic procedure;
- reproducible execution;
- appropriate independent check.

### Exhaustive claim

Required:

- explicit finite domain;
- complete enumeration;
- zero failures;
- reproducibility evidence.

### Formal claim

Required:

- actual formal checker receipt.

### Literature claim

Required:

- source explicitly supporting the stated proposition and scope.

### Conjecture

Remains conjecture unless independently established.

### Refuted claim

Remains refuted unless a later independent correction demonstrates that
the counterexample or refutation itself was invalid.

---

# 4. CURRENT STATE VOCABULARY

Use:

`DEFINED`

`SUPPORTED`

`VERIFIED-ANALYTIC`

`VERIFIED-COMPUTATIONAL`

`VERIFIED-EXHAUSTIVE`

`VERIFIED-FORMAL`

`OPEN`

`CONJECTURE`

`REFUTED`

`QUARANTINED`

`HISTORICAL`

`BLOCKED`

Do not use a stronger label merely because a file exists.

---

# 5. SOURCE-OF-TRUTH RULE

The current repository truth state is maintained by:

`AQARION-TRUTH-BASELINE-2026-09-17.md`

Historical checkpoints remain historical records.

They are not silently rewritten into current specifications.

---

# 6. NO GLOBAL PUBLICATION CLAIM

AQARION must not use a global repository statement claiming:

`PUBLICATION-READY`

or:

`SUBMISSION-READY`

as a substitute for claim-specific evidence review.

Publication readiness is claim-specific.

---

# 7. NO FABRICATED RECEIPTS

Never report:

- a test that did not run;
- a metric that was not calculated;
- a hash that was not computed;
- a proof that was not checked;
- a mutation that was not executed;
- an independent implementation that was not independently run.

---

# 8. NO AUTOMATIC PROMOTION

The existence of:

- Python code;
- Lean source;
- Kotlin source;
- JSON;
- a checkpoint;
- a GitHub file;
- an AI-generated derivation;

does not itself establish the corresponding epistemic status.

---

# 9. CURRENT RESEARCH PRIORITY

Repository reconciliation takes precedence over speculative expansion when
definitions or status records conflict.

---

# 10. EFFECTIVE POLICY

DERIVE
→ COMPUTE
→ BREAK
→ INDEPENDENTLY CHECK
→ SEARCH LITERATURE
→ CLASSIFY
→ PACKAGE
→ OPTIONAL FORMALIZE

This is the current AQARION evidence workflow.

---

**AQ-POLICY-001 — ACTIVE**
