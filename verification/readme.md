AQARION Verification Infrastructure


Repository: JASKSG9/Aqarion-Quantarion-AI

Directory: verification/

Governance: FROZEN AUDIT · NO PROMOTION · C4 BLOCKED · PUBLICATION BLOCKED



1. Purpose


This directory is the executable verification and adversarial-audit surface for the AQARION / Quantarion research corpus.


It provides:




executable semantic checks;


exact finite-domain verification;


independent-oracle comparisons;


adversarial mutation checks;


metamorphic checks;


verification manifests;


fail-closed orchestration;


provenance and receipt infrastructure;


repository self-audit infrastructure;


isolated research-side verification artifacts.




The verification layer is an evidence mechanism.


It is not a mathematical oracle.


A passing executable check establishes only the proposition and finite domain that the executable actually checks.



2. Governance State


The current governance boundary is:




Gate
State




C3
OPEN


C4
BLOCKED


Lean
OPEN


Publication
BLOCKED


Promotion
BLOCKED




The repository must not silently promote:




computed results to theorems;


executable replay to formal proof;


deterministic serialization to RFC 8785 compliance;


repeated computation to independent reproduction;


repository policy approval to mathematical truth.





3. Evidence Discipline


AQARION uses the following evidence labels:




Label
Meaning




[D]
DEFINED


[V]
VERIFIED COMPUTATION


[P]
PROVED


[PV]
PROVED + VERIFIED


[C]
CONJECTURE


[R]
RESEARCH


[F]
REFUTED / KILLED


[Q]
QUARANTINED




The following distinctions are mandatory:


public              ≠ certified
runnable            ≠ verified
numeric agreement   ≠ proof
repeated computation ≠ independent computation
Lean source         ≠ Lean proof
policy PASS         ≠ mathematical truth
matching outputs    ≠ independence
repository exists   ≠ reproduction



A receipt records an execution event.


A receipt does not, by itself, establish the mathematical truth of the proposition being tested.



4. Canonical Verification Manifest


The canonical registry is:


verification/manifest.json



Current manifest:


schema:  AQARION-VERIFICATION-MANIFEST-1
version: 1.4.0
status:  ACTIVE_ADVERSARIAL



The manifest currently registers seven executable checks.


Registered checks




ID
Executable




AQ-S14-SEMANTIC-K3
verification/aq_s14/aq_s14_semantic_suite.py


AQ-CONTRACT-OBJECT-OPERATOR
verification/aq_contract/aq_contract_semantic_suite.py


AQ-ORACLE-EXHAUSTIVE-N4
verification/aq_oracle/aq_independent_oracle_suite.py


AQ-MUTATION-SEMANTIC
verification/aq-mutation-suite.py


SV-001-V2
verification/sv-001-v2/verifier.py


SV-001-V2-MUTATION
verification/sv-001-v2/mutation/executor.py


SV-001-V2-METAMORPHIC
verification/sv-001-v2/mutation/metamorphic.py




The manifest is authoritative for registered executable paths.


Documentation must not substitute another filename for a manifest-bound executable.


In particular, the registered mutation path is:


verification/aq-mutation-suite.py



Do not silently rename it in documentation or execution commands.



5. Manifest Promotion Rules


The current manifest requires:


pass_requires_all_registered_checks = true
not_implemented_is_failure = true
missing_artifact_is_failure = true
external_fallback_paths_forbidden = true
independent_oracle_required_for_semantic_promotion = true
mutation_suite_required_for_semantic_promotion = true



Therefore:




A missing executable is a failure.




It is not a successful skip.


Likewise:




NOT_IMPLEMENTED is a failure.




It is not a successful placeholder.



6. Explicitly Excluded Checks


The manifest currently records two excluded regions:


K2R-PARAMETRIC


verification/fixtures/k2r-family.json



The fixture is present, but no executable verifier is currently bound to it in the active manifest.


BETA-ENVELOPE


No independent executable verifier is currently bound.


Excluded does not mean passed.


Excluded means outside the currently registered executable boundary.



7. Verification Orchestrator


Primary runner:


verification/run-all.py



Canonical invocation:


python3 verification/run-all.py \
  --manifest verification/manifest.json \
  --receipt verification/receipts/run_all_receipt.json



The runner is intended to fail closed.


A successful runner invocation means that the registered checks accepted by that particular execution completed according to the runner's actual logic.


It does not mean:


all AQARION mathematics is proved



and it does not mean:


C4 is satisfied



or:


publication is approved




8. Manifest Binding Audit


Additional audit infrastructure:


verification/manifest_binding_audit.py



Identifier:


AQ-SIDE-PIVOT-002



Purpose:




verify that manifest.json parses;


verify that registered check IDs are unique;


verify that every registered command is a valid argv list;


verify Python script paths exist;


verify registered path case exactly;


verify generic executables resolve.




This audit does not execute the registered verification checks.


It audits the binding between the manifest and the executable filesystem.


Run:


python3 verification/manifest_binding_audit.py



Expected successful classification:


RESULT=PASS



This artifact is deliberately not automatically added to the seven-check manifest merely by existing.


Its execution status must be established by an actual runtime execution.



9. AQ-S15 Exact Compressed-Bridge Audit


Additional research-side verifier:


verification/sv-001-v2/bridge_exact.py



Identifier:


AQ-S15-SIDE-PIVOT-002



This verifier uses exact rational arithmetic via Python Fraction.


It independently constructs:


W  = block-incidence matrix
Q  = W Wᵀ / k
K  = Koopman pullback permutation
D  = (I-Q) K Q



and the compressed operator:


A_actual = Wᵀ K W / k



It compares that exact operator against:


A_model = q S^b + p S^(b+1)



for:


s = b k + r
p = r/k
q = (k-r)/k
0 < r < k



It then checks:


AᵀA = I - p q L



and:


UᵀDᵀDU = p q L



using exact rational arithmetic.


The deterministic audit domain is:


m = 2,...,20
k = 2,...,12
b = 0,...,m-1
r = 1,...,k-1



The verifier calculates and prints the actual number of cases at runtime.


No case count is hard-coded into the reported result.


Run:


python3 verification/sv-001-v2/bridge_exact.py



A successful run reports:


RESULT=PASS
CLASSIFICATION=EXACT_FINITE_REPLAY
CLAIM_BOUNDARY=NOT_A_UNIVERSAL_PROOF



The last line is intentional.


This verifier provides finite exact computational evidence.


It does not constitute a universal theorem proof.



10. AQ-S15 Bridge Contract


The exact bridge being tested is:


s = b k + r

p = r/k
q = (k-r)/k

A_actual = Uᵀ K U
         = Wᵀ K W / k

A_model  = q S^b + p S^(b+1)



followed by:


Aᵀ A = I - p q L_m



and:


UᵀDᵀDU = p q L_m.



The associated spectral residual is:


2I - S - S⁻¹.



For:


α² = p q = r(k-r)/k²,



the expected singular-value expression is:


σ_ℓ(D) = 2 α sin(πℓ/m)



for the corresponding nonzero Fourier modes.


The executable bridge verifier checks the finite algebraic identities directly.


It does not replace a formal proof.



11. Orientation Requirement


The Koopman convention must remain explicit.


For the pullback convention:


(Kf)(x) = f(T(x))



and:


T(x) = x+s,



the implementation constructs the corresponding permutation matrix directly.


The compressed operator is not allowed to be replaced by a guessed transpose or reversed shift convention.


In particular, documentation must not silently change:


S



to:


Sᵀ



or interchange:


b



and:


-b



without changing the stated convention and re-running the exact audit.



12. SV-001-V2


The registered finite verification package is:


verification/sv-001-v2/
├── contract.json
├── oracle.py
├── verifier.py
├── replay.py
├── mutation/
│   ├── executor.py
│   └── metamorphic.py
└── receipt/
    ├── schema.json
    └── writer.py



The active manifest registers:


verifier.py
mutation/executor.py
mutation/metamorphic.py



The package's finite replay evidence must remain described as finite computational evidence.


A green finite replay is not a universal theorem.



13. Receipts


Receipts are runtime evidence artifacts.


They must not be fabricated.


A receipt should identify, where supported by the executing infrastructure:




repository revision;


executable;


manifest;


input;


execution;


output;


comparison;


result;


timestamp;


relevant hashes.




A receipt must describe what actually happened.


Do not manually manufacture a receipt claiming a run that did not occur.


Do not copy an old receipt forward as evidence for a new revision.



14. Independence


AQARION distinguishes several forms of independence.


Two programs can be operationally different while still sharing:




the same mathematical construction;


the same fixture;


the same generated data;


the same implementation assumption;


the same semantic orientation.




Therefore:


different code



does not automatically imply:


independent reproduction



An independent-oracle check is stronger when the oracle is constructed from a genuinely different computational route.


The repository must state the actual independence boundary rather than using the word "independent" as a generic synonym for "separate script."



15. Mutation Testing


Mutation checks are adversarial controls.


Their purpose is to demonstrate that verification infrastructure can reject deliberately incorrect constructions.


Examples of relevant semantic mutations include:




reversed Koopman orientation;


incorrect defect placement;


incorrect incidence construction;


altered transition semantics;


invalid block interpretation.




A mutation suite is evidence about the sensitivity of the verification system.


It is not itself proof of the underlying mathematical theorem.



16. Compile / Syntax Check


A syntax-level check can be performed with:


python3 -m compileall -q verification



This establishes only that Python source files successfully compile under the interpreter used for that execution.


It does not establish:


mathematical correctness



or:


semantic correctness



or:


formal proof




17. Recommended Verification Order


For a local audit, use the following order.


Step 1 — verify manifest bindings


python3 verification/manifest_binding_audit.py



Step 2 — compile the verification tree


python3 -m compileall -q verification



Step 3 — execute the registered checks


Use the canonical runner:


python3 verification/run-all.py \
  --manifest verification/manifest.json \
  --receipt verification/receipts/run_all_receipt.json



Step 4 — execute the AQ-S15 bridge audit separately


python3 verification/sv-001-v2/bridge_exact.py



The AQ-S15 bridge audit remains separate until its scope, semantics, runtime result, and governance status have been reviewed.



18. What Must Not Be Claimed


The following statements are prohibited unless independently established by the corresponding evidence:


"The theorem is proved."



from a finite computation.


"The result is Lean certified."



from a Python verifier.


"The repository is mathematically certified."



from a passing CI workflow.


"The result is independently reproduced."



merely because two scripts produce the same output.


"RFC 8785 compliant."



when only deterministic JSON serialization has been implemented.


"C4 passed."



while the C4 gate remains blocked.


"Publication approved."



while the publication gate remains blocked.



19. Runtime Truth Rule


The strongest statement permitted after an execution is determined by the actual evidence produced by that execution.


Examples:


syntax check
    → source compiled

finite computation
    → computational evidence over the tested domain

exhaustive finite computation
    → exhaustive evidence over the declared finite domain

independent computational route
    → independent computational evidence, if the independence claim is actually justified

formal proof checked by the formal system
    → formal proof evidence

provenance receipt
    → evidence about what was executed

promotion gate
    → evidence that the stated policy conditions were satisfied



These categories must not be silently substituted for one another.



20. Current Scope Boundary


This verification directory does not claim to verify all AQARION mathematics.


In particular, the existence of:


manifest.json
run-all.py
repo_self_audit.py
manifest_binding_audit.py
bridge_exact.py



does not itself establish correctness of every claim in the AQARION research corpus.


The current scope is the executable artifacts actually bound and executed.



21. Governance


Current standing governance:


FROZEN AUDIT
NO PROMOTION
C4 BLOCKED
PUBLICATION BLOCKED



No new verifier, receipt, benchmark, numerical result, or computational replay automatically changes that governance state.


Promotion requires the separately defined governance and evidence gates.



22. Final Rule


The verification directory exists to make claims more falsifiable, reproducible, and auditable.


It does not exist to manufacture certainty.


The governing rule is:




State exactly what was defined, exactly what was executed, exactly what was compared, and exactly what remains unproved.




No fabricated receipts.


No fabricated execution counts.


No fabricated hashes.


No silent filename substitutions.


No promotion by repetition.


No computational result may be described as a theorem unless the corresponding proof obligation has actually been discharged.



23. Primary Files


verification/
├── README.md
├── manifest.json
├── manifest_binding_audit.py
├── run-all.py
├── replay-harness.py
├── provenance.py
├── repo_self_audit.py
├── requirements.txt
│
├── aq_s14/
│   └── aq_s14_semantic_suite.py
│
├── aq_contract/
│   └── aq_contract_semantic_suite.py
│
├── aq_oracle/
│   └── aq_independent_oracle_suite.py
│
├── aq-mutation-suite.py
│
├── receipts/
│
└── sv-001-v2/
    ├── bridge_exact.py
    ├── contract.json
    ├── oracle.py
    ├── verifier.py
    ├── replay.py
    ├── mutation/
    │   ├── executor.py
    │   └── metamorphic.py
    └── receipt/
        ├── schema.json
        └── writer.py



The tree above describes the intended/current verification artifacts relevant to this documentation. A filesystem audit remains authoritative for whether an individual artifact is actually present at a particular repository revision.



Governance: FROZEN AUDIT · NO PROMOTION · C4 BLOCKED · PUBLICATION BLOCKED
