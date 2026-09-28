# CLAIM FIREWALL POLICY

**2026-09-27**

AI systems may propose transitions.

AI systems do not determine claim status.

The VERIFY layer is authoritative for evidence-policy decisions.

Allowed verification outcomes:

    ACCEPT
    QUARANTINE
    REFUTE
    RETRACT

Promotion is an evidence-policy decision.

Promotion is not equivalent to formalization.

Formalization status remains an independent evidence dimension.

Every promoted claim must bind to:

    source identity
    source commit/tree
    artifact identity
    artifact hash
    evidence scope
    checker identity
    checker hash
    environment identity
    dependency cone
    receipt

The Grok adapter may propose receipts.

The Grok adapter may not write final claim status.

Provenance should use established standards such as W3C PROV
and RO-Crate rather than introducing a new provenance ontology.
