![Aqarions-Quantarion-AI](https://img.shields.io/badge/license-Apache--2.0-blue) ![C3](https://img.shields.io/badge/C3-OPEN-yellow) ![C4](https://img.shields.io/badge/C4-BLOCKED-red) ![Lean](https://img.shields.io/badge/Lean-OPEN-lightgrey) ![SDS-002](https://img.shields.io/badge/SDS--002-QUARANTINED-orange) ![Publication](https://img.shields.io/badge/publication-BLOCKED-red) ![Promotable](https://img.shields.io/badge/promotable-false-lightgrey)

# Aqarions-Quantarion-AI

Governance, policy, provenance, and cross-repository orchestration hub for the AQARION / Quantarion research corpus, covering finite dynamical systems, observable quotients, and Koopman defect operators.

**This repository is a hub, not a self-contained mathematical library.** It provides:

- CLAIMLOCK policy evaluation.
- Reproduction-object and provenance semantics.
- Independent verification entry points.
- Cross-repository dependency declarations.
- Adversarial negative controls.
- A public computational replay surface for selected AQARION claims.

**It does not decide mathematical truth.**

## Governance state

| Layer | State |
|-------|-------|
| C3 | OPEN |
| C4 | BLOCKED |
| Lean | OPEN |
| SDS-002 | QUARANTINED |
| Publication | BLOCKED |
| Promotable | false |

No repository-level policy result is a mathematical proof.
No public application status is itself mathematical certification.

---

## Evidence discipline

AQARION distinguishes:

| Label | Meaning |
|-------|---------|
| [D] | DEFINED |
| [V] | VERIFIED COMPUTATION |
| [P] | PROVED |
| [PV] | PROVED + VERIFIED |
| [C] | CONJECTURE |
| [R] | RESEARCH |
| [F] | REFUTED / KILLED |
| [Q] | QUARANTINED |

Evidence must not migrate upward merely because a later artifact repeats the same statement.

In particular:

- public ≠ certified
- runnable ≠ verified
- numeric agreement ≠ proof
- repeated computation ≠ independent computation
- Lean source file ≠ Lean proof
- policy ALLOW ≠ mathematical truth
- matching outputs ≠ independence
- repository existence ≠ reproduction

---

## CLAIMLOCK

`source/python/claimlock.py` is a policy evaluator. It answers:

> Does this evidence set satisfy this promotion policy?

It does not answer:

> Is the mathematical claim true?

That distinction is fundamental. `policy decision ≠ mathematical truth`.

---

## Reproduction provenance

AQARION uses a reproduction-object model with separate predicates:

`CLAIM`, `SPECIFICATION`, `SOURCE`, `IMPLEMENTATION`, `FIXTURE`, `EXECUTION`, `OUTPUT`, `COMPARISON`, `INDEPENDENCE`, `FORMAL STATUS`, `DRIFT`.

A reproduction requires execution, binding, and output agreement.
An independent reproduction additionally requires an independent basis.
Formalization and proof are separate evidence dimensions.

---

## Verification entry point

Run the fail-closed runner:

```bash
python3 verification/run-all.py \
  --manifest verification/manifest.json \
  --receipt verification/receipts/run_all_receipt.json
```

The runner never treats NOT_IMPLEMENTED as PASS. A missing registered artifact is a failure, not a silent success.

---

Registered verification manifest

Canonical manifest: verification/manifest.json
Schema: AQARION-VERIFICATION-MANIFEST-1
Status: ACTIVE_ADVERSARIAL

The manifest is the authoritative registry of checks participating in the current semantic promotion boundary. The promotion rule requires:

· all registered checks to pass,
· required executable artifacts to be present,
· NOT_IMPLEMENTED to be treated as failure,
· missing artifacts to be treated as failure,
· external fallback paths to be forbidden,
· an independent oracle to be present,
· a mutation suite to be present.

Currently registered checks

ID Executable Scope
AQ-S14-SEMANTIC-K3 verification/aq_s14/aq_s14_semantic_suite.py K3 forest/incidence semantic suite
AQ-CONTRACT-OBJECT-OPERATOR verification/aq_contract/aq_contract_semantic_suite.py Frozen object/operator semantics: Koopman orientation, arbitrary-map transport, raw image-block distinction, T_* equivalence generation
AQ-ORACLE-EXHAUSTIVE-N4 verification/aq_oracle/aq_independent_oracle_suite.py Every deterministic map and every partition for \|X\| ≤ 4
AQ-MUTATION-SEMANTIC verification/aq_mutation_suite.py Registered semantic mutations

Explicitly excluded until bound

Excluded checks are not equivalent to passing checks. They are declared unbound regions of the verification boundary.

ID Reason
K2R-PARAMETRIC Fixture present; no executable verifier bound.
BETA-ENVELOPE No independent executable verifier bound.
SV-001-V2 See next section — status depends on whether the executable package is committed at this revision.

Verify before committing: the exact filename of the AQ-MUTATION-SEMANTIC executable. Two candidates appear in this repository's own documentation: verification/aq_mutation_suite.py and verification/aq-mutation-suit.py. Only one exists on disk, and the manifest must match it exactly.

---

SV-001-V2 — Cyclic block-shift defect (1176-case replay contract)

Canonical domain:

```
m ∈ {2,…,8},  k ∈ {2,…,8},  s ∈ {1,…, m·k − 1}
```

Total cases: 1176.
Zero-remainder (s mod k = 0): 196.
Nonzero-remainder: 980.

The historical 5720-case domain is deprecated. It must not appear as an active execution count in any verifier, CI step, or manifest.

Contract

Let n = m·k, r = s mod k, α² = r(k−r)/k², Q = U Uᵀ, D = (I − Q) K Q, and S the m×m cyclic shift. Then

```
Uᵀ Dᵀ D U      = α² (2I − S − Sᵀ)
tr(Uᵀ Dᵀ D U)   = 2 m α²
‖D‖₂            = 2 √(α²)              if m even
‖D‖₂            = 2 √(α²) cos(π / 2m)  if m odd
```

Package layout (declared)

```
verification/sv-001-v2/contract.json
verification/sv-001-v2/oracle.py
verification/sv-001-v2/verifier.py
verification/sv-001-v2/replay.py
verification/sv-001-v2/mutation/executor.py
verification/sv-001-v2/mutation/metamorphic.py
verification/sv-001-v2/receipt/schema.json
verification/sv-001-v2/receipt/writer.py
.github/workflows/sv-001-v2.yaml
claims/sv-001-v2.json
aqarion.toml
```

Receipt policy

Receipts are runtime artifacts. They are written to artifacts/SV-001-V2/ by the workflow and are uploaded as CI artifacts. They are not committed. A committed receipt/latest.json would violate the repository receipt policy and is rejected by verification/repo_self_audit.py.

Evidence state

· Evidence class: [V] finite computational replay.
· Independence: the oracle uses closed-form contract identities; the verifier constructs U, Q, K, D directly and does not call the oracle for answers. This is implementation-route independence within one repository. It is not external independent reproduction.
· Formal status: LEAN OPEN.
· C4: BLOCKED.
· Publication: BLOCKED.

A green run of sv-001-v2.yaml establishes finite computational evidence over the declared 1176-case domain only. It does not establish a universal theorem, a Lean proof, or C4 promotion.

---

AQ-SM-003-MATRIX — Block-transition defect geometry

For a partition Π = {B₁,…,B_q} with |B_i| = p_i and transition counts m_ij = #{x ∈ B_i : T(x) ∈ B_j}:

```
‖D‖_F²  =  Σ_{i,j}  (m_ij / p_j) (1 − m_ij / p_i)
rank(D) ≤ q − 1
G_Π = Uᵀ Dᵀ D U = Σ_i p_i · Cov_{a_i}(z),   a_ij = m_ij / p_i
```

Two-block specialization:

```
‖D‖_F² = [ b(p − b)/p + c(q − c)/q ] [ 1/p + 1/q ]
```

S14 specialization (p = 4, q = 1):

```
‖D‖_F² = 5 b (4 − b) / 16
```

Values: b = 1 → 15/16, b = 2 → 5/4, b = 3 → 15/16.
Realization counts: 256, 96, 16. Total: 368.

Evidence class: [D] derivation + [V] finite checks. Lean OPEN. C4 BLOCKED.
Full derivation: docs/research/AQ-SM-003-MATRIX.md.

---

K2R closure-stabilization replay

Independent computational replay of the K2R closure family.

Fixtures:

```
verification/k2r/fixtures/AQ-K2R-R2.json
verification/k2r/fixtures/AQ-K2R-R3.json
verification/k2r/fixtures/AQ-K2R-R5.json
verification/k2r/fixtures/AQ-K2R-R15.json
```

Verifier: verification/k2r/verify.py

```bash
python3 verification/k2r/verify.py
```

The verifier reconstructs objects from r rather than importing a mathematical implementation from another AQARION repository.

Recorded computational results for the tested fixtures:

```
h_min(P) = 2
h_min(Q) = r
h_min(M) = 2r
h_min(U) = 1
Δ        = −(r − 1)
```

Evidence status: RECONSTRUCTED_INDEPENDENT_COMPUTATION. Not Lean-certified. The fixture boundary and verifier implementation must remain visible when these results are cited.

Three-orbit-term negative control

The closure certificate defines "three orbit terms" as R ∨ T(R) ∨ T²(R). This is not the same as three recurrence applications — the distinction already matters for r = 2. The verifier checks both the three-orbit-term result and full orbit closure separately.

Canonicalization

The K2R certificate manifest declares RFC 8785 JSON Canonicalization Scheme (JCS) as the intended canonical serialization contract.

json.dumps(sort_keys=True, …) is deterministic JSON. It is not automatically RFC 8785 JCS. Deterministic serialization must not be described as RFC 8785 compliance unless a conforming implementation has been established.

---

Two-application federation architecture

Role URL
Public federation hub https://aqarion-federation-hub--quantarion9.replit.app
Certificate / evidence service https://quantarion-federation-hub--aqarionaaron.replit.app

These two roles must remain explicit in machine-readable metadata. A single ambiguous liveAppUrl field must not represent both.

---

Cross-repository policy

The hub declares sibling repositories and their pinned commits.

A pinned commit is a dependency statement. It does not mean the referenced repository is current, correct, or mathematically certified. It identifies a specific revision.

---

AI and provenance

AQARION does not claim its infrastructure can determine whether a human or an AI produced a particular mathematical idea.

The relevant provenance questions are: What claim was evaluated? What specification was used? What source revision was executed? What implementation ran? What input was used? What output was produced? What comparison was performed? Was independence established? Was a formal proof artifact checked?

AI-assisted activity can be recorded in the provenance graph where known. That provenance does not itself establish mathematical truth.

---

Reproducibility hierarchy

```
CLAIMED
  → AVAILABLE
    → EXECUTED
      → REPRODUCED
        → INDEPENDENTLY REPRODUCED
          → FORMALIZED
            → PROVED
```

Each stage requires its own evidence. A repository being public is not an independent reproduction. Agreement between two programs that share the same semantic construction is not independence.

---

What a green CI result means

A green CI result means only what the executed workflow actually checked, for that specific repository revision.

It does not establish: that all AQARION mathematics is correct, that any conjecture is proved, that all repositories are synchronized, that external dependencies are correct, or that all possible implementations are correct.

CI is an evidence mechanism, not an oracle for mathematical truth.

---

Publication gate

Publication status is deliberately separated from computational status.

· A computational replay may establish RECONSTRUCTED_INDEPENDENT_COMPUTATION without changing a publication gate.
· CI PASS does not imply PUBLICATION APPROVED.
· PROMOTION POLICY SATISFIED does not imply MATHEMATICAL THEOREM PROVED.

Current gate: BLOCKED.

---

Repository layout

```
.github/
  workflows/
    aqarion-ci.yml
    sv-001-v2.yaml
    verify.yml
    readme.md

api/
claims/
  sv-001-v2.json

docs/
  discovery/
    SV001-V2.md
  research/
    AQ-SM-003-MATRIX.md
  markdowns/
  checkpoints/
  logs/
  scripts/

objects/
pdf/
projects/
schemas/
skills/
source/
  python/
    claimlock.py

verification/
  manifest.json
  run-all.py
  replay-harness.py
  provenance.py
  repo_self_audit.py
  requirements.txt
  aq_s14/
  aq_contract/
  aq_oracle/
  aq-mutation-suit.py
  k2r/
    verify.py
    fixtures/
  receipts/
  sv-001-v2/
    contract.json
    oracle.py
    verifier.py
    replay.py
    mutation/
      executor.py
      metamorphic.py
    receipt/
      schema.json
      writer.py
```

Path names above marked from the repository's own documentation. Verify each against the live tree before citing. In particular, the mutation-suite filename appears in this repository's own documentation under two spellings; only one is correct.

---

Minimal local verification procedure

From the repository root:

```bash
python3 -m compileall -q verification
python3 verification/aq_s14/aq_s14_semantic_suite.py
python3 verification/aq_contract/aq_contract_semantic_suite.py
python3 verification/aq_oracle/aq_independent_oracle_suite.py
python3 verification/aq_mutation_suite.py
python3 verification/sv-001-v2/verifier.py
python3 verification/sv-001-v2/mutation/executor.py
python3 verification/sv-001-v2/mutation/metamorphic.py
python3 verification/sv-001-v2/replay.py --receipt artifacts/SV-001-V2/receipt.json
python3 verification/run-all.py \
  --manifest verification/manifest.json \
  --receipt verification/receipts/run_all_receipt.json
```

A successful local run must not be described as a successful CI run unless the CI workflow itself executed the same required verification. A successful local run must not be described as a universal mathematical proof.

---

Anti-overclaiming rules

Documentation must avoid:

· "verified" when the result was only computed once.
· "proved" when the result was only exhaustively checked for |X| ≤ 4 or for 1176 cases.
· "independent" when the second implementation shares the same semantic construction.
· "RFC 8785 compliant" when the implementation is merely deterministic JSON.
· "certified" when the artifact has only passed a repository policy gate.

Precision of language is part of the verification system.

---

Verification Infrastructure — Current Audit Boundary


Governance: FROZEN AUDIT · NO PROMOTION · C4 BLOCKED · PUBLICATION BLOCKED


The canonical executable verification registry is:


verification/manifest.json



Current manifest:


AQARION-VERIFICATION-MANIFEST-1
version 1.4.0
status ACTIVE_ADVERSARIAL



The manifest currently contains seven registered executable checks:


AQ-S14-SEMANTIC-K3
AQ-CONTRACT-OBJECT-OPERATOR
AQ-ORACLE-EXHAUSTIVE-N4
AQ-MUTATION-SEMANTIC
SV-001-V2
SV-001-V2-MUTATION
SV-001-V2-METAMORPHIC



The manifest-bound mutation executable is:


verification/aq-mutation-suite.py



The manifest is authoritative for the executable filename. Documentation must not substitute another spelling.


Verification Documentation


The complete verification-directory documentation is:


verification/README.md



It defines:




the active verification boundary;


manifest semantics;


registered checks;


excluded checks;


fail-closed requirements;


receipt policy;


independence requirements;


mutation requirements;


AQ-S15 research-side verification;


anti-overclaiming rules;


runtime evidence classifications.




Manifest Binding Audit


The repository now includes:


verification/manifest_binding_audit.py



Identifier:


AQ-SIDE-PIVOT-002



This audit checks the binding between the active manifest and the executable filesystem without executing the registered checks.


Run:


python3 verification/manifest_binding_audit.py



A successful result is reported as:


RESULT=PASS



This audit is infrastructure evidence. Its existence does not itself modify the active seven-check manifest.


AQ-S15 Exact Bridge Audit


The repository also contains the research-side exact verifier:


verification/sv-001-v2/bridge_exact.py



Identifier:


AQ-S15-SIDE-PIVOT-002



It uses exact rational arithmetic and independently constructs the block-incidence matrix, projection, Koopman pullback, defect, and compressed operator.


It checks the finite identity:


A_actual = Wᵀ K W / k



against:


A_model = q S^b + p S^(b+1)



with:


s = b k + r
p = r/k
q = (k-r)/k
0 < r < k



and then checks:


AᵀA = I - p q L_m



and:


UᵀDᵀDU = p q L_m.



The audit uses exact Fraction arithmetic rather than floating-point numerical comparison.


Its finite execution domain is:


m = 2,...,20
k = 2,...,12
b = 0,...,m-1
r = 1,...,k-1



A successful execution is classified:


EXACT_FINITE_REPLAY



and explicitly retains the boundary:


NOT_A_UNIVERSAL_PROOF



Therefore this artifact must not be described as a universal proof merely because its finite exact checks pass.


Current Verification Rule


The repository distinguishes:


computed
verified computation
independent computation
formalized
proved



These are separate evidence states.


In particular:


CI PASS ≠ mathematical proof
finite exhaustive replay ≠ universal theorem
policy PASS ≠ mathematical truth
different scripts ≠ automatic independence
public artifact ≠ certification



Current Governance


The current governance boundary remains:


C3              OPEN
C4              BLOCKED
Lean            OPEN
Publication     BLOCKED
Promotion       BLOCKED



Adding verification infrastructure does not automatically change any of these states.


The repository remains under:


FROZEN AUDIT · NO PROMOTION · C4 BLOCKED · PUBLICATION BLOCKED



Canonical Verification Entry Point


The primary fail-closed runner remains:


python3 verification/run-all.py \
  --manifest verification/manifest.json \
  --receipt verification/receipts/run_all_receipt.json



The exact registered checks are determined by the manifest, not by an independently maintained README list.


For the full verification-directory specification, see:


verification/README.md



Evidence Boundary


The strongest permissible statement about any result is determined by the evidence actually generated.


A finite executable result establishes finite computational evidence over its tested domain.


A formal proof establishes a formal proposition only after the formal system actually checks that proof.


A provenance receipt establishes evidence concerning an execution.


A promotion gate establishes satisfaction of its stated policy conditions.


None of these categories may be silently substituted for another.


No fabricated receipts. No fabricated execution counts. No fabricated hashes. No promotion by repetition.


Final interpretation rule

The strongest statement that can safely be made about an AQARION result is determined by its actual evidence.

· A computation establishes computational evidence.
· An independent computation establishes stronger computational evidence.
· An exhaustive finite computation establishes exhaustive evidence over its declared finite domain — for SV-001-V2 this is 1176 cases.
· A formal proof establishes a mathematical proposition within its formal system.
· A provenance receipt establishes evidence about what was executed.
· A promotion gate establishes that an evidence policy was satisfied.

None of these may be silently substituted for another.

---

License

Apache 2.0. See LICENSE.

Primary pointers

· AQARION mathematical core: JASKSG9/AQARION-ARITHMETIC-FDS-FINITE-DYNAMICAL-SYSTEMS-
· Kaprekar spectral case study: JASKSG9/KAPREKAR-SPECTRAL-GEOMETRY
· AQARION Academy: huggingface.co/spaces/Quantarion9/AQARION-ACADEMY

```
