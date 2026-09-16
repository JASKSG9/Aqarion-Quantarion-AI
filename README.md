# AQARION & QUANTARION AI

**Replayable Research Objects for Finite Dynamical Systems**

[![Status](https://img.shields.io/badge/status-FROZEN%20AUDIT-blue)]()
[![C4](https://img.shields.io/badge/C4-BLOCKED-red)]()
[![Publication](https://img.shields.io/badge/publication-BLOCKED-red)]()
[![Lean](https://img.shields.io/badge/Lean-OPEN-yellow)]()
[![License](https://img.shields.io/badge/license-Apache%202.0-green)](LICENSE)

AQARION is a research framework and evidence infrastructure for certifying
observable quotients of finite deterministic dynamical systems. It combines
operator theory, exact-rational computation, formal verification targets, and
a portable replay contract that makes every claim independently checkable.

> **Replay is not proof. A receipt is not certification. No axis promotes another silently.**

---

## Table of contents

- [What AQARION is](#what-aqarion-is)
- [What AQARION is not](#what-aqarion-is-not)
- [Governance status](#governance-status)
- [Core equation](#core-equation)
- [Repository layout](#repository-layout)
- [Quick start](#quick-start)
- [The Replay Contract (RPL-001)](#the-replay-contract-rpl-001)
- [ARRO — Replayable Research Objects](#arro--replayable-research-objects)
- [Verdict lattice](#verdict-lattice)
- [Claim and evidence registry](#claim-and-evidence-registry)
- [Formal verification](#formal-verification)
- [Replay Lab](#replay-lab)
- [Contributing](#contributing)
- [Citation](#citation)
- [License](#license)

---

## What AQARION is

AQARION studies **when a proposed observable space of a finite dynamical
system is exactly invariant under the Koopman operator**, and when it is not,
**how the leakage is structured**.

Given:

- a finite set `X` with a deterministic map `T : X → X`,
- the Koopman operator `(K_T f)(x) = f(T(x))`,
- a partition `Π` of `X` with orthogonal projector `P_Π`,

the framework is built on one object — the **observable defect operator**:

```

D_Π = (I − P_Π) K_T P_Π

```

The central theorem (AQ-THM-001) states:

```

D_Π = 0  ⟺  K_T(V_Π) ⊆ V_Π

```

Everything else — rank, spectrum, Frobenius energy, entropy, transfer dual,
closure refinement — is a derived invariant of this operator.

**AQARION is not an observable-learning method.** It is a post-hoc
certification layer that evaluates proposed observable spaces produced by
any method: analytic construction, EDMD, kernel EDMD, neural Koopman
approximations, Fourier truncation, polynomial bases.

---

## What AQARION is not

AQARION does **not** claim, and will not claim without a kernel-accept
receipt, any of the following:

- that finite computation establishes a universal theorem;
- that a passing CI run certifies mathematics;
- that a `Sorry`-free Lean file is a verified theorem;
- that a healthy API implies valid evidence;
- that a receipt implies certification;
- that any axis (math / replay / provenance / formal) silently promotes another.

---

## Governance status

| Component | Status | Meaning |
|---|---|---|
| **C3** | 🟢 OPEN | Active research; no freeze. |
| **C4** | 🔴 BLOCKED | Publication gate is closed. |
| **Lean** | 🟡 OPEN | Formal targets declared; kernel receipts pending. |
| **SDS-002** | 🟠 QUARANTINED | Semantic-drift surface under audit. |
| **Publication** | 🔴 BLOCKED | No external submission authorized. |
| **Promotable** | ❌ false | No claim is currently promotable. |

Releases of AQARION are **evidence snapshots**, not certifications.

---

## Core equation

```

CLAIM  →  RUN  →  RECEIPT  →  REPLAY  →  VERDICT

```

with the load-bearing invariants:

```

NO RECEIPT  ⇒  NO REPLAY CLAIM
REPLAY      ≠  PROOF
COMPUTED    ≠  PROVED

```

Every claim, run, and verdict carries an explicit evidence class. No output
is promoted above what its receipt supports.

---

## Repository layout

```

AQARION/
├── AQARION-CORE/                 Core operator definitions
├── AQARION-LAKE/                 Lean 4 formalization targets
│   ├── AqarionLake.lean          Canonical library root (target)
│   ├── lakefile.lean
│   └── lean-toolchain
├── AQARION-SKILLS/
│   ├── AQARION-REPLAY-LAB/       Replay Contract v0.1
│   │   ├── scripts/
│   │   │   └── capture.py        RPL-001 compliant runner
│   │   ├── schema/
│   │   │   └── receipt.schema.json
│   │   ├── claims/               Claim YAML definitions
│   │   ├── ENGINES/              Per-claim execution engines
│   │   ├── FIXTURES/             Inputs and negative controls
│   │   ├── RECEIPTS/             Written receipts (immutable)
│   │   ├── runs/                 Run artifacts (stdout, stderr, receipt)
│   │   └── tests/
│   └── aqarion-replay/
│       └── SKILL.md              Agent Skills format
├── QUICKSTART/
│   └── AQARION-RIP/              Getting-started guides
├── DOCS/                         Design documents and audit trails
├── EXAMPLES/                     Worked ARROs
└── README.md

```

---

## Quick start

### Requirements

- Python 3.10+
- `git`
- (optional) Lean 4 + Lake for formal targets
- No GPU, no cloud account, no paid API required for the evidence core.

### Minimal local run

```sh
git clone https://github.com/JASKSG9/AQARION-ARITHMETIC-FDS-FINITE-DYNAMICAL-SYSTEMS-.git
cd AQARION-ARITHMETIC-FDS-FINITE-DYNAMICAL-SYSTEMS-
python -m pip install numpy sympy pytest

# Initialize the Replay Lab skeleton
python aqreplay.py init

# Run the RPL-001 receipt integrity tests
python -m pytest tests/ -q

# Capture the first ARRO
python aqreplay.py capture AQ-S16-SAT-001 RPL-SAT-001 \
  -- python ENGINES/saturation_equal_margin.py

# Verify and close the object
python aqreplay.py verify RPL-SAT-001
python aqreplay.py closure AQ-S16-SAT-001
```

Expected closure output:

```json
{
  "claim_id": "AQ-S16-SAT-001",
  "parts": {
    "claim_yaml": "RESOLVED",
    "engine": "RESOLVED",
    "receipt": "RESOLVED (1)",
    "lean": "OPEN",
    "promotion": "BLOCKED"
  },
  "object_status": "REPLAY_CLOSED"
}
```

REPLAY_CLOSED means the computational object is replayable. It does
not mean the theorem is proved.

---

The Replay Contract (RPL-001)

Every run produces a receipt. Every receipt — including failures — is
written unconditionally.

RPL-001 invariant:

```
FAILED RUN  ⇒  COMPLETE RECEIPT
```

The reference implementation captures the subprocess exit code directly
via subprocess.run(...).returncode. It does not use a shell pipeline,
because "$@" | tee; echo $? reports the exit status of tee, not of the
wrapped command.

Receipt schema

```json
{
  "receipt_id": "AQ-RPL-RPL-SAT-001",
  "claim_id": "AQ-S16-SAT-001",
  "run_id": "RPL-SAT-001",
  "timestamp_utc": "2026-09-16T00:00:00+00:00",
  "command": ["python", "ENGINES/saturation_equal_margin.py"],
  "exit_code": 0,
  "stdout_sha256": "…",
  "stderr_sha256": "NO_STDERR",
  "source_sha256": "…",
  "commit": "abcdef123456",
  "environment": { "python": "3.13.0", "platform": "Linux-…" },
  "policy": {
    "filesystem": "workspace_only",
    "network": false,
    "external_actions": false,
    "package_install": false
  },
  "verdict": "COMPUTED",
  "residual": null,
  "promotion_allowed": false,
  "independent_machine": false
}
```

Verdict vocabulary (deliberately weak)

```
OBSERVED  |  COMPUTED  |  FAILED  |  QUARANTINED
REPLAYED  |  INDEPENDENTLY_REPLAYED
```

PROVEN and CERTIFIED are not in this list. They belong to the
formal axis and require kernel receipts.

---

ARRO — Replayable Research Objects

A Replayable Research Object is a tuple:

```
R = (C, S, I, E, O, Rc, V)
```

Symbol Component Content
C Claim statement, scope, expected residual, policy
S Source exact git commit + source SHA-256
I Inputs fixture digests
E Execution command, environment, policy
O Output stdout/stderr hashes
Rc Receipt schema-validated JSON
V Verdict multi-axis result

A replay is valid iff the receipt's declared source, inputs, and policy
match the replay environment. A replay is independent iff it occurs on
a distinct machine and the hashes agree.

Every ARRO lives in a directory:

```
claims/AQ-XXXX.yaml
ENGINES/engine_name.py
FIXTURES/fixture.json
runs/RPL-XXXX/receipt.json
RECEIPTS/AQ-RPL-RPL-XXXX.json
```

---

Verdict lattice

AQARION maintains four independent axes. No axis promotes another
silently.

Axis Values
MATH OBSERVED · COMPUTED · CONSISTENT · KILLED · FORMALLY_VERIFIED
REPLAY NOT_REPLAYED · REPLAYED · INDEPENDENTLY_REPLAYED
PROVENANCE ALIGNED · DRIFTED · UNKNOWN
FORMAL NOT_STARTED · NOT_COMPILED · COMPILES · ZERO_SORRY · AXIOM_AUDITED · KERNEL_ACCEPTED

A single receipt may carry, for example:

```
MATH:        COMPUTED
REPLAY:      REPLAYED
PROVENANCE:  ALIGNED
FORMAL:      NOT_COMPILED
```

That means: the computation ran, was replayed in-session, the source
matches its declared hash, and no formal verification has been done.

---

Claim and evidence registry

Claims are declared in claims/*.yaml:

```yaml
claim_id: AQ-S16-SAT-001
statement: >
  For equal-margin non-negative integer 3×3 multiplicity matrices M
  (all row and column sums equal to n), the reduced residual Gram G_M
  satisfies λ_max(G_M) = 1 if and only if rank(M) < 3.
status: OPEN
engine: ENGINES/saturation_equal_margin.py
inputs: []
expected:
  residual: "0"
  mismatches: 0
  domain: "n=1..5 exhaustive transportation polytope"
policy:
  filesystem: workspace_only
  network: false
math_axis: STRUCTURALLY_DERIVED
replay_axis: NOT_YET_REPLAYED
formal_axis: LEAN_OPEN
promotion_allowed: false
```

The full registry is machine-readable. aqreplay closure CLAIM_ID reports
which parts of the object resolve and which remain open.

---

Formal verification

AQARION maintains Lean 4 targets under AQARION-LAKE/. Formal status is
reported using strict labels:

```
NOT_COMPILED      no build attempted
COMPILES          lake build succeeds
ZERO_SORRY        no `sorry` in the certified slice
AXIOM_AUDITED     #print axioms reports no project axioms
KERNEL_ACCEPTED   an external kernel check accepted the proof
```

The formal axis is orthogonal to computation and replay. A theorem can
be COMPUTED, REPLAYED, PROVENANCE: ALIGNED, and still FORMAL:
NOT_COMPILED — and it will be reported exactly that way.

Canonical build:

```sh
cd AQARION-LAKE
lake build
```

---

Replay Lab

The Replay Lab (AQARION-SKILLS/AQARION-REPLAY-LAB/) is the first
concrete AQARION product. It is not a UI; it is a small, portable,
evidence-first engine.

Commands

```sh
aqreplay init                    # initialize skeleton
aqreplay capture CLAIM RUN -- CMD
aqreplay verify RUN              # validate receipt schema + hashes
aqreplay closure CLAIM           # report object closure
aqreplay diff RUN_A RUN_B        # compare two receipts
aqreplay explain RUN             # show residual and provenance
```

Design constraints

· Python standard library + optional numpy / sympy.
· No cloud, no GPU, no paid API, no authentication.
· Runs on Android / Termux, Linux, macOS, and CI equally.
· Emits machine-readable JSON receipts.
· Never mutates remote state.

---

Contributing

Before opening a pull request:

1. A claim is declared in claims/*.yaml.
2. An engine exists under ENGINES/ and reproduces the claim.
3. A receipt is produced by aqreplay capture.
4. aqreplay closure reports the object status.
5. python -m pytest tests/ passes.
6. No status is promoted above what the receipt supports.

See DOCS/ for the full evidence policy.

---

Citation

```bibtex
@misc{aqarion2026,
  author       = {Aaron, James},
  title        = {AQARION: Replayable Research Objects for Finite Dynamical Systems},
  year         = {2026},
  howpublished = {\url{https://github.com/JASKSG9/AQARION-ARITHMETIC-FDS-FINITE-DYNAMICAL-SYSTEMS-}},
  note         = {Version 0.1 · FROZEN AUDIT · C4 blocked}
}
```

---

License

Apache License 2.0. See LICENSE.

---

AQARION does not replace observable-learning methods. It provides a
mathematically grounded certification layer that evaluates whether a
proposed observable space is exactly or approximately closed under the
dynamics, together with quantitative measures of leakage when it is not.

```
