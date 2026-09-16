Aqarions-Quantarion-AI

"License" (https://img.shields.io/badge/license-Apache--2.0-blue)
"C3" (https://img.shields.io/badge/C3-OPEN-yellow)
"C4" (https://img.shields.io/badge/C4-BLOCKED-red)
"Lean" (https://img.shields.io/badge/Lean-OPEN-lightgrey)
"SDS--002" (https://img.shields.io/badge/SDS--002-QUARANTINED-orange)
"Publication" (https://img.shields.io/badge/publication-BLOCKED-red)
"Promotable" (https://img.shields.io/badge/promotable-false-lightgrey)

Governance, policy, provenance, and cross-repository orchestration hub for
the AQARION / Quantarion research corpus.

This repository is a hub, not a self-contained mathematical library.

It provides:

1. CLAIMLOCK policy evaluation.
2. Reproduction-object and provenance semantics.
3. Independent verification entry points.
4. Cross-repository dependency declarations.
5. Adversarial negative controls.
6. A public computational replay surface for selected AQARION claims.

It does not decide mathematical truth.

---

Current governance state

C3 ............. OPEN
C4 ............. BLOCKED
Lean ........... OPEN
SDS-002 ........ QUARANTINED
Publication .... BLOCKED
Promotable ..... false

No repository-level policy result is a mathematical proof.

No public application status is itself mathematical certification.

---

Evidence discipline

AQARION distinguishes:

[D]  DEFINED
[V]  VERIFIED COMPUTATION
[P]  PROVED
[PV] PROVED + VERIFIED
[C]  CONJECTURE
[R]  RESEARCH
[F]  REFUTED / KILLED
[Q]  QUARANTINED

Evidence must not migrate upward merely because a later artifact repeats the
same statement.

In particular:

public == certified            NO
runnable == verified           NO
numeric == proof               NO
Lean file == Lean proof        NO
policy ALLOW == truth          NO
matching output == independence NO

---

CLAIMLOCK

"source/python/claimlock.py" is a policy evaluator.

It answers:

«Does this evidence set satisfy this promotion policy?»

It does not answer:

«Is the mathematical claim true?»

That distinction is fundamental.

---

Reproduction provenance

AQARION uses a reproduction-object model with separate predicates:

CLAIM
SPECIFICATION
SOURCE
IMPLEMENTATION
FIXTURE
EXECUTION
OUTPUT
COMPARISON
INDEPENDENCE
FORMAL STATUS
DRIFT

A reproduction requires execution, binding, and output agreement.

Independent reproduction additionally requires an independent basis.

Formalization and proof are separate evidence dimensions.

---

Verification entry point

Run:

python3 verification/run-all.py \
  --manifest verification/manifest.json \
  --receipt verification/receipts/run_all_receipt.json

The runner is fail-closed.

It never treats "NOT_IMPLEMENTED" as "PASS".

---

K2R closure-stabilization replay

The current hub contains an independent computational replay of the K2r
closure family.

The fixtures are:

verification/k2r/fixtures/AQ-K2R-R2.json
verification/k2r/fixtures/AQ-K2R-R3.json
verification/k2r/fixtures/AQ-K2R-R5.json
verification/k2r/fixtures/AQ-K2R-R15.json

The verifier is:

verification/k2r/verify.py

Run:

python3 verification/k2r/verify.py

The verifier reconstructs the objects from "r", rather than importing a
mathematical implementation from another AQARION repository.

The current computational results include:

h_min(P) = 2
h_min(Q) = r
h_min(M) = 2r
h_min(U) = 1

Delta = -(r-1)

for the tested fixtures.

These are currently recorded as:

RECONSTRUCTED_INDEPENDENT_COMPUTATION

They are not being represented here as Lean-certified theorems.

---

Three-orbit-term negative control

The closure certificate defines “three orbit terms” explicitly as:

R ∨ T(R) ∨ T²(R)

This is not the same thing as three recurrence applications.

The distinction matters already for "r = 2".

The K2R verifier therefore checks both:

three-orbit-term result

and

full orbit closure

separately.

---

Canonicalization

The K2R certificate manifest declares RFC 8785 JSON Canonicalization Scheme
(JCS) as the intended canonical serialization contract.

A true JCS implementation is required for normative certificate generation.

Generic "json.dumps(sort_keys=True, ...)" is deterministic JSON, but it is not
itself evidence of RFC 8785 compliance.

---

Two-application federation architecture

The public federation uses separate application roles.

PUBLIC FEDERATION HUB
https://aqarion-federation-hub--quantarion9.replit.app

        |
        v

CERTIFICATE / EVIDENCE SERVICE
https://quantarion-federation-hub--aqarionaaron.replit.app

        |
        v

GitHub / Hugging Face / archival artifacts

These roles must be explicit in machine-readable metadata.

A single ambiguous "liveAppUrl" field must not be used to represent both roles.

---

Cross-repository policy

The hub declares sibling repositories and their pinned commits.

A cross-repository declaration is a dependency statement.

It is not a proof that the referenced repository is current, correct, or
mathematically certified.

A pinned commit identifies a specific revision.

---

AI and provenance

AQARION does not claim that its infrastructure can determine whether a human
or AI produced a particular mathematical idea.

The relevant provenance question is:

What claim was evaluated?
What specification was used?
What source revision was executed?
What implementation ran?
What input was used?
What output was produced?
What comparison was performed?
Was independence established?
Was a formal proof artifact checked?

AI-assisted activity can be represented in the provenance graph where known.

That provenance does not itself establish mathematical truth.

---

Reproducibility

A repository being public is not equivalent to an independent reproduction.

AQARION therefore distinguishes:

AVAILABLE
EXECUTED
REPRODUCED
INDEPENDENTLY REPRODUCED
FORMALIZED
PROVED

Each requires its own evidence.

---

Publication gate

The current publication gate remains:

BLOCKED

The K2R computational replay does not by itself change C4 or publication
status.

Any eventual promotion must satisfy the applicable evidence policy and the
underlying mathematical proof requirements.

---

License

Apache 2.0. See "LICENSE".

---

Primary pointers

AQARION mathematical core:

"JASKSG9/AQARION-ARITHMETIC-FDS-FINITE-DYNAMICAL-SYSTEMS-"

Kaprekar spectral case study:

"JASKSG9/KAPREKAR-SPECTRAL-GEOMETRY"

AQARION Academy:

"huggingface.co/spaces/Quantarion9/AQARION-ACADEMY"
