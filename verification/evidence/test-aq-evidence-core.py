from __future__ import annotations

import copy

import pytest

from aq_evidence_core import (
    canonical_bytes,
    content_hash,
    make_receipt,
    verify_receipt,
)


def sample_evidence():
    return {
        "experiment": "AQ-S15-green",
        "parameters": {
            "m_min": 2,
            "m_max": 10,
        },
        "result": {
            "failures": 0,
            "cases": 9,
        },
    }


def test_original_receipt_passes():
    evidence = sample_evidence()

    receipt = make_receipt(
        evidence=evidence,
        evidence_id="AQ-EVIDENCE-0001",
        producer="AQARION",
        claim_status="COMPUTED",
    )

    assert verify_receipt(evidence, receipt)


def test_reordering_dictionary_keys_passes():
    evidence = sample_evidence()

    receipt = make_receipt(
        evidence=evidence,
        evidence_id="AQ-EVIDENCE-0001",
        producer="AQARION",
        claim_status="COMPUTED",
    )

    reordered = {
        "result": evidence["result"],
        "parameters": evidence["parameters"],
        "experiment": evidence["experiment"],
    }

    assert verify_receipt(reordered, receipt)


def test_unicode_normalization_is_stable():
    e1 = {"text": "é"}
    e2 = {"text": "e\u0301"}

    assert canonical_bytes(e1) == canonical_bytes(e2)


def test_result_mutation_fails():
    evidence = sample_evidence()

    receipt = make_receipt(
        evidence,
        "AQ-EVIDENCE-0001",
        "AQARION",
        "COMPUTED",
    )

    mutated = copy.deepcopy(evidence)
    mutated["result"]["failures"] = 1

    assert not verify_receipt(mutated, receipt)


def test_numeric_result_mutation_fails():
    evidence = sample_evidence()

    receipt = make_receipt(
        evidence,
        "AQ-EVIDENCE-0001",
        "AQARION",
        "COMPUTED",
    )

    mutated = copy.deepcopy(evidence)
    mutated["result"]["cases"] = 10

    assert not verify_receipt(mutated, receipt)


def test_evidence_id_mutation_fails():
    evidence = sample_evidence()

    receipt = make_receipt(
        evidence,
        "AQ-EVIDENCE-0001",
        "AQARION",
        "COMPUTED",
    )

    mutated = copy.deepcopy(receipt)
    mutated["evidence_id"] = "AQ-EVIDENCE-0002"

    assert not verify_receipt(evidence, mutated)


def test_claim_status_mutation_fails():
    evidence = sample_evidence()

    receipt = make_receipt(
        evidence,
        "AQ-EVIDENCE-0001",
        "AQARION",
        "COMPUTED",
    )

    mutated = copy.deepcopy(receipt)
    mutated["claim_status"] = "FORMALLY_CERTIFIED"

    assert not verify_receipt(evidence, mutated)


def test_producer_mutation_fails():
    evidence = sample_evidence()

    receipt = make_receipt(
        evidence,
        "AQ-EVIDENCE-0001",
        "AQARION",
        "COMPUTED",
    )

    mutated = copy.deepcopy(receipt)
    mutated["producer"] = "UNTRUSTED"

    assert not verify_receipt(evidence, mutated)


def test_content_hash_mutation_fails():
    evidence = sample_evidence()

    receipt = make_receipt(
        evidence,
        "AQ-EVIDENCE-0001",
        "AQARION",
        "COMPUTED",
    )

    mutated = copy.deepcopy(receipt)
    mutated["content_hash"] = "0" * 64

    assert not verify_receipt(evidence, mutated)


def test_schema_mutation_fails():
    evidence = sample_evidence()

    receipt = make_receipt(
        evidence,
        "AQ-EVIDENCE-0001",
        "AQARION",
        "COMPUTED",
    )

    mutated = copy.deepcopy(receipt)
    mutated["schema"] = "AQ-EVIDENCE-CORE/999"

    assert not verify_receipt(evidence, mutated)


def test_receipt_hash_mutation_fails():
    evidence = sample_evidence()

    receipt = make_receipt(
        evidence,
        "AQ-EVIDENCE-0001",
        "AQARION",
        "COMPUTED",
    )

    mutated = copy.deepcopy(receipt)
    mutated["receipt_hash"] = "0" * 64

    assert not verify_receipt(evidence, mutated)


def test_identical_evidence_has_identical_content_hash():
    evidence1 = sample_evidence()
    evidence2 = sample_evidence()

    assert content_hash(
        "AQ-EVIDENCE-0001",
        evidence1,
    ) == content_hash(
        "AQ-EVIDENCE-0001",
        evidence2,
    )


def test_different_evidence_has_different_hash():
    evidence1 = sample_evidence()
    evidence2 = copy.deepcopy(evidence1)

    evidence2["result"]["failures"] = 1

    assert content_hash(
        "AQ-EVIDENCE-0001",
        evidence1,
    ) != content_hash(
        "AQ-EVIDENCE-0001",
        evidence2,
  )
