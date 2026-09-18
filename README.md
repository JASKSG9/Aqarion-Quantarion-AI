AQARION × QUANTARION AI is a research repository for finite dynamical systems, observable quotients, and Koopman defect operators, designed to reliably enforce strict claim-level evidence governance by strictly maintaining an absolute architectural separation between IDEA, COMPUTATION, REPLAY, FORMALIZATION, and CERTIFICATION across key workflows. · GitHub

Aqarions_Quantarion-AI, "License" (https://img.shields.io/badge/license-Apache--2.0-blue), "C3" (https://img.shields.io/badge/C3-OPEN-yellow), "C4" (https://img.shields.io/badge/C4-BLOCKED-red), "Lean" (https://img.shields.io/badge/Lean-OPEN-lightgrey), "SDS--002" (https://img.shields.io/badge/SDS--002-QUARANTINED-orange), "Publication" (https://img.shields.io/badge/publication-BLOCKED-red), "Promotable" (https://img.shields.io/badge/promotable-false-lightgrey)

Governance, policy, provenance, and cross-repository orchestration hub for the AQARION / Quantarion research corpus.

This repository is a hub, not a self-contained mathematical library.

It provides:
CLAIMLOCK policy evaluation.
Reproduction-object and provenance semantics.
Independent verification entry points.
Cross-repository dependency declarations.
Adversarial negative controls.
A public computational replay surface for selected AQARION claims.

It does not decide mathematical truth.

---
Current governance state, C3............. OPEN, C4............. BLOCKED, Lean........... OPEN, SDS-002........ QUARANTINED, Publication.... BLOCKED, Promotable..... false
No repository-level policy result is a mathematical proof.
No public application status is itself mathematical certification.
---

Evidence discipline
AQARION distinguishes: [D] DEFINED, [V] VERIFIED COMPUTATION, [P] PROVED, [PV] PROVED + VERIFIED, [C] CONJECTURE, [R] RESEARCH, [F] REFUTED / KILLED, [Q] QUARANTINED
Evidence must not migrate upward merely because a later artifact repeats the same statement.
In particular: public == certified NO, runnable == verified NO, numeric == proof NO, Lean file == Lean proof NO, policy ALLOW == truth NO, matching output == independence NO

---
CLAIMLOCK
"source/python/claimlock.py" is a policy evaluator. It answers: «Does this evidence set satisfy this promotion policy?» It does not answer: «Is the mathematical claim true?» That distinction is fundamental.

---
Reproduction provenance
AQARION uses a reproduction-object model with separate predicates: CLAIM, SPECIFICATION, SOURCE, IMPLEMENTATION, FIXTURE, EXECUTION, OUTPUT, COMPARISON, INDEPENDENCE, FORMAL STATUS, DRIFT
A reproduction requires execution, binding, and output agreement. Independent reproduction additionally requires an independent basis. Formalization and proof are separate evidence dimensions.

---
Verification entry point
Run: python3 verification/run-all.py --manifest verification/manifest.json --receipt verification/receipts/run_all_receipt.json
The runner is fail-closed. It never treats "NOT_IMPLEMENTED" as "PASS".

---
K2R closure-stabilization replay
The current hub contains an independent computational replay of the K2r closure family.
The fixtures are: verification/k2r/fixtures/AQ-K2R-R2.json, verification/k2r/fixtures/AQ-K2R-R3.json, verification/k2r/fixtures/AQ-K2R-R5.json, verification/k2r/fixtures/AQ-K2R-R15.json
The verifier is: verification/k2r/verify.py
Run: python3 verification/k2r/verify.py
The verifier reconstructs the objects from "r", rather than importing a mathematical implementation from another AQARION repository.
The current computational results include: h_min(P) = 2, h_min(Q) = r, h_min(M) = 2r, h_min(U) = 1, Delta = -(r-1) for the tested fixtures.
These are currently recorded as: RECONSTRUCTED_INDEPENDENT_COMPUTATION
They are not being represented here as Lean-certified theorems.

---
Three-orbit-term negative control
The closure certificate defines “three orbit terms” explicitly as: R ∨ T(R) ∨ T²(R)
This is not the same thing as three recurrence applications. The distinction matters already for "r = 2".
The K2R verifier therefore checks both: three-orbit-term result and full orbit closure separately.

---
Canonicalization
The K2R certificate manifest declares RFC 8785 JSON Canonicalization Scheme (JCS) as the intended canonical serialization contract.
A true JCS implementation is required for normative certificate generation.
Generic "json.dumps(sort_keys=True,...)" is deterministic JSON, but it is not itself evidence of RFC 8785 compliance.

---
Two-application federation architecture
PUBLIC FEDERATION HUB https://aqarion-federation-hub--quantarion9.replit.app
CERTIFICATE / EVIDENCE SERVICE https://quantarion-federation-hub--aqarionaaron.replit.app
These roles must be explicit in machine-readable metadata. A single ambiguous "liveAppUrl" field must not be used to represent both roles.

---
Cross-repository policy
The hub declares sibling repositories and their pinned commits. A cross-repository declaration is a dependency statement. It is not a proof that the referenced repository is current, correct, or mathematically certified. A pinned commit identifies a specific revision.

---
AI and provenance
AQARION does not claim that its infrastructure can determine whether a human or AI produced a particular mathematical idea.
The relevant provenance question is: What claim was evaluated? What specification was used? What source revision was executed? What implementation ran? What input was used? What output was produced? What comparison was performed? Was independence established? Was a formal proof artifact checked?
AI-assisted activity can be represented in the provenance graph where known. That provenance does not itself establish mathematical truth.

---
Reproducibility
A repository being public is not equivalent to an independent reproduction.
AQARION therefore distinguishes: AVAILABLE, EXECUTED, REPRODUCED, INDEPENDENTLY REPRODUCED, FORMALIZED, PROVED
Each requires its own evidence.

---
Publication gate
The current publication gate remains: BLOCKED
The K2R computational replay does not by itself change C4 or publication status.
Any eventual promotion must satisfy the applicable evidence policy and the underlying mathematical proof requirements.

---
AQARION Verification, Reproducibility, and Evidence Architecture
Purpose of this section
This section defines how AQARION distinguishes mathematical claims, executable verification, independent computation, adversarial testing, provenance, and formal proof.
The purpose is not merely to make computations runnable.
The purpose is to make it possible to determine, for a specific repository revision:
what was claimed; 2. what specification was intended; 3. what executable artifact was used; 4. what exact command was executed; 5. what finite domain was covered; 6. what independent oracle, if any, was used; 7. what adversarial controls were applied; 8. what output was actually observed; 9. what evidence status is justified; 10. and what remains unproved, unbound, or quarantined.
AQARION therefore treats reproducibility as an evidence discipline rather than as a synonym for "the code ran."

---
1. Evidence status model
| Label | Meaning |
| --- | --- |
| [D] DEFINED | The object, operator, specification, or claim has been explicitly defined. |
| [V] VERIFIED COMPUTATION | A stated executable computation has been successfully verified over its stated scope. |
| [P] PROVED | A mathematical proof has established the stated proposition. |
| [PV] PROVED + VERIFIED | Both a mathematical proof and an independently checkable computational verification are present. |
| [C] CONJECTURE | The statement remains a conjectural mathematical claim. |
| [R] RESEARCH | The statement is an active research result, observation, derivation, or investigation that has not been promoted to a stronger status. |
| [F] REFUTED / KILLED | A specific implementation, specification, mutation, or proposition has been falsified or killed by a registered counterexample/control. |
| [Q] QUARANTINED | The evidence exists but is intentionally prevented from receiving a stronger status until specified requirements are satisfied. |
These labels are evidence classifications. They are not decorative badges.
A result must not receive a stronger label merely because: it appears in a README; it appears in another repository; a public application displays it; a computation agrees with another computation; a file has been committed; a Lean file exists; a policy evaluator returns ALLOW; or an author reports that a result has been verified.
Evidence must be promoted only when the corresponding evidence requirement has actually been satisfied.

---
2. Core evidence principle
public!= certified
runnable!= verified
numeric agreement!= proof
repeated computation!= independent computation
Lean source file!= Lean proof
policy ALLOW!= mathematical truth
matching outputs!= independence
repository existence!= reproduction
These distinctions are fundamental to the AQARION verification architecture.
A computational result can be extremely strong evidence without being a mathematical theorem.
Likewise, a formal proof can establish a theorem without automatically establishing that a separate computational implementation correctly implements the theorem's intended objects.
The two evidence dimensions are therefore tracked separately.

---
Reproduction is an evidence object
AQARION treats a reproduction as a structured object rather than as a sentence such as "the result was reproduced."
The relevant evidence dimensions are: CLAIM, SPECIFICATION, SOURCE, IMPLEMENTATION, FIXTURE, EXECUTION, OUTPUT, COMPARISON, INDEPENDENCE, FORMAL STATUS, DRIFT
A valid reproduction record should make it possible to answer: What claim was evaluated? What specification was used? Which source revision was executed? Which implementation was executed? Which fixture or input was used? What exact command was run? Did the command actually execute? What was the exit status? What output was produced? What expected output was compared against it? Was the comparison exact? Was the reproduction independent? Was a formal proof artifact involved? Did the executed source differ from the declared source revision?
A reproduction claim without this binding is weaker than a reproduction whose source, executable, command, input, output, and revision are all explicitly identified.

---
Reproduction-status vocabulary
AQARION distinguishes the following states: AVAILABLE, EXECUTED, REPRODUCED, INDEPENDENTLY REPRODUCED, FORMALIZED, PROVED
These are not interchangeable.
AVAILABLE: An artifact exists and can potentially be inspected or executed. Availability alone is not verification.
EXECUTED: The declared executable was actually invoked. Execution alone is not proof.
REPRODUCED: The executable was run against the declared specification/input and the observed result agrees with the declared expected result under the applicable comparison rule.
INDEPENDENTLY REPRODUCED: The result has been reproduced using an independent computational basis. Agreement between two programs that share the same semantic construction is not automatically independence. Independence must be justified by the architecture of the second computation.
FORMALIZED: The mathematical object or proposition has been represented in a formal system. Formalization alone does not establish that the represented proposition is true.
PROVED: A formal or mathematical proof has actually established the proposition under the applicable proof system.

---
Independent computation
AQARION treats independence as a separate evidence dimension.
The following does not automatically constitute independent verification: implementation A -> implementation B -> same hidden helper, or implementation A -> same algorithm rewritten with different variable names, or production implementation -> test implementation -> same semantic construction
A stronger independent oracle uses a materially different construction. For example, a production computation may construct equivalence classes using union-find while an independent oracle constructs the corresponding connected components explicitly from an incidence graph and traverses that graph using DFS.
The objective is to make a shared implementation defect less likely to survive both computations.
Independence therefore concerns the basis of computation, not merely the fact that two files produced the same number.

---
Exhaustive finite verification
For finite domains, AQARION can distinguish exhaustive verification from sampling.
An exhaustive claim must specify: domain, enumeration method, case-generation rule, semantic construction, oracle construction, comparison rule, termination condition
For example, an exhaustive finite verification over deterministic maps on a finite set must identify the complete map space being enumerated.
If the set has cardinality n, the number of deterministic maps T : X -> X is: n^n
An exhaustive verification must account for all of those maps within the declared range.
Likewise, if every set partition is part of the verification domain, the partition enumeration must cover the complete partition space rather than a selected sample.
A finite exhaustive result is therefore always interpreted relative to its declared finite boundary.
For example: |X| <= 4 means exactly that. It does not mean: all finite sets and it does not by itself establish a universal theorem.

---
Registered verification manifest
The canonical verification manifest is: verification/manifest.json
The manifest currently declares schema: AQARION-VERIFICATION-MANIFEST-1 and version: 1.3.0 with status: ACTIVE_ADVERSARIAL
The manifest is the authoritative registry of the checks that participate in the repository's current semantic promotion boundary.
The current registered checks are: AQ-S14-SEMANTIC-K3, AQ-CONTRACT-OBJECT-OPERATOR, AQ-ORACLE-EXHAUSTIVE-N4, AQ-MUTATION-SEMANTIC, SV-001-V2
The manifest explicitly requires all registered checks to pass for promotion.
It also states that: NOT_IMPLEMENTED = FAILURE, missing artifact = FAILURE, external fallback = FORBIDDEN, independent oracle = REQUIRED, mutation suite = REQUIRED
Therefore, a missing verifier cannot silently disappear from the evidence chain by being treated as successful.

---
Registered check: AQ-S14-SEMANTIC-K3
Identifier: AQ-S14-SEMANTIC-K3, Executable: verification/aq_s14/aq_s14_semantic_suite.py, Scope: K3 forest/incidence semantic suite
This check is registered as a finite semantic verification. It is repository-local and does not require an external repository at execution time.

---
Registered check: AQ-CONTRACT-OBJECT-OPERATOR
Identifier: AQ-CONTRACT-OBJECT-OPERATOR, Executable: verification/aq_contract/aq_contract_semantic_suite.py
Scope: Frozen object/operator semantics: - Koopman orientation, - arbitrary-map transport, - raw image-block distinction, - T_* equivalence generation
This check exists to prevent a particularly dangerous class of verification failure: a program can produce plausible numerical results while silently implementing a different mathematical object from the one specified.
The contract suite therefore verifies semantics, not merely output formatting.

---
Registered check: AQ-ORACLE-EXHAUSTIVE-N4
Identifier: AQ-ORACLE-EXHAUSTIVE-N4, Executable: verification/aq_oracle/aq_independent_oracle_suite.py
Scope: Every deterministic map and every partition for |X| <= 4
The purpose of this check is independent finite verification.
The production-side calculation and oracle calculation use materially different constructions.
The oracle uses explicit graph connectivity / DFS reasoning rather than merely reusing the production equivalence-generation machinery.
The oracle also compares the resulting finite quantity against an exact matrix-rank computation.
This provides two independent semantic routes to the same finite result.
The boundary remains: |X| <= 4. The result must not be represented as a universal theorem merely because the finite verification is exhaustive within that boundary.

---
Registered check: AQ-MUTATION-SEMANTIC
Identifier: AQ-MUTATION-SEMANTIC, Executable: verification/aq_mutation_suite.py, Purpose: adversarial semantic mutation testing
Mutation testing asks a different question from ordinary regression testing.
A regression test asks: Does the intended implementation still produce the expected result?
A mutation test asks: Would a semantically wrong implementation be detected?
This is critical because a test suite can pass while failing to detect an important semantic error.
The registered mutation family includes controls for: Koopman orientation, defect placement, incidence construction
A registered mutation must be killed by the semantic suite. A mutation that survives is evidence of a verification weakness and must not be silently treated as harmless.

---
Why mutation testing is part of the promotion boundary
A verification suite that only confirms the correct implementation can be under-sensitive.
For example, suppose the intended construction is: D = Q K P with: Q = I - P
A test suite should not merely confirm that the correct construction works. It should also demonstrate that meaningful semantic substitutions fail.
Examples include: incorrect Koopman orientation, incorrect placement of P and Q, incorrect incidence construction
The purpose is not to prove that every possible bug will be detected. That would be an unjustified claim.
The purpose is to demonstrate that explicitly registered semantic errors are actually observable by the verification machinery.

---
Fail-closed verification
The AQARION runner is intentionally fail-closed.
The canonical entry point is: verification/run-all.py
Run it with: python3 verification/run-all.py \ --manifest verification/manifest.json \ --receipt verification/receipts/run_all_receipt.json
The runner is not permitted to interpret: NOT_IMPLEMENTED as: PASS
Likewise, a missing registered artifact must not silently become a successful check.
This prevents a common provenance failure in which an incomplete verification pipeline reports a green result merely because the missing component was never executed.

---
Verification receipt
The verification runner produces a machine-readable receipt.
The receipt records the execution result of the registered verification manifest.
The receipt is intended to bind the result to repository state rather than merely reporting: tests passed
A valid repository-level verification record should establish, where applicable: repository commit, repository tree, manifest identity, manifest hash, registered checks, individual check results, overall status
The receipt is therefore evidence about a particular execution of a particular repository state. It is not a permanent mathematical certificate merely because it exists.

---
Repository-state binding
AQARION treats repository state as part of reproducibility.
A statement such as: the verifier passed is incomplete without knowing: which verifier? which revision? which manifest? which source tree? which command? which inputs?
Consequently, promotion evidence should bind execution to the repository revision that was actually evaluated.
A later modification to the repository does not retroactively change what an earlier receipt proves.
Conversely, an old receipt does not automatically certify a newer repository state.

---
Provenance integrity versus mathematical truth
AQARION deliberately separates two questions: Provenance question (Did the declared artifact actually execute as claimed?) and Mathematical question (Is the mathematical proposition actually true?)
A provenance system can establish strong evidence that: source S at revision R was executed with command C on input I and produced output O without proving that the underlying mathematics is correct.
Likewise, a mathematical proof does not automatically prove that a separate software implementation faithfully realizes the same specification.
These are complementary evidence dimensions. They must not be conflated.

---
Formal proof boundary
AQARION does not treat the presence of a Lean file as proof.
The following distinctions remain explicit: Lean source exists!= Lean theorem checked!= the theorem states the intended proposition!= the theorem covers the computational implementation
Formal verification must therefore be evaluated according to the actual proof artifact and its relationship to the claimed proposition.
A computational result may remain: [V] VERIFIED COMPUTATION even when a corresponding theorem has not yet been formally proved. That is a deliberate and legitimate evidence state.

---
K2R closure-stabilization replay
AQARION also contains a computational replay of the K2R closure family.
Relevant fixtures are: verification/k2r/fixtures/AQ-K2R-R2.json, verification/k2r/fixtures/AQ-K2R-R3.json, verification/k2r/fixtures/AQ-K2R-R5.json, verification/k2r/fixtures/AQ-K2R-R15.json
The verifier is: verification/k2r/verify.py
Run: python3 verification/k2r/verify.py
The verifier reconstructs the relevant objects from r rather than importing a mathematical implementation from another AQARION repository.
The currently recorded computational results include: h_min(P) = 2, h_min(Q) = r, h_min(M) = 2r, h_min(U) = 1, Delta = -(r-1) for the tested fixtures.
These results are recorded as: RECONSTRUCTED_INDEPENDENT_COMPUTATION
They are not represented as Lean-certified theorems merely because the computation succeeds.
The fixture boundary and verifier implementation must remain visible when these results are cited.

---
Three-orbit-term negative control
The K2R closure certificate explicitly distinguishes: R ∨ T(R) ∨ T²(R) from three recurrence applications.
These are not automatically the same statement. The distinction matters even for small values such as: r = 2
The K2R verifier therefore treats the following as separate checks: three-orbit-term result and full orbit closure
This is an example of a semantic negative control: the verification system must distinguish two superficially similar but mathematically different interpretations.

---
Canonicalization and certificate identity
The K2R certificate manifest declares: RFC 8785 JSON Canonicalization Scheme (JCS) as the intended canonical serialization contract.
Deterministic JSON is not automatically RFC 8785 JCS.
For example: json.dumps(sort_keys=True) may provide deterministic serialization while still failing to implement all requirements of RFC 8785.
Therefore: deterministic serialization must not be described as: RFC 8785 compliance unless an actual conforming implementation has been established.
This distinction is important for cryptographic hashes, certificate identity, cross-language reproducibility, and provenance.

---
Cross-repository dependencies
AQARION is a hub rather than a self-contained mathematical library.
The hub can declare dependencies on sibling repositories and specific repository revisions.
A pinned commit means: this dependency refers to this exact repository revision. It does not mean: the referenced repository is mathematically correct and it does not mean: the referenced repository has been independently verified
Cross-repository references are therefore dependency declarations, not mathematical certificates.
Where reproducibility depends on an external repository, the dependency should be explicitly identified and pinned.
Where a verification is intended to be repository-local, external fallback paths should not be silently substituted.

---
External fallback prohibition
The semantic promotion boundary forbids external fallback paths for registered checks.
This means that if a registered verifier is declared to be: verification/example.py then the verification pipeline must not silently substitute: another repository, remote service, cached result, application endpoint, previous receipt, manual assertion for the missing executable.
The purpose is to prevent a repository from appearing reproducible while its actual committed verification machinery is incomplete.

---
Drift
AQARION treats drift as an explicit provenance condition.
Relevant forms include: source drift, specification drift, fixture drift, implementation drift, manifest drift, output drift, dependency drift
A previously valid receipt cannot automatically certify a modified source tree.
Likewise, a source revision cannot automatically certify a changed specification.
Reproduction therefore requires the evidence objects to remain properly bound.

---
What a green CI result means
A green CI result means only what the executed CI workflow actually checked.
For example, if CI verifies: compileall, manifest checks, oracle, mutation suite, receipt integrity then a successful run establishes evidence about those checks for that specific CI execution and repository revision.
It does not automatically establish: all AQARION mathematics is correct, all conjectures are proved, all repositories are synchronized, all external dependencies are correct, all possible implementations are correct
CI is therefore an evidence mechanism, not an oracle for mathematical truth.

---
What exhaustive verification does and does not establish
Suppose a computation exhaustively verifies a proposition over: all maps and all partitions for |X| <= 4
Then the supported statement is: the proposition was exhaustively checked over that finite domain, subject to the correctness and independence of the verification machinery.
It does not automatically establish: the proposition holds for every finite X.
The transition from finite computational evidence to a universal theorem requires a mathematical argument.
This distinction is especially important when empirical patterns suggest a closed formula.
Observed finite agreement is evidence for the conjecture. It is not itself a proof of the universal formula.

---
Mathematical claim lifecycle
AQARION uses the following conceptual lifecycle: IDEA -> DEFINED -> IMPLEMENTED -> COMPUTATIONALLY TESTED -> VERIFIED OVER DECLARED FINITE SCOPE -> +------> INDEPENDENTLY VERIFIED -> FORMALLY SPECIFIED -> FORMALLY PROVED -> PROMOTION-ELIGIBLE
Not every claim must pass through every stage in the same order.
However, evidence must not be represented as though a later stage has been reached when only an earlier stage has been established.

---
What AQARION does not claim
AQARION does not claim that its infrastructure can determine: whether an idea was created by a human, whether an idea was created by an AI, whether a result is true merely because it is public, whether two implementations are independent merely because their outputs agree, whether a computational result is a theorem
The provenance system instead records what can actually be evidenced.
For AI-assisted research, provenance may record known AI involvement, human involvement, executable artifacts, revisions, commands, and outputs.
Provenance does not determine authorship of mathematical insight.

---
AI-assisted research provenance
Where AI-assisted development is known, AQARION can record provenance around: claim, specification, source revision, implementation, execution, output, comparison, independence, formal verification
The relevant question is not: "Was AI involved?" as a substitute for mathematical evidence.
The relevant reproducibility questions are: What was produced? What was committed? What was executed? What was verified? What was independently reproduced? What was formally proved?
The provenance architecture therefore focuses on observable evidence rather than unverifiable authorship inference.

---
Promotion gate
Promotion is a policy decision over evidence. It is not a mathematical theorem.
A promotion policy may require: all registered checks PASS, required executable artifacts present, manifest bound to repository state, receipt bound to manifest, independent oracle present, registered mutations killed, no forbidden external fallback
Satisfying those requirements means that the evidence set satisfies the defined promotion policy. It does not mean that the policy evaluator has mathematically proven the claim.
This distinction is fundamental: policy decision!= mathematical truth

---
Current registered semantic boundary
The current manifest registers five semantic checks:
AQ-S14-SEMANTIC-K3
AQ-CONTRACT-OBJECT-OPERATOR
AQ-ORACLE-EXHAUSTIVE-N4
AQ-MUTATION-SEMANTIC
SV-001-V2 — uniform-block koopman defect reduced-gram identity — 1176-case replay contract (196 zero-r, 980 nonzero-r, 5/5 mutations killed, receipt hash-bound)
The current manifest also explicitly identifies checks that are excluded until their executable bindings exist: K2R-PARAMETRIC, BETA-ENVELOPE
An excluded check is not equivalent to a passing check. It is an explicitly unbound portion of the verification boundary. This prevents incomplete infrastructure from being mistaken for completed verification.
SV-001-V2 status: REPLAYABLE DESIGN / C4 BLOCKED — contract verification/sv-001-v2/contract.json, verifier verification/sv-001-v2/verifier.py, oracle verification/sv-001-v2/oracle.py, replay verification/sv-001-v2/replay.py, mutation verification/sv-001-v2/mutation/executor.py (5/5 killed), metamorphic verification/sv-001-v2/mutation/metamorphic.py, receipt verification/sv-001-v2/receipt/latest.json — canonical domain 1176 (deprecated 5720 quarantined).

---
SV-001-V2 1176-case replay contract
Identifier: SV-001-V2, Executable: verification/sv-001-v2/replay.py, Contract: verification/sv-001-v2/contract.json
Domain: m=2..8, k=2..8, s=1..m*k-1 — 1176 total cases (196 zero-r where s mod k = 0, 980 nonzero-r), deprecated 5720 is historical governance mismatch quarantined
Identity:
n = m*k
r = s mod k
alpha^2 = r(k-r)/k^2
Q = U U^T where U is normalized uniform block-indicator (m blocks, k per block)
K = cyclic shift by s: K[x,(x+s) mod n] = 1
D = (I-Q) K Q
Reduced gram: U^T D^T D U = alpha^2 (2I - S - S^T) where S is cyclic shift on m
Trace: trace(U^T D^T D U) = 2*m*alpha^2
Norm even m: ||D|| = 2 sqrt(alpha^2)
Norm odd m: ||D|| = 2 sqrt(alpha^2) cos(pi/(2m))
Verification:
verifier.py — 1176/1176 PASS, max_gram 5.55e-16, max_trace 4.44e-15, max_norm 5.55e-16, finite_outputs true
mutation/executor.py — suite aq-ml-adversary-003 — 5/5 KILLED: wrong_gram, wrong_trace, wrong_norm, nan, wrong_case_count
metamorphic.py — METAMORPHIC_PASS 1176-domain: zero-r periodicity and r symmetry
replay.py — generates receipt with hash binding contract_sha256, verifier_sha256, oracle_sha256 — receipt schema ARC-1.0
Governance: C4 BLOCKED, promotion false, replayable_not_c4 — local replay is not public CI, public CI must replay independently — exact false, independent oracle true
Evidence: RECONSTRUCTED_INDEPENDENT_COMPUTATION over finite domain 1176, not Lean proof, not publication certificate, computational replay surface only
Lowercase canonical tree (no uppercase boulders):
verification/sv-001-v2/contract.json
verification/sv-001-v2/oracle.py
verification/sv-001-v2/verifier.py
verification/sv-001-v2/replay.py
verification/sv-001-v2/mutation/executor.py
verification/sv-001-v2/mutation/metamorphic.py
verification/sv-001-v2/receipt/schema.json
verification/sv-001-v2/receipt/writer.py
.github/workflows/sv-001-v2.yml — name sv-001-v2 replay contract (exact hyphenated id)
claims/sv-001-v2.json — cases 1176, deprecated 5720 quarantined
aqarion.toml — claim.sv-001-v2 points to lowercase paths, canonical_domain 1176

---
Minimal local verification procedure
From the repository root, the intended local verification sequence is:
python3 -m compileall -q verification
python3 verification/aq_s14/aq_s14_semantic_suite.py
python3 verification/aq_contract/aq_contract_semantic_suite.py
python3 verification/aq_oracle/aq_independent_oracle_suite.py
python3 verification/aq_mutation_suite.py
python3 verification/sv-001-v2/verifier.py
python3 verification/sv-001-v2/mutation/executor.py
python3 verification/sv-001-v2/mutation/metamorphic.py
python3 verification/sv-001-v2/replay.py
python3 verification/run-all.py --manifest verification/manifest.json --receipt verification/receipts/run_all_receipt.json
The commands should be executed against the intended repository revision.
A successful local run should not be described as a successful CI run unless the CI workflow itself executed the same required verification.
Likewise, a successful local run should not be described as a universal mathematical proof.

---
Expected independent-oracle scope
The exhaustive independent-oracle suite covers: all deterministic maps, all partitions, |X| <= 4
The important distinction is between: exhaustive within the declared finite boundary and universal over all finite systems
Only the first is established by an exhaustive |X| <= 4 computation. A universal theorem requires a separate mathematical argument.

---
Adversarial verification philosophy
AQARION uses adversarial verification because correctness-only testing is insufficient for high-assurance mathematical software.
The verification process should actively attempt to expose: orientation errors, operator-order errors, incorrect quotient construction, incorrect image semantics, incorrect incidence construction, shared implementation assumptions, fixture interpretation errors, serialization ambiguities, repository drift, missing executable bindings
A verification suite becomes stronger when it demonstrates not only that the intended implementation passes, but also that meaningful incorrect implementations fail.

---
Reproducibility hierarchy
The following hierarchy is useful when interpreting AQARION evidence:
CLAIMED -> AVAILABLE -> EXECUTED -> REPRODUCED -> INDEPENDENTLY REPRODUCED -> FORMALIZED -> PROVED
This is not a universal ranking of scientific quality. It is a distinction between different kinds of evidence.
For a particular claim, some stages may be applicable while others are not.
The repository must state which stage is actually supported.

---
Anti-overclaiming rules
AQARION documentation should avoid statements such as: "verified" when what was actually established is only: "computed once"
Likewise, avoid: "proved" when the result is only: "exhaustively checked for |X| <= 4" or "exhaustively checked for 1176 cases"
Avoid: "independent" when the second implementation shares the same semantic construction.
Avoid: "RFC 8785 compliant" when the implementation is merely deterministic JSON.
Avoid: "certified" when the artifact has only passed a repository policy gate.
Precision of language is part of the verification system.

---
Publication boundary
Publication status is deliberately separated from computational status.
A computational replay may establish: RECONSTRUCTED_INDEPENDENT_COMPUTATION without changing a publication gate.
Similarly: CI PASS does not automatically imply: PUBLICATION APPROVED and PROMOTION POLICY SATISFIED does not automatically imply: MATHEMATICAL THEOREM PROVED
Publication decisions remain subject to their own evidence requirements.

---
Current governance interpretation
The repository currently distinguishes governance state from mathematical state.
The governance labels appearing in this repository should therefore be read as infrastructure/policy states. They are not mathematical truth labels.
In particular: C3 OPEN, C4 BLOCKED, Lean OPEN, SDS-002 QUARANTINED, Publication BLOCKED, Promotable false should not be interpreted as mathematical propositions.
They describe the current governance/promotion boundary.
SV-001-V2: REPLAYABLE DESIGN / C4 BLOCKED — 1176-case computational replay verified locally, independent oracle true, 5/5 mutations killed, not promoted, not publication certificate.

---
Repository architecture at a glance
The main repository functions as a governance and reproducibility hub.
Conceptually: AQARION HUB -> CLAIM / POLICY, VERIFICATION, PROVENANCE -> S14, CONTRACT, ORACLE, MUTATION, SV-001-V2 -> REPRODUCTION -> PROMOTION GATE -> PUBLICATION BOUNDARY
Each layer has a different responsibility. No layer should silently impersonate another.

---
Canonical verification principle
The central AQARION principle is: > Every promoted computational claim must be bound to an explicit specification, executable artifact, repository revision, execution record, comparison rule, and applicable independence evidence.
Where formal proof exists, it is tracked separately. Where only computation exists, the result remains computational evidence. Where only a claim exists, it remains a claim. Where an artifact is missing, it remains missing. Where a mutation survives, that weakness remains visible. Where a result has not been proved, the documentation must not call it proved.

---
Final interpretation rule
The strongest statement that can safely be made about an AQARION result is determined by its actual evidence.
In particular: A computation can establish computational evidence. An independent computation can establish stronger computational evidence. An exhaustive finite computation can establish exhaustive evidence over its declared finite domain — for SV-001-V2 this is 1176 cases (m=2..8, k=2..8, s=1..m*k-1). A formal proof can establish a mathematical proposition within its formal system. A provenance receipt can establish evidence about what was executed. A promotion gate can establish that an evidence policy was satisfied.
None of these should be silently substituted for another.
AQARION therefore treats reproducibility, independence, formalization, provenance, and mathematical proof as distinct but complementary components of a high-assurance research record.

---
License
Apache 2.0. See "LICENSE".

---
Primary pointers
AQARION mathematical core: "JASKSG9/AQARION-ARITHMETIC-FDS-FINITE-DYNAMICAL-SYSTEMS-"
Kaprekar spectral case study: "JASKSG9/KAPREKAR-SPECTRAL-GEOMETRY"
AQARION Academy: "huggingface.co/spaces/Quantarion9/AQARION-ACADEMY"
