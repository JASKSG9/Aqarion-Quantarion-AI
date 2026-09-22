AQARION Reproduction Contract


Version: 1.0-draft


Date: 2026-09-22


Purpose


AQARION distinguishes:




rerun;


reproduction;


independent reproduction;


semantic agreement;


mathematical proof.




These are different evidence states.


1. Rerun


A rerun uses substantially the same implementation.


Example:


same source
same executable
same inputs
same environment
second execution



A matching output demonstrates repeatability of that execution.


It does not establish implementation independence.


2. Reproduction


A reproduction reconstructs the stated computation from its specification and inputs.


The implementation may differ.


Successful reproduction requires agreement with the reference result under the declared comparison contract.


3. Independent reproduction


Independence is a relation between executions.


It MUST NOT be inferred from output inequality.


The following is required:


reference execution
    source digest
    executable digest
    input digest
    environment digest
    output digest

reproduction execution
    source digest
    executable digest
    input digest
    environment digest
    output digest

reproduction relation
    specification_equal
    input_equal
    implementation_independent
    output_equal



4. Critical rule


For an exact reproduction:


[
\text{observed output}=\text{expected output}
]


is a success condition.


The following rule is forbidden:


if observed_output == expected_output:
    raise ProvenanceError(...)



Output equality is not evidence against independence.


Independence must be established separately.


5. Adversarial cases


Case A — genuine rerun


Same source and executable.


Expected classification:


RERUN



Not independent reproduction.


Case B — independent implementation


Different implementation digest, same specification and inputs, same exact output.


Expected classification:


INDEPENDENT_REPRODUCTION



subject to the declared independence contract.


Case C — same executable falsely labeled independent


Same source and executable digests.


Expected classification:


NOT_INDEPENDENT



Case D — changed input


Different input digest.


Expected classification:


NOT_COMPARABLE



unless the claim explicitly allows the changed input.


Case E — independent implementation, different output


Different implementation but output mismatch.


Expected classification:


REPRODUCTION_FAILURE



not provenance success.


6. Hash semantics


A SHA-256 digest establishes byte equality when the compared byte sequences have identical digests under the declared hashing procedure.


It does not establish:




semantic equality;


mathematical truth;


independence;


correctness of the implementation;


absence of specification error.




7. Evidence hierarchy


rerun
  <
reproduction
  <
independent reproduction
  <
independent reproduction + adversarial mutation
  <
formal proof



This is an evidence hierarchy, not a numerical score.


8. AQARION-specific value


AQARION's reproducibility layer should therefore audit not only:


"Can this computation be rerun?"


but:


"Can the claim be independently reconstructed, and does the independent implementation agree under the same explicit specification?"


That is the intended reproducibility contribution.


9. External standards


AQARION should use existing provenance standards rather than inventing a replacement provenance ontology.


The current Workflow Run RO-Crate ecosystem provides a suitable provenance substrate.


AQARION's additional layer is the semantic claim/evidence/reproduction relation.


Exact profile versions MUST be pinned in any future crate.


Status:


[C1] specification


[O] machine-enforced independence relation


[SUP] existing reproducibility infrastructure


No claim of formal verification.

