#!/usr/bin/env python3

"""
AQARION Layer 4 — reproduction-contract adversarial tests.

This test does NOT establish mathematical truth.

It tests whether the provenance/reproduction
classification correctly distinguishes:

    * rerun
    * independent reproduction
    * reproduction failure
    * input drift
    * stale receipt
    * false independence

Important semantic rule:

    output equality is required for successful
    exact reproduction, but output equality does
    NOT establish independence.

Likewise:

    output inequality is reproduction failure,
    not evidence of independence.
"""


from dataclasses import dataclass
from enum import Enum
from typing import Optional


class Verdict(Enum):
    RERUN = "RERUN"
    INDEPENDENTLY_REPRODUCED = (
        "INDEPENDENTLY_REPRODUCED"
    )
    REPRODUCTION_FAILURE = (
        "REPRODUCTION_FAILURE"
    )
    INPUT_DRIFT = "INPUT_DRIFT"
    STALE_RECEIPT = "STALE_RECEIPT"
    FALSE_INDEPENDENCE = (
        "FALSE_INDEPENDENCE"
    )
    INCOMPLETE_PROVENANCE = (
        "INCOMPLETE_PROVENANCE"
    )


@dataclass(frozen=True)
class Execution:
    source_digest: str
    executable_digest: str
    input_digest: str
    environment_digest: str
    output_digest: str
    commit: str


@dataclass(frozen=True)
class ReproductionRelation:
    specification_same: bool
    inputs_same: bool
    implementation_independent: bool
    environment_independent: bool
    outputs_equal: bool


def classify(
    reference: Execution,
    reproduction: Execution,
    relation: ReproductionRelation,
    expected_commit: Optional[str] = None,
):
    """
    Classify the relation between two executions.

    Priority:

        stale receipt
        input drift
        incomplete provenance
        false independence
        rerun
        reproduction failure
        independent reproduction
    """

    if expected_commit is not None:
        if (
            reference.commit
            != expected_commit
            or reproduction.commit
            != expected_commit
        ):
            return Verdict.STALE_RECEIPT

    if not relation.specification_same:
        return Verdict.INCOMPLETE_PROVENANCE

    if not relation.inputs_same:
        return Verdict.INPUT_DRIFT

    required_reference = (
        reference.source_digest,
        reference.executable_digest,
        reference.input_digest,
        reference.environment_digest,
        reference.output_digest,
    )

    required_reproduction = (
        reproduction.source_digest,
        reproduction.executable_digest,
        reproduction.input_digest,
        reproduction.environment_digest,
        reproduction.output_digest,
    )

    if any(
        value == ""
        for value in (
            *required_reference,
            *required_reproduction,
        )
    ):
        return Verdict.INCOMPLETE_PROVENANCE

    same_implementation = (
        reference.source_digest
        == reproduction.source_digest
        and
        reference.executable_digest
        == reproduction.executable_digest
    )

    if relation.implementation_independent:
        if same_implementation:
            return Verdict.FALSE_INDEPENDENCE

    if not relation.implementation_independent:
        if same_implementation:
            if relation.outputs_equal:
                return Verdict.RERUN

            return Verdict.REPRODUCTION_FAILURE

    if not relation.outputs_equal:
        return Verdict.REPRODUCTION_FAILURE

    return Verdict.INDEPENDENTLY_REPRODUCED


def execution(
    source="SRC-A",
    executable="EXE-A",
    input_digest="INPUT-1",
    environment="ENV-A",
    output="OUT-1",
    commit="COMMIT-1",
):
    return Execution(
        source_digest=source,
        executable_digest=executable,
        input_digest=input_digest,
        environment_digest=environment,
        output_digest=output,
        commit=commit,
    )


def relation(
    specification_same=True,
    inputs_same=True,
    implementation_independent=False,
    environment_independent=False,
    outputs_equal=True,
):
    return ReproductionRelation(
        specification_same=specification_same,
        inputs_same=inputs_same,
        implementation_independent=(
            implementation_independent
        ),
        environment_independent=(
            environment_independent
        ),
        outputs_equal=outputs_equal,
    )


def assert_case(name, expected, observed):
    if observed != expected:
        raise AssertionError(
            f"{name}: expected "
            f"{expected.value}, got "
            f"{observed.value}"
        )

    print(
        f"PASS {name}: "
        f"{observed.value}"
    )


def main():
    ref = execution()

    # -------------------------------------------------
    # M1 — same implementation falsely labelled
    #      independent.
    # -------------------------------------------------

    repro = execution()

    assert_case(
        "M1 false independence",
        Verdict.FALSE_INDEPENDENCE,
        classify(
            ref,
            repro,
            relation(
                implementation_independent=True,
                outputs_equal=True,
            ),
        ),
    )

    # -------------------------------------------------
    # M2 — ordinary same-code rerun.
    # -------------------------------------------------

    assert_case(
        "M2 same-code rerun",
        Verdict.RERUN,
        classify(
            ref,
            repro,
            relation(
                implementation_independent=False,
                outputs_equal=True,
            ),
        ),
    )

    # -------------------------------------------------
    # M3 — genuinely different implementation,
    #      same specification/input/output.
    # -------------------------------------------------

    independent = execution(
        source="SRC-B",
        executable="EXE-B",
        environment="ENV-B",
    )

    assert_case(
        "M3 independent agreement",
        Verdict.INDEPENDENTLY_REPRODUCED,
        classify(
            ref,
            independent,
            relation(
                implementation_independent=True,
                environment_independent=True,
                outputs_equal=True,
            ),
        ),
    )

    # -------------------------------------------------
    # M4 — independent implementation disagrees.
    # -------------------------------------------------

    independent_failure = execution(
        source="SRC-B",
        executable="EXE-B",
        environment="ENV-B",
        output="OUT-DIFFERENT",
    )

    assert_case(
        "M4 independent disagreement",
        Verdict.REPRODUCTION_FAILURE,
        classify(
            ref,
            independent_failure,
            relation(
                implementation_independent=True,
                environment_independent=True,
                outputs_equal=False,
            ),
        ),
    )

    # -------------------------------------------------
    # M5 — input drift hidden by identical output.
    # -------------------------------------------------

    input_drift = execution(
        source="SRC-B",
        executable="EXE-B",
        input_digest="INPUT-ALTERED",
        environment="ENV-B",
        output="OUT-1",
    )

    assert_case(
        "M5 hidden input drift",
        Verdict.INPUT_DRIFT,
        classify(
            ref,
            input_drift,
            relation(
                inputs_same=False,
                implementation_independent=True,
                environment_independent=True,
                outputs_equal=True,
            ),
        ),
    )

    # -------------------------------------------------
    # M6 — stale receipt / commit mismatch.
    # -------------------------------------------------

    stale = execution(
        source="SRC-B",
        executable="EXE-B",
        environment="ENV-B",
        commit="OLD-COMMIT",
    )

    assert_case(
        "M6 stale receipt",
        Verdict.STALE_RECEIPT,
        classify(
            ref,
            stale,
            relation(
                implementation_independent=True,
                environment_independent=True,
                outputs_equal=True,
            ),
            expected_commit="COMMIT-1",
        ),
    )

    # -------------------------------------------------
    # M7 — different implementation but disagreement.
    # -------------------------------------------------

    assert_case(
        "M7 different implementation disagreement",
        Verdict.REPRODUCTION_FAILURE,
        classify(
            ref,
            independent_failure,
            relation(
                implementation_independent=True,
                outputs_equal=False,
            ),
        ),
    )

    # -------------------------------------------------
    # M8 — incomplete provenance.
    # -------------------------------------------------

    incomplete = execution(
        source="",
    )

    assert_case(
        "M8 incomplete provenance",
        Verdict.INCOMPLETE_PROVENANCE,
        classify(
            ref,
            incomplete,
            relation(),
        ),
    )

    # -------------------------------------------------
    # M9 — same output is not enough to establish
    #      independence.
    #
    # This explicitly protects against the old
    # semantic inversion.
    # -------------------------------------------------

    same_output_same_code = execution(
        source="SRC-A",
        executable="EXE-A",
        environment="ENV-B",
        output="OUT-1",
    )

    observed = classify(
        ref,
        same_output_same_code,
        relation(
            implementation_independent=False,
            environment_independent=True,
            outputs_equal=True,
        ),
    )

    assert_case(
        "M9 equal output does not imply independence",
        Verdict.RERUN,
        observed,
    )

    print()
    print(
        "AQARION Layer 4 "
        "reproduction-contract tests: "
        "ALL PASS"
    )


if __name__ == "__main__":
    main()
